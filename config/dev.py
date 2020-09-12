# config/dev.py

from .default import *
from os import environ


# Environment configuration
APP_ENV = APP_ENV_DEVELOPMENT

# Database configuration
#SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_DATABASE_URI = 'postgresql://apirest:1234@localhost:5432/gestion'
SQLALCHEMY_ECHO = True

#SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
SECRET_KEY = environ.get('SECRET_KEY')
CACHE_TYPE = 'simple'

#Hash method for generation and password check
PWD_HASH_METHOD = 'sha256'

#Json web Token lifetime (minutes)
APP_TOKEN_LIFE_TIME = 30


