import os
from werkzeug.utils import secure_filename
from backgound_check import backgound_detected
from deep_learnig import prediction
from flask import Flask, request


app = Flask(__name__)

UPLOAD_FOLDER = './uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'jpg','png', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']


@app.route('/prediction', methods=['POST'])
def create_predict():
    if 'file' not in request.files:
        return {'error': 'No file in request'}, 400
    file = request.files['file']

    if file.filename == '':
        return {'error': 'No file selected'}, 400

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        prediction_response = prediction('./uploads/' + filename)

        os.remove('./uploads/' + filename)

        return prediction_response, 200
    else:
        return {}, 404


@app.route('/test', methods=['POST'])
def test():
    if 'file' not in request.files:
        return {'error': 'No file in request'}, 400
    file = request.files['file']

    if file.filename == '':
        return {'error': 'No file selected'}, 400

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        detected_respone = backgound_detected('./uploads/' + filename)

        if detected_respone != False:
            prediction_response = prediction('./uploads/' + filename)
            os.remove('./uploads/' + filename)

            return prediction_response, 200

        os.remove('./uploads/' + filename)

        return {'message': 'process is rejected'}, 204
    else:
        return {}, 404

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return {'error': 'No file in request'}, 400
#     file = request.files['file']

#     if file.filename == '':
#         return {'error': 'No file selected'}, 400

#     if file and allowed_file(file.filename):

#         filename = secure_filename(file.filename)

#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#         return {'message': 'success', 'filename': filename}, 200

#     else:
#         return {'error': 'Invalid file type'}, 400


# @app.route('/predict', methods=['GET'])
# def predict():

#     files = os.listdir(app.config['UPLOAD_FOLDER'])

#     if len(files) > 0:
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], files[0])

#         prediction_response = prediction(file_path)

#         os.remove(file_path)

#         return prediction_response
#     else:
#         return {}, 404
