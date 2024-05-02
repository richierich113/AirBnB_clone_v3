#!/usr/bin/python3
"""index file, main view file
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def get_status():
    """returns the status of the RESTful service"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def num_of_objs():
    """endpoint that retrieves the number of each
    objects by type
    """

    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
        }
    for c_key, c_value in classes.items():
        classes[c_key] = storage.count(c_value)
    return jsonify(classes)
