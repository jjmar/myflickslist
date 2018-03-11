from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='email_templates')

from . import routes
