#!/usr/bin/python3
"""
handles the user route and its resources
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import base_model, storage


@app_views.route('/users', strict_slashes=False)
def all_users():
    """
    list of all states
    """
    my_user = storage.all(User).values()
    user_list = [user.to_dict() for user in my_user]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', strict_slashes=False)
def users_id(user_id):
    """
    fetches all users per their id
    """
    user = storage.all(User)
    for key, value in user.items():
        my_user_id = key.split('.')[1]
        if my_user_id == user_id:
            return jsonify(value.to_dict())
    else:
        return abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    deletes users
    """
    user = storage.get(User, user_id)
    if user is not None:
        user.delete()
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """
    uploads a user
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()

    if 'email' not in kwargs:
        abort(400, 'Missing email')
    if 'password' not in kwargs:
        abort(400, 'Missing password')
    user = User(**kwargs)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a City object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
            user.save()
    return jsonify(user.to_dict()), 200
