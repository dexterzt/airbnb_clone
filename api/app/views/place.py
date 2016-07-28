from flask import Flask
from flask import request
from app import app
from app.models.base import db
from app.models.place import Place
from app.models.city import City
from flask import jsonify
from flask import make_response


@app.route('/places', methods=['GET', 'POST'])
def list_of_place():
    # returning a list of all places
    if request.method == 'GET':
        list = []
        for place in Place.select():
            list.append(place.to_hash())
        return jsonify(list)

    if request.method == 'POST':
        new_place = Place(owner=request.form['owner'],
                          city=request.form['city'],
                          name=request.form['name'],
                          description=request.form['description'],
                          number_rooms=request.form['number_rooms'],
                          number_bathrooms=request.form['number_bathrooms'],
                          max_guest=request.form['max_guest'],
                          price_by_night=request.form['price_by_night'],
                          latitude=request.form['latitude'],
                          longitude=request.form['longitude']
                          )
        new_place.save()
        return "place created"


@app.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def modify_place(place_id):
    id = place_id
    if request.method == 'GET':
        return Place.get(Place.id == id).to_hash()

    if request.method == 'PUT':
        id = place_id
        try:
            # updating name
            query = Place.update(name=request.form['name']).where(Place.id == id)
        except:
            pass

        try:
            return jsonify(Place.get(Place.id == id).to_hash())
        except:
            return make_response(jsonify({'code': '10001',
                                          'msg': 'no place found'}), 404)
    elif request.method == 'PUT':
        place = Place.select().where(Place.id == place_id).get()
        params = request.values
        for key in params:
            if key == 'owner' or key == 'city':
                return jsonify(msg="You may not update the %s." % key), 409
            if key == 'updated_at' or key == 'created_at':
                continue
            else:
                setattr(place, key, params.get(key))
        place.save()
        return jsonify(msg="Place information updated successfully."), 200

    elif request.method == 'DELETE':
        try:
            get_place = Place.get(Place.id == id)
            get_place.delete_instance()
            return "Place with id = %d was deleted\n" % (int(id))
        except:
            return make_response(jsonify({'code': '10001', 'msg': 'no place found with that id'}), 409)

@app.route('/states/<int:state_id>/cities/<int:city_id>/places', methods=['GET', 'POST'])
# Function returns a list of places within specific city or adds new place
def places_within_city(state_id, city_id):
    if request.method == 'GET':
        try:
            locations = Place.get(Place.city == city_id, City.state == state_id)
            list = []
            for i in locations:
                list.append(i.to_hash())
            return jsonify(list)
        except:
            print("Unknown location. Try again...")

    elif request.method == 'POST':
        try:
            City.get(City.id == city_id, City.state == state_id)
            add_place = Place.create(owner=request.form['owner'],
                                    city=request.form['city'],
                                    name=request.form['name'],
                                    description=request.form['description'],
                                    number_rooms=request.form['number_rooms'],
                                    number_bathrooms=request.form['number_bathrooms'],
                                    max_guest=request.form['max_guest'],
                                    price_by_night=request.form['price_by_night'],
                                    latitude=request.form['latitude'],
                                    longitude=request.form['longitude'])
            add_place.save()
            return jsonify(add_place.to_hash())
            print("You've just added a place!")
        except:
            print("Something went wrong. Try again...")
