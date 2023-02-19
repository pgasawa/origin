import numpy as np
from scipy.spatial.distance import cosine as cosine_similarity

def recommendations(db, username, cluster_id):
    cluster = db.collection('clusters').document(cluster_id).get().to_dict()
    cluster_mean = cluster['center']
    
    url_refs = db.collection('urls').where('username', '!=', username).stream()
    urls = []
    for ref in url_refs:
        d = ref.to_dict()
        d['cosine_sim'] = 1.0 - float(cosine_similarity(np.array(cluster_mean), np.array(d['embedding'])))
        del d['embedding']
        urls.append(d)
    
    urls = list(sorted(urls, key=lambda u: u['cosine_sim'], reverse=True))[:3]
    return urls
