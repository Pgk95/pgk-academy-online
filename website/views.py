from flask import Blueprint, render_template

# Create a blueprint
views = Blueprint('views', __name__);

# Initialize the routes
@views.route('/')
def home():
    return render_template('home.html')