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
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    reset_token = db.Column(db.String(1000), unique=True)

    # set the table name to 'users'
    __tablename__ = 'users'


# Create a Course model

# class Course(db.Model, UserMixin):
    # Create the columns of the table
    # id = db.Column(db.Integer, primary_key=True)
   # name = db.Column(db.String(255), nullable=False)
   # description = db.Column(db.Text, nullable=False)
   # pdf_link = db.Column(db.String(255), nullable=False)
   # created_at = db.Column(db.DateTime(timezone=True),
                          # server_default=func.now())

    # set the table name to 'courses'
    # __tablename__ = 'courses'
