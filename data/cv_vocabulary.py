import json
from sklearn.feature_extraction.text import CountVectorizer

# This file can be used to write the vocabulary.json file used by the search engines.

file = open('smaller_songs.json', 'r', encoding='utf-8')
data = json.load(file)
lyrics = [item['lyrics'] for item in data['songs'] if 'lyrics' in item]
cv = CountVectorizer(lowercase=True, binary=True)
cv.fit(lyrics)

with open('vocabulary.json', 'w', encoding='utf-8') as file:
    json.dump(cv.vocabulary_, file)
