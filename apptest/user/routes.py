# APIRest_securizada_bdd_blueprints\apptest\user\routes.py

import datetime
import logging
import uuid
from functools import wraps

import jwt
from flask import abort, current_app, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from apptest import db
from apptest.models import User

from . import user_bp

logger = logging.getLogger(__name__)

# TODO: Crear un paquete auth para el login y modelo de usuario. auth/models.py; auth/routes.py
# TODO: Crear los decorator necesarios en una paquete separado auth/decorators.py;. Por ejemplo este de token_required y uno de admin_required

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


@user_bp.route('/login')
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


@user_bp.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    logger.info('Obtenemos todos los usuarios, sin paginar')

    if not current_user.admin:
        abort(403)

    users = User.query.all()
   
    # TODO: Verificar si la lista está vacia. if not users: abort(404)
   
    # Creamos la lista con los resultados
    output = []
    # Rellenamos la lista de resultados en base a diccionarios de dastos
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    
    return jsonify({'users' : output})


@user_bp.route('/userpaginated', methods=['GET'])
@token_required
def get_all_users_paginated(current_user):

    logger.info('Obtenemos todos los usuarios, con paginado')

    if not current_user.admin:
        abort(403)

    if 'page' not in request.args or 'per_page' not in request.args:
        abort(400)

    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
    except ValueError:
        abort(400)

    users = User.query.order_by(User.name.asc()).paginate(page=page, per_page=per_page, error_out=False)
    
    # TODO: Verificar si la lista está vacia
   
    # Creamos la lista con los resultados
    output = []
    # Rellenamos la lista de resultados en base a diccionarios de dastos
    for user in users.items:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    
    return jsonify({'users' : output})


@user_bp.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    logger.info('Obtenemos el usuario vía su public_id')

    if not current_user.admin:
        abort(403)

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return abort(404)

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})


@user_bp.route('/user', methods=['POST'])
@token_required
def create_user(current_user):

    logger.info('Creamos el usuario')

    if not current_user.admin:
        abort(403)

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})


@user_bp.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):

    logger.info('Promocionamos a administrador al usuario indicado')

    if not current_user.admin:
        abort(403)

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        abort(404)

    if user.admin:
        # TODO: Devolver un mensaje estándar http como toca. Analizar que código hay que devolver
        return jsonify({'message' : 'ya es admin!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})


@user_bp.route('/user/<public_id>', methods=['DELETE'])
@token_required
#@admin_required
def delete_user(current_user, public_id):

    logger.info('Eliminamos el usuario indicado')

    if not current_user.admin:
        abort(403)

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        abort(404)

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})
