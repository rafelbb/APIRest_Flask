# APIRest_Flask\apptest\user\routes.py

import logging
from apptest.user.service import User_service
from apptest.auth.decorators import admin_required, token_required

from . import user_bp



logger = logging.getLogger(__name__)
user_service = User_service()

@user_bp.route('/list', methods=['GET'])
@token_required
def get_all_users():

    logger.info('Obtenemos todos los usuarios, sin paginar')
    return user_service.find_all_users()


@user_bp.route('/paginatedlist', methods=['GET'])
@token_required
def get_all_users_paginated():

    logger.info('Obtenemos todos los usuarios, con paginado')
    return user_service.find_all_users_paginated()


@user_bp.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(public_id):

    logger.info('Obtenemos el usuario vía su public_id')
    return user_service.find_user_by_Id(public_id)


@user_bp.route('/user/<user_id>/todos', methods=['GET'])
@token_required
def get_user_todos(user_id):

    # TODO: La referencia al usuario debe ser vía el id público

    logger.info('Obtenemos los todo del usuario')
    return user_service.find_user_todos(user_id)
    

@user_bp.route('/user/<user_id>/todo/<todo_id>', methods=['GET'])
@token_required
def get_user_todo(user_id, todo_id):
    
    # TODO: La referencia al usuario debe ser vía el id público
    
    logger.info('Obtenemos un todo del usuario')
    return user_service.find_user_todo(user_id, todo_id)


@user_bp.route('/create', methods=['POST'])
@token_required
@admin_required
def create_user():

    logger.info('Creamos el usuario')
    return user_service.save_user()


@user_bp.route('/create/<user_id>/todo', methods=['POST'])
@token_required
def create_user_todo(user_id):

    # TODO: La referencia al usuario debe ser vía el id público

    logger.info('Creamos un todo para un usuario')
    return user_service.save_user_todo(user_id)


@user_bp.route('/user/<public_id>/promote', methods=['PUT'])
@token_required
@admin_required
def promote_user(public_id):

    logger.info('Promocionamos a administrador al usuario indicado')
    return user_service.save_promote_user(public_id)
    


@user_bp.route('/delete/<public_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(public_id):

    logger.info('Eliminamos el usuario indicado')
    return user_service.delete(public_id)
    

