from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Create a User model
class User(db.Model, UserMixin):
    # Create the columns of the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # set the table name to 'users'
    __tablename__ = 'users'
