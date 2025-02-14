from app import app
from flask import render_template, request, redirect, session
import query

@app.route('/', methods=['GET'])
def index():
    results = session.pop('results', None)
    return render_template('index.html', results = results)

@app.route('/process', methods=['GET', 'POST'])
def process():
    try:
        if request.method == "POST":
            user_input = request.form.get('query')
            engine = int(request.form.get('engine'))
            results = query.search_songs(user_input, engine)
            session['results'] = results
            return redirect('/')
    except:
        print(Exception)
