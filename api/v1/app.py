#!/usr/bin/python3
"""
create a flask api and mark its blueprint to an instance
"""

from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

CORS(app, origins="0.0.0.0")


@app.teardown_appcontext
def teardown_db(self):
    """
    closes current db session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    handles the default 404 request
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host_vr = getenv('HBNB_API_HOST')
    port_vr = int(getenv('HBNB_API_PORT'))
    app.run(host=host_vr, port=port_vr, threaded=True)
