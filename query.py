from search_engines import neural_search
from search_engines import boolean_search
from search_engines import tf_idf_search
from nltk.stem import LancasterStemmer
from rapidfuzz import process, fuzz
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
                return tf_idf_search.return_docs(query, False, filters)
            
        elif selected_engine == 3:
            return neural_search.return_docs(query, filters)
    except Exception as e:
        print(e)
        return None



def search_word(query):
    words = query.split()
    suggestion = []
    try:
        for word in words:
            min_length_ratio = 0.7
            matches = process.extract(word, word_list, limit=5, score_cutoff=70)
            for best_match, score, _ in matches:
                if len(best_match) >= len(word) * min_length_ratio:
                    suggestion.append(best_match)
                    break
        suggestion = " ".join(i for i in suggestion)
        if suggestion == query:
            return None # No suggestion, if the best matches are the same query
        return suggestion
    except:
       return None