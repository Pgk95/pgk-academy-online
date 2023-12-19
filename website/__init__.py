from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_login import LoginManager
import os


db = SQLAlchemy()
migrate = Migrate()
login_manager=LoginManager()


# Load environment variables
load_dotenv()

# Create app
def create_app():
    # intializing the name of the app
    app = Flask(__name__)

    # setting the secret key and database uri
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    
    # initialize the database
    db.init_app(app)
    migrate.init_app(app, db)

    # import the views, models, auth
    from .views import views
    from .auth import auth

    # register the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # database creation
    from .models import User

    return app


# function to create the database
def create_db(app):
    with app.app_context():
        db.create_all()