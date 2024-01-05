from flask import Blueprint, render_template, request, flash, url_for, redirect, abort
from .models import db, User
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from .token import generate_confirmation_token, confirm_token
from .email import send_email
from .decorators import reset_requested, g
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

# initialize the bcrypt
bcrypt = Bcrypt()

# create a blueprint
auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # get the form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            # create the new user
            hashed_password = bcrypt.generate_password_hash(
                password).decode('utf-8')
            new_user = User(username=username, email=email,
                            password_hash=hashed_password)

            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            # generate the confirmation token
            token = generate_confirmation_token(new_user.email)
            confirm_url = url_for('views.confirm_email',
                                  token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(new_user.email, subject, html)

            # login the user
            login_user(new_user, remember=True)
            flash('Account created successfully! Please check your email to confirm your account.', category='success')
            return redirect(url_for('views.unconfirmed', username=username))
        except IntegrityError as e:
            # check if the username or email already exists
            db.session.rollback()
            if 'username' in str(e):
                flash('Username already exists.', category='error')
            elif 'email' in str(e):
                flash('Email already exists.', category='error')

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get the form data
        identifier = request.form.get('identifier') # username or email
        password = request.form.get('password')

        # check if the identifier (email or username) exists
        user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()

        # check if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.dashboard', username=user.username))
        else:
            flash('Incorrect username or password', category='error')

    return render_template('login.html')

# a route function to handle the password reset page
@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        # if a email is founded send the reset password email
        if user:
            # Invalidate the previous reset token if it exists
            user.reset_token = None
            db.session.commit()

            # Generate a new reset token and send the email
            update_reset_token(user)

            # send the emai with the new reset token
            token = user.reset_token
            reset_url = url_for('auth.reset_password',
                                  token=token, _external=True)
            html = render_template('reset_email.html', reset_url=reset_url)
            subject = "Password Reset Request"
            send_email(user.email, subject, html)
            flash('A reset link has been sent to your email address.', category='success')
        else:
            flash('Email address not found. If you do not have an account consider signing up', category='danger')
            return redirect(url_for('auth.sign_up'))
        
    return render_template('reset_request.html')


# a route function to handle the process of reseting the password
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
@reset_requested
def reset_password(token):
    try:
        email = confirm_token(token)
    except Exception as e:
        flash('The reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first_or_404()

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        hashed_password = bcrypt.generate_password_hash(
            new_password).decode('utf-8')
        
        # update the user password
        user.password_hash = hashed_password
        user.reset_token = None
        db.session.commit()

        flash('Your password has been updated!', category='success')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html', token=token)


            

# function to update the reset token and the reset token expiration time because the first token must be used
def update_reset_token(user):
    # Generate a new reset token and set its expiration time
    token = generate_confirmation_token(user.email)

    # update the user reset token and reset token expiration time
    user.reset_token = token
    db.session.commit()


# route function to logout the user
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
