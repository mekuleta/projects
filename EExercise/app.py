from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import os
from datetime import datetime
from flask_migrate import Migrate

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database and secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'horses and tulips are fed' 
# Replaced with a strong, random value - I know I shouldn't be hardcoding this, but do not fully understand where to store it just yet

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the User model for storing user accounts
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Define the Exercise model for storing exercise data
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    body_part = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer)
    hold = db.Column(db.Integer)
    total_time = db.Column(db.Integer, nullable=False)  # Duration in seconds
    equipment = db.Column(db.String(150))
    state = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    space = db.Column(db.String(50))
    directions = db.Column(db.Text, nullable=False)
    added_by = db.Column(db.String(50))
    last_completed = db.Column(db.DateTime)  # Keeping track to minimize repetition

# Define the ExerciseDone model for storing completion records
class ExerciseDone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer)  # Duration in seconds

# Home route to display the home page
@app.route('/')
def index():
    return render_template('index.html')

# Login route to handle user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('exercise'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html')

# Register route to handle user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Exercise route to display the exercise input form and return an exercise routine
@app.route('/exercise', methods=['GET', 'POST'])
def exercise():
    if request.method == 'POST':
        try:
            body_part = request.form.get('body_part')
            type = request.form.get('type')
            time_available = int(request.form.get('time_available')) * 60  # Convert minutes to seconds
            equipment = request.form.getlist('equipment')
            difficulty = request.form.getlist('difficulty')
            space = request.form.get('space')

            print(f"Body Part: {body_part}, Type: {type}, Time Available: {time_available}, Equipment: {equipment}, Difficulty: {difficulty}, Space: {space}")

            # Query to filter exercises based on user input
            exercises = Exercise.query.filter_by(body_part=body_part, type=type).all()

            # Filter exercises based on equipment
            if equipment:
                exercises = [exercise for exercise in exercises if exercise.equipment and any(equip in exercise.equipment.split(', ') for equip in equipment)]

            # Exclude recently completed exercises for logged-in users
            if 'user_id' in session:
                user_id = session['user_id']
                recent_exercises = ExerciseDone.query.filter_by(user_id=user_id).order_by(ExerciseDone.timestamp.desc()).limit(10).all()
                recent_exercise_ids = [exercise.exercise_id for exercise in recent_exercises]
                exercises = [exercise for exercise in exercises if exercise.id not in recent_exercise_ids]

            # Select exercises based on user input and total duration
            selected_exercises = []
            total_duration = 0
            for exercise in exercises:
                if total_duration + exercise.total_time <= time_available:
                    selected_exercises.append(exercise)
                    total_duration += exercise.total_time

            return render_template('routine_proposal.html', exercises=selected_exercises, total_duration=total_duration)
        except Exception as e:
            print(f"Error: {e}")
            flash('An error occurred while generating the routine. Please try again.', 'danger')
            return redirect(url_for('exercise'))

    body_parts = Exercise.query.with_entities(Exercise.body_part).distinct().all()
    types = Exercise.query.with_entities(Exercise.type).distinct().all()
    equipment = Exercise.query.with_entities(Exercise.equipment).distinct().all()
    difficulties = Exercise.query.with_entities(Exercise.level).distinct().all()
    return render_template('exercise_now.html', body_parts=body_parts, types=types, equipment=equipment, difficulties=difficulties)

# Routine Proposal route to display the proposed exercise routine
@app.route('/routine_proposal', methods=['POST'])
def routine_proposal():
    # Logic to display proposed routine and handle marking exercises as complete
    return render_template('routine_proposal.html')

# Route to mark an exercise as completed
@app.route('/mark_completed/<int:exercise_id>', methods=['POST'])
def mark_completed(exercise_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    timestamp = datetime.utcnow()
    exercise_done = ExerciseDone(user_id=user_id, exercise_id=exercise_id, timestamp=timestamp, duration=0)  # Duration can be set if needed
    db.session.add(exercise_done)
    db.session.commit()
    
    # Update last_completed in Exercise table
    exercise = Exercise.query.get(exercise_id)
    exercise.last_completed = timestamp
    db.session.commit()
    
    flash('Exercise marked as completed!', 'success')
    return redirect(url_for('track_record'))

# Track Record route to display the user's exercise history
@app.route('/track_record')
def track_record():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    exercises_done = ExerciseDone.query.filter_by(user_id=user_id).all()
    return render_template('track_record.html', exercises_done=exercises_done)

# Add Exercise route to allow users to add new exercises to the database
@app.route('/add_exercise', methods=['GET', 'POST'])
def add_exercise():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        body_part = request.form.get('body_part')
        type = request.form.get('type')
        sets = request.form.get('sets')
        reps = request.form.get('reps')
        hold = request.form.get('hold')
        total_time = request.form.get('total_time')
        equipment = request.form.get('equipment')
        state = request.form.get('state')
        level = request.form.get('level')
        space = request.form.get('space')
        directions = request.form.get('directions')

        new_exercise = Exercise(name=name, body_part=body_part, type=type, sets=sets, reps=reps, hold=hold,
                                total_time=total_time, equipment=equipment, state=state, level=level, space=space, 
                                directions=directions, added_by='user')
        db.session.add(new_exercise)
        db.session.commit()
        flash('Exercise added successfully!', 'success')
        return redirect(url_for('exercise'))
    
    return render_template('add_exercise.html')

# Function to populate the database with initial exercise data from CSV
def populate_db():
    if Exercise.query.first() is None:
        csv_path = 'data/exercises.csv'
        exercises_data = pd.read_csv(csv_path)
        for index, row in exercises_data.iterrows():
            new_exercise = Exercise(
                name=row['Exercise'],
                body_part=row['Body Part'],
                type=row['Type'],
                sets=row['Sets'],
                reps=row['Reps (x)'],
                hold=row['Hold (s)'],
                total_time=row['Total Time (s)'],
                equipment=row['Equipment'],
                state=row['State'],
                level=row['Level'],
                space=row['Space'],
                directions=row['Directions'],
                added_by=row['Added by (us or user)']
            )
            db.session.add(new_exercise)
        db.session.commit()

# Main block to create the database tables and run the Flask application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        populate_db()
    app.run(debug=True)