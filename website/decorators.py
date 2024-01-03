from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

# a check_confirmed decorator to check if the user has confirmed their email address
def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **Kwargs):
        if current_user.confirmed is False:
            return redirect(url_for('views.unconfirmed'))
        return func(*args, **Kwargs)

    return decorated_function
