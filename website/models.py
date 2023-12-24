from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Create a User model

class User(db.Model, UserMixin):
    # Create the columns of the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    profile_picture = db.Column(db.String(255), default='default.png')
    password_hash = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    # set the table name to 'users'
    __tablename__ = 'users'


# Create a Course mode

class Course(db.Model, UserMixin):
    # Create the columns of the table
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(255), nullable=False)
    course_description = db.Column(db.String(1000), nullable=False)
    course_intructor = db.Column(db.String(255), nullable=False)
    course_price = db.Column(db.Integer, nullable=False)
    course_level = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    # set the table name to 'courses'
    __tablename__ = 'courses'