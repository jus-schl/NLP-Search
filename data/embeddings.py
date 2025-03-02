import numpy
import json
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# This file can be used to create the embeddings that are used by the neural search engine.

file = open('smaller_songs.json', 'r', encoding='utf-8')
data = json.load(file)
lyrics = [item['lyrics'].replace("\n", " ") for item in data['songs'] if 'lyrics' in item]

doc_embeddings = model.encode(lyrics)

numpy.save("embeddings.npy", doc_embeddings)