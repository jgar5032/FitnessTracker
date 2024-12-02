from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    fitness_level = db.Column(db.String(20), nullable=True)

    activities = db.relationship('Activity', back_populates='user', cascade="all, delete-orphan")
    fitness_goals = db.relationship('Goal', back_populates='user', cascade="all, delete-orphan")
    friends = db.relationship('Friendship', foreign_keys='Friendship.user_id', back_populates='user', cascade="all, delete-orphan")

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Float, nullable=True)
    distance = db.Column(db.Float, nullable=True)
    steps = db.Column(db.Integer, nullable=True)
    date_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship('User', back_populates='activities')

class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    goal_type = db.Column(db.String(100), nullable=False)
    target_value = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    progress = db.Column(db.Float, default=0.0, nullable=False)
    user = db.relationship('User', back_populates='fitness_goals')

class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)

    user = db.relationship('User', foreign_keys=[user_id], back_populates='friends')
    friend = db.relationship('User', foreign_keys=[friend_id])

    # Ensure unique friendships between user and friend
    __table_args__ = (db.UniqueConstraint('user_id', 'friend_id', name='unique_friendship'),)

