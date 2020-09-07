# config/testing.py

from .default import *


# Parámetros para activar el modo debug
TESTING = True
DEBUG = True
WTF_CSRF_ENABLED = False

# Environment configuration
APP_ENV = APP_ENV_TESTING
"""
# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_ECHO = True

SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
"""
