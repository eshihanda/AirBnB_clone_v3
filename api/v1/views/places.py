#!/usr/bin/python3
"""
handles the route for all places
in a city
"""

from api.v1.views import app_views
from flask import abort, request
from flask.json import jsonify
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """
    defines all places in a city
    """
    cities = storage.all(City)
    all_places = []
    if cities and city_id:
        for city in cities.values():
            if city.id == city_id:
                for place in city.places:
                    all_places.append(place.to_dict())
                return jsonify(all_places)

    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def places_id(place_id):
    """
    finds places a per their id
    """
    places = storage.get(Place, place_id)
    for place in places.values():
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """
    deletes a place
    """
    place = storage.get(Place, place_id)
    if place is not None:
        place.delete()
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def new_place(city_id):
    """
    adds a new place in a city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    place = Place(**data)
    place.city_id = city_id
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def place_update(place_id):
    """
    updates the places
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
            place.save()
    return jsonify(place.to_dict()), 200
