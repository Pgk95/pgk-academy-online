from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import db, User
from flask_login import login_user
from website import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

# create a blueprint
auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    error_messages = {
        'username_error': 'Username already exists',
        'email_error': 'Email already exists',
        'password_error': 'Passwords do not match'}

    if request.method == 'POST':
        # Get the data from the form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if the username or email already exists
        if User.query.filter_by(username=username).first():
            flash(error_messages['username_error'], category='error')

        # Check if the email already exists
        elif User.query.filter_by(email=email).first():
            flash(error_messages['email_error'], category='error')

        # Check if the password and confirm password match
        elif password != confirm_password:
            flash(error_messages['password_error'], category='error')
        else:
            # Create a new user
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username,
                email=email,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()

            # Log in the user
            if login_user(new_user):
                return redirect(url_for('views.dashboard', username=username))

    return render_template('signup.html', error_messages=error_messages)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template(url_for('auth.login'))
