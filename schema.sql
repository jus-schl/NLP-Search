CREATE TABLE songs (
    id INTEGER PRIMARY KEY,
    artist TEXT,
    title TEXT,
    tag TEXT,
    year INTEGER,
    lyrics TEXT
);

CREATE TABLE emotions (
    id INTEGER PRIMARY KEY REFERENCES songs(id),
    emotion1 FLOAT,
    emotion2 FLOAT,
    emotion3 FLOAT,
    emotion4 FLOAT,
    emotion5 FLOAT,
    emotion6 FLOAT
);