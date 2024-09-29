import os
from flask import Flask
from database.db import db
from tokens.jwt import jwt
from routes.auth import auth_blueprint


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.abspath(os.getcwd()) + "/instance/database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_blueprint)

    return app


app = create_app()
