# APIRest_securizada_bdd_blueprints\apptest\entrypoint.py
from apptest import create_app



# TODO: crear la variable de entorno 'APP_SETTINGS_MODULE' para definir la configuración del proyecto
#settings_module = os.getenv('APP_SETTINGS_MODULE')
settings_module = 'config.dev'
app = create_app(settings_module)

