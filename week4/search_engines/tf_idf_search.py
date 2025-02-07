from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}


def rewrite_token(t, t2i):
    if t not in d and t not in t2i: # handle unknown tokens
        return 'np.matrix([0] * sparse_td_matrix.shape[1])'
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t))

def rewrite_query(query, t2i):
    tokens = query.split()
    return " ".join(rewrite_token(token, t2i) for token in tokens)


def return_docs(input_query, documents, stemmed_documents=None):
    tfv4 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    sparse_td_matrix = tfv4.fit_transform(stemmed_documents if stemmed_documents else documents).T.tocsr()
    t2i = tfv4.vocabulary_
  
    hits_matrix = eval(rewrite_query(input_query, t2i))
    hits_matrix = np.asarray(hits_matrix).flatten()
    hits_list = hits_matrix.nonzero()[0]
          
  
    sorted_results = sorted(
        [(doc_idx, hits_matrix[doc_idx]) for doc_idx in hits_list],
        key=lambda x: x[1],
        reverse=True
    )
    for doc_idx, score in sorted_results:
        print(f"Matching doc #{doc_idx} (Score: {score:.4f}): {documents[doc_idx]}")