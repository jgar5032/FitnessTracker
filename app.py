from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Goal, Activity, Friendship
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ensure the database directory exists
os.makedirs('instance', exist_ok=True)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "fitness_tracker.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Ensure tables are created once
first_request_done = False
@app.before_request
def create_tables_once():
    global first_request_done
    if not first_request_done:
        db.create_all()
        first_request_done = True

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Registration route
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

# Login route
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

# Profile page
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

# Log new activity
@app.route('/add_activity', methods=['GET', 'POST'])
def add_activity():
    if 'user_id' not in session:
        flash('Please log in to add activities.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        activity = Activity(
            user_id=session['user_id'],
            activity_type=request.form['activity_type'],
            duration=request.form['duration'],
            distance=request.form['distance'],
            steps=request.form['steps'],
            calories=request.form['calories']
        )
        db.session.add(activity)
        db.session.commit()
        flash('Activity logged successfully.')
        return redirect(url_for('profile'))
    return render_template('add_activity.html')

# Manage friends
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
            existing_friendship = Friendship.query.filter(
                ((Friendship.user_id == user.id) & (Friendship.friend_id == friend.id)) |
                ((Friendship.user_id == friend.id) & (Friendship.friend_id == user.id))
            ).first()
            if not existing_friendship:
                new_friendship = Friendship(user_id=user.id, friend_id=friend.id, status='pending')
                db.session.add(new_friendship)
                db.session.commit()
                flash('Friend request sent successfully.')
            else:
                flash('You are already connected or have a pending request.')
        else:
            flash('Invalid email address or user not found.')

    incoming_requests = Friendship.query.filter_by(friend_id=user.id, status='pending').all()
    accepted_friendships = Friendship.query.filter(
        ((Friendship.user_id == user.id) | (Friendship.friend_id == user.id)) &
        (Friendship.status == 'accepted')
    ).all()

    def calculate_metrics(person):
        activities = Activity.query.filter_by(user_id=person.id).all()
        return {
            'name': person.name,
            'email': person.email,
            'bmi': round(person.weight / ((person.height / 100) ** 2), 2) if person.height and person.weight else None,
            'avg_steps': round(sum(a.steps for a in activities if a.steps) / len(activities), 2) if activities else None,
            'avg_duration': round(sum(a.duration for a in activities if a.duration) / len(activities), 2) if activities else None,
            'goals_met': Goal.query.filter_by(user_id=person.id).filter(Goal.progress >= Goal.target_value).count(),
            'goals_unmet': Goal.query.filter_by(user_id=person.id).filter(Goal.progress < Goal.target_value).count()
        }

    friends_data = [calculate_metrics(friendship.friend if friendship.user_id == user.id else friendship.user)
                    for friendship in accepted_friendships]
    friends_data.append(calculate_metrics(user))  # Include logged-in user in comparison

    # Sorting logic
    sort_category = request.args.get('sort', 'bmi')
    reverse_sort = sort_category not in ['bmi']  # BMI is sorted ascending; others descending

    # Sort with N/A (None values) pushed to the bottom
    def sorting_key(item):
        value = item.get(sort_category)
        if value is None:
            # Assign inf or -inf based on sorting direction
            return float('inf') if not reverse_sort else float('-inf')
        return value

    # Sort friends_data
    friends_data.sort(key=sorting_key, reverse=reverse_sort)

    return render_template('friends.html', user=user, incoming_requests=incoming_requests, accepted_friends=friends_data, sort_category=sort_category)

# Update friendship status
@app.route('/update_friendship/<int:friendship_id>', methods=['POST'])
def update_friendship(friendship_id):
    if 'user_id' not in session:
        flash('Please log in to update friendships.')
        return redirect(url_for('login'))
    friendship = Friendship.query.get(friendship_id)
    if friendship and friendship.friend_id == session['user_id']:
        friendship.status = request.form['status']
        db.session.commit()
        flash('Friendship status updated successfully.')
    return redirect(url_for('friends'))

# Manage goals
@app.route('/goals', methods=['GET', 'POST'])
def goals():
    if 'user_id' not in session:
        flash('Please log in to access your goals.')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if request.method == 'POST' and 'goal_type' in request.form:
        goal = Goal(user_id=user.id, goal_type=request.form['goal_type'], target_value=request.form['target_value'],
                    end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'))
        db.session.add(goal)
        db.session.commit()
        flash('New goal added successfully.')

    active_goals = Goal.query.filter_by(user_id=user.id).filter(Goal.progress < Goal.target_value).all()
    return render_template('goals.html', user=user, goals=active_goals)

@app.route('/update_goal/<int:goal_id>', methods=['POST'])
def update_goal(goal_id):
    if 'user_id' not in session:
        flash('Please log in to update goals.')
        return redirect(url_for('login'))
    goal = Goal.query.get(goal_id)
    if goal and goal.user_id == session['user_id']:
        if request.form['status'] == 'met':
            goal.progress = goal.target_value
            db.session.commit()
            flash('Goal marked as met and removed.')
    return redirect(url_for('goals'))

# Metrics page
@app.route('/metrics')
def metrics():
    if 'user_id' not in session:
        flash('Please log in to access your metrics.')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    activities = Activity.query.filter_by(user_id=user.id).all()
    bmi = round(user.weight / ((user.height / 100) ** 2), 2) if user.weight and user.height else None
    target_heart_rate = f"{int((220 - user.age) * 0.5)} - {int((220 - user.age) * 0.85)} bpm" if user.age else None
    avg_steps = round(sum(a.steps for a in activities if a.steps) / len(activities), 2) if activities else None
    avg_duration = round(sum(a.duration for a in activities if a.duration) / len(activities), 2) if activities else None
    return render_template('metrics.html', bmi=bmi, target_heart_rate=target_heart_rate, avg_steps=avg_steps, avg_duration=avg_duration)

# Progress page
@app.route('/progress')
def progress():
    if 'user_id' not in session:
        flash('Please log in to access your progress.')
        return redirect(url_for('login'))

    activities = Activity.query.filter_by(user_id=session['user_id']).all()
    total_distance = round(sum(a.distance for a in activities if a.distance), 2) if activities else 0
    total_steps = sum(a.steps for a in activities if a.steps) if activities else 0
    total_calories = round(sum(a.calories for a in activities if a.calories), 2) if activities else 0
    return render_template('progress.html', activities=activities, total_distance=total_distance,
                           total_steps=total_steps, total_calories=total_calories)

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
