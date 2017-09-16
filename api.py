import os
import requests as re
from flask import Flask, jsonify, request, redirect, url_for,session
from flask_cors import CORS
import json

from werkzeug import secure_filename

UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
app.secret_key = 'development'

# xe.com
xe_account_id = 'rhnvrm895754975'
xe_api_key = 'rhv2pfncfeei6gvm1dvl709ajf'


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/")
def helloWorld():
    return "Hello, world! <a href='https://github.com/rhnvrm/'>Fork me on GitHub!</a>"


@app.route('/translate', methods=['GET'])
def translate(text):
    if request.method == 'GET':
        input_text  = text
        print(text)
        pass


@app.route('/convert/<val>/<_to>/<_from>', methods=['GET'])
def convert(val, _to, _from):
    if request.method == 'GET':
        print(val, _to, _from)
        params = (
            ('from', _from),
            ('to', _to),
            ('amount', val),
        )

        resp = re.get('https://xecdapi.xe.com/v1/convert_from.json/', params=params, auth=(xe_account_id, xe_api_key))
        result = {"result": resp.json()["to"][0]["mid"], 'status': 'OK'}

        return jsonify(result)




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port,debug=True)