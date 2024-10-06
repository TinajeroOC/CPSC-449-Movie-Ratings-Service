# routes/file_upload.py

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import os

file_upload_blueprint = Blueprint('file_upload', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@file_upload_blueprint.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message': f'File {filename} uploaded successfully'}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400
