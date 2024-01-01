from flask import Blueprint, render_template, request, flash, url_for, redirect, abort
from .models import db, User
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from .token import generate_confirmation_token, confirm_token
from .email import send_email
from sqlalchemy.exc import IntegrityError

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
        username = request.form.get('username')
        password = request.form.get('password')

        # check if the username or password exists
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.dashboard', username=username))
        else:
            flash('Incorrect username or password.', category='error')
    return render_template('login.html')

# route function to logout the user
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
