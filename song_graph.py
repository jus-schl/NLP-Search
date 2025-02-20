from transformers import pipeline
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
classifier = pipeline("text-classification", model='bhadresh-savani/distilbert-base-uncased-emotion', top_k=None)

stopwords = ["yo", "uh", "yuh", "yeah", "the", "chorus", "a", "but"]

def return_scores(lyrics):
    lyrics = lyrics.strip()
    lyric_list = lyrics.split()
    lyric_list = [lyrics for lyrics in lyric_list if lyrics not in stopwords]
    if len(lyric_list) > 300:
        lyrics = " ".join(lyric_list[0:299]) # The model has a limit for token size
    prediction = classifier(lyrics)          # Cutting a part of the lyrics probably does not affect the results much.
    emotions = []
    for dict in prediction[0]:
        emotions.append([dict['label'], dict['score']])

    # [ [love, score], [joy, score], [sadness, score], [anger, score], [surprise, score], [fear, score] ]
    return emotions


def create_graph(id, song_name, lyrics):
    emotions = return_scores(lyrics)
    fig = plt.figure(facecolor='none')
    ax = plt.gca()
    ax.set_facecolor('darkgray')
    plt.title(f"Emotions in the song {song_name}")
    plt.bar(range(len(emotions)), [score for [emotion, score] in emotions], align='center', color="#00051d")
    plt.xticks(range(len(emotions)), [emotion for [emotion, score] in emotions])
    plt.gcf().subplots_adjust(bottom=0.30)
    plt.savefig(f'static/{id}.png')
