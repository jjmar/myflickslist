from app import mail

from flask import current_app, render_template
from flask_mail import Message

from threading import Thread


def _send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def _send_email(recipient, subject, template_name, **kwargs):
    msg = Message(subject, recipients=[recipient])
    msg.body = render_template('{}.txt'.format(template_name), **kwargs)
    app = current_app._get_current_object()
    thread = Thread(target=_send_async_email, args=[app, msg])
    thread.start()
    return thread


def send_welcome_email(recipient, username, token):
    _send_email(recipient=recipient, subject='MFL - Welcome!', template_name='welcome', username=username, token=token)


def send_reset_password_email(recipient, username, token):
    _send_email(recipient=recipient, subject='MFL - Reset Password', template_name='reset_password', username=username,
                token=token)
