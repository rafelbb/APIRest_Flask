# APIRest_securizada_bdd_blueprints\apptest\todo\routes.py

import datetime
import uuid
from functools import wraps

import jwt
from flask import abort, current_app, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from apptest import db
from apptest.models import Todo, User
from apptest.auth.decorators import token_required
from . import todo_bp



@todo_bp.route('/todo', methods=['GET'])
#@token_required
#def get_all_todos(current_user):
def get_all_todos():
    todos = Todo.query.all()

    output = []

    for todo in todos:
        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete
        todo_data['user_id'] = todo.user_id
        output.append(todo_data)

    return jsonify({'todos' : output})

"""
@todo_bp.route('/todo', methods=['GET'])
#@token_required
#def get_all_todos(current_user):
def get_all_todos(current_user):
    todos = Todo.query.filter_by(user_id=current_user.id).all()

    output = []

    for todo in todos:
        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete
        output.append(todo_data)

    return jsonify({'todos' : output})
"""
"""
@todo_bp.route('/todo/<todo_id>', methods=['GET'])
@token_required
def get_one_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({'message' : 'No todo found!'})

    todo_data = {}
    todo_data['id'] = todo.id
    todo_data['text'] = todo.text
    todo_data['complete'] = todo.complete

    return jsonify(todo_data)

"""

@todo_bp.route('/todo', methods=['POST'])
#@token_required
#def create_todo(current_user):
def create_todo():
    data = request.get_json()

    new_todo = Todo(text=data['text'], complete=False, user_id=1)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message' : "Todo created!"})

"""
@todo_bp.route('/todo/<todo_id>', methods=['PUT'])
@token_required
def complete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({'message' : 'No todo found!'})

    todo.complete = True
    db.session.commit()

    return jsonify({'message' : 'Todo item has been completed!'})
"""


@todo_bp.route('/todo/<todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({'message' : 'No todo found!'})

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message' : 'Todo item deleted!'})
