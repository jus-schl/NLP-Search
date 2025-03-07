from app import app
from flask import render_template, request, redirect, session, jsonify
import query
import songs
import urllib.parse
import json

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        engine = session.get("engine", 3) # Neural search is the default engine
        return render_template('index.html', engine = engine)
    if request.method == "POST":
        user_input = request.form.get('query')
        engine = int(request.form.get('engine'))
        artists = request.form.get('artists', '[]') # Get artists to filter results
        artists = json.loads(artists)
        print(artists)
        session['engine'] = engine
        session['artists'] = artists
        if not user_input:
            return render_template('index.html', engine = engine)
        encoded_input = urllib.parse.quote(user_input)
        return redirect(f'/process/{encoded_input}')
    return render_template("index.html")


@app.route('/process/<encoded_input>', methods=['GET', 'POST'])
def process(encoded_input):
    user_input = urllib.parse.unquote(encoded_input)
    if request.method == "GET":
        engine = session['engine']
        artists = session.get('artists', [])
        results = query.search_songs(user_input, engine, artists)
        if results:
            return render_template('index.html', results = results, engine = engine)
        else:
            suggestion = query.search_word(user_input)
            error_message = f"No results found for query '{user_input}'"
            return render_template('index.html', error_message = error_message, engine = engine, suggestion = suggestion)

@app.route('/songs/<song_id>', methods=['GET', 'POST'])
def song(song_id):
    results = songs.info(song_id)
    songs.create_graph(song_id, results[0])
    return render_template('song.html', results = results)

@app.route('/add_artists', methods=["POST"])
def add_artists():
    artist = request.json.get("artists")
    if "artists" not in session:
        session["artists"] = []
    session["artists"].append(artist)
    return jsonify({"success": True, "artists": session["artists"]})

@app.route('/get_artists')
def get_artists():
    return jsonify(session.get("artists", []))

@app.route('/delete_artist/<artist>', methods=["POST"])
def delete_artists(artist):
    print(session["artists"])
    if "artists" in session:
        session["artists"] = [f for f in session["artists"] if f != artist]
    print(artist)
    print(artist in session["artists"])
    return jsonify({"success": True})
