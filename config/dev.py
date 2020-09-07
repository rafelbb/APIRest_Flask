# config/dev.py
from .default import *


# Environment configuration
APP_ENV = APP_ENV_DEVELOPMENT

# Database configuration
#SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_DATABASE_URI = 'postgresql://apirest:1234@localhost:5432/gestion'
SQLALCHEMY_ECHO = True

SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
