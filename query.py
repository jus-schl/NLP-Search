from search_engines import neural_search
from search_engines import boolean_search
from search_engines import tf_idf_search
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
from nltk.stem import LancasterStemmer
ls = LancasterStemmer()



def search_songs(query, selected_engine):
    if query == "":
        return None
    
    if selected_engine == 1:
        if query[0] == '"' and query[-1] == '"':
            return boolean_search.return_docs(query[1:len(query)-1], True)
        else:
            query = " ".join(ls.stem(word) for word in query.split())
            return boolean_search.return_docs(query, False)
        
    elif selected_engine == 2:
        if query[0] == '"' and query[-1] == '"':
            return tf_idf_search.return_docs(query[1:len(query)-1], True)
        else:
            print(ls.stem(query))
            query = " ".join(ls.stem(word) for word in query.split())
            return tf_idf_search.return_docs(query, True)

    elif selected_engine == 3:
        return neural_search.return_docs(query)