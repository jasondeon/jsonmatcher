"""

General text mining functions for json files.
Python 2.7+

"""

import json
import re
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


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
        self.query_vocabulary = []
        self.corpus_vocabulary = []
    
    @staticmethod
    def _load_json(input_type, object):
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
            json_object = list(json_object)
        return json_object
        
    def separate_by_word(self, json_object):
        """Creates a new dict from the json object, splitting
        the strings into words.
        """
        result = json_object
        for i in range(len(json_object)):
            for key in json_object[i].keys():
                result[i][key] = self.tokenizer(result[i][key])
        return result
    
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
        """Removes duplicates from iterable structures.
        Accepts a list or dict of lists.
        """
        if isinstance(input, list) and input:
            if isinstance(input[0], list):
                return [self.remove_duplicates(input[i])
                        for i in range(len(input))]
            else:
                return list(set(input))
        elif isinstance(input, dict):
            return {key: self.remove_duplicates(val)
                    for key, val in input.iteritems()}
        else:
            print "Error: input must be a list or dict of lists."
        
    def remove_stop_words(self, input):
        """Removes common words from iterable structures.
        Accepts a list or dict of lists.
        """
        if isinstance(input, list) and input:
            if isinstance(input[0], list):
                return [self.remove_stop_words(input[i])
                        for i in range(len(input))]
            else:
                return [word for word in input
                        if word not in self.stop_words]
        elif isinstance(input, dict):
            return {key: self.remove_stop_words(val)
                    for key, val in input.iteritems()}
        else:
            print "Error: input must be a list or dict of lists."
                    
    def stem_tokens(self, input):
        """Converts all strings in an interable structure
        to their stem form. Accepts a list or dict of lists.
        """
        if isinstance(input, list) and input:
            if isinstance(input[0], list):
                return [self.stem_tokens(input[i])
                        for i in range(len(input))]
            else:
                return [self.stemmer(w) for w in input]
        elif isinstance(input, dict):
            return {key: self.stem_tokens(val)
                    for key, val in input.iteritems()}
        else:
            print "Error: input must be a list or dict of lists."

    def match(self, n, m):
        """Generates a list of attribute pairings, with each
        sublist containing the following entries:
        [
            obj1.attribute_i,
            obj2.attribute_k,
            obj1.attribute_i.len,
            ob2.attribute_k.len,
            # of overlapping words,
            cosine similarity
        ]
        Uses the query and corpus lists contained in the instance.
        n refers to the index of the query object of interest.
        m refers to the index of the corpus object of interest.
        The objects are expected to be simple key:value pair dicts.
        """
        matches = []
        query_tokens = self.separate_by_word(self.query_json)
        corpus_tokens = self.separate_by_word(self.corpus_json)
        for key_q, val_q in self.query_json[n]:
            for key_c, val_c in self.corpus_json[m]:
                entry = []
                entry.append(key_q)
                entry.append(key_c)
                entry.append(len(val_q))
                entry.append(len(val_c))
                ###TODO: # of matches, cosine similarity
            
    def word_count_all(self, key):
        """Returns a dictionary containing word counts for
        all in every object and under every key.
        """
        
        
#c_vect = CountVectorizer(vocabulary=query_vocabulary[3])
#print c_vect.fit_transform(corpus_arr[1]).toarray()

###TfIdf for description key
###vocabulary=the text that you want to analyze e.g. a query
#vect = TfidfVectorizer(sublinear_tf=True, vocabulary=query_vocabulary[3], stop_words=stopwords.words('english'))
#transformed = vect.fit_transform(corpus_arr[1])
#print dict(zip(vect.get_feature_names(), vect.idf_))
#print (transformed * transformed.T).A