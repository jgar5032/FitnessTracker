from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_migrate import Migrate  # Import Flask-Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Goal, Activity, Friendship
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ensure the 'instance' folder exists
os.makedirs('instance', exist_ok=True)

# Configure the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "fitness_tracker.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Initialize a global flag for creating tables
first_request_done = False

@app.before_request
def create_tables_once():
    global first_request_done  # Declare the variable as global
    if not first_request_done:
        db.create_all()
        first_request_done = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful.')
            return redirect(url_for('profile'))
        flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in to access your profile.')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    activities = Activity.query.filter_by(user_id=user.id).all()

    if request.method == 'POST':
        user.height = request.form.get('height', type=float)
        user.weight = request.form.get('weight', type=float)
        user.age = request.form.get('age', type=int)
        user.gender = request.form.get('gender')
        user.fitness_level = request.form.get('fitness_level')

        db.session.commit()
        flash('Profile updated successfully.')

    return render_template('profile.html', user=user, activities=activities)

@app.route('/add_activity', methods=['GET', 'POST'])
def add_activity():
    if 'user_id' not in session:
        flash('Please log in to add activities.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        activity_type = request.form['activity_type']
        duration = request.form['duration']
        distance = request.form['distance']
        steps = request.form['steps']
        calories = request.form['calories']
        activity = Activity(
            user_id=session['user_id'],
            activity_type=activity_type,
            duration=duration,
            distance=distance,
            steps=steps,
            calories=calories
        )
        db.session.add(activity)
        db.session.commit()
        flash('Activity logged successfully.')
        return redirect(url_for('profile'))
    return render_template('add_activity.html')

@app.route('/goals', methods=['GET', 'POST'])
def goals():
    if 'user_id' not in session:
        flash('Please log in to access your goals.')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        goal_type = request.form['goal_type']
        target_value = request.form['target_value']
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        new_goal = Goal(user_id=user.id, goal_type=goal_type, target_value=target_value, end_date=end_date)
        db.session.add(new_goal)
        db.session.commit()
        flash('New goal added successfully.')

    goals = Goal.query.filter_by(user_id=user.id).all()
    return render_template('goals.html', user=user, goals=goals)

@app.route('/friends', methods=['GET', 'POST'])
def friends():
    if 'user_id' not in session:
        flash('Please log in to access your friends list.')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        friend_email = request.form['friend_email']
        friend = User.query.filter_by(email=friend_email).first()
        if friend and friend.id != user.id:
            existing_friendship = Friendship.query.filter_by(user_id=user.id, friend_id=friend.id).first()
            if not existing_friendship:
                new_friendship = Friendship(user_id=user.id, friend_id=friend.id)
                db.session.add(new_friendship)
                db.session.commit()
                flash('Friend request sent successfully.')
            else:
                flash('You are already connected or have a pending request.')
        else:
            flash('Invalid email address or user not found.')

    friends = Friendship.query.filter_by(user_id=user.id).all()
    return render_template('friends.html', user=user, friends=friends)

@app.route('/update_friendship/<int:friendship_id>', methods=['POST'])
def update_friendship(friendship_id):
    friendship = Friendship.query.get(friendship_id)
    if 'status' in request.form:
        friendship.status = request.form['status']
        db.session.commit()
        flash('Friendship status updated successfully.')
    return redirect(url_for('friends'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
