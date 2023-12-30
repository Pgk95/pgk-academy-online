from flask_mail import Message
from . import mail
from dotenv import load_dotenv
import os

load_dotenv()
# function to send email


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=os.getenv('MAIL_DEFAULT_SENDER')
    )
    mail.send(msg)
