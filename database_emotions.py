from app import app
import json
from db import db
from sqlalchemy.sql import text
import emotion_scores as es

# Adding the emotion scores for 12500 songs takes a bit under 2 hours
batch_size = 2000

with app.app_context():
    with open("./data/smaller_songs.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    sql = text("""INSERT INTO emotions (id, emotion1, emotion2, emotion3, emotion4, emotion5, emotion6)
                VALUES (:id, :emotion1, :emotion2, :emotion3, :emotion4, :emotion5, :emotion6)""")

    batch = []
    for i, song in enumerate(data.get("songs", []), start=1):
        id = song.get("id")
        lyrics = song.get("lyrics")
        emotions = es.return_emotions(lyrics)
        batch.append({
            "id": song.get("id"),
            "emotion1": emotions['sadness'],
            "emotion2": emotions['joy'],
            "emotion3": emotions['love'],
            "emotion4": emotions['anger'],
            "emotion5": emotions['fear'],
            "emotion6": emotions['surprise']
        })
        if i % batch_size == 0:
            db.session.execute(sql, batch)
            db.session.commit()
            batch.clear()
            print(i)
    if batch:
        db.session.execute(sql, batch)
        db.session.commit()