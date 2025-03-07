from search_engines import neural_search
from search_engines import boolean_search
from search_engines import tf_idf_search
from nltk.stem import LancasterStemmer
from rapidfuzz import process
ls = LancasterStemmer()

with open("./data/word_list.txt", "r", encoding="utf-8") as f:
    word_list = f.read().splitlines()

def search_songs(query, selected_engine, filters):
    filters = [artist.lower() for artist in filters]
    if query == "":
        return None
    
    try:
    
        if selected_engine == 1:
            if query[0] == '"' and query[-1] == '"':
                return boolean_search.return_docs(query[1:len(query)-1], True, filters)

            else:
                query = " ".join(ls.stem(word) for word in query.split())
                return boolean_search.return_docs(query, False, filters)
            
        elif selected_engine == 2:
            if query[0] == '"' and query[-1] == '"':
                return tf_idf_search.return_docs(query[1:len(query)-1], True, filters)
            else:
                print(ls.stem(query))
                query = " ".join(ls.stem(word) for word in query.split())
                return tf_idf_search.return_docs(query, True, filters)
            
        elif selected_engine == 3:
            return neural_search.return_docs(query, filters)
    except Exception as e:
        print(e)
        return None



def search_word(query):
    try:
        max_edit_distance = 3
        min_length_ratio = 0.7
        matches = process.extract(query, word_list, limit=5, score_cutoff=100 - (max_edit_distance * 10))
        for best_match, score, _ in matches:
            if len(best_match) >= len(query) * min_length_ratio:
                return best_match
        return None
    except:
        return None