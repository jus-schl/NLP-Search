import json
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem import LancasterStemmer
ls = LancasterStemmer()
# This file can be used to write the vocabulary.json file used by the search engines.

file = open('smaller_songs.json', 'r', encoding='utf-8')
data = json.load(file)
lyrics = [item['lyrics'] for item in data['songs'] if 'lyrics' in item]
stemmed_lyrics = []

for song in lyrics:
    song = nltk.word_tokenize(song)
    stemmed_song = " ".join(ls.stem(word) for word in song)
    stemmed_lyrics.append(stemmed_song)



cv = CountVectorizer(lowercase=True, binary=True)
cv.fit(lyrics)

stem_cv = CountVectorizer(lowercase=True, binary=True)
stem_cv.fit(stemmed_lyrics)

with open('vocabulary.json', 'w', encoding='utf-8') as file:
    json.dump(cv.vocabulary_, file)

with open('stem_vocabulary.json', 'w', encoding='utf-8') as file:
    json.dump(stem_cv.vocabulary_, file)
