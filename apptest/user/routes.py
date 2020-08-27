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
from apptest.auth.decorators import token_required, admin_required
from apptest.models import User

from . import user_bp

logger = logging.getLogger(__name__)



@user_bp.route('/list', methods=['GET'])
@token_required
@admin_required
def get_all_users(current_user, is_admin):

    logger.info('Obtenemos todos los usuarios, sin paginar')

    users = User.query.all()

    if not users:
        abort(404)
    
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    
    return jsonify({'users' : output})


@user_bp.route('/paginatedlist', methods=['GET'])
@token_required
@admin_required
def get_all_users_paginated(current_user, is_admin):

    logger.info('Obtenemos todos los usuarios, con paginado')

    if 'page' not in request.args or 'per_page' not in request.args:
        abort(400)

    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
    except ValueError:
        abort(400)

    users = User.query.order_by(User.name.asc()).paginate(page=page, per_page=per_page, error_out=False)
   
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
@admin_required
def get_one_user(current_user, is_admin, public_id):

    logger.info('Obtenemos el usuario vía su public_id')

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return abort(404)

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})


@user_bp.route('/create', methods=['POST'])
@token_required
@admin_required
def create_user(current_user, is_admin):

    logger.info('Creamos el usuario')

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})


@user_bp.route('/promote/<public_id>', methods=['PUT'])
@token_required
@admin_required
def promote_user(current_user, is_admin, public_id):

    logger.info('Promocionamos a administrador al usuario indicado')

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        abort(404)

    if user.admin:
        # TODO: Devolver un mensaje estándar http como toca. Analizar que código hay que devolver
        return jsonify({'message' : 'El usuario ya es administrador'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})


@user_bp.route('/delete/<public_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(current_user, is_admin, public_id):

    logger.info('Eliminamos el usuario indicado')

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        abort(404)

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})
