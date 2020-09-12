# config/pro.py

from .default import *
from os import environ


# Environment configuration
APP_ENV = APP_ENV_PRODUCTION

# Postgre heroku database url
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
SQLALCHEMY_ECHO = False

SECRET_KEY = environ.get('SECRET_KEY')   
CACHE_TYPE = environ.get('CACHE_TYPE')

#Hash method for generation and password check
PWD_HASH_METHOD = environ.get('PWD_HASH_METHOD')

#Json web Token lifetime (minutes)
APP_TOKEN_LIFE_TIME = environ.get('APP_TOKEN_LIFE_TIME')
