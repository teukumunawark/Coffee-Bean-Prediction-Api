import os
from werkzeug.utils import secure_filename
from deep_learning.single_classification import singleclassification, highestscore
from deep_learning.multi_classification import multiclassification
from flask import Flask, request
from utils.backgound_check import single_bg_detected


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


@app.route('/singleclassification', methods=['POST'])
def single_processing():
    file = request.files['image']
    file = check_file(file)

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    detected_respone = single_bg_detected(file_path)

    if detected_respone != False:
        prediction_response = singleclassification(file_path)
        os.remove(file_path)
        return prediction_response, 200

    os.remove(file_path)

    return {'message': 'process is rejected'}, 204


@app.route('/highestscore', methods=['POST'])
def highest_score():
    file = request.files['image']
    file = check_file(file)

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    prediction_response = highestscore(file_path)
    os.remove(file_path)
    return prediction_response, 200


@app.route('/multiclassifications', methods=['POST'])
def multiple_processing():
    uploaded_files = request.files.getlist('image')

    if not uploaded_files:
        return {'error': 'No files uploaded'}, 400

    filenames = []
    for file in uploaded_files:
        file = check_file(file)
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        filenames.append(file_path)

    response = multiclassification(filenames)

    for filename in filenames:
        try:
            os.remove(filename)
        except FileNotFoundError:
            print(f"File not found: {filename}")

    return response
