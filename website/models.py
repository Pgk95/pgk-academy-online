from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Create a User model
class User(db.Model, UserMixin):
    # Create the columns of the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(1000), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    # Create a function to set the password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Create a function to check the password
    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    # set the table name to 'users'
    __tablename__ = 'users'
