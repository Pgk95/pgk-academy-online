from flask import Blueprint, render_template

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

@views.route('/Dashboard/<username>')
def dashboard(username):
    return render_template("dashboard.html", username=username)