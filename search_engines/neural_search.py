from sentence_transformers import SentenceTransformer
import numpy as np
from db import db
from sqlalchemy.sql import text
from itertools import islice
model = SentenceTransformer('all-MiniLM-L6-v2')

doc_embeddings = np.load("./data/embeddings.npy")

def return_docs(query, filters):

    query_embedding = model.encode(query)

    # apply cosine similarity
    # Search for most similar document
    cosine_similarities = np.dot(query_embedding, doc_embeddings.T)

    # Rank hits
    ranked_doc_indices = np.argsort(cosine_similarities)[::-1]  # Sort descending

    docs = {}
    top_ids = [int(doc_idx+1) for doc_idx in ranked_doc_indices]
    if len(filters) == 0:
        sql = text("SELECT artist, title, tag, year, id FROM songs WHERE id IN :ids")
        result = db.session.execute(sql, {"ids": tuple(top_ids)})
    else:
        sql = text("SELECT artist, title, tag, year, id FROM songs WHERE id IN :ids AND LOWER(artist) IN :artists")
        result = db.session.execute(sql, {"ids": tuple(top_ids), "artists": tuple(filters)})
    docs = {row[4]: row for i, row in enumerate(result.fetchall())}
    sorted_docs = {i: docs[doc_id] for i, doc_id in enumerate(top_ids) if doc_id in docs} # docs are filtered by their rank in top ids
    return dict(islice(sorted_docs.items(), 30))