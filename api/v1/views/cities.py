#!/usr/bin/python3
"""
Handles REST API actions for City related to State.
"""

from api.v1.views import app_views
from flask import jsonify, Flask, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities',
    methods=['GET', 'POST'], strict_slashes=False)
def handle_state_cities(state_id):
    """Handles requests to the /states/<state_id>/cities route."""
    my_state = storage.get("State", state_id)
    if my_state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in my_state.cities])

    if request.method == 'POST':
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({'error': 'Not a JSON'}), 400

        name = data.get('name')
        if not name:
            return jsonify({'error': 'Missing name'}), 400

        new_city = City(state_id=state_id, **data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False)
def handle_city_with_id(city_id):
    """Handles requests to the /cities/<city_id> route."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({'error': 'Not a JSON'}), 400

        ignored_keys = ['id', 'created_at', 'updated_at', 'state_id']
        city.update(ignored_keys, **data)
        return jsonify(city.to_dict()), 200
