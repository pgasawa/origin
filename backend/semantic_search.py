import numpy as np
from embeddings import get_high_dim_embeddings

def find_k_closest_urls(db, k, username, query):
    query_embedding = np.array(get_high_dim_embeddings([query]))

    url_refs = db.collection('urls').where('username', '==', username).stream()
    urls = []
    for ref in url_refs:
        doc = ref.to_dict()
        doc['embedding'] = np.array(doc['embedding'])
        doc['l2_dist'] = np.linalg.norm(doc['embedding'] - query_embedding)
        urls.append(doc)

    urls = list(sorted(urls, key=lambda d: d['l2_dist']))[:k]
    return urls
