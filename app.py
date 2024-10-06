import os
from flask import Flask
from database.db import db
from tokens.jwt import jwt
from routes.auth import auth_blueprint
from routes.movies import movies_blueprint
from routes.ratings import ratings_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.abspath(os.getcwd()) + "/instance/database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'pdf'}

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])


    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(movies_blueprint)
<<<<<<< HEAD
    
    from routes.file_upload import file_upload_blueprint
    app.register_blueprint(file_upload_blueprint)

=======
    app.register_blueprint(ratings_blueprint)
>>>>>>> 416056dbd6b9cd7abc91c35bfb34aa1e8e7e936a

    return app


app = create_app()
