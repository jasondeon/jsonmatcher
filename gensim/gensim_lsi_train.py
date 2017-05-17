#Load dictionary and train
import logging, gensim
from gensim import corpora, models

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

print "\nReading files ... "
#Load the dictionary and mapping from the disk.
dictionary = corpora.Dictionary()
dic = dictionary.load('brown.dict')
mm = corpora.MmCorpus('brown.mm')

print "\nTraining LSI model ... "
#Train LSI model and save for future use.
lsi = models.lsimodel.LsiModel(corpus=mm, id2word=dic, num_topics=200)
lsi.save('brown_lsi')