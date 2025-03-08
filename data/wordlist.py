import json

file = open('smaller_songs.json', 'r', encoding='utf-8')
data = json.load(file)

lyrics = [item['lyrics'].replace("\n", " ") for item in data['songs'] if 'lyrics' in item]
words = set()
for lyric in lyrics:
    words.update(word.lower() for word in lyric.split())
words = list(words)

with open("word_list.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(words))