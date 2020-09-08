# APIRest_Flask\apptest\auth\service.py

import datetime

import jwt
from flask import abort, jsonify, request, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

from apptest.models import User
from . import auth_bp


class Auth_sevice:

    def login_user(self):
        
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            abort(400)

        user = User.query.filter_by(name=auth.username).first()

        if not user or not user.active:
            abort(404)

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=current_app.config['APP_TOKEN_LIFE_TIME'])}, current_app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('UTF-8')})

        abort(401)
