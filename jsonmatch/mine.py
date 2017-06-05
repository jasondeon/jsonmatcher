"""

jsonmatch.mine

Depends on external libraries:
scikit-learn

"""
from sklearn.feature_extraction.text import TfidfVectorizer
from jsonmatch.nlp import untokenize_object

def match(query, corpus, query_i=0, corpus_i=0):
    """Generates a list of all possible attribute pairings,
    with each sublist containing the following entries:
    [
        query.attribute_i key,
        corpus.attribute_k key,
        query.attribute_i length,
        corpus.attribute_k length,
        # of overlapping words (not including duplicates),
        cosine similarity compared to all objects in corpus
    ]
    Accepts a lists of json objects for 'query' and 'corpus'.
    'query_i', 'corpus_i' are the indices of the objects of interest
    for 'query' and 'corpus'.
    """
    matches = []
    for key_q, val_q in query[query_i].iteritems():
        for key_c, val_c in corpus[corpus_i].iteritems():
            entry = []
            entry.append(key_q)
            entry.append(key_c)
            entry.append(len(val_q))
            entry.append(len(val_c))
            entry.append(len([w for w in val_q if w in set(val_c)]))
            if len(val_q) != 0 and len(val_c) != 0:
                entry.append(cos_sim(val_q, corpus, corpus_i, key_c))
            else:
                entry.append(None)
            matches.append(entry)
    return matches
    
def cos_sim(query, corpus_tokens, corpus_i, corpus_key):
    """Determines the cosine similarity using two json-like objects.
    'query' is a list containing the words of the query.
    'corpus_tokens' is a list of json objects in the corpus.
    'corpus_i' is the index of the json object to be compared to.
    'corpus_key' is the key of the value of interest in the corpus.
    """
    corpus = untokenize_object(corpus_tokens)
    corpus_arr = corpus[corpus_i].values()
    vect = TfidfVectorizer(sublinear_tf=True, vocabulary=query)
    transformed = vect.fit_transform(corpus_arr)
    cos_matrix = (transformed * transformed.T).A
    cos_list = cos_matrix[len(cos_matrix) - 1]
    index = corpus[corpus_i].keys().index(corpus_key)
    return cos_list[index]
    
def k_means():
    """Performs k-means clustering on the corpus."""
    pass
    
def lsi_search(self, num_topics):
    """Extracts topics from the corpus and returns cosine
    similarities of the query against the corpus in the
    LSI space.
    """
    pass