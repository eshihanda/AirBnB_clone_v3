#!/usr/bin/python3
"""
create route and status for the blueprint
"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import base_model, storage


@app_views.route('/states', strict_slashes=False)
def all_states():
    """
    list of all states
    """
    my_states = storage.all(State).values()
    state_list = [state.to_dict() for state in my_states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def states_id(state_id):
    """
    fetches all states per their id
    """
    state = storage.all(State)
    for key, value in state.items():
        my_state_id = key.split('.')[1]
        if my_state_id == state_id:
            return jsonify(value.to_dict())
    else:
        return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    deletes a state
    """
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
        else:
            return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """
    uploads a state
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        abort(400, 'Missing name')
    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """
    updates the details in state
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            if not request.get_json():
                return abort(400, 'Not a JSON')
            result_json = request.get_json()

            jump_keys = ['id', 'created_at', 'updated_at']
            for key, value in result_json.items():
                if key not in jump_keys:
                    setattr(state, key, value)
                    state.save()
                return jsonify(state.to_dict()), 200
        else:
            return abort(404)
