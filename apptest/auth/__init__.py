# APIRest_Flask\apptest\auth\__init__.py

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
from . import routes