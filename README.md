## A description of the app

The app aims to solve the problem of finding songs by their lyrics, and the database consists of 12 500 popular songs of which the lyrics can be queried.
Our app uses three different search engines: boolean search, tf-idf and neural search.
The boolean search returns the songs that match the words provided in the query, tf-idf does the same , but ranks the songs by their relevance and thus returns the songs that are the most relevant for the query, and neural search returns the songs that are the most semantically similar to the query. The songs that are returned can be filtered by artist, by adding artists to the form in the sidebar on the right. 
The page that shows the individual song's lyrics also has a graph that displays the computed emotions based on the song's lyrics. These emotion scores are in the database, so this would enable a straightforward way to search songs by their emotions. However this is not implemented in the current app.

## How to run the app locally

First clone the app with the command

```bash
git clone https://github.com/jus-schl/NLP-Search.git
```
and move to the root directory.

The app uses a PostgreSQL database, so in order to run the app locally you need to install PostgreSQL, create a database with your default user as the owner and create the needed tables to the database with the command 
```bash
psql < schema.sql.
```
Creating PostgreSQL users and databases can for example be done by following the instructions of the following YouTube video: https://www.youtube.com/watch?v=RySuQtMiBxQ

To create a virtual environment run
```bash
python3 -m venv venv
```

and activate the virtual environment with
```bash
source venv/bin/activate
```

then install the requirements with
```bash
pip install -r requirements.txt
```

The .env file should have the database address of the form DATABASE_URL=postgresql://user:password@localhost:port/databasename and a secret key of the form SECRET_KEY=yoursecretkey

user, password, port and databasename should be changed according to your local info, but the port is by default 5432.

After the tables are created, the songs can be added to the database by running the create_db.py file to add songs to the database and running database_emotions.py to add the song's emotions to the database. Because running database_emotions.py takes a lot of time, we have provided the contents of the table in the directory db_contents in csv format. Adding the emotion data to the database can then be done with the command
```bash
psql -U user -d databasename -c "\copy emotions FROM 'insertPathToEmotions.csv' WITH (FORMAT csv, HEADER true);"
```

Finally, the app can be run in the root directory with the command
```bash
flask run
```

