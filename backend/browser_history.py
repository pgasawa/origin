from embeddings import run_kmeans_2
import uuid
import numpy as np
import math

import web_scraper
from ChatBot import ingest_data

def generateId():
    return uuid.uuid4().hex

def new_clusters(db, username, titles, urls, timestamps):
    # Generate clusters and URLs from scratch
    cluster_objs = []
    cluster_ids = []
    url_objs = []
    url_ids = []

    kmeans, embeddings, cluster_indices, cluster_titles = run_kmeans_2(titles, 4)
    cluster_centers = kmeans.cluster_centers_
    for cluster_num in cluster_indices:
        cluster_id = generateId()
        cluster_name = f'{cluster_titles[cluster_num]}'
        cluster_center = cluster_centers[cluster_num].tolist()

        cluster_objs.append({
            'name': cluster_name,
            'username': username,
            'center': cluster_center
        })
        cluster_ids.append(cluster_id)

        for idx in cluster_indices[cluster_num]:
            url_id = generateId()
            embedding = embeddings[idx].tolist()
            title = titles[idx]
            url = urls[idx]
            timestamp = timestamps[idx]

            url_objs.append({
                'title': title,
                'url': url,
                'timestamp': timestamp,
                'username': username,
                'cluster_id': cluster_id,
                'embedding': embedding
            })
            url_ids.append(url_id)

    cluster_batch = db.batch()
    for cluster_id, cluster_obj in zip(cluster_ids, cluster_objs):
        doc_ref = db.collection('clusters').document(cluster_id)
        cluster_batch.set(doc_ref, cluster_obj)

    url_batch = db.batch()
    for url_id, url_obj in zip(url_ids, url_objs):
        url_ref = db.collection('urls').document(url_id)
        url_batch.set(url_ref, url_obj)

    cluster_batch.commit()
    url_batch.commit()

    # Web scraper and ingest data
    cluster_id_to_urls = dict()
    for url_id, url_obj in zip(url_ids, url_objs):
        cluster_id = url_obj['cluster_id']
        url = url_obj['url']
        if cluster_id not in cluster_id_to_urls:
            cluster_id_to_urls[cluster_id] = []
        cluster_id_to_urls[cluster_id].append(url)
    
    for cluster_id, urls in cluster_id_to_urls.items():
        web_scraper.scrape(urls, cluster_id) # all urls for a cluster id
        ingest_data.ingestion(cluster_id)


def existing_clusters(db, username, titles, urls, timestamps):
    existing_cluster_objs = []
    existing_cluster_ids = []
    # Get existing clusters (old)
    cluster_refs = db.collection('clusters').where('username', '==', username).stream()
    for cluster_ref in cluster_refs:
        id = cluster_ref.id
        d = cluster_ref.to_dict()
        existing_cluster_objs.append(d)
        existing_cluster_ids.append(id)

    new_url_objs = []
    new_url_ids = []
    # Append new URLs (new)
    for idx in range(len(titles)):
        url_id = generateId()
        title = titles[idx]
        url = urls[idx]
        timestamp = timestamps[idx]

        new_url_objs.append({
            'title': title,
            'url': url,
            'timestamp': timestamp,
            'username': username,
            # 'cluster_id': cluster_id,
            # 'embedding': embedding
        })
        new_url_ids.append(url_id)

    existing_url_objs = []
    existing_url_ids = []
    # Get existing URLs (old)
    url_refs = db.collection('urls').where('username', '==', username).stream()
    for url_ref in url_refs:
        id = url_ref.id
        d = url_ref.to_dict()
        existing_url_objs.append(d)
        existing_url_ids.append(id)

    all_url_objs = existing_url_objs + new_url_objs
    all_url_ids = existing_url_ids + new_url_ids
    all_titles = list(map(lambda o: o['title'], existing_url_objs)) + titles
    new_old_cluster_mapping = {}
    new_cluster_objs = []
    new_cluster_ids = []
    # Calculate new clusters
    kmeans, embeddings, cluster_indices, _ = run_kmeans_2(all_titles)
    for cluster_idx in cluster_indices:
        new_cluster_mean = kmeans.cluster_centers_[cluster_idx].tolist()
        best_old_mean_id, best_old_mean_obj, best_old_dist = None, None, math.inf
        for existing_cluster_id, existing_cluster_obj in zip(existing_cluster_ids, existing_cluster_objs):
            old_cluster_mean = existing_cluster_obj['center']
            dist = np.linalg.norm(np.array(new_cluster_mean) - np.array(old_cluster_mean))
            if dist < best_old_dist:
                best_old_mean_id, best_old_mean_obj, best_old_dist = existing_cluster_id, existing_cluster_obj, dist

        new_old_cluster_mapping[cluster_idx] = best_old_mean_id
        new_cluster_objs.append({
            'center': new_cluster_mean
        })
        new_cluster_ids.append(best_old_mean_id)

    # Add embedding and cluster_id for each new URL
    for new_url_obj in new_url_objs:
        exit = False
        for cluster_idx in cluster_indices:
            for url_idx in cluster_indices[cluster_idx]:
                if all_url_objs[url_idx]['url'] == new_url_obj['url']:
                    new_url_obj['embedding'] = embeddings[url_idx].tolist()
                    new_url_obj['cluster_id'] = new_cluster_ids[cluster_idx]
                    exit = True
                    break
            if exit == True:
                break
        if exit == True:
            continue


    # Update cluster centers for existing clusters
    update_clusters_batch = db.batch()
    for new_cluster_id, new_cluster_obj in zip(new_cluster_ids, new_cluster_objs):
        ref = db.collection('clusters').document(new_cluster_id)
        update_clusters_batch.update(ref, new_cluster_obj)

    # Push new URLs
    create_urls_batch = db.batch()
    for new_url_id, new_url_obj in zip(new_url_ids, new_url_objs):
        ref = db.collection('urls').document(new_url_id)
        create_urls_batch.set(ref, new_url_obj)

    update_clusters_batch.commit()
    create_urls_batch.commit()

    # Web scraper and ingest data
    cluster_id_to_urls = dict()
    for url_id, url_obj in zip(all_url_ids, all_url_objs):
        cluster_id = url_obj['cluster_id']
        url = url_obj['url']
        if cluster_id not in cluster_id_to_urls:
            cluster_id_to_urls[cluster_id] = []
        cluster_id_to_urls[cluster_id].append(url)
    
    for cluster_id, urls in cluster_id_to_urls.items():
        web_scraper.scrape(urls, cluster_id) # all urls for a cluster id
        ingest_data.ingestion(cluster_id)
