from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User model representing application users
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    name = db.Column(db.String(100), nullable=False)  # User's name
    email = db.Column(db.String(100), unique=True, nullable=False)  # Unique email
    password = db.Column(db.String(200), nullable=False)  # Hashed password
    height = db.Column(db.Float, nullable=True)  # User's height in cm
    weight = db.Column(db.Float, nullable=True)  # User's weight in kg
    age = db.Column(db.Integer, nullable=True)  # User's age
    gender = db.Column(db.String(10), nullable=True)  # User's gender
    fitness_level = db.Column(db.String(20), nullable=True)  # Fitness level

    # Relationships
    activities = db.relationship('Activity', back_populates='user', cascade="all, delete-orphan")
    fitness_goals = db.relationship('Goal', back_populates='user', cascade="all, delete-orphan")
    friends = db.relationship('Friendship', foreign_keys='Friendship.user_id', back_populates='user', cascade="all, delete-orphan")

# Activity model for logging user activities
class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each activity
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Associated user ID
    activity_type = db.Column(db.String(100), nullable=False)  # Type of activity
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    calories = db.Column(db.Float, nullable=True)  # Calories burned
    distance = db.Column(db.Float, nullable=True)  # Distance in km
    steps = db.Column(db.Integer, nullable=True)  # Steps taken
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Date of activity
    user = db.relationship('User', back_populates='activities')  # Link to user

# Goal model for tracking user fitness goals
class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each goal
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Associated user ID
    goal_type = db.Column(db.String(100), nullable=False)  # Type of goal
    target_value = db.Column(db.Float, nullable=False)  # Target value for the goal
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Goal start date
    end_date = db.Column(db.DateTime, nullable=False)  # Goal end date
    progress = db.Column(db.Float, default=0.0, nullable=False)  # Current progress
    user = db.relationship('User', back_populates='fitness_goals')  # Link to user

# Friendship model for managing user relationships
class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each friendship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Requesting user ID
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Friend's user ID
    status = db.Column(db.String(20), default='pending', nullable=False)  # Friendship status

    # Relationships for user and friend
    user = db.relationship('User', foreign_keys=[user_id], back_populates='friends')
    friend = db.relationship('User', foreign_keys=[friend_id])

    # Ensure unique friendships
    __table_args__ = (db.UniqueConstraint('user_id', 'friend_id', name='unique_friendship'),)
