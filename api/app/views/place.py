from flask import Flask
from flask import request
from app import app
from app.models.base import db
from app.models.place import Place
from app.models.city import City
from app.models.state import State
from flask import jsonify
from flask import make_response
from app.models.place_book import PlaceBook
from datetime import datetime
from datetime import timedelta
from return_styles import ListStyle


@app.route('/places', methods=['GET', 'POST'])
def list_of_place():
    # returning a list of all places
    if request.method == 'GET':
        list = ListStyle.list(Place.select(), request)
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
        try:
            get_place = Place.get(Place.id == id).to_dict()
            return jsonify(get_place)
        except:
            return make_response(jsonify({'code': '10001',
                                          'msg': 'Place not found'}), 404)
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
            return make_response(jsonify({'code': '10001',
                                          'msg': 'Place not found'}), 404)


# Function returns a list of places within specific city or adds new place
@app.route('/states/<int:state_id>/cities/<int:city_id>/places',
           methods=['GET', 'POST'])
def places_within_city(state_id, city_id):
    response = jsonify({'code': 404, 'msg': 'not found'})
    response.status_code = 404

    # Getting the information for the place
    if request.method == 'GET':
        try:
            list = ListStyle.list(Place.select()
                                  .join(City)
                                  .where(City.id == city_id)
                                  .where(Place.city == city_id,
                                         City.state == state_id), request)
            return jsonify(list)
        except:
            return response
    # Creating a new place
    elif request.method == 'POST':
        try:
            # Getting the city to check if it exist
            City.get(City.id == city_id, City.state == state_id)
            # adding city by Using Post
            add_place = Place.create(owner=request.form['owner'],
                                     city=city_id,
                                     name=request.form['name'],
                                     description=request.form['description'],
                                     number_rooms=request.form['number_rooms'],
                                     number_bathrooms=request.form['number_bathrooms'],
                                     max_guest=request.form['max_guest'],
                                     price_by_night=request.form['price_by_night'],
                                     latitude=request.form['latitude'],
                                     longitude=request.form['longitude'])
            add_place.save()
            return jsonify(add_place.to_dict())
            print("You've just added a place!")
        except:
            return response


@app.route('/states/<int:state_id>/places', methods=['GET'])
def get_list_places(state_id):
    try:
        # Checking if a state exist
        State.get(State.id == state_id)
    except State.DoesNotExist:
            return make_response(jsonify({'code': '10001',
                                          'msg': 'Place not found'}), 404)
    if request.method == 'GET':
        try:
            # getting a place that is in a specific state
            list = ListStyle.list(Place.select()
                                  .join(City)
                                  .where(Place.city == City.id)
                                  .join(State)
                                  .where(State.id == City.state), request)
            return jsonify(list)
        except:
            return make_response(jsonify({'code': '10001',
                                          'msg': 'Place not found'}), 404)


@app.route('/places/<int:place_id>/available', methods=['POST'])
def make_reservation(place_id):
    try:
        Place.get(Place.id == place_id)
    except Place.DoesNotExist:
            return make_response(jsonify({'code': '10001',
                                          'msg': 'Place not found'}), 404)
    if request.method == "POST":
        year = int(request.form["year"])
        month = int(request.form["month"])
        day = int(request.form["day"])

        try:
            # getting the place
            get_booking = PlaceBook.get(PlaceBook.place == place_id)

            # Creating a datetime with the post parameters
            date_object = datetime(year, month, day).strftime("%d/%m/%Y")

            # getting the date from start and formatting its
            date = get_booking.to_dict()['date_start'].strftime("%d/%m/%Y")

            # Getting the duration of the booking
            duration = get_booking.to_dict()['number_nights']

            # Getting the exact day of checkout
            total_days = (get_booking.to_dict()['date_start'] +
                          timedelta(duration)).strftime("%d/%m/%Y")

            if date_object >= date and date_object <= total_days:
                return jsonify({'Available': False})
            else:
                return jsonify({'Available': True})
        except:
            return make_response(jsonify({'code': '10001',
                                          'msg': 'Wrong date format'}), 400)
