# FitnessTracker
CS480 Final Project

Names: Ayush Panda, Jose Garcia Rowlands, Shreeya Ryali, Pritika Bhattacharya
Fitness Tracker System Project

How To Run Program:
Create a virtual environment: python3 -m venv venv

Activate virtual environment: (macOS/Linux): source venv/bin/activate (Windows): venv\Scripts\activate

Install dependencies: pip install -r requirements.txt

start a mysql server: mysql.server start

login to mysql (just hit enter for password): mysql -u root -p

create the database and your user:

CREATE DATABASE fitness_tracker;
CREATE USER 'demo_user'@'localhost' IDENTIFIED BY 'demo_pass';
GRANT ALL PRIVILEGES ON fitness_tracker.* TO 'demo_user'@'localhost';
FLUSH PRIVILEGES;
EXIT


Start flask development server: flask run

Open browser: http://127.0.0.1:5000

Overview: This project aims to build a fitness tracker system to track activities, set goals, monitor progress, and
analyze data. There are two primary roles: users and administrators. Users can log activities, set personal goals,
track progress, and engage in social challenges with friends. Administrators can manage user accounts, view system
stats, and configure settings like goals and metrics.

Data Requirements
Users Each user has the following data:
  ● User ID (unique identifier)
  ● Name (first and last)
  ● Email Address (login)
  ● Password (secure access)
  ● Height (cm)
  ● Weight (kg)
  ● Age (years)
  ● Gender
  ● Fitness Level (Beginner, Intermediate, Advanced)
  ● Fitness Goals (e.g., weight loss, muscle gain)
  ● Friends List (connected users for challenges)

Activities Tracks fitness activities:
  ● Activity ID (unique identifier)
  ● Activity Type (e.g., running, cycling, weightlifting)
  ● Duration (minutes)
  ● Calories Burned (calculated)
  ● Distance (for running, cycling)
  ● Steps Count (for walking/running)
  ● Date & Time (activity completion)
  
Goals Tracks user goals:
  ● Goal ID (unique identifier)
  ● Goal Type (e.g., weight loss, stamina)
  ● Target Value (e.g., 10 kg weight loss)
  ● Start Date (goal set date)
  ● End Date (target completion date)
  ● Progress (real-time tracking)
  
Friends & Challenges Supports social interaction:
  ● Friendship Records (user connections)
  ● Challenge Records (e.g., “most kilometers in a month”)
  ● Challenge Status (completed, ongoing)
  
Metrics Tracks fitness analysis:
  ● BMI (Body Mass Index)
  ● Heart Rate (optional, with devices)
  ● Steps Per Day
  ● Average Activity Duration
  
Application Requirements
Users
  ● Registration & Login: New users register with personal details (name, email, password). Login is via
email/password.
  ● Tracking Activities: Users log activities manually or sync with devices, with calories burned, distance, etc.
Users can view activity history.
  ● Set Goals: Users set and track goals (e.g., weight loss). Track progress versus actual activity.
  ● Social Interaction: Users can add friends, view their progress, and challenge them in fitness competitions.
  ● View Progress: Users can view reports on their progress, like total distance run and calories burned.
  ● Update Profile: Users can update details like height, weight, and fitness level.
Administrators
  ● User Management: View profiles, activity data, and manage user accounts (e.g., deactivate or reset
  passwords).
  ● System Settings: Configure goals, metrics, and user categories (e.g., beginner, advanced). Generate
  reports on system usage.
  ● Activity & Device Management: Manage supported devices and activity types.
  ● Data Analysis: Access aggregate user data to generate reports on trends, popular goals, and average
  progress.
  System Features & Technologies
  ● User Interface: Mobile-friendly or web interface for navigation.
  ● Database: Secure storage for user data, activities, goals, and metrics.
  ● Notifications: Send reminders for activity tracking and challenges.
  ● Analytics: Display graphs for progress tracking over time.
