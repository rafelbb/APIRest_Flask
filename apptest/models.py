# APIRest_Flask\apptest\models.py

# relative import  . porque estamos importando db del mismo package (Remember that importing a package essentially imports the package’s __init__.py file as a module)
from .extensions import db

#class User(db.Model, UserMixin):
class User(db.Model):
    #__tablename__ = 'tbl_users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    #email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(255))
    #active = db.Column(db.Boolean())
    #confirmed_at = db.Column(db.DateTime())
    admin = db.Column(db.Boolean)
    todos = db.relationship('Todo', backref='user', lazy='dynamic')
    #roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


#class Role(db.Model, RoleMixin):
class Role(db.Model):
    #__tablename__ = "tbl_roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True)
    description = db.Column(db.String(255))


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Todo(db.Model):
    __tablename__ = 'tbl_todos'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))