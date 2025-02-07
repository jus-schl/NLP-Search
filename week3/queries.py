import neural_search
import boolean_search
import tf_idf_search
from nltk.stem import LancasterStemmer
ls = LancasterStemmer()
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# The file is opened with a path relative to week3
file = open('test_documents.txt', 'r', encoding='utf-8')
stemmed_documents = []
documents = []
stemmed_article = []
article = []

for line in file:
    line = line.split()
    if line[0] == "<article":
        continue
    if line[0] == "</article>":
        article_string = " ".join(word for word in article)
        stem_article_string = " ".join(stem for stem in stemmed_article)
        documents.append(article_string)
        stemmed_documents.append(stem_article_string)
        article = []
        stemmed_article = []
        continue
    for word in line:
        article.append(word)
        print(ls.stem(word))
        stemmed_article.append(ls.stem(word))

# Encoding the documents with the dataset of current size takes a long time
doc_embeddings = model.encode(documents) # doc_embeddings is assigned here so that it does not have to be ran every time neural search is used

#main loop
while True:
    try:
        selected_engine = int(input("Write 1 for boolean search, 2 for tf_idf and 3 for neural search: "))
    except:
        print("Invalid input")
        break

    if selected_engine == 1:
        input_query = input("Search for: ")
        if input_query == "":
            break
        if input_query[0] == '"' and input_query[-1] == '"':
            boolean_search.return_docs(input_query[1:len(input_query)-1], documents)
        else:
            input_query = input_query.split()
            input_query = " ".join(ls.stem(word) for word in input_query)
            boolean_search.return_docs(input_query, documents, stemmed_documents)

    if selected_engine == 2:
        input_query = input("Search for: ")
        if input_query == "":
            break
        if input_query[0] == '"' and input_query[-1] == '"':
            tf_idf_search.return_docs(input_query[1:len(input_query)-1], documents)
        else:
            input_query = input_query.split()
            input_query = " ".join(ls.stem(word) for word in input_query)
            tf_idf_search.return_docs(input_query, documents, stemmed_documents)

    elif selected_engine == 3:
        input_query = input("Search for: ")
        if input_query == "":
            break
        neural_search.return_docs(input_query, documents, doc_embeddings)

    else:
        print("Input 1, 2 or 3")

    