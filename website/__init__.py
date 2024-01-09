from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
import os


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


# Load environment variables
load_dotenv()

# Create app


def create_app():
    # intializing the name of the app
    app = Flask(__name__)

    # handling static files for the profile picture
    app.config['UPLOAD_FOLDER'] = 'website/static/profile_pics'

    # setting the secret key and database uri
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

    # configurations for the email server
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_MAX_EMAILS'] = os.getenv('MAIL_MAX_EMAILS')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    app.config['MAIL_ASCII_ATTACHMENTS'] = os.getenv('MAIL_ASCII_ATTACHMENTS')

    # initialize the database
    db.init_app(app)
    migrate.init_app(app, db)

    # initialize the mail server
    mail.init_app(app)

    # import the views, models, auth
    from .views import views
    from .auth import auth
    from .course import course
    from .profile import profile


    # register the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(course, url_prefix='/dashboard/')
    app.register_blueprint(profile, url_prefix='/dashboard/')

    # database creation
    from .models import User

    create_db(app)

    # initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # load the user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # function to handle the error 404 status code
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app


# function to create the database
def create_db(app):
    with app.app_context():
        db.create_all()
