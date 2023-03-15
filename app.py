import os
from werkzeug.utils import secure_filename
from deep_learnig import single_prediction, multiprediction
from flask import Flask, request
from backgound_check import single_bg_detected



app = Flask(__name__)

UPLOAD_FOLDER = './uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


@app.route('/singleprediction', methods=['POST'])
def single_processing():
    if 'file' not in request.files:
        return {'error': 'No file in request'}, 400
    file = request.files['file']

    if file.filename == '':
        return {'error': 'No file selected'}, 400

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        detected_respone = single_bg_detected('./uploads/' + filename)

        if detected_respone != False:
            prediction_response = single_prediction('./uploads/' + filename)
            os.remove('./uploads/' + filename)

            return prediction_response, 200

        os.remove('./uploads/' + filename)

        return {'message': 'process is rejected'}, 204
    else:
        return {}, 404


@app.route('/multipredictions', methods=['POST'])
def multiple_processing():
    if 'file' not in request.files:
        return {'error': 'No file in request'}, 400
    file = request.files['file']

    if file.filename == '':
        return {'error': 'No file selected'}, 400

    uploaded_files = request.files.getlist('file')

    filenames = []

    for file in uploaded_files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        filenames.append(file_path)

    response = multiprediction(filenames)

    # Remove uploaded files after processing
    for filename in filenames:
        print(f"Deleting file: {filename}")
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print(f"File not found: {filename}")

    return response
