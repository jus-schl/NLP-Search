from scipy.sparse import save_npz
from sklearn.feature_extraction.text import TfidfVectorizer  
import json
import nltk
from nltk.stem import LancasterStemmer
ls = LancasterStemmer()


# This file can be used to create the tf_idf files that are used by the tf_idf search engine.

file = open('smaller_songs.json', 'r', encoding='utf-8')
data = json.load(file)
lyrics = [item['lyrics'] for item in data['songs'] if 'lyrics' in item]
stemmed_lyrics = []

for song in lyrics:
    song = nltk.word_tokenize(song)
    stemmed_song = " ".join(ls.stem(word) for word in song)
    stemmed_lyrics.append(stemmed_song)


tfv4 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
stem_sparse_td_matrix = tfv4.fit_transform(stemmed_lyrics).T.tocsr()
sparse_td_matrix = tfv4.fit_transform(lyrics).T.tocsr()


save_npz('stem_tf_idf.npz', stem_sparse_td_matrix)
save_npz('tf_idf.npz', sparse_td_matrix)