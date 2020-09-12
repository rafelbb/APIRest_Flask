# APIRest_securizada_bdd_blueprints\apptest\entrypoint.py
from os import environ
from apptest import create_app



settings_module = environ.get('APP_SETTINGS_MODULE')
app = create_app(settings_module)

