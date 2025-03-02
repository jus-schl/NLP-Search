from sentence_transformers import SentenceTransformer
import numpy as np
from db import db
from sqlalchemy.sql import text
model = SentenceTransformer('all-MiniLM-L6-v2')

doc_embeddings = np.load("./data/embeddings.npy")

def return_docs(query):

    query_embedding = model.encode(query)

    # apply cosine similarity
    # Search for most similar document
    cosine_similarities = np.dot(query_embedding, doc_embeddings.T)

    # Rank hits
    ranked_doc_indices = np.argsort(cosine_similarities)[::-1]  # Sort descending

    docs = {}
    top_ids = [int(doc_idx+1) for doc_idx in ranked_doc_indices[:20]]
    sql = text("SELECT artist, title, tag, year, id FROM songs WHERE id IN :ids")
    result = db.session.execute(sql, {"ids": tuple(top_ids)})
    docs = {i: row for i, row in enumerate(result.fetchall())}
    return docs