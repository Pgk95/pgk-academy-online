from flask import render_template, Blueprint
from flask_login import login_required

# Create a blueprint
course = Blueprint('course', __name__)


# Initialize the routes
@course.route('/course', methods=['GET', 'POST'])
@login_required
def view_course():
    return render_template('course.html', course=course)

@course.route('/course_page')
@login_required
def course_page():
    return render_template('./courses/course_python.html')