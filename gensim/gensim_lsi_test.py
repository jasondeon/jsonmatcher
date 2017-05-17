#Load pre-trained lsi model
import logging, gensim
from gensim import models

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

print "\Loading LSI model ... "
#Load pre-trained model.
lsi = models.LsiModel.load('brown_lsi')
lsi.print_topics(num_topics=20)