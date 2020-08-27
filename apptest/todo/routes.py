# APIRest_Flask\apptest\todo\routes.py

import logging

from flask import abort, current_app, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from apptest import db
from apptest.auth.decorators import admin_required, token_required
from apptest.models import Todo

from . import todo_bp

logger = logging.getLogger(__name__)


@todo_bp.route('/list', methods=['GET'])
@token_required
def get_all_todos(current_user):
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


@todo_bp.route('/list/<todo_id>', methods=['GET'])
@token_required
def get_one_todo(current_user, todo_id):
    #todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        return jsonify({'message' : 'No todo found!'})

    todo_data = {}
    todo_data['id'] = todo.id
    todo_data['text'] = todo.text
    todo_data['complete'] = todo.complete

    return jsonify(todo_data)


@todo_bp.route('/todo', methods=['POST'])
@token_required
def create_todo(current_user):

    data = request.get_json()

    new_todo = Todo(text=data['text'], complete=False, user_id=1)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message' : "Todo created!"})


@todo_bp.route('/complete/<todo_id>', methods=['PUT'])
@token_required
def complete_todo(current_user, todo_id):

    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        return jsonify({'message' : 'No todo found!'})

    todo.complete = True
    db.session.commit()

    return jsonify({'message' : 'Todo item has been completed!'})


@todo_bp.route('/delete/<todo_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_todo(current_user, is_admin, todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if not todo:
        return jsonify({'message' : 'No todo found!'})

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message' : 'Todo item deleted!'})
