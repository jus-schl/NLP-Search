from app import app
from flask import render_template, request, redirect, session
import traceback
import query
import song_graph
import os

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    try:
        if request.method == "POST":
            user_input = request.form.get('query')
            engine = int(request.form.get('engine'))
            results = query.search_songs(user_input, engine)
            for key, song in results.items():
                song_graph.create_graph(key, song[1], song[4])
            return render_template('index.html', results = results)
    except Exception as e:
        print("Error in /:", e)
        print(traceback.format_exc())

@app.route('/process', methods=['GET', 'POST'])
def process():
    pass