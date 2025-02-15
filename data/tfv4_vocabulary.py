from sklearn.feature_extraction.text import TfidfVectorizer
import json

file = open('smaller_songs.json', 'r', encoding='utf-8')
data = json.load(file)
lyrics = [item['lyrics'] for item in data['songs'] if 'lyrics' in item]

tfv4 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
sparse_td_matrix = tfv4.fit_transform(lyrics).T.tocsr()
t2i = tfv4.vocabulary_

with open('tfv4_vocabulary.json', 'w', encoding='utf-8') as file:
    json.dump(t2i, file)