# APIRest_Flask\apptest\user\service.py

import uuid
from flask import abort, jsonify, request
from werkzeug.security import generate_password_hash

from apptest.models import Todo, User

class User_service:

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
            user_data['admin'] = user.admin
            output.append(user_data)
        
        return jsonify({'users' : output})


    def find_all_users_paginated(self):

        if 'page' not in request.args or 'per_page' not in request.args:
            abort(400)

        try:
            page = int(request.args.get('page'))
            per_page = int(request.args.get('per_page'))
        except ValueError:
            abort(400)

        users = User.query.order_by(User.name.asc()).paginate(page=page, per_page=per_page, error_out=False)
    
        output = []
        for user in users.items:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['name'] = user.name
            user_data['password'] = user.password
            user_data['admin'] = user.admin
            output.append(user_data)
        
        return jsonify({'users' : output})


    def find_user_by_Id(self, public_id):

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return abort(404)

        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin

        return jsonify({'user' : user_data})


    def find_user_todos(self, user_id):
        
        todos = Todo.query.filter_by(user_id = user_id)

        if not todos:
            abort(404)

        output = []
        for todo in todos:
            todo_data = {}
            todo_data['id'] = todo.id
            todo_data['text'] = todo.text
            todo_data['complete'] = todo.complete
            output.append(todo_data)

        return jsonify({'todos' : output})


    def find_user_todo(self, user_id, todo_id):
        
        todo = Todo.query.filter_by(user_id = user_id, id = todo_id).first()
        
        if not todo:
            abort(404)

        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete

        return jsonify({'todo' : todo_data})

    def save_user(self):

        data = request.get_json()

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message' : 'New user created!'})


    def save_user_todo(self, user_id):
        
        data = request.get_json()

        new_todo = Todo(text = data['text'], complete = data['complete'], user_id = user_id)

        db.session.add(new_todo)
        db.session.commit()

        return jsonify({'message' : 'New todo created!'})


    def save_promote_user(self, public_id):

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            abort(404)

        if user.admin:
            # TODO: Devolver un mensaje estándar http como toca. Analizar que código hay que devolver
            return jsonify({'message' : 'El usuario ya es administrador'})

        user.admin = True
        db.session.commit()

        return jsonify({'message' : 'The user has been promoted!'})


    def delete (self, public_id):
        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            abort(404)

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message' : 'The user has been deleted!'})
