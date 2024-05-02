#!/usr/bin/python3
"""main app file
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

# Create a Flask application instance
app = Flask(__name__)

# Register the blueprint app_views to the Flask instance app
app.register_blueprint(app_views)
# CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})


def not_found_errror_handler(e):
    """a handler for 404 errors that returns a JSON-formatted
    404 status code response
    """
    err_key = 'error'
    err_val = "Not found"
    err_code = 404
    return jsonify({err_key: err_val}), err_code


# Declare a method to handle app teardown
@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Called on teardown of app contexts of Flask.
    Closes the database connection.
    """
    storage.close()


# Run the Flask server if the script is executed directly
if __name__ == "__main__":
    # Retrieve host and port from environment variables
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    # Run the Flask application with specified host, port, and threading option
    app.run(host=host, port=port, threaded=True)
