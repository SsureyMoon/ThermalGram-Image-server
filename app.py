import os
import json
from flask import Flask, request, redirect,\
    url_for, render_template, flash, jsonify, make_response
from werkzeug.utils import secure_filename
from settings import config
from core import face_recognizer as fr
from core import linear_regressor as lr
from core import thermal_grader as tg
import httplib2

app = Flask(__name__)
app.config.from_object(__name__)
auth_token = config.AUTH_TOKEN
IMAGE_FOLDER = os.path.join(config.BASE_DIR, 'data/image')
TRAIN_FOLDER = os.path.join(config.BASE_DIR, 'data/train')
ALLOWED_EXTENSIONS = set(['jpeg', 'JPEG', 'jpg', 'png', 'bmp', 'bin', 'txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return jsonify(result="success")

@app.route("/image/", methods=['GET', 'POST'])
def image():
    if request.method == 'GET':
        response = make_response(
            render_template('upload.html')
        )
        return response

    if request.method == 'POST':
        if request.form.get('_auth_token') != auth_token:
            response = make_response(
                json.dumps("Token is not valid"), 401
            )
            response.headers['Content-Type'] = 'application/json'
            return response

        image_file_url = request.form.get('justimage', None)

        if image_file_url and allowed_file(image_file_url):
            h = httplib2.Http('.cache')
            response, content = h.request(image_file_url, "GET")

            if response.status == '200' or '304':
                filename="image.jpg"
                # filename = secure_filename(image_file.filename)
                image_file_path = os.path.join(IMAGE_FOLDER, filename)
                with open(image_file_path, 'wb') as f:
                    f.write(content)
                #image_file.save(image_file_path)

        temp_file_url = request.form.get('temperature', None)

        if temp_file_url and allowed_file(temp_file_url):
            h = httplib2.Http('.cache')
            response, content = h.request(temp_file_url, "GET")

            filename = "temp.bin"
            temperature_path = os.path.join(TRAIN_FOLDER, filename)
            with open(temperature_path, 'wb') as f:
                    f.write(content)

        rate = request.form.get('rate')

        if rate:
            has_user_rate = True
        else:
            has_user_rate = False
            rate = 2.5

        upload_result = {
            "result": "success",
            "rate": rate,
            "image_file": image_file_url if image_file_url else None,
            "temperature_file": temp_file_url if temp_file_url else None,
            "result": None
        }
        if image_file_url or temp_file_url:
            result, res = fr.face_recognizer(image_file_path, int(rate))
            if result:
                predicted_rate =lr.linear_regressor(res, int(rate))
                upload_result['result'] = {"how_other_user_say": predicted_rate}
            else:
                upload_result['result'] = {"how_other_user_say": "no face found"}

            if image_file_url:
                thermal_rate = tg.thermal_grader(image_file_path)
                upload_result['result']['thermal_rate'] = thermal_rate if thermal_rate else 2.5

        return jsonify(upload_result)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
