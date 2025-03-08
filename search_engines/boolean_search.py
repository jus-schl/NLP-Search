from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.sparse import load_npz
from db import db
from sqlalchemy.sql import text
import json
from itertools import islice

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}

operator = ["and", "AND", "or", "OR", "not", "NOT"]
operator_without = ["and", "AND", "or", "OR"]


def rewrite_token(t, t2i):
    if t not in d and t not in t2i: # handle unknown tokens
        return 'np.matrix([0] * sparse_td_matrix.shape[1])'
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t))

def rewrite_query(query, t2i):
    tokens = query.split()
    
    if len(tokens) > 1:
        for i in range(len(tokens)):
            if tokens[i] not in operator and tokens[i+1] not in operator_without:
                tokens.insert(i+1, "and")
            if i == len(tokens) - 2:
                break
    return " ".join(rewrite_token(token, t2i) for token in tokens)

def load_vocabulary(literal_search):
    if literal_search:
        with open('./data/cv_vocabulary.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        with open('./data/stem_vocabulary.json', 'r', encoding='utf-8') as file:
            return json.load(file)    

def return_docs(input_query, literal_search, filters):
    t2i = load_vocabulary(literal_search)
    cv = CountVectorizer(lowercase=True, binary=True, vocabulary=t2i)
    if literal_search:
        sparse_td_matrix = load_npz('./data/sparse_td_matrix.npz')
    else:
        sparse_td_matrix = load_npz('./data/stem_sparse_td_matrix.npz')
    #searching for matching word in dataset
    hits_matrix = eval(rewrite_query(input_query, t2i))
    hits_list = list(hits_matrix.nonzero()[1])

    docs = {}
    top_ids = [int(doc_idx+1) for doc_idx in hits_list]
    if len(filters) == 0:
        sql = text("SELECT artist, title, tag, year, id FROM songs WHERE id IN :ids")
        result = db.session.execute(sql, {"ids": tuple(top_ids)})
    else:
        sql = text("SELECT artist, title, tag, year, id FROM songs WHERE id IN :ids AND LOWER(artist) IN :artists")
        result = db.session.execute(sql, {"ids": tuple(top_ids), "artists": tuple(filters)})
    docs = {i: row for i, row in enumerate(result.fetchall())}
    return dict(islice(docs.items(), 30))