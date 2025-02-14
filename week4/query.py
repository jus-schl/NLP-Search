from search_engines import neural_search
from search_engines import boolean_search
from search_engines import tf_idf_search
import nltk
import numpy
from nltk.stem import LancasterStemmer
ls = LancasterStemmer()
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
import json

file = open('./data/test_documents.json', 'r', encoding='utf-8')
data = json.load(file)
lyrics = [item['lyrics'] for item in data['songs'] if 'lyrics' in item]

stemmed_songs = []

for song in lyrics:
    song = nltk.word_tokenize(song)
    stemmed_song = " ".join(ls.stem(word) for word in song)
    stemmed_songs.append(stemmed_song)


doc_embeddings = model.encode(lyrics) # doc_embeddings is assigned here so that it does not have to be ran every time neural search is used
print(type(doc_embeddings))
numpy.ndarray.tofile(doc_embeddings, './data/embeddings')
def search_songs(query, selected_engine):
    if query == "":
        return None
    
    if selected_engine == 1:
        if query[0] == '"' and query[-1] == '"':
            return boolean_search.return_docs(query[1:len(query)-1], lyrics)
        else:
            print(ls.stem(query))
            query = " ".join(ls.stem(word) for word in query.split())
            return boolean_search.return_docs(query, lyrics, stemmed_songs)
        
    elif selected_engine == 2:
        if query[0] == '"' and query[-1] == '"':
            return tf_idf_search.return_docs(query[1:len(query)-1], lyrics)
        else:
            print(ls.stem(query))
            query = " ".join(ls.stem(word) for word in query.split())
            return tf_idf_search.return_docs(query, lyrics, stemmed_songs)

    elif selected_engine == 3:
        return neural_search.return_docs(query, lyrics, doc_embeddings)