# APIRest_Flask\apptest\auth\routes.py

import logging
from apptest.auth.service import Auth_sevice
from flask import abort, jsonify, request, current_app
from . import auth_bp


logger = logging.getLogger(__name__)
auth_service = Auth_sevice()


@auth_bp.route('/login', methods=['GET'])
def login():

    logger.info(
        'Hacemos login del usuario para obtener el token de autenticación')
    return auth_service.login_user()
