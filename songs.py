import matplotlib.pyplot as plt
import matplotlib
from db import db
from sqlalchemy.sql import text
matplotlib.use('Agg')

def info(song_id):
    sql = text("SELECT title, artist, lyrics FROM songs WHERE id=:id")
    result = db.session.execute(sql, {"id":song_id})
    return result.fetchone()


def create_graph(song_id, song_name):
    sql = text("SELECT * FROM emotions WHERE id=:id")
    result = db.session.execute(sql, {"id":song_id})
    emotions = result.fetchone()
    emotions = [["sadness", emotions[1]], ["joy", emotions[2]], ["love", emotions[3]], ["anger", emotions[4]], ["fear", emotions[5]], ["surprise", emotions[6]]]
    fig = plt.figure(facecolor='none')
    ax = plt.gca()
    ax.set_facecolor('darkgray')
    plt.title(f"Emotions in the song {song_name}", color='white')
    plt.bar(range(len(emotions)), [score for [emotion, score] in emotions], align='center', color="#00051d")
    plt.xticks(range(len(emotions)), [emotion for [emotion, score] in emotions], color='white')
    plt.yticks(color='white')
    plt.gcf().subplots_adjust(bottom=0.30)
    plt.savefig(f'static/emotions.png')
