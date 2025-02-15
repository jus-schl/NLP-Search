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
    for i, doc_idx in enumerate(ranked_doc_indices[:5]):
        sql = text("SELECT artist, title, tag, year, lyrics FROM songs WHERE id=:id")
        result = db.session.execute(sql, {"id": doc_idx+1})
        song = result.fetchone()
        docs[i] = song
    return docs