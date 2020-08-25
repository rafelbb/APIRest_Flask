# APIRest_securizada_bdd_blueprints\apptest\__init__.py

import logging
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData


# Esta chapuza es por usar sqlite, que no genera nombres para ix:index, up:uniquekey, ck:check, fk:foreignkey, pk:primarykey. 

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

#db = SQLAlchemy()
migrate = Migrate()
	
def create_app(settings_module):
	
	app = Flask(__name__)
	app.config.from_object(settings_module)

	# 
	db.init_app(app)

	#migrate.init_app(app, db, render_as_batch=True)
	migrate.init_app(app, db, render_as_batch=True) # solo para sqlite que no puede gestionar correctamente los ALTER...
	
	
	# Registro de los Blueprints
	from .user import user_bp
	app.register_blueprint(user_bp)
	from .todo import todo_bp
	app.register_blueprint(todo_bp)
	
	# Registro de los handlers de errores customizados
	register_error_handlers(app)

	# Configuración de logger
	configure_logging(app)

	return app


def register_error_handlers(app):

	@app.errorhandler(400)
	def bad_request(error):
		return make_response(jsonify({'error' : 'bad request'}), 400)

	@app.errorhandler(401)
	def unauthorized(error):
		return make_response(jsonify({'error' : 'unauthorized'}), 401)

	@app.errorhandler(403)
	def forbidden(error):
		return make_response(jsonify({'error' : 'forbidden'}), 403)

	@app.errorhandler(404)
	def not_found(error):
		return make_response(jsonify({'error' : 'not found'}), 404)


def configure_logging(app):
    """
		DEBUG: Para depurar información. Nivel de información muy detallado.
		INFO: Para mensajes informativos que indican que la aplicación se está ejecutando correctamente.
		WARNING: Para mensajes de advertencia cuando la aplicación, aun funcionando correctamente, detecta una situación inesperada o posible problema futuro.
		ERROR: Para mensajes de error.
		EXCEPTION: Para mensajes de error que se producen debido a una excepción. Se muestra la traza de la excepción.
	"""
    # Eliminamos los posibles manejadores, si existen, del logger por defecto
    del app.logger.handlers[:]
    
	# Añadimos el logger por defecto a la lista de loggers
    loggers = [app.logger, ]
    handlers = []
    
	# Creamos el manejador para escribir los mensajes por consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())
	
    # Configuramos el nivel logging en función del entorno
    if (app.config['APP_ENV'] == app.config['APP_ENV_LOCAL']) or (app.config['APP_ENV'] == app.config['APP_ENV_TESTING']) or (app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']):
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)
    
    handlers.append(console_handler)
    
	# Asociamos cada uno de los handlers a cada uno de los loggers
    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
		# TODO: Averiguar si esta linea es necesario o no, ya la configuración del nivel del logger va en función del entorno 
        #l.setLevel(logging.DEBUG)


def verbose_formatter():
	return logging.Formatter(
	'[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
	datefmt='%d/%m/%Y %H:%M:%S'
    )
