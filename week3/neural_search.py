from sentence_transformers import SentenceTransformer
import numpy as np
model = SentenceTransformer('all-MiniLM-L6-v2')


def return_docs(query, documents, doc_embeddings):
    query_embedding = model.encode(query)

    # apply cosine similarity
    # Search for most similar document
    cosine_similarities = np.dot(query_embedding, doc_embeddings.T)

    # Rank hits
    ranked_doc_indices = np.argsort(cosine_similarities)[::-1]  # Sort descending

    print(f"Your query '{query}' matches the following documents:")
    for i, doc_idx in enumerate(ranked_doc_indices[:5]):
        print(f"Doc #{i} (score: {cosine_similarities[doc_idx]:.4f}): {documents[doc_idx]}")