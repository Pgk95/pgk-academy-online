from flask import Flask, render_template, Blueprint
from flask_login import login_required

# Create a blueprint
course = Blueprint('course', __name__)


# Initialize the routes
@course.route('/create_course')
@login_required
def create_course():
    return render_template('create_course.html')