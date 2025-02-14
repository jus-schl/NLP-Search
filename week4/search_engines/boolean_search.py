from sklearn.feature_extraction.text import CountVectorizer
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
    cv = CountVectorizer(lowercase=True, binary=True)
    sparse_matrix = cv.fit_transform(stemmed_documents if stemmed_documents else documents)
    sparse_td_matrix = sparse_matrix.T.tocsr()
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T

    t2i = cv.vocabulary_
    #searching for matching word in dataset
    hits_matrix = eval(rewrite_query(input_query, t2i))
    hits_list = list(hits_matrix.nonzero()[1])   

    docs = {}

    for i, doc_idx in enumerate(hits_list):
        docs[i] = documents[doc_idx]
    return docs