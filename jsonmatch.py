"""

General text mining functions for json files.
Python 2.x

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
    
    def __init__(self, input_type="filename", query=None, corpus=None,
                 tokenizer=word_tokenize, stemmer=PorterStemmer.stem,
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
        If it's a dict, insert into a list. Always returns a list.
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
    
    @staticmethod
    def remove_special_chars(str):
        """Accepts a single string."""
        return re.sub('[^\w\s]', ' ', str)

    def to_lowercase(self, input):
        """Accepts a single string, list, or dict. Iterables may
        be multidimensional. Returns structure as is.
        """
        if isinstance(input, basestring):
            return input.lower()
        elif isinstance(input, list):
            return [self.to_lowercase(x) for x in input]
        elif isinstance(input, dict):
            return {key: self.to_lowercase(val)
                    for key, val in input.iteritems()}
        else:
            print "Error: input must be a string, list, or dict."
    
    def remove_duplicates(self, input):
        """Accepts a list or dict of lists."""
        if isinstance(input, list):
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
        """Accepts a list or dict of lists."""
        if isinstance(input, list):
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
        """Accepts a list."""
        return [self.stemmer(item) for item in input]
        
    def _filter_text(self, text):
        """Some explanation"""
        text = self._remove_special_chars(text)
        text = self._to_lowercase(text)
        text_arr = self._tokenize(text)
        text_arr = self._remove_duplicates(text_arr)
        text_arr = self._remove_stop_words(text_arr)
        text_arr = self._stem_tokens(text_arr)
        return text_arr

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