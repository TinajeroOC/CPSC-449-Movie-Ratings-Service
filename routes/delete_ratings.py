from flask import Blueprint, jsonify, request
from database.db import db
from models.movie import Movie
from models.rating import Rating
from flask_jwt_extended import jwt_required, decode_token

from uuid import UUID
delete_blueprint = Blueprint('delete_blueprint', __name__)

@delete_blueprint.route("/delete", methods=['POST'])
@jwt_required()
def delete_rating():

    # Get user ID from token
    token = request.authorization.token
    user = decode_token(token).get('sub')
    user_id = UUID(user['id'])

    # Get form data
    rating_value = request.form.get("rating")
    movie_title = request.form.get("movie_title")
    movie_release_year = request.form.get("movie_release_year")
    genre = request.form.get("genre")
    director = request.form.get("director")

    # Error Checking
    # Validate required fields
    missing_fields = []
    if not movie_title:
        missing_fields.append("movie_title")
    if not movie_release_year:
        missing_fields.append("movie_release_year")
    if not genre:
        missing_fields.append("genre")
    if not director:
        missing_fields.append("director")

    # Display missing form fields, if any
    if missing_fields:
        if len(missing_fields) == 1:
            return jsonify({"message": f"{missing_fields[0]} is missing"}), 400
        else:
            return jsonify({"message": f"{', '.join(missing_fields)} are missing"}), 400

    # Check if the movie and rating exists
    movie = Movie.query.filter_by(title=movie_title, genre=genre, director=director, release_year=movie_release_year).first()
    if not movie:
        return jsonify({"message": "Specified movie not found"}), 404


    # Check if the user has already rated the movie
    existing_rating = Rating.query.filter_by(movie_id=movie.id, user_id=user_id).first()

    if not existing_rating:
        # check if new rating is different
        return jsonify({"message": "Error, no rating to delete"}), 400
        # Update existing rating if different value

    db.session.delete(existing_rating)
    db.session.commit()
    return jsonify({"message": "Rating has been deleted"}), 200
  
