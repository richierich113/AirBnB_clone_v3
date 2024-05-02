#!/usr/bin/python3
"""
Handles REST API actions for Place Amenity.
"""

from api.v1.views import app_views
from os import getenv
from flask import jsonify, Flask, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Handles requests to the /places/<place_id>/amenities route."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        return jsonify(place.amenity_ids)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>', methods=['POST'], strict_slashes=False)
def add_place_amenity(place_id, amenity_id):
    """Handles requests to the /places/<place_id>/amenities/<amenity_id> route."""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        if amenity_id not in place.amenity_ids:
            place.amenity_ids.append(amenity_id)
    else:
        place.amenities.append(amenity)

    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>', methods=['DELETE'], strict_slashes=False)
def remove_place_amenity(place_id, amenity_id):
    """Handles requests to the /places/<place_id>/amenities/<amenity_id> route."""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        if amenity_id in place.amenity_ids:
            place.amenity_ids.pop(amenity_id)
    elif amenity in place.amenities:
        place.amenities.remove(amenity)

    storage.save()
    return jsonify({}), 200
