import os
from werkzeug.utils import secure_filename
from deep_learning.multi_classification import classify_multiple_images
from flask import Flask, request

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


def check_file(file):
    if file is None:
        return {'error': 'No file in request'}, 400

    if file.filename == '':
        return {'error': 'No file selected'}, 400

    if not allowed_file(file.filename):
        return {'error': 'File type not allowed'}, 400

    return file



@app.route('/multiclassifications', methods=['POST'])
def multiple_processing():
 
    uploaded_files = request.files.getlist('image')

    if not uploaded_files:
        return {'error': 'No files uploaded'}, 400

    image_paths = []
    for image_file in uploaded_files:
        image_file = check_file(image_file)
        image_name = secure_filename(image_file.filename)
        image_path = f"{app.config['UPLOAD_FOLDER']}/{image_name}"
        with open(image_path, 'wb') as f:
            f.write(image_file.read())
        image_paths.append(image_path)

    response = classify_multiple_images(image_paths)

    for image_path in image_paths:
        try:
            os.remove(image_path)
        except FileNotFoundError:
            print(f"File not found: {image_path}")

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'))