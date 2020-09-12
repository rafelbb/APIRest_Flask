# APIRest_Flask\apptest\user\service.py

from flask import abort, jsonify, request, make_response
from marshmallow import Schema, ValidationError, fields
from apptest.extensions import db
from apptest.models import Todo, User, Role

#TODO: Pasar los schema de validación de datos a una fichero dentro del mismo package
class UserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.String(required=True)
    password = fields.String(required=True)


class User_service:

    def find_user_roles(self, user_id):

        roles = Role.query.filter(Role.users.any(id=user_id)).all()

        if not roles:
            abort(404)

        output = []
        for role in roles:
            roles_data = {}
            roles_data['id'] = role.id
            roles_data['name'] = role.name
            roles_data['description'] = role.description
            output.append(roles_data)

        return jsonify({'roles': output})

    def find_role_users(self, role_id):

        users = User.query.filter(User.roles.any(id=role_id)).all()

        if not users:
            abort(404)

        output = []
        for user in users:
            user_data = {}
            user_data['name'] = user.name
            user_data['public_id'] = user.public_id
            user_data['email'] = user.email
            user_data['active'] = user.active
            output.append(user_data)

        return jsonify({'users': output})

    def find_all_users(self):

        users = User.query.all()

        if not users:
            abort(404)

        output = []
        for user in users:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['name'] = user.name
            user_data['password'] = user.password
            user_data['email'] = user.email
            user_data['admin'] = user.admin
            output.append(user_data)

        return jsonify({'users': output})

    def find_all_users_paginated(self):

        if 'page' not in request.args or 'per_page' not in request.args:
            abort(400)

        try:
            page = int(request.args.get('page'))
            per_page = int(request.args.get('per_page'))
        except ValueError:
            abort(400)

        users = User.query.order_by(User.name.asc()).paginate(
            page=page, per_page=per_page, error_out=False)

        output = []
        for user in users.items:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['name'] = user.name
            user_data['password'] = user.password
            user_data['admin'] = user.admin
            output.append(user_data)

        return jsonify({'users': output})

    def find_user_by_Id(self, public_id):

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return abort(404)

        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin

        return jsonify({'user': user_data})

    def find_user_todos(self, user_id):

        todos = Todo.query.filter_by(user_id=user_id)

        if not todos:
            abort(404)

        output = []
        for todo in todos:
            todo_data = {}
            todo_data['id'] = todo.id
            todo_data['text'] = todo.text
            todo_data['complete'] = todo.complete
            output.append(todo_data)

        return jsonify({'todos': output})

    def find_user_todo(self, user_id, todo_id):

        todo = Todo.query.filter_by(user_id=user_id, id=todo_id).first()

        if not todo:
            abort(404)

        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete

        return jsonify({'todo': todo_data})

    def save_user(self):

        request_data = request.get_json()

        try:
            UserSchema().load(request_data)
        # except ValidationError as err:
        except ValidationError:
            abort(400)

        new_user = User(
            email=request_data['email'], name=request_data['name'], password=request_data['password'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'New user created!'})

    def save_user_todo(self, user_id):

        data = request.get_json()

        new_todo = Todo(text=data['text'],
                        complete=data['complete'], user_id=user_id)

        db.session.add(new_todo)
        db.session.commit()

        return jsonify({'message': 'New todo created!'})

    def save_promote_user(self, public_id):

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            abort(404)

        if user.admin:
            # TODO: Devolver un mensaje estándar http como toca. Analizar que código hay que devolver
            return jsonify({'message': 'El usuario ya es administrador'})

        user.admin = True
        db.session.commit()

        return jsonify({'message': 'The user has been promoted!'})

    def delete(self, public_id):
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            abort(404)

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'The user has been deleted!'})
