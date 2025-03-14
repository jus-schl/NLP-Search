from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

documents = []
article = []
with open('documents.txt', "r", encoding='utf-8') as file:
    for line in file:
        line = line.split()
        if line[0] == "<article":
            continue
        if line[0] == "</article>":
            article_string = " ".join(word for word in article)
            documents.append(article_string)
            article = []
            continue
        for word in line:
            article.append(word)

d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}

cv = CountVectorizer(lowercase=True, binary=True)
sparse_matrix = cv.fit_transform(documents)
sparse_td_matrix = sparse_matrix.T.tocsr()
dense_matrix = sparse_matrix.todense()
td_matrix = dense_matrix.T

t2i = cv.vocabulary_

def rewrite_token(t):
    if t not in d and t not in t2i: # handle unknown tokens
        return 'np.matrix([0] * sparse_td_matrix.shape[1])'
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t))

def rewrite_query(query):
    tokens = query.split()
    return " ".join(rewrite_token(token) for token in tokens) # if possible, the next token is also given to the function


#main loop
while True:
    
    input_query = input("Search for: ") #user input
    #loop exit
    if input_query == "":
        break

    #searching for matching word in dataset
    try:
        hits_matrix = eval(rewrite_query(input_query))
        hits_list = list(hits_matrix.nonzero()[1])   

        #printing results
        for i, doc_idx in enumerate(hits_list):
            print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))
    except:
        print("Query failed")
