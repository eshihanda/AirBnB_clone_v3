#!/usr/bin/python3
"""
handles the amenities route
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', strict_slashes=False)
def all_amenities():
    """
    fetches all amenities
    """
    amenities = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenitys_id(amenity_id):
    """
    fetches all Amenitys per their id
    """
    amenity = storage.all(Amenity)
    for key, value in amenity.items():
        my_amenity_id = key.split('.')[1]
        if my_amenity_id == amenity_id:
            return jsonify(value.to_dict())
    else:
        return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amAmenity(amenity_id):
    """
    deletes amenity
    """
    amenity = storage.all(Amenity)
    for amenity in amenity.values():
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
        else:
            return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """
    uploads aAmenity
    """
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(404, 'Not a JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        abort(404, 'Missing name')
    amenity = Amenity(**kwargs)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    updates the details inAmenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
            amenity.save()
    return jsonify(amenity.to_dict()), 200
