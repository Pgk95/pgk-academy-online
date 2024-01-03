from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .models import User
from .decorators import check_confirmed
from . import db
from .email import send_email
from .token import confirm_token, generate_confirmation_token

# Create a blueprint
views = Blueprint('views', __name__)

# Initialize the routes


@views.route('/')
def home():
    return render_template('base.html')


@views.route('/About_Us')
def about_us():
    return render_template("about.html")


@views.route('/Contact')
def contact():
    return render_template("contact_us.html")


@views.route('/dashboard')
@login_required
@check_confirmed
def dashboard():
    return render_template("dashboard.html")


@views.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except Exception as e:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()

    if user.confirmed:
        flash('Account already confirmed.', 'success')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('views.dashboard'))


@views.route('/resend')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('views.dashboard'))
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')


@views.route('/resend_confirmation')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('views.confirm_email',
                          token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation emai has been sent.', 'success')
    return redirect(url_for('views.unconfirmed'))
   

# a route function to handle the reset_request.html page
@views.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    return render_template('reset_request.html', title='Reset Password')


@views.route('/courses')
def courses():
    return render_template('courses.html')