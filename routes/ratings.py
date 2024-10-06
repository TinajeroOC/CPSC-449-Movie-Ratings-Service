from flask import Blueprint, jsonify, request
from database.db import db
from models.movie import Movie
from models.rating import Rating
from flask_jwt_extended import jwt_required, decode_token
from datetime import datetime

from uuid import UUID

ratings_blueprint = Blueprint('ratings_blueprint', __name__)

# prevent admins from adding user rating

@ratings_blueprint.route("/ratings", methods=["POST"])
@jwt_required()
def add_rating():

    rating_value = request.form.get("rating")  # The rating value
    created_date = datetime.now()
    # movie_id = request.form.get("movie_id")

    # We dont have movie ids readily accesable so we will use Title and relase date instead
    movie_title = request.form.get("movie_title")
    movie_release_year = request.form.get("movie_release_year")

    # decode token for auth
    token = request.authorization.token
    user = decode_token(token).get('sub')
    user_id = UUID(user['id'])


    # check if user is admin 
    if user.get('is_admin'):
        return jsonify({"message":"Admins may not add movie ratings"}), 403
    
    
    # Check if the movie already exists (i shortened the filters to make devlopment easier)
    movie_exists = Movie.query.filter_by(
        title=movie_title, release_year=movie_release_year).first()
        # title=title, genre=genre, director=director, release_year=release_year).first()

    if movie_exists:
        movie_id = movie_exists.id
        # print("Movie Found!")
    else:
        return jsonify({"message":"Specified movie not found"}), 404

    # Validate required fields
    if not movie_id or not rating_value:
        return jsonify({"message": "movie_id or rating is undefined"}), 400    
    

    # print("check for previous rating")
    # Check if the user has already rated the movie... make sure UUID are type UUID and not str
    existing_rating = Rating.query.filter_by(movie_id=movie_id, user_id=user_id).first()
    if existing_rating:
        return jsonify({"message": "User has already rated this movie"}), 409

    # validate rating range
    try:
        rating_value = int(rating_value)
        if rating_value < 1 or rating_value > 5:
            return jsonify({"message": "Rating must be between 1 and 5"}), 400
    except (ValueError, TypeError):
        return jsonify({"message": "Rating must be an integer"}), 400
    

    # print("Create new Rating record")
    # create rating object and add to database

    new_rating = Rating(
        movie_id=movie_id,
        user_id=user_id,
        rating=rating_value,
        created_date=created_date
    )

    db.session.add(new_rating)
    db.session.commit()


    return jsonify({"message": "Rating has been added"}), 200


# @ratings_blueprint.route("/ratings", methods=["GET"])
# @jwt_required()
# def get_all_ratings():
#     # get all user ratings for all moview, group by movie, created date
    
    