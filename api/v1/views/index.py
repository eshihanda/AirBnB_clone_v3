#!/usr/bin/python3
"""
create route and status for the blueprint
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/status')
def status_api():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def some_stats():
    return jsonify({
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
        })
