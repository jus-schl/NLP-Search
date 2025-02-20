from sklearn.feature_extraction.text import TfidfVectorizer
import json
import nltk
from nltk.stem import LancasterStemmer
ls = LancasterStemmer()

file = open('smaller_songs.json', 'r', encoding='utf-8')
data = json.load(file)
lyrics = [item['lyrics'] for item in data['songs'] if 'lyrics' in item]
stemmed_lyrics = []

for song in lyrics:
    song = nltk.word_tokenize(song)
    stemmed_song = " ".join(ls.stem(word) for word in song)
    stemmed_lyrics.append(stemmed_song)

tfv4 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
sparse_td_matrix = tfv4.fit_transform(lyrics).T.tocsr()
t2i = tfv4.vocabulary_

stem_tfv4 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
stem_sparse_td_matrix = stem_tfv4.fit_transform(stemmed_lyrics).T.tocsr()
stem_t2i = stem_tfv4.vocabulary_

with open('tfv4_vocabulary.json', 'w', encoding='utf-8') as file:
    json.dump(t2i, file)

with open('stem_tfv4_vocabulary.json', 'w', encoding='utf-8') as file:
    json.dump(stem_t2i, file)