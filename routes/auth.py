import datetime
from flask import Blueprint, jsonify, request
from database.db import db
from models.user import User
from flask_jwt_extended import create_access_token
import re


email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    is_admin = True if request.form.get("is_admin") == 'true' else False

    if not email or not password:
        return jsonify({"message": "Email or password is undefined"}), 400

    if not re.match(email_regex, email):
        return jsonify({"message": "Email is invalid"}), 400

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"message": "User already exists"}), 409

    user = User(email=email, password=password, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User has been registered"}), 200


@auth_blueprint.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "Email or password is undefined"}), 400

    if not re.match(email_regex, email):
        return jsonify({"message": "Email is invalid"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Email or password is incorrect"}), 401

    access_token = create_access_token(
        identity={"id": user.id, "email": user.email, "is_admin": user.is_admin}, expires_delta=datetime.timedelta(days=7))

    return jsonify({"message": "Authenticated successfully", "access_token": access_token}), 200
