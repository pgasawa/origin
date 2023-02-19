import json
import math
import numpy as np
import ast
import uuid
from flask import Flask, request
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials, firestore

import web_scraper, summarization
from ChatBot import cli_app, ingest_data
from browser_history import new_clusters, existing_clusters

from embeddings import run_kmeans, run_kmeans_2

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("firebase-credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return json.dumps({'message': 'hello world'})

@app.route('/get-clusters')
def get_clusters():
    args = request.args
    username = args.get('username')

    clusters = []
    docs = db.collection('clusters').where('username', '==', username).stream()
    for doc in docs:
        doc_dict = doc.to_dict()
        clusters.append({
            'name': doc_dict['name'],
            'center': doc_dict['center'],
            'id': doc.id
        })
    
    return json.dumps({
        'message': 'succeeded!',
        'clusters': clusters
    })

@app.route('/change-cluster-name')
def change_cluster_name():
    args = request.args
    cluster_id = args.get('cluster_id')
    new_cluster_name = args.get('new_cluster_name')

    doc = db.collection('clusters').document(cluster_id)
    doc.update({
        'name': new_cluster_name
    })

    return json.dumps({'message': 'succeeded!'})

@app.route('/summarize-cluster')
def summarize_cluster():
    args = request.args
    cluster_id = args.get('cluster_id')

    f = open(f"./{cluster_id}_output.txt", "w")
    input_text = " ".join(f.readlines()).replace("\n\n", " ")
    return summarization.summary(input_text)

@app.route('/cluster-chat-bot')
def cluster_chat():
    args = request.args
    cluster_id = args.get('cluster_id')
    question = args.get('question')
    chat_history = ast.literal_eval(args.get('history'))
    
    answer, chat_history = cli_app.ask_question(cluster_id, question, chat_history)
    return answer, repr(chat_history)

@app.route('/send-browser-history', methods=['POST'])
def send_browser_history():
    form = request.form
    username = form['username']
    urls = form['urls'].split(',')
    titles = form['titles'].split(',')
    timestamps = form['timestamps'].split(',')

    num_urls = db.collection('urls').where('username', '==', username).count().get()[0][0].value
    if num_urls == 0:
        new_clusters(db, username, titles, urls, timestamps)
    else:
        existing_clusters(db, username, titles, urls, timestamps)

    return json.dumps({'message': 'succeeded!'})

@app.route('/top-n-urls')
def top_n_urls():
    N = 5
    args = request.args
    username = args['username']
    cluster_id = args['cluster_id']

    docs = db.collection('urls').where('username', '==', username)\
                                .where('cluster_id', '==', cluster_id)\
                                .order_by('timestamp', direction=firestore.Query.DESCENDING)\
                                .limit(N)\
                                .stream()
    
    urls = []
    for doc in docs:
        urls.append(doc.to_dict())
        del urls[-1]['embedding']
    
    return json.dumps({
        'message': 'succeeded!',
        'urls': urls
    })

app.run()
