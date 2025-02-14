from search_engines import neural_search
from search_engines import boolean_search
from search_engines import tf_idf_search
from nltk.stem import LancasterStemmer
ls = LancasterStemmer()
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

file = open('./data/test_documents.txt', 'r', encoding='utf-8')
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
        print(stem_article_string)
        stemmed_documents.append(stem_article_string)
        article = []
        stemmed_article = []
        continue
    for word in line:
        article.append(word)
        if word[-1] in ["?", ".", ",", "!", ":", ";", "/"]: #punctuation messes up the stemming so it needs to be accounted for
            punct = word[-1]
            word = word[:len(word)-1]
            stemmed_word = ls.stem(word)
            stemmed_article.append(stemmed_word+punct)
            continue
        stemmed_article.append(ls.stem(word))

# Encoding the documents with the dataset of current size takes a long time
doc_embeddings = model.encode(documents) # doc_embeddings is assigned here so that it does not have to be ran every time neural search is used


def search_songs(query, selected_engine):
    if query == "":
        return None
    
    if selected_engine == 1:
        if query[0] == '"' and query[-1] == '"':
            return boolean_search.return_docs(query[1:len(query)-1], documents)
        else:
            print(ls.stem(query))
            query = " ".join(ls.stem(word) for word in query.split())
            return boolean_search.return_docs(query, documents, stemmed_documents)
        
    elif selected_engine == 2:
        if query[0] == '"' and query[-1] == '"':
            return tf_idf_search.return_docs(query[1:len(query)-1], documents)
        else:
            print(ls.stem(query))
            query = " ".join(ls.stem(word) for word in query.split())
            return tf_idf_search.return_docs(query, documents, stemmed_documents)

    elif selected_engine == 3:
        return neural_search.return_docs(query, documents, doc_embeddings)