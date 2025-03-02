from app import app
from flask import render_template, request, redirect, session
import query
import songs
import urllib.parse

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        engine = session.get("engine", 3)
        return render_template('index.html', engine = engine)
    if request.method == "POST":
        user_input = request.form.get('query')
        engine = int(request.form.get('engine'))
        session['engine'] = engine
        if not user_input:
            return render_template('index.html', engine = engine)
        encoded_input = urllib.parse.quote(user_input)
        return redirect(f'/process/{encoded_input}')


@app.route('/process/<encoded_input>', methods=['GET', 'POST'])
def process(encoded_input):
    user_input = urllib.parse.unquote(encoded_input)
    if request.method == "GET":
        engine = session['engine']
        results = query.search_songs(user_input, engine)
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