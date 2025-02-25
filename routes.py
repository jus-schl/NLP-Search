from app import app
from flask import render_template, request, redirect, session
import traceback
import query
import songs
import urllib.parse

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    try:
        if request.method == "POST":
            user_input = request.form.get('query')
            engine = int(request.form.get('engine'))
            session['engine'] = engine
            encoded_input = urllib.parse.quote(user_input)
            return redirect(f'/process/{encoded_input}')
    except Exception as e:
        print("Error in /:", e)
        print(traceback.format_exc())

@app.route('/process/<encoded_input>', methods=['GET', 'POST'])
def process(encoded_input):
    try:
        user_input = urllib.parse.unquote(encoded_input)
        if request.method == "GET":
            engine = session['engine']
            results = query.search_songs(user_input, engine)
            return render_template('index.html', results = results)
    except Exception as e:
        print("Error in /process:", e)
        print(traceback.format_exc())

@app.route('/songs/<song_id>', methods=['GET', 'POST'])
def song(song_id):
    results = songs.info(song_id)
    songs.create_graph(song_id, results[0])
    return render_template('song.html', results = results)