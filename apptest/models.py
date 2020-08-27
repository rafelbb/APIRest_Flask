# APIRest_securizada_bdd_blueprints\apptest\models.py

# relative import  . porque estamos importando db del mismo package (Remember that importing a package essentially imports the package’s __init__.py file as a module)
from .extensions import db


class User(db.Model):
    __tablename__ = 'tbl_users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    todos = db.relationship('Todo', backref='user', lazy='dynamic')

class Todo(db.Model):
    __tablename__ = 'tbl_todos'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_users.id'))

# TODO: Existirá una relación N-M entre User y Roles
class Rol(db.Model):
    __tablename__ = "tbl_roles"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20))

