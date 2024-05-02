#!/usr/bin/python3
"""
Handles REST API actions for the State model.
"""

from api.v1.views import app_views
from flask import jsonify, Flask, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def handle_states():
    """Handles requests to the /states route."""
    if request.method == 'GET':
        states = storage.all("State").values()
        return jsonify([state.to_dict() for state in states])

    if request.method == 'POST':
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({'error': 'Not a JSON'}), 400

        name = data.get('name')
        if not name:
            return jsonify({'error': 'Missing name'}), 400

        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_state_with_id(state_id):
    """Handles requests to the /states/<state_id> route."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({'error': 'Not a JSON'}), 400

        ignored_keys = ['id', 'created_at', 'updated_at']
        state.update(ignored_keys, **data)
        return jsonify(state.to_dict()), 200
