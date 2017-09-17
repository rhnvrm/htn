import os
import requests as re
from flask import Flask, jsonify, request, redirect, url_for,session
from flask_cors import CORS
import json
import six
import pandas as pd
from math import sqrt

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

# maps api
MAPS_API_KEY = 'AIzaSyCMAR2RmRLRVJ_LLFYOQqaRVRy3ckE3mVY'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/")
def helloWorld():
    return "Hello, world! <a href='https://github.com/rhnvrm/'>Fork me on GitHub!</a>"


@app.route('/convert/<val>/<_to>/<_from>', methods=['GET'])
def convert(val, _to, _from):
    if request.method == 'GET':
        params = (
            ('from', _from),
            ('to', _to),
            ('amount', val),
        )

        resp = re.get('https://xecdapi.xe.com/v1/convert_from.json/', params=params, auth=(xe_account_id, xe_api_key))
        result = {"result": resp.json()["to"][0]["mid"], 'status': 'OK'}

        return jsonify(result)


@app.route('/translate/<target>/<text>')
def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import storage
    from google.cloud import translate

    # Explicitly use service account credentials by specifying the private key
    # file. All clients in google-cloud-python have this helper, see
    # https://google-cloud-python.readthedocs.io/en/latest/core/modules.html
    #   #google.cloud.client.Client.from_service_account_json
    storage_client = storage.Client.from_service_account_json(
        'service_account.json')

    # Make an authenticated API request    
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target)

    return jsonify({'status': 'OK',
                    'text': result['input'],
                    'translation': result['translatedText'],
                    'detected_source': result['detectedSourceLanguage']})


@app.route('/city_ratings')
def city_ratings():
    with open(os.path.join(os.path.dirname(__file__), 'ratings.json')) as f:
        content = f.read()

    return jsonify(json.loads(content))


@app.route('/crime')
def crime():
    with open(os.path.join(os.path.dirname(__file__), 'assaults.json')) as f:
        content = f.read()

    return jsonify(json.loads(content))


@app.route('/pricy')
def pricy():
    with open(os.path.join(os.path.dirname(__file__), 'pricy.json')) as f:
        content = f.read()

    return jsonify(json.loads(content))


@app.route('/suggestion/<loc>/<crime>/<price>')
def suggest(loc, crime, price):
    
    loc = float(loc)
    crime = float(crime)
    price = float(price)

    for i in [loc, crime, price]:
        if i < 0.0 or i > 5.0:
            return jsonify({"status": "Invalid Input"})

    loc /= 5
    crime /= 5 
    price /= 5

    with open(os.path.join(os.path.dirname(__file__), 'ratings.json')) as f:
        ratings = f.read()
    ratings = json.loads(ratings)
    with open(os.path.join(os.path.dirname(__file__), 'assaults.json')) as f:
        assaults = f.read()
    assaults = json.loads(assaults)
    with open(os.path.join(os.path.dirname(__file__), 'pricy.json')) as f:
        pricy = f.read()
    pricy = json.loads(pricy)

    n1 = set()
    for i in ratings["result"]:
        n1.add(i['neighborhood'])
        
    # print(len(n1))

    n2 = set()
    for i in assaults["result"]:
        n2.add(i['neighborhood'])
        
    # print(len(n2))

    inter = n1.intersection(n2)

    dl = {}
    fl = {}

    for i in inter:
        dl[i] = [0, 0, 0]

    for i in ratings["result"]:
        if i["neighborhood"] in inter:
            dl[i["neighborhood"]][0] = i["reviews"]
    for i in assaults["result"]:
        if i["neighborhood"] in inter:
            dl[i["neighborhood"]][1] = i["crime"]
            # print(i["crime"])
    for i in pricy["result"]:
        if i["neighbourhood"] in inter:
            dl[i["neighbourhood"]][2] = i["price"]

    for i in inter:
        l, c, p = dl[i][0], dl[i][1], dl[i][2]
        fl[i] = sqrt((l - loc)**2 + (c - crime)**2 + (p - price)**2)

    result = {}
    for key in sorted(fl, key=lambda x: fl[x], reverse=True)[:5]:
        result[key] = fl[key]

    return jsonify({"result": result})


@app.route('/geocode/<address>')
def geocode(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=" + MAPS_API_KEY
    res = re.get(url)
    
    return jsonify(json.loads(res.text))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)