# APIRest_securizada_bdd_blueprints\app\todo\__init__.py

from flask import Blueprint

todo_bp = Blueprint('todo', __name__)
from . import routes