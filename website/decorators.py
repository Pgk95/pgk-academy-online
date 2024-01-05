from functools import wraps

from flask import g, flash, redirect, url_for
from flask_login import current_user
from .models import User
from .token import confirm_token
from datetime import datetime

# a check_confirmed decorator to check if the user has confirmed their email address
def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **Kwargs):
        if current_user.confirmed is False:
            return redirect(url_for('views.unconfirmed'))
        return func(*args, **Kwargs)

    return decorated_function

# a reset_requested decorator to check if the user has requested a password reset
def reset_requested(func):
    @wraps(func)
    def decoratedd_function(*args, **Kwargs):
        token = Kwargs.get('token')
        if not token:
            flash('Invalid reset link', 'danger')
            return redirect(url_for('auth.login'))
        try:
            email = confirm_token(token)
        except Exception as e:
            flash('The reset link is invalid or has expired.', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first_or_404()
        if not user or user.reset_token != token:
            flash('Invalid reset link', 'danger')
            return redirect(url_for('auth.login'))
        
        # Store the user in the context for further use
        g.user = user

        return func(*args, **Kwargs)
    return decoratedd_function
