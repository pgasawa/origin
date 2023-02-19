import json
import math
import numpy as np
import ast
from flask import Flask, request
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials, firestore

import web_scraper, summarization
from ChatBot import cli_app, ingest_data

from embeddings import run_kmeans

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
            'center': doc_dict['center']
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

@app.route('/send-browser-history')
def send_browser_history():
    args = request.args
    username = args.get('username')
    urls = args.get('urls').split(',')
    titles = args.get('titles').split(',')
    timestamps = args.get('timestamps').split(',')

    # Push new URLs to DB
    for i in range(len(urls)):
        doc = db.collection('urls').document()
        doc.set({
            'username': username,
            'url': urls[i],
            'title': titles[i],
            'timestamp': timestamps[i]
        })

    # Fetch old URLs
    old_url_docs = db.collection('urls').where('username', '==', username).stream()
    for doc in old_url_docs:
        doc_dict = doc.to_dict()
        urls.append(doc_dict['url'])
        titles.append(doc_dict['title'])
        timestamps.append(doc_dict['timestamp'])

    kmeans = run_kmeans(titles, num_clusters=2)
    cluster_centers = kmeans.cluster_centers_

    labels = kmeans.labels_
    cluster_urls = {}

    clusters_count = db.collection('clusters').where('username', '==', username).count().get()[0][0].value
    if clusters_count == 0:

        # Create doc id array
        doc_ids = []

        # Create new clusters
        for i in range(cluster_centers.shape[0]):
            cluster_center = cluster_centers[i].tolist()
            doc = db.collection('clusters').document()
            doc.set({
                'username': username,
                'name': f'Unnamed Cluster {i+1}',
                'center': cluster_center
            })
            doc_ids.append(doc.id)
        
        for i, label in enumerate(labels):
            if doc_ids[label] not in cluster_urls:
                cluster_urls[doc_ids[label]] = [urls[i]]
            else:
                cluster_urls[doc_ids[label]].append(urls[i])
        # Run web scraper on each cluster of urls
        for id, urls in cluster_urls.items():
            web_scraper.scrape(urls, id)
            ingest_data.ingestion(id)
    else:
        # Switch existing clusters
        clusters = db.collection('clusters').where('username', '==', username).stream()
        cluster_ids = []
        for cluster in clusters:
            old_center = cluster.to_dict()['center']
            old_center_np = np.array(old_center)
            best_center, best_dist = None, math.inf
            for i in range(cluster_centers.shape[0]):
                center = cluster_centers[i]
                dist = np.linalg.norm(old_center_np - center)
                if dist < best_dist:
                    best_center, best_dist = center, dist
            best_center = best_center.tolist()
            cluster.reference.update({
                'center': best_center
            })
            cluster_ids.append(cluster.id)
        for i, label in enumerate(labels):
            if cluster_ids[label] not in cluster_urls:
                cluster_urls[cluster_ids[label]] = [urls[i]]
            else:
                cluster_urls[cluster_ids[label]].append(urls[i])
        # Run web scraper on each cluster of urls
        for id, urls in cluster_urls.items():
            web_scraper.scrape(urls, id)
            ingest_data.ingestion(id)

    return json.dumps({'message': 'succeeded!'})

app.run()
