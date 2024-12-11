# Exercise Everywhere Web App

Welcome to the Exercise Everywhere web app! This application allows users to customize their physical therapy routines based on their specific needs and constraints. Users can register, log in, and generate exercise routines tailored to their available time, equipment, and desired body part. The app also tracks users' exercise history to minimize repetition and promote varied routines.

## Apart from the helpful text below, please make sure to visit the video overview of this project, linked here:
https://youtu.be/vShsaSIrjzY

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Setup and Installation](#setup-and-installation)
5. [Running the App](#running-the-app)
6. [Usage](#usage)
7. [Contributions](#contributions)

## Introduction
Exercise Everywhere is a web application designed to help users create customized physical therapy routines. The app leverages a database of exercises and allows users to add new exercises, ensuring a growing and diverse set of routines. Users can specify their workout preferences, and the app generates a routine that fits their criteria.

## Features
- User registration and login
- Customizable exercise routines based on user input: dynamic filtering based on available equipment, time, and body part
- Tracking of exercise history to minimize repetition (WIP)
- Ability to add new exercises to the database

## Requirements
To run this web app, you need the following:
- GitHub account
- GitHub Codespaces or Visual Studio Code
- Python 3.7 or higher
- Flask and other dependencies listed in `requirements.txt`

## Setup and Installation
Follow these steps to set up and run the app:

1. Clone the Repository:
   Download the zip file (submission) of the project and extract it to your desired location. Alternatively, I think you can clone the repository from my GitHub:
   ```bash
   git clone https://github.com/mekuleta/EExercise.git
   cd EExercise

2. Open in GitHub Codespaces or VS Code

3. Set Up the Environment:
- GitHub Codespaces: The environment should be set up right out of the box.
- VS Code: Ensure you have the Remote - Containers extension installed. Open the project in a container by clicking on the green button in the bottom-left corner and selecting "Remote-Containers: Open Folder in Container...".

4. Install Dependencies: Open a terminal in your Codespace or VS Code and run the following command to install the required dependencies:
   pip install -r requirements.txt

5. Set up the Database: Initialize and migrate as follows:
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

## Running the App
To run the app, use the following command in the terminal:
   flask run

This will start the Flask development server. Open your web browser and navigate to http://127.0.0.1:5000 to access the app.

## Usage

1. Register: Create a new account by clicking on the "Register" link in the navigation bar and filling out the registration form.
2. Log In: Log in to your account using the "Log In" link in the navigation bar.
3. Exercise Now: Click on the "Exercise Now" link to access the form for generating your customized exercise routine. Fill out the form with your preferences and submit it to generate a routine.
4. Mark Exercises as Completed: In the routine proposal, mark exercises as completed to add them to your personal track record. (WIP)
5. Track Record: View your exercise history by clicking on the "Track Record" link in the navigation bar. (WIP)
6. Add Exercise: Add new exercises to the database by clicking on the "Add Exercise" link and filling out the form.

## Contributing
Contributions welcome! I'd love to improve the app beyond what I was able to showcase for this first prototype and welcome any help, feedback or suggestions.
Please fork the repository, make your changes, and submit a pull request :)