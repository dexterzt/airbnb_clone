from app.models.review import Review
from app.models.review_place import ReviewPlace
from app import app
from flask import jsonify, request
from flask import make_response


@app.route('/users/<user_id>/reviews', methods=['GET', 'POST'])
def get_reviews_user(user_id):
    id == user_id
    # Getting all the review by user id
    if request.method == "GET":
        try:
            list = []
            for review in Review.select().where(Review.user == id):
                list.append(review.to_hash)
            return jsonify(list)
        except:
                return make_response(jsonify({'code': 10000,
                                              'msg': 'Review not found'}), 404)

    elif request.method == "POST":
        user_message = request.form["message"]
        user_stars = request.form["stars"]
        user_id = id  # Not sure about this one

        try:
            Review(message=user_message,
                   stars=user_stars,
                   user=user_id)
        except:
            return make_response(jsonify({'code': 10000,
                                          'msg': 'Review not found'}), 404)


@app.route('users/<user_id>/reviews/<review_id>', methods=['GET', 'DELETE'])
def delete_reviews_user(user_id, review_id):
    if request.method == 'GET':
        try:
            list = []
            for review in Review.select().where(Review.id == review_id):
                list.append(review.to_hash())
            return jsonify(list)
        except:
            return make_response(jsonify({'code': 10000,
                                          'msg': 'Review not found'}), 404)
    elif request.method == 'DELETE':
        try:
            get_review = Review.get(Review.id == review_id)
            get_review.delete_instance()
            return "Review was deleted"
        except:
            return make_response(jsonify({'code': 10000,
                                          'msg': 'Review not found'}), 404)


@app.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def get_review_place(place_id):
    if request.method == 'GET':
        try:
            list = []
            for review in ReviewPlace.select().where(ReviewPlace.place == place_id):
                list.append(review.to_hash())
            return jsonify(list)
        except:
            return make_response(jsonify({'code': 10000,
                                          'msg': 'Review not found'}), 404)
    elif request.method == 'POST':
        user_message = request.form["message"]
        user_stars = request.form["stars"]
        user_id = request.form["id"]  # Not sure about this one
        try:
            Review(message=user_message,
                   stars=user_stars,
                   user=user_id)
        except:
            return make_response(jsonify({'code': 10000,
                                          'msg': 'Review not found'}), 404)


@app.route('/places/<place_id>/reviews/<review_id>', methods=['GET', 'DELETE'])
def delete_reviews_place(place_id, review_id):
    if request.method == 'GET':
        try:
            list = []
            for review in Review.select().where(Review.id == review_id):
                list.append(review.to_hash())
            return jsonify(list)
        except:
            return make_response(jsonify({'code': 10000,
                                          'msg': 'Review not found'}), 404)
    elif request.method == 'DELETE':
        try:
            get_review = Review.get(Review.id == review_id)
            get_review.delete_instance()
            return "Review was deleted"
        except:
            return make_response(jsonify({'code': 10000,
                                          'msg': 'Review not found'}), 404)
