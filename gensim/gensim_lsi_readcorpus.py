#In this example I use nltk to parse the brown corpus and store it in
#appropriate gensim formats for future use.
import logging, gensim
import string
from nltk.corpus import brown, stopwords
from gensim import corpora, models

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

print "\nNLTK pre-processing ... "
#Text preprocessing: obtain all tokens from all documents.
files = brown.fileids()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
final_text = []
for id in files:
    print id
    doc = []
    for w in brown.words(fileids=id):
        w = w.lower()
        w = w.translate(remove_punctuation_map)
        if w not in set(stopwords.words('english')) and w:
            doc.append(w)
    final_text.append(doc)

print "\nSaving documents ... "
#Store 2 files: .dict (a dictionary mapping) and .mm (corpus bag-of-words)
dic = corpora.dictionary.Dictionary(final_text)
dic.save('brown.dict')
corpus = [dic.doc2bow(text) for text in final_text]
corpora.MmCorpus.serialize('brown.mm', corpus)