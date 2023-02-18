import json
from flask import Flask, request
from flask_cors import CORS, cross_origin

from embeddings import get_high_dim_embeddings

app = Flask(__name__)
CORS(app) 

@app.route('/')
def index():
    response = Flask.jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return json.dumps({'message': 'hello world'})

@app.route('/send-browser-history', methods=['POST'])
def send_browser_history():
    # print("Raw request", request)
    data = request.json
    # print("Received data:", data)
    count = int(request.form['url_count'])
    urls, titles = [], []
    for i in range(count):
        urls.append(request.form['url' + str(i)])
        titles.append(request.form['title' + str(i)])
    
    embeddings = get_high_dim_embeddings(titles)
    # print(embeddings)
    response = Flask.jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

app.run()
