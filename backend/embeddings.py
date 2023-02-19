import requests
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

HF_TOKEN = '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'
embedder = SentenceTransformer('paraphrase-MiniLM-L6-v2', cache_folder='embedder')


# texts = [
#     "How do I get a replacement Medicare card?",
#     "What is the monthly premium for Medicare Part B?",
#     "How do I terminate my Medicare Part B (medical insurance)?",
#     "How do I sign up for Medicare?",
#     "Can I sign up for Medicare Part B if I am working and have health insurance through an employer?",
#     "How do I sign up for Medicare Part B if I already have Part A?",
#     "What are Medicare late enrollment penalties?",
#     "What is Medicare and who can get it?",
#     "How can I get help with my Medicare Part A and Part B premiums?",
#     "What are the different parts of Medicare?",
#     "Will my Medicare premiums be higher because of my higher income?",
#     "What is TRICARE ?",
#     "Should I sign up for Medicare Part B if I have Veterans' Benefits?",
#     "Strawberry Fields Forever: A Guide to Growing Your Own Berries",
#     "Strawberry Recipes for Every Occasion: From Smoothies to Shortcake",
#     "The Health Benefits of Strawberries: Why You Should Be Eating More",
#     "Strawberry Farming Techniques: Tips and Tricks from the Pros",
#     "Strawberry Season: Where to Pick Your Own Berries Near You",
#     "All About Strawberries: From Seed to Harvest",
#     "Strawberry Nutrition: Facts and Figures You Need to Know",
#     "The Best Strawberry Varieties for Your Garden: A Comprehensive Guide",
#     "Cooking with Strawberries: Sweet and Savory Recipes to Try at Home",
#     "Strawberry Shortcake: A Classic Dessert Recipe with a Modern Twist"
# ]

def get_high_dim_embeddings(texts):
    embeddings = embedder.encode(texts)
    embeddings = np.array(embeddings)
    return embeddings

def run_kmeans_2(texts, num_clusters=2):
    # Define number of clusters and fit k-means model
    vec_embeddings = get_high_dim_embeddings(texts)
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(vec_embeddings)

    # Get the labels and indices of vectors in each cluster
    labels = kmeans.labels_
    cluster_indices = {}
    for i, label in enumerate(labels):
        if label not in cluster_indices:
            cluster_indices[label] = [i]
        else:
            cluster_indices[label].append(i)

    # # Print indices of vectors in each cluster
    # for cluster, indices in cluster_indices.items():
    #     print(f"Cluster {cluster} has {len(indices)} vectors with indices: {indices}")

    cluster_titles = {}
    for i, label in enumerate(labels):
        if label not in cluster_titles:
            cluster_titles[label] = [texts[i]]
        else:
            cluster_titles[label].append(texts[i])

    titles = []
    # print(cluster_titles)
    for cluster in cluster_titles:
        prompt = "What noun describes the following texts? Please output only the noun and no other text. If you are unsure, please only output a noun that is most similar to the texts and nothing more: \"" + ' '.join(cluster_titles[cluster]) + "\""
        # print(prompt)
        prompt = prompt[:14000]
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )
        titles.append(response.choices[0].text.strip())

    return kmeans, vec_embeddings, cluster_indices, titles

def run_kmeans(texts, num_clusters=2):
    # Define number of clusters and fit k-means model
    vec_embeddings = get_high_dim_embeddings(texts)
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(vec_embeddings)
    # return kmeans

    # # Get the labels and indices of vectors in each cluster
    labels = kmeans.labels_
    cluster_titles = {}
    for i, label in enumerate(labels):
        if label not in cluster_titles:
            cluster_titles[label] = [texts[i]]
        else:
            cluster_titles[label].append(texts[i])

    titles = []
    # print(cluster_titles)
    for cluster in cluster_titles:
        prompt = "What noun describes the following texts? Please output only the noun and no other text. If you are unsure, please only output a noun that is most similar to the texts and nothing more: \"" + ' '.join(cluster_titles[cluster]) + "\""
        # print(prompt)
        prompt = prompt[:14000]
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )
        titles.append(response.choices[0].text.strip())
    return kmeans, titles

    # # Print indices of vectors in each cluster
    # for cluster, indices in cluster_indices.items():
    #     print(f"Cluster {cluster} has {len(indices)} vectors with indices: {indices}")

# # read in test_titles.txt as a list of sentences per line
# with open('ChatBot/test_titles.txt', 'r') as f:
#     test_titles = f.readlines()

# print(run_kmeans(test_titles, num_clusters=10))