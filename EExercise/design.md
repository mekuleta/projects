# Design Document for Exercise Everywhere Web App

## Introduction

The Exercise Everywhere web app is designed to help users create customized physical therapy routines based on their specific needs and constraints. 

Inspired by the CS50 Finance project, with the help of AI the starter code expanded into new avenues, with the aim of providing a more comprehensive and user-friendly experience. The primary goals achieved were to create an already useful web app with a nice UI and maintaining the complexity of the problem it aims to solve for future iterations.

## Project Overview

### Files and Structure

The project consists of several key files and directories, each serving a specific purpose:

- `app.py`: The main application file containing the Flask app, route definitions, and database models.
- `requirements.txt`: Lists all the dependencies required to run the app.
- `templates/`: Directory containing HTML templates for different pages of the web app.
  - `index.html`: The homepage template.
  - `exercise_now.html`: The template for the "Exercise Now" page.
  - `routine_proposal.html`: The template for displaying the proposed exercise routine.
  - `login.html`: The template for the login page.
  - `register.html`: The template for the registration page.
  - `add_exercise.html`: The template for adding new exercises.
  - `track_record.html`: The template for displaying the user's exercise history (not yet fully implemented).
- `static/`: Directory containing static files such as CSS and images.
  - `css/styles.css`: Custom CSS for styling the web app.
  - `images/`: Directory containing images used in the web app, such as the logo and background images.
- `data/`: Directory containing the initial exercise data in CSV format. This data had been provided and structured based on my own experience with PT exercises.

## Design Decisions

Indeed, similarily as with CS50 Finance, I wanted the web app to work across all of:
- HTML - for the contents of my (sub)pages
- CSS - for the styling
- Python - for the functionality
- with Databases and SQL logic - as I wanted to relate multiple tables to the exercises I had uploaded

### User Interface (UI)

One of the primary goals was to create a web app with a nicer UI than CS50 Finance. To achieve this, I used Bootstrap for responsive design and custom CSS for additional styling. The UI is designed to be clean, modern, and user-friendly, with a focus on ease of navigation and accessibility. I had also added a logo and a key graphic to visually communicate what the app is about to any users who would come across the webpage in the future.

### Database Design

The database is designed using SQLAlchemy, with three main models:

- `User`: Stores user account information, including email and hashed password. I have learned about hashing in another course and tried to implement some basic security functionality.
- `Exercise`: Stores exercise data, including name, body part, type, sets, reps, hold time, total time, equipment, state, level, space, directions, and the date it was last completed. This database expanded as I realized the need for completion timestamps in line with expected functionality.
- `ExerciseDone`: Stores records of completed exercises, including user ID, exercise ID, timestamp, and duration.

### Route Definitions

The Flask app defines several routes to handle different functionalities:

- `/`: Home route to display the homepage.
- `/login`: Route to handle user login.
- `/register`: Route to handle user registration.
- `/exercise`: Route to display the exercise input form and generate an exercise routine based on user input.
- `/routine_proposal`: Route to display the proposed exercise routine as a result.
- `/mark_completed/<int:exercise_id>`: Route to mark an exercise as completed (not yet fully implemented).
- `/track_record`: Route to display the user's exercise history (not yet fully implemented).
- `/add_exercise`: Route to allow users to add new exercises to the database.

### Handling Complexity

In order to write my own spec elements I had to understand what's possible and how I want to think through structuring this problem. I had gone through a couple of ideas on a literal whiteboard thinking through the screens and relationships between pages and tables etc.
I cared about keeping the complexity of the problem I am trying to solve in its fullness, even if that meant that the prototype does not yet work fully as intended as some elements have not yet been fully implemented.
However, the app already generates exercise routines according to certain inputs and also allows adding new exercises to the mix. It also has a first stab at handling multiple users and related functionalities.

### Next Steps

Beyond the scope of this submission, there are several suggested next steps to improve the web app:

1. **Handling Multiple Input Problems**: Improve the logic for handling multiple pieces of equipment, ensuring that exercises utilizing any combination of selected equipment are suggested.
2. **Enhancing Logging and Logged-In Functionalities**: Improve the handling of user sessions, ensuring that users remain logged in and their actions are correctly tracked.
3. **Handling Edge Cases for Inputs**: Implement robust validation and error handling for all user inputs to ensure a smooth user experience.
4. **Completing and Rotating Through Exercises**: Implement logic to track completed exercises in Track Record and rotate through available exercises to minimize repetition and promote varied routines.

## Thank you

Thank you to my TAs and all of the CS50 staff for letting me pick up some first coding chops in this course. I can better recognize how to problem-solve with code and what building blocks may be needed to create different elements. Those were indeed some of my learning goals. I am encouraged and excited to explore this space further in my spare time.