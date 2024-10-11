from flask import Blueprint, jsonify, request
from database.db import db
from models.movie import Movie
from models.rating import Rating
from flask_jwt_extended import jwt_required, decode_token
from uuid import UUID


delete_blueprint = Blueprint('delete_blueprint', __name__)

@delete_blueprint.route("/delete", methods=['POST'])
@jwt_required()
def user_delete_rating():

    # Get user ID from token
    token = request.authorization.token
    user = decode_token(token).get('sub')
    user_id = UUID(user['id'])

    # Get form data
    movie_title = request.form.get("movie_title")
    movie_release_year = request.form.get("movie_release_year")
    
    # Validate required fields
    missing_fields = []
    if not movie_title:
        missing_fields.append("movie_title")
    if not movie_release_year:
        missing_fields.append("movie_release_year")

    # Display missing form fields, if any
    if missing_fields:
        return jsonify({"message": f"{missing_fields[0]} is missing" if len(missing_fields) == 1 else f"{', '.join(missing_fields)} are missing"}), 400

    # Check if the movie and rating exists
    movie = Movie.query.filter_by(title=movie_title, release_year=movie_release_year).first()
    if not movie:
        return jsonify({"message": "Specified movie not found"}), 404

    # Check if the user has already rated the movie
    existing_rating = Rating.query.filter_by(movie_id=movie.id, user_id=user_id).first()
    if not existing_rating:
        return jsonify({"message": "Error, you have not rated this movie"}), 404

    # Delete the existing rating
    db.session.delete(existing_rating)
    db.session.commit()
    return jsonify({"message": "Rating has been deleted"}), 200
  

@delete_blueprint.route("/admin/delete", methods=['POST'])
@jwt_required()
def admin_delete_rating():

    # Get user ID from token
    token = request.authorization.token
    user = decode_token(token).get('sub')

    # Check if admin sent the request
    if not user.get("is_admin"):
        return jsonify({"message":"Only admins may delete other user ratings."}), 403

    # Get form data
    movie_title = request.form.get("movie_title")
    movie_release_year = request.form.get("movie_release_year")
    user_id = UUID(request.form.get("user_id"))

    # Validate required fields
    missing_fields = []
    if not movie_title:
        missing_fields.append("movie_title")
    if not movie_release_year:
        missing_fields.append("movie_release_year")
    if not user_id:
        missing_fields.append("user_id")

    # Display missing form fields, if any
    if missing_fields:
        return jsonify({"message": f"{missing_fields[0]} is missing" if len(missing_fields) == 1 else f"{', '.join(missing_fields)} are missing"}), 400

    # Check if the movie exists 
    movie = Movie.query.filter_by(title=movie_title, release_year=movie_release_year).first()
    if not movie:
        return jsonify({"message": "Specified movie not found"}), 404

    # Check if the user has rated the movie
    existing_rating = Rating.query.filter_by(movie_id=movie.id, user_id=user_id).first()
    if not existing_rating:
        return jsonify({"message": "Rating not found for this user"}), 404

    # Delete the rating
    db.session.delete(existing_rating)
    db.session.commit()
    return jsonify({"message": "User rating has been deleted"}), 200
