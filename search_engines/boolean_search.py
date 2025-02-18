from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.sparse import load_npz
from db import db
from sqlalchemy.sql import text
import json

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
        with open('./data/cv_vocabulary.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        with open('./data/stem_vocabulary.json', 'r', encoding='utf-8') as file:
            return json.load(file)    

def return_docs(input_query, literal_search):
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

    for i, doc_idx in enumerate(hits_list):
        if i == 10:
            break
        sql = text("SELECT artist, title, tag, year, lyrics FROM songs WHERE id=:id")
        result = db.session.execute(sql, {"id": int(doc_idx+1)})
        song = result.fetchone()
        docs[i] = [song[0], song[1], song[2], song[3], song[4]]

    return docs