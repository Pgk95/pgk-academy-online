from . import db
from flask_login import UserMixin

# Create a User model
class User(db.Model, UserMixin):
    # Create the columns of the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    # set the table name to 'users'
    __tablename__ = 'users'