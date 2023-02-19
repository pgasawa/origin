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
from semantic_search import find_k_closest_urls
from collaborative_filtering import recommendations

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
    print("ID", cluster_id)
    print("New", new_cluster_name)

    doc = db.collection('clusters').document(cluster_id)
    doc.update({
        'name': new_cluster_name
    })

    return json.dumps({'message': 'succeeded!'})

@app.route('/summarize-cluster')
def summarize_cluster():
    args = request.args
    cluster_id = args.get('cluster_id')

    f = open(f"{cluster_id}_output.txt", "r")
    print(f"{cluster_id}_output.txt")
    input_text = " ".join(f.readlines()).replace("\n\n", " ")
    return summarization.summary(input_text)

@app.route('/cluster-chat-bot')
def cluster_chat():
    args = request.args
    cluster_id = args.get('cluster_id')
    question = args.get('question')
    title = args.get('title')
    chat_history = ast.literal_eval(args.get('history'))
    
    answer, chat_history = cli_app.ask_question(cluster_id, title, question, chat_history)
    return json.dumps({'answer': answer, 'history': repr(chat_history)})

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

def send_browser_history_params(username, urls, titles, timestamps):
    urls = urls.split('||||')
    titles = titles.split('||||')
    timestamps = timestamps.split('||||')

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

@app.route('/semantic-search')
def semantic_search_endpoint():
    args = request.args
    query = args['query']
    username = args['username']

    urls = find_k_closest_urls(db, 3, username, query)
    return json.dumps({
        'message': 'succeeded!',
        'urls': urls
    })
    
@app.route('/recommendations')
def recommendations_endpoint():
    args = request.args
    username = args['username']
    cluster_id = args['cluster_id']

    urls = recommendations(db, username, cluster_id)
    return json.dumps({
        'message': 'succeeded!',
        'urls': urls
    })

app.run()
# existing_clusters(db, "arvind6902@gmail.com", [], [], [])

send_browser_history_params("test6",
                            "https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm||||https://cs170.org/syllabus/||||https://hackmd.io/jH9Qta6NRHa1P_bQjV2f6w||||https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/||||https://jarednielsen.com/big-o-omega-theta/||||https://www.geeksforgeeks.org/greedy-algorithms/||||https://www.programiz.com/dsa/bellman-ford-algorithm||||https://www.baeldung.com/cs/bellman-ford||||https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/||||https://cs170.org/||||https://www.investopedia.com/terms/f/financial-literacy.asp#:~:text=Financial%20literacy%20is%20the%20ability,management%2C%20budgeting%2C%20and%20investing.||||https://online.hbs.edu/blog/post/how-to-read-a-balance-sheet||||https://www.vocabulary.com/dictionary/finances#:~:text=When%20you're%20talking%20about,having%20to%20do%20with%20money.||||https://digit.business/financial-literacy/what-is-an-asset-what-is-a-liability#:~:text=Assets%20are%20the%20items%20your,and%20liabilities%20take%20money%20out!||||https://www.investopedia.com/terms/t/t-account.asp#:~:text=Key%20Takeaways-,A%20T%2Daccount%20is%20an%20informal%20term%20for%20a%20set,appears%20just%20above%20the%20T.||||https://online.hbs.edu/blog/post/how-to-prepare-a-balance-sheet||||https://www.shopify.com/blog/what-is-fiscal-year#:~:text=A%20fiscal%20year%20is%20a,up%20with%20the%20calendar%20year.||||https://www.investopedia.com/ask/answers/090415/are-dividends-considered-expense.asp#:~:text=Cash%20or%20stock%20dividends%20distributed,section%20of%20the%20balance%20sheet.||||https://corporatefinanceinstitute.com/resources/accounting/t-accounts/||||https://ramp.com/startup-accounting/how-to-create-a-balance-sheet||||https://people.eecs.berkeley.edu/~jrs/189/||||https://en.wikipedia.org/wiki/Support_vector_machine||||https://en.wikipedia.org/wiki/Linear_regression||||https://people.eecs.berkeley.edu/~jrs/189/lec/04.pdf||||https://people.eecs.berkeley.edu/~jrs/189/lec/02.pdf||||https://people.eecs.berkeley.edu/~jrs/189/lec/05.pdf||||https://people.eecs.berkeley.edu/~jrs/189/lec/06.pdf||||https://realpython.com/python-ai-neural-network/||||https://www.activestate.com/resources/quick-reads/how-to-create-a-neural-network-in-python-with-and-without-keras/||||https://towardsdatascience.com/how-to-code-linear-regression-from-scratch-quick-easy-cfd8c8f9eb9d||||https://www.chess.com/openings/Sicilian-Defense-Open-Dragon-Variation||||https://chesspathways.com/chess-openings/||||https://enthu.com/blog/chess/chess-middlegame/||||https://www.masterclass.com/articles/chess-middlegame-positions-and-chess-strategy-tips||||https://www.simplifychess.com/fried-liver-attack/index.html||||https://en.wikipedia.org/wiki/Magnus_Carlsen||||https://en.wikipedia.org/wiki/World_Chess_Championship_2023||||https://www.ragchess.com/endgame-theory-opposition-triangulation-and-trebuchets-explained/||||https://www.chessable.com/blog/caro-kann-defense/||||https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/",
                            "Bellman–Ford algorithm - Wikipedia||||CS 170 - Efficient Algorithms and Intractable Problems - Syllabus and Policies||||Fast Fourier Transform (FFT)||||Dijkstra's Shortest Path Algorithm | Greedy Algo-7||||What’s the Difference Between Big O, Big Omega, and Big Theta?||||Greedy Algorithms - GeeksforGeeks||||Bellman Ford's Algorithm||||Bellman Ford Shortest Path Algorithm | Baeldung on Computer Science||||Kruskal’s Minimum Spanning Tree Algorithm | Greedy Algo-2||||CS 170 - Efficient Algorithms and Intractable Problems||||What Is Accounting, Financial Literacy, and Why Is It So Important?||||HOW TO READ & UNDERSTAND A BALANCE SHEET||||Finances and Accounting - Definition, Meaning & Synonyms||||What is an Asset? What is a Liability?||||T-Account: Definition, Example, Recording, and Benefits||||How to Prepare an Accounting Balance Sheet: 5 Steps for Beginners||||What Is a Fiscal Year? Definition and Guide||||Are Dividends Considered a Company Expense in Accounting?||||Accounting: T Accounts Guide||||A small business guide to creating a balance sheet||||CS 189/289A: Introduction to Machine Learning||||Support vector machine (Machine Learning) - Wikipedia||||Linear regression (Artificial Intelligence) - Wikipedia||||CS 189: Soft-Margin Support Vector Machines for Machine Learning; Features||||CS 189: Linear Classifiers and Perceptrons for Machine Learning||||CS 189: Machine Learning Abstractions and Numerical Optimization||||CS 189: Machine Learning Decision Theory; Generative and Discriminative Models||||Python AI: How to Build a Machine Learning Neural Network & Make Predictions||||How To Create a Machine Learning Neural Network In Python – With And Without Keras - ActiveState||||How To Code Linear Regression From Scratch — Artificial Intelligence||||Sicilian Defense: Open, Dragon Variation (Chess)||||The Ultimate Guide to Chess Openings||||8 Chess Middlegame Strategies and Tips for Beginners - EnthuZiastic||||Chess Middlegame Positions and Chess Strategy Tips - 2023 - MasterClass||||Chess - Fried Liver Attack (How To Play It, Attack It, And Counter It)||||Magnus Carlsen (Chess)||||World Chess Championship 2023 - Wikipedia||||Endgame Theory Explained (Opposition, Triangulation, & Trebuchets)||||The Caro-Kann: How to Play It as White and Black - Chess Blog||||A step-by-step guide to building a simple chess AI",
                            "7000||||6000||||3000||||3500||||1000||||6050||||6800||||6900||||7300||||10000||||500||||1000||||1200||||3000||||4000||||8000||||6000||||3005||||5000||||8100||||10000||||1050||||2000||||6000||||3500||||3000||||5000||||90000||||11000||||10500||||1000||||2000||||4000||||18000||||3000||||10000||||6000||||3500||||1205||||5505"
)