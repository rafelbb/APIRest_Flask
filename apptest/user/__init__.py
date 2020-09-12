# APIRest_Flask\apptest\user\__init__.py

from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/users')
from . import routes