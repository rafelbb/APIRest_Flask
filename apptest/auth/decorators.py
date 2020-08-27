# APIRest_Flask\apptest\auth\decorators.py
import datetime
from functools import wraps
import jwt
from flask import abort, current_app, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

from apptest import db
from apptest.models import User

from . import auth_bp


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            abort(400)

        try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            abort(401)

        return f(current_user, *args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            abort(400)

        try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            is_admin = User.query.filter_by(public_id=data['public_id'], admin=True).first()
            if not is_admin:
                abort(403)

        except:
            abort(401)

        return f(is_admin, *args, **kwargs)

    return decorated
