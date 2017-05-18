print "\nImporting libraries ... "

import logging
from jsonmatch import Matcher
from collections import defaultdict
from gensim import corpora, models, similarities
from sklearn.cluster import KMeans
import numpy as np

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
dims = 5 #The number of topics and the dimension of the LSI space
matcher = Matcher(query="test_query.json",
                  corpus="output.json")

print "\nText pre-processing ... "
# Query - tokenize, remove stopwords, remove duplicates
query_tokens = matcher.separate_by_word(matcher.query_json)
query_tokens = matcher.remove_stop_words(query_tokens)
query_tokens = matcher.remove_duplicates(query_tokens)
# Corpus - tokenize, remove stopwords
corpus_tokens = matcher.separate_by_word(matcher.corpus_json)
corpus_tokens = matcher.remove_stop_words(corpus_tokens)
# Exract descriptions
des_tokens = []
for dict in corpus_tokens:
    des_tokens.append(dict["DESCRIPTION"])
# Remove words that only appear once
frequency = defaultdict(int)
for text in des_tokens:
    for token in text:
        frequency[token] += 1
des_tokens = [[token for token in text if frequency[token] > 1] for text in des_tokens]

print "\nCreating dictionary and corpus ... "
dic = corpora.Dictionary(des_tokens)
corpus = [dic.doc2bow(text) for text in des_tokens]

print "\nCreating TF-IDF model ... "
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

print "\nCreating LSI model ... "
lsi = models.LsiModel(corpus=corpus_tfidf, id2word=dic, num_topics=dims)
corpus_lsi = lsi[corpus_tfidf]

print "\nK-means clustering ... "
X = np.array([[i[1] for i in t] for t in corpus_lsi])
kmeans = KMeans(n_clusters=dims, random_state=0).fit(X)
for i in range(len(kmeans.labels_)):
    print kmeans.labels_[i], "#", matcher.corpus_json[i]["INDICATOR"]
raw_input("Press Enter to continue ... ")

query = matcher.get_query()[0]["query"]
print "\nSearching on query: \"" + query + "\" ... "
vec_bow = dic.doc2bow(query_tokens[0]["query"])
vec_lsi = lsi[vec_bow]
print "\nQuery-topic cosine similarity:\n", vec_lsi
index = similarities.MatrixSimilarity(lsi[corpus])
sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print "\nSearch results (best to worst cosine similarity):"
for s in sims:
    print s, "#", matcher.corpus_json[s[0]]["INDICATOR"]
raw_input("Press Enter to continue ... ")
print