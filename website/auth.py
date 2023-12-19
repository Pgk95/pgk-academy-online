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
    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
