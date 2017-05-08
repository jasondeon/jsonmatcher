"""

General text mining functions for json files.
Python 2.7+

"""

import json
import re
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from autocorrect import spell


class Matcher:
    """This class implements various methods for matching text.
    
    Here I will explain more.
    
    """
    
    def __init__(self,
                 input_type="filename",
                 query=None,
                 corpus=None,
                 tokenizer=word_tokenize,
                 stemmer=PorterStemmer().stem,
                 stop_words=set(stopwords.words('english'))):
        """
        
        Some explanation
        
        """
        self.query_json = self._load_json(input_type, query)
        self.corpus_json = self._load_json(input_type, corpus)
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.stop_words = stop_words
    
    def _load_json(self, input_type, object):
        """Loads json contents into a python list or dict.
        If it's a dict, inserts into a list, so it always
        returns a list.
        """
        json_object = None
        if input_type == "filename":
            with open(object) as file:
                json_object = json.load(file)
        elif input_type == "file":
            json_object = object
        else:
            #input_type must be "filename" or "file".
            sys.exit("Bad input type")
        #If not already a list, turn into a list.
        if not isinstance(json_object, list):
            lst = []
            lst.append(json_object.copy())
            return self.to_lowercase(lst)
        else:
            return self.to_lowercase(json_object)
        
    def get_query(self):
        """Returns the query json object."""
        return self.query_json
        
    def get_corpus(self):
        """Returns the corpus json object."""
        return self.corpus_json
    
    def separate_by_word(self, input):
        """Accepts a json object or list of json objects and
        creates a new list where the string values are tokenized.
        """
        if not input or input is None:
            return input
        #Single json object.
        elif isinstance(input, dict):
            return {key: self.tokenizer(val)
                for key, val in input.iteritems()}
        #List of json objects.
        elif isinstance(input, list):
            return [{key: self.tokenizer(val)
                    for key, val in input[i].iteritems()}
                    for i in range(len(input))]
        else:
            print ("Error: input must be a list or dict of lists. "
                   "Try tokenizing the strings.")
            
    def merge_words(self, input):
        """Accepts a json objet or list of json objects and
        creates a new list where tokens are merged into sentences.
        """
        if not input or input is None:
            return input
        #Single json object.
        if isinstance(input, dict):
            return {key: " ".join(val)
                    for key, val in input.iteritems()}
        #List of json objects.
        elif isinstance(input, list):
            return [{key: " ".join(val)
                    for key, val in input[i].iteritems()}
                    for i in range(len(input))]

    def separate_by_key(self, json_object):
        """Creates a dict merging words across all objects
        that are under the same key.
        
        Json object should be of the form:
        [ {key1:val1, key2:val2, ...}, {}, {}, ...]
        
        Output is a dict of the form:
        {key1:[val1, ...], key2:[val2, ...]}
        """
        result = {}
        for i in range(len(json_object)):
            for key in json_object[i].keys():
                if result.has_key(key):
                    result[key].extend(self.tokenizer(json_object[i][key]))
                else:
                    result[key] = [w for w in json_object[i][key].split()]
        return result
    
    def separate_by_object(self, json_object):
        """Creates a list merging all words in an object,
        ignoring keys.
        
        Json object should be of the form:
        [ {key1:val, key2:val2, ...}, {}, {}, ...]
        
        Output is of the form:
        [ [val1, val2, ...], [...], ...]
        """
        result = []
        for i in range(len(json_object)):
            temp = []
            for key in json_object[i].keys():
                temp.extend(self.tokenizer(json_object[i][key]))
            result.append(temp)
        return result
        
    def get_all_words(self, json_object):
        """Creates a list of all words across all objects and keys."""
        result = []
        #Make sure to check if already tokenized.
        for i in range(len(json_object)):
            for key in json_object[i].keys():
                if len(json_object[i][key]) > 1:
                    result.extend(json_object[i][key])
                else:
                    result.extend(self.tokenizer(json_object[i][key]))
        return result
    
    def remove_special_chars(self, input):
        """Accepts a single string, list, or dict. Iterables may
        be multidimensional. Returns structure as is.
        """
        if isinstance(input, basestring):
            return re.sub('[^\w\s]', ' ', input)
        elif isinstance(input, list):
            return [self.remove_special_chars(w) for w in input]
        elif isinstance(input, dict):
            return {key: self.remove_special_chars(val)
                    for key, val in input.iteritems()}
        else:
            print "Error: input must be a string, list, or dict."

    def to_lowercase(self, input):
        """Converts all strings to lowercase.
        Accepts a single string, list, or dict. Iterables may
        be multidimensional. Returns structure as is.
        """
        if isinstance(input, basestring):
            return input.lower()
        elif isinstance(input, list):
            return [self.to_lowercase(w) for w in input]
        elif isinstance(input, dict):
            return {key: self.to_lowercase(val)
                    for key, val in input.iteritems()}
        else:
            print "Error: input must be a string, list, or dict."
    
    def remove_duplicates(self, input):
        """Removes duplicate tokens from iterable structures.
        Accepts a list or dict of lists.
        """
        if not input or input is None:
            return input
        if isinstance(input, list):
            #List of iterables.
            if isinstance(input[0], (list, dict)):
                return [self.remove_duplicates(input[i])
                        for i in range(len(input))]
            #Simple list.
            else:
                return list(set(input))
        elif isinstance(input, dict):
            #Dict of lists.
            return {key: self.remove_duplicates(val)
                    for key, val in input.iteritems()}
        else:
            print ("Error: input must be a list or dict of lists. "
                   "Try tokenizing the strings.")
        
    def remove_stop_words(self, input):
        """Removes common words from iterable structures.
        Accepts a list or dict of lists.
        """
        if not input or input is None:
            return input
        if isinstance(input, list):
            #List of iterables.
            if isinstance(input[0], (list, dict)):
                return [self.remove_stop_words(input[i])
                        for i in range(len(input))]
            #Simple list.
            else:
                return [word for word in input
                        if word not in self.stop_words]
        elif isinstance(input, dict):
            #Dict of lists.
            return {key: self.remove_stop_words(val)
                    for key, val in input.iteritems()}
        else:
            print "Error: input must be a list or dict of lists."
                    
    def stem_tokens(self, input):
        """Converts all strings in an iterable structure
        to their stem form. Accepts a list or dict.
        """
        if not input or input is None:
            return input
        if isinstance(input, list):
            #List of iterables.
            if isinstance(input[0], (list, dict)):
                return [self.stem_tokens(input[i])
                        for i in range(len(input))]
            #Simple list.
            else:
                return [self.stemmer(w) for w in input]
        elif isinstance(input, dict):
            #Dict of lists.
            return {key: self.stem_tokens(val)
                    for key, val in input.iteritems()}
        else:
            print "Error: input must be a list or dict of lists."
            
    def correct_spelling(self, input):
        """Converts all strings in an iterable structure
        to their closest correct spelling using a
        spell-correcting model.
        """
        if not input or input is None:
            return input
        elif isinstance(input, list):
            #List of iterables.
            if isinstance(input[0], (list, dict)):
                return [self.correct_spelling(input[i])
                        for i in range(len(input))]
            #Simple list.
            else:
                return [spell(w) for w in input]
        elif isinstance(input, dict):
            #Dict of lists.
            return {key: self.correct_spelling(val)
                    for key, val in input.iteritems()}
        else:
            print "Error: input must be a list or dict of lists."

    def match(self, objectq=None, objectc=None,
              objectq_i=None, objectc_i=None):
        """Generates a list of all possible attribute pairings,
        with each sublist containing the following entries:
        [
            objectq.attribute_i key,
            objectc.attribute_k key,
            objectq.attribute_i length,
            objectc.attribute_k length,
            # of overlapping words (not including duplicates),
            cosine similarity compared to all objects in objectc
        ]
        Accepts single json objects or lists of json objects.
        By default, uses the query and corpus json objects
        belonging to the instance of the object.
        objectq_i, objectc_i are the indices of the objects of interest
        for objectq and objectc if they contain a list of json objects.
        """
        #If objects aren't supplied, use defaults.
        if objectq is None:
            objectq = self.separate_by_word(self.query_json)
        if objectc is None:
            objectc = self.separate_by_word(self.corpus_json)
        #Determine the matching results.
        matches = []
        for key_q, val_q in objectq[objectq_i].iteritems():
            for key_c, val_c in objectc[objectc_i].iteritems():
                entry = []
                entry.append(key_q)
                entry.append(key_c)
                entry.append(len(val_q))
                entry.append(len(val_c))
                entry.append(len([w for w in val_q if w in set(val_c)]))
                entry.append(self.cos_sim(val_q, objectc,
                                          objectc_i, key_c))
                matches.append(entry)
        return matches
        
    def cos_sim(self, query, corpus_tokens,
                corpus_i, corpus_key):
        """Determines the cosine similarity using two json objects.
        query is a list containing the words of the query.
        corpus_tokens is a list of json objects in the corpus.
        corpus_i is the index of the json object to be compared to.
        corpus_key is the key of the value of interest in the corpus.
        """
        corpus = self.merge_words(corpus_tokens)
        corpus_arr = corpus[corpus_i].values()
        vect = TfidfVectorizer(sublinear_tf=True, vocabulary=query)
        transformed = vect.fit_transform(corpus_arr)
        cos_matrix = (transformed * transformed.T).A
        cos_list = cos_matrix[len(cos_matrix) - 1]
        index = corpus[corpus_i].keys().index(corpus_key)
        return cos_list[index]
        