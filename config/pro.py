# config/pro.py

from .default import *
from os import environ


# Environment configuration
APP_ENV = APP_ENV_PRODUCTION

# Postgre heroku database url
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
SQLALCHEMY_ECHO = False


SECRET_KEY = environ.get('SECRET_KEY')   
