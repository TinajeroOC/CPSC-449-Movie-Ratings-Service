from flask import Blueprint, jsonify, request
from database.db import db
from models.movie import Movie
from flask_jwt_extended import jwt_required, decode_token


movies_blueprint = Blueprint('movie_blueprint', __name__)


@movies_blueprint.route("/movies", methods=["POST"])
@jwt_required()
def add_movie():
    title = request.form.get("title")
    genre = request.form.get("genre")
    director = request.form.get("director")
    release_year = request.form.get("release_year")

    token = request.authorization.token
    user = decode_token(token).get('sub')

    if not user.get('is_admin'):
        return jsonify({"message": "Must be an admin to add a movie"}), 403

    if not title or not genre or not director or not release_year:
        return jsonify({"message": "title, genre, director, or release_year is undefined"}), 400

    try:
        release_year = int(release_year)
    except (ValueError, TypeError):
        return jsonify({"message": "release_year is not an integer"}), 400

    movie_exists = Movie.query.filter_by(
        title=title, genre=genre, director=director, release_year=release_year).first()
    if movie_exists:
        return jsonify({"message": "Movie already exists"}), 409

    movie = Movie(title=title, genre=genre, director=director,
                  release_year=release_year)
    db.session.add(movie)
    db.session.commit()

    return jsonify({"message": "Movie has been added"}), 200



# ● An endpoint to fetch details for a specific movie, including its user ratings.

@movies_blueprint.route("/movies", methods=["GET"])
@jwt_required()
def get_movies():
    title = request.form.get("title")
    release_year = request.form.get("release_year")

    if not title or not release_year:
        return jsonify({"message": "A title and release year are required for results"}), 400
    
    # query database and get all related ratings
    movie = Movie.query.filter_by(title=title, release_year=release_year).first()

    # return related ratings to themovie title
    ratings = []
    if movie:
        for r in movie.ratings:
            ratings.append({
                "user_id": r.user_id,
                "rating": r.rating
            })
    
    return jsonify({"title": movie.title, "release_year": movie.release_year, "ratings": ratings}), 200