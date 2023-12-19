from flask import Blueprint, render_template
from flask_login import login_required

# Create a blueprint
views = Blueprint('views', __name__)

# Initialize the routes
@views.route('/')
def home():
    return render_template('base.html')

@views.route('/About_Us')
def about_us():
    return render_template("about.html")

@views.route('/Contact_Us')
def contact_us():
    return render_template("contact us.html")

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")