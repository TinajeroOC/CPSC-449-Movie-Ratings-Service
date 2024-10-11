from flask import Blueprint, jsonify, request
from database.db import db
from models.movie import Movie
from models.rating import Rating
from flask_jwt_extended import jwt_required, decode_token
from datetime import datetime

from uuid import UUID

update_blueprint = Blueprint('update_blueprint', __name__)

@update_blueprint.route("/update", methods=['POST'])
@jwt_required()
def update_rating():

    # Get user ID from token
    token = request.authorization.token
    user = decode_token(token).get('sub')
    user_id = UUID(user['id'])

    # Get form data
    rating_value = request.form.get("rating")
    movie_title = request.form.get("movie_title")
    movie_release_year = request.form.get("movie_release_year")

    try:
        movie_release_year = int(movie_release_year)
    except (ValueError, TypeError):
        return jsonify({"message": "movie_release_year is not an integer"}), 400
    
    # Validate required fields
    missing_fields = []
    if not rating:
        missing_fields.append("rating")
    if not movie_title:
        missing_fields.append("movie_title")
    if not movie_release_year:
        missing_fields.append("movie_release_year")

    # Display missing form fields, if any
    if missing_fields:
        return jsonify({"message": f"{missing_fields[0]} is missing" if len(missing_fields) == 1 else f"{', '.join(missing_fields)} are missing"}), 400

    # Check if the movie exists
    movie = Movie.query.filter_by(title=movie_title,release_year=movie_release_year).first()
    if not movie:
        return jsonify({"message": "Specified movie not found"}), 404

    # Check if the user has already rated the movie
    existing_rating = Rating.query.filter_by(movie_id=movie.id, user_id=user_id).first()
    
    # Check if rating exists
    if not existing_rating:
        return jsonify({"message": "Error, you have not rated this movie"}), 404

    # Check if new rating is a different value
    if existing_rating.rating == rating_value:
        return jsonify({"message": "Rating was not updated, must be a new value"}), 409
        
    # Update existing rating if different value
    existing_rating.rating = rating_value
    existing_rating.created_date = datetime.now()
    db.session.commit()
    return jsonify({"message": "Rating has been updated"}), 200
