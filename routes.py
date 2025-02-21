from app import app
from flask import render_template, request, redirect, session
import traceback
import query
import song_graph
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
            for key, song in results.items():
                song_graph.create_graph(key, song[1], song[5])
            return render_template('index.html', results = results)
    except Exception as e:
        print("Error in /process:", e)
        print(traceback.format_exc())

@app.route('/songs/<song_name>', methods=['GET', 'POST'])
def song(song_name):
    pass