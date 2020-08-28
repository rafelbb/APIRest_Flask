# config/default.py

# Configuración de base de datos
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Entornos de ejecución
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''

# Tiempo de vida del token (minutos)
APP_TOKEN_LIFE_TIME = 30