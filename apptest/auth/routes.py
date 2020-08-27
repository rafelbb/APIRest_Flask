# APIRest_Flask\apptest\auth\routes.py

import datetime
import logging
from functools import wraps

import jwt
from flask import abort, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

from apptest import db
from apptest.models import User

from .decorators import token_required
from . import auth_bp



logger = logging.getLogger(__name__)


@auth_bp.route('/login')
def login():

    logger.info('Hacemos login del usuario para obtener el token de autenticación')

    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        abort(400)
    
    user = User.query.filter_by(name=auth.username).first()

    if not user:
        abort(401)

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    abort(401)
    