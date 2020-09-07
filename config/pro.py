# config/pro.py

from .default import *
from os import environ, path
from dotenv import load_dotenv



basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# Environment configuration
APP_ENV = APP_ENV_PRODUCTION

# Database configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://apirest:1234@localhost:5432/gestion'
SQLALCHEMY_ECHO = False


SECRET_KEY = environ.get('SECRET_KEY')

