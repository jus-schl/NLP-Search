import neural_search
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# The file is opened with a path relative to week3
file = open('../week2/documents.txt', 'r', encoding='utf-8')
documents = []
article = []

for line in file:
    line = line.split()
    if line[0] == "<article":
        continue
    if line[0] == "</article>":
        article_string = " ".join(word for word in article)
        documents.append(article_string)
        article = []
        continue
    for word in line:
        article.append(word)


search_engine = neural_search # The value of search_engine should be changed depending on the chosen engine

# Encoding the documents with the dataset of current size takes a long time
doc_embeddings = model.encode(documents) # doc_embeddings is assigned here so that it does not have to be ran every time neural search is used

#main loop
while True:
    selected_engine = int(input("Write 1 for boolean search, 2 for tf_idf and 3 for neural search: "))

    if selected_engine == 3:
        input_query = input("Search for: ") #user input
        #loop exit
        if input_query == "":
            break
        search_engine.return_docs(input_query, documents, doc_embeddings)
    else:
        print("This engine is not yet implemented")

    