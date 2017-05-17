#Here is a complete example comparing some documents.
import logging, gensim
from collections import defaultdict
from pprint import pprint
from nltk.corpus import stopwords
from gensim import corpora, models, similarities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",              
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]
print "\nDocuments:"
pprint(documents)
raw_input("Press Enter to continue ... ")
print

print "Text pre-processing ... "
#Parse and remove stopwords
texts = [[word for word in doc.lower().split()
          if word not in set(stopwords.words('english'))]
          for doc in documents]
#Remove words that only appear once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
texts = [[token for token in text if frequency[token] > 1] for text in texts]
pprint(texts)
raw_input("Press Enter to continue ... ")
print

print "Creating dictionary and corpus ... "
dic = corpora.Dictionary(texts)
corpus = [dic.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('brown.mm', corpus)
for c in corpus:
    print c
raw_input("Press Enter to continue ... ")
print

print "Creating TF-IDF model ... "
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print doc
raw_input("Press Enter to continue ... ")
print

print "Creating LSI model ... "
lsi = models.LsiModel(corpus=corpus_tfidf, id2word=dic, num_topics=2)
corpus_lsi = lsi[corpus_tfidf]
for doc in corpus_lsi:
    print doc
raw_input("Press Enter to continue ... ")
print

print "Searching on query: \"human computer interaction\" ... "
query = "human computer interaction"
vec_bow = dic.doc2bow(query.lower().split())
vec_lsi = lsi[vec_bow]
print "Query-topic cosine similarity:\n", vec_lsi
index = similarities.MatrixSimilarity(lsi[corpus])
sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print "Search results (best to worst cosine similarity):"
for s in sims:
    print s, "#", documents[s[0]]