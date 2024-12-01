document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const activityForm = document.getElementById('activity-form');
    const activityList = document.getElementById('activity-list');

    let users = [];
    let activities = [];

    // Handle Registration
    registerForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const user = {
            id: Date.now(),
            firstName: document.getElementById('first-name').value,
            lastName: document.getElementById('last-name').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            height: document.getElementById('height').value,
            weight: document.getElementById('weight').value,
            age: document.getElementById('age').value,
            gender: document.getElementById('gender').value,
            fitnessLevel: document.getElementById('fitness-level').value,
        };
        users.push(user);
        alert('Registration successful!');
        registerForm.reset();
    });

    // Handle Login
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        const user = users.find((u) => u.email === email && u.password === password);
        if (user) {
            alert('Login successful!');
            document.getElementById('activity-section').style.display = 'block';
            loginForm.reset();
        } else {
            alert('Invalid email or password.');
        }
    });

    // Log Activities
    activityForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const activity = {
            id: Date.now(),
            type: document.getElementById('activity-type').value,
            duration: document.getElementById('duration').value,
            calories: document.getElementById('calories').value,
            distance: document.getElementById('distance').value,
        };
        activities.push(activity);
        const li = document.createElement('li');
        li.textContent = `${activity.type}: ${activity.duration} min, ${activity.calories} cal, ${activity.distance} km`;
        activityList.appendChild(li);
        activityForm.reset();
    });
});
