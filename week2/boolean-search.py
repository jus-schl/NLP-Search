from sklearn.feature_extraction.text import CountVectorizer

documents = [
    "this is test data",
    "this too is testing data",
    "some random words here nothing special",
    "duck is interesting data"
    ]

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


previous_token = None
def rewrite_token(t, next_token=None):
    global previous_token
    if t == previous_token and previous_token not in d: # if the token was already handled an empty string is returned
        previous_token = None
        return ''
    if t not in d and t not in t2i: # handle unknown tokens
        return '(0)'
    if t in ["NOT", "not"] and next_token not in d and next_token not in t2i: # if the operator is NOT and the next token is unknown (1) is returned
        previous_token = next_token
        return '(1)'
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t))

def rewrite_query(query):
    tokens = query.split()
    return " ".join(rewrite_token(tokens[i], tokens[i + 1] if i + 1 < len(tokens) else None) for i in range(len(tokens))) # if possible, the next token is also given to the function


#main loop
while True:
    
    input_query = input("Search for: ") #user input
    #loop exit
    if input_query == "":
        break

    #searching for matching word in dataset
    hits_matrix = eval(rewrite_query(input_query))
    hits_list = list(hits_matrix.nonzero()[1])   

    #printing results
    for i, doc_idx in enumerate(hits_list):
        print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))

