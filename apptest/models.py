# APIRest_Flask\apptest\models.py

import uuid
import datetime
from werkzeug.security import generate_password_hash
from .extensions import db



roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model):

    def __init__(self, email, name, password):
        self.public_id = str(uuid.uuid4())
        self.email = email
        self.name = name
        self.password = generate_password_hash(password, method='sha256')
        self.active = True
        self.confirmed_at = datetime.datetime.utcnow()
        self.admin = False

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    #TODO: Eiminar la propiedad 'admin' al ser sustituida por el rol 'admin'
    admin = db.Column(db.Boolean)
    todos = db.relationship('Todo', backref='user', lazy='dynamic')
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users'))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True)
    description = db.Column(db.String(255))
    other_description = db.Column(db.String(255))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))