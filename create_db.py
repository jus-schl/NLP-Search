from app import app
import json
from db import db
from sqlalchemy.sql import text

with app.app_context():
    with open("./data/smaller_songs.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    sql = text("""INSERT INTO songs (id, artist, title, tag, year, lyrics)
                VALUES (:id, :artist, :title, :tag, :year, :lyrics)""")

    batch = []
    for song in data.get("songs", []):
        batch.append({
            "id": song.get("id"),
            "artist": song.get("artist", "Unknown"),
            "title": song.get("title", "Unknown"),
            "tag": song.get("tag", ""),
            "year": song.get("year", None),
            "lyrics": song.get("lyrics", "")
        })

    db.session.execute(sql, batch)
    db.session.commit()