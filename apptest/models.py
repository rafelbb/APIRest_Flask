# APIRest_Flask\apptest\models.py

import uuid
import datetime
from flask import current_app
from werkzeug.security import generate_password_hash
from .extensions import db



roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model):

    def __init__(self, email, name, password, active=True, admin=False):
        self.public_id = str(uuid.uuid4())
        self.email = email
        self.name = name
        self.password = generate_password_hash(password, method=current_app.config['PWD_HASH_METHOD'])
        self.active = active
        self.confirmed_at = datetime.datetime.utcnow()
        self.admin = admin

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

    def __repr__(self):
        return "User ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(self.public_id, self.email, self.name, self.password, 
                                                                        self.active, self.confirmed_at, self.admin)

    def __str__(self):
        return '{} {}'.format(self.public_id, self.email, self.name, self.active, self.confirmed_at, self.admin)


class Role(db.Model):

    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True)
    description = db.Column(db.String(255))
    other_description = db.Column(db.String(255))

    def __repr__(self):
        return "Role('{}', '{}')".format(self.name, self.description)

    def __str__(self):
        return '{} {}'.format(self.name, self.description)


class Todo(db.Model):

    def __init__(self, text, complete, user_id):
        self.text = text
        self.complete = complete
        self.user_id = user_id

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "Todo('{}', '{}', '{}')".format(self.text, self.complete, self.user_id)
    
    def __str__(self):
        return '{} {} {}'.format(self.text, self.complete, self.user_id)

