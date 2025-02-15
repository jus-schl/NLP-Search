from scipy.sparse import save_npz
from sklearn.feature_extraction.text import CountVectorizer    
import json
import nltk
from nltk.stem import LancasterStemmer
ls = LancasterStemmer()

# This file can be used to create the sparse_td_matrix files that are used by the boolean search engine.

file = open('smaller_songs.json', 'r', encoding='utf-8')
data = json.load(file)
lyrics = [item['lyrics'] for item in data['songs'] if 'lyrics' in item]
stemmed_lyrics = []

for song in lyrics:
    song = nltk.word_tokenize(song)
    stemmed_song = " ".join(ls.stem(word) for word in song)
    stemmed_lyrics.append(stemmed_song)

cv = CountVectorizer(lowercase=True, binary=True)
stem_sparse_matrix = cv.fit_transform(stemmed_lyrics)
sparse_matrix = cv.fit_transform(lyrics)

stem_sparse_td_matrix = stem_sparse_matrix.T.tocsr()
sparse_td_matrix = sparse_matrix.T.tocsr()

save_npz('stem_sparse_td_matrix.npz', stem_sparse_td_matrix)
save_npz('sparse_td_matrix.npz', sparse_td_matrix)