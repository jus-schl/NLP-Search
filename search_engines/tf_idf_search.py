from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from db import db
from sqlalchemy.sql import text
from scipy.sparse import load_npz
import json
from itertools import islice


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

def load_vocabulary(literal_search):
    if literal_search:
        with open('./data/tfv4_vocabulary.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        with open('./data/stem_tfv4_vocabulary.json', 'r', encoding='utf-8') as file:
            return json.load(file)

def return_docs(input_query, literal_search, filters):
    print(literal_search)
    t2i = load_vocabulary(literal_search)
    tfv4 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", vocabulary=t2i)
    if literal_search:
        sparse_td_matrix = load_npz('./data/tf_idf.npz')
    else:
        sparse_td_matrix = load_npz('./data/stem_tf_idf.npz')
    tokens = input_query.split()

    for i,token in enumerate(tokens):
        hits_matrix = eval(rewrite_query(token, t2i))
        hits_matrix = np.asarray(hits_matrix).flatten()
        if i == 0:
            hits_matrix_addition = hits_matrix
        else:
            hits_matrix_addition = hits_matrix_addition + hits_matrix

    hits_list = hits_matrix_addition.nonzero()[0]
          
  
    sorted_results = sorted(
        [(doc_idx, hits_matrix_addition[doc_idx]) for doc_idx in hits_list],
        key=lambda x: x[1],
        reverse=True
    )
    docs = {}
    top_ids = [int(doc_idx[0]+1) for doc_idx in sorted_results]
    if len(filters) == 0:
        sql = text("SELECT artist, title, tag, year, id FROM songs WHERE id IN :ids")
        result = db.session.execute(sql, {"ids": tuple(top_ids)})
    else:
        sql = text("SELECT artist, title, tag, year, id FROM songs WHERE id IN :ids AND LOWER(artist) in :artists")
        result = db.session.execute(sql, {"ids": tuple(top_ids), "artists": tuple(filters)})
    docs = {row[4]: row for i, row in enumerate(result.fetchall())}
    sorted_docs = {i: docs[doc_id] for i, doc_id in enumerate(top_ids) if doc_id in docs}
    return dict(islice(sorted_docs.items(), 30))