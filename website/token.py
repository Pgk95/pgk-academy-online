from itsdangerous import URLSafeTimedSerializer
from flask import app
from dotenv import load_dotenv
import os

load_dotenv()

# function to generate token


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    return serializer.dumps(email, salt=os.getenv('SECURITY_PASSWORD_SALT'))
# function to confirm token


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    try:
        email = serializer.loads(
            token,
            salt=os.getenv('SECURITY_PASSWORD_SALT'),
            max_age=expiration
        )
    except:
        return False
    return email
