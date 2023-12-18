from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create app
def create_app():
    # intializing the name of the app
    app = Flask(__name__)

    # setting the secret key and database uri
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

    # import the views, models, auth
    from .views import views
    from .auth import auth

    # register the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app