from transformers import pipeline
classifier = pipeline("text-classification", model='bhadresh-savani/distilbert-base-uncased-emotion', top_k=None)

def return_scores(lyrics):
    # TODO strip newline characters before classifying the song.

    prediction = classifier(lyrics)
    emotions = []
    for dict in prediction[0]:
        emotions.append([dict['label'], dict['score']])

    # [ [love, score], [joy, score], [sadness, score], [anger, score], [surprise, score], [fear, score] ]
    return emotions


def create_graph(lyrics):
    # TODO this function should create the graph and call return_scores to get the values
    pass
