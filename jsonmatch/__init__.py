"""

General text mining functions for json files.
Python 2.7+

Depends on external libraries:
nltk
autocorrect

"""

import json
from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from autocorrect import spell

from .dbase import *
from .mine import *
from .nlp import *


class Matcher:
    """This is a struct-like class which stores several
    text mining related variables.
    """
    
    def __init__(self,
                 input_type="object",
                 query=None,
                 corpus=None,
                 tokenizer=word_tokenize,
                 speller=spell,
                 stemmer=PorterStemmer().stem,
                 stop_words=set(stopwords.words('english'))):
        """
        
        Creates a Matcher instance used to store several variables
        for text mining. The query and corpus should be provided
        in a json-like format (currently a dictionary or a list 
        of dictionaries).
        
        input_type: a string containing "filename" to indicate
            the query/corpus are names of files or "object" to
            indicate query/corpus are json-like objects.
            
        query: an object containing the search terms to use.
        
        corpus: an object containing the searchable documents.
        
        tokenizer: a handle for a function that will parse strings
            into words.
        
        stemmer: a handle for a function that will stem words.
        
        stop_words: a collection of stopwords for text mining.
        
        """
        self.query_json = self._load_json(input_type, query)
        self.corpus_json = self._load_json(input_type, corpus)
        self.tokenizer = tokenizer
        self.speller = speller
        self.stemmer = stemmer
        self.stop_words = stop_words
    
    @staticmethod
    def _load_json(input_type, object):
        """A helper method for the constructor.
        Given the 'input_type' either reads a json object from
        a file or simply returns a direct json_object.
        
        If the object given is not a list, it will be inserted into
        a list of length 1 so the function always returns a list.
        
        When 'input_type' is invalid, the function will print
        a warning and return an empty list.
        """
        return_object = None
        if input_type == "filename":
            with open(object) as file:
                return_object = json.load(file)
        elif input_type == "object":
            return_object = object
        else:
            print "Error: input_type contains invalid value {}.".format(
                input_type)
            return []
        #If object is not a list, turn into a list.
        if not isinstance(return_object, list):
            return [return_object.copy()]
        else:
            return return_object

def merge_by_key(input):
    """Given a list of json objects, creates a dict merging
    words across all objects that are under the same key.
    
    This should only be called AFTER tokenizing the strings,
    since it looks for values that are lists or tuples and
    will ignore complete, untokenized strings.
    
    'input' should be of the form:
    [ {key1:[w1, w2], key2:[...], ...}, {key1:[w3, w4], ...}, ... ]
    
    Return value is a dict of the form:
    {key1:[w1, w2, w3, w4], key2:[...], ...}
    """
    result = {}
    for j_obj in input:
        for key in j_obj.keys():
            if result.has_key(key):
                result[key].extend(j_obj[key])
            else:
                result[key] = j_obj[key]
    return result
    
def merge_by_object(input):
    """Given a list of json objects, creates a list merging
    all words in an object, ignoring keys.
    
    This should only be called AFTER tokenizing the strings,
    since it looks for values that are lists or tuples and
    will ignore complete, untokenized strings.
    
    'input' should be of the form:
    [ {key1:[w1, w2], key2:[w3, w4], ...}, {...}, ... ]
    
    Return value is of the form:
    [ [w1, w2, w3, w4, ...], [...], ...]
    """
    result = []
    for j_obj in input:
        temp = []
        for key in j_obj.keys():
            temp.extend(j_obj[key])
        result.append(temp)
    return result
    
def get_all_words(input):
    """Given a list of json objects, creates a list of all
    words across all objects and keys.
    
    This should only be called AFTER tokenizing the strings,
    since it looks for values that are lists or tuples and
    will ignore complete, untokenized strings.
    
    'input' should be of the form:
    [ {key1:[w1, w2], key2:[w3, w4], ...}, {key1:[w5, w6], ...} ... ]

    Return value is a list of the form:
    [w1, w2, w3, w4, w5, w6, ... ]
    """
    result = []
    for j_obj in input:
        for key in j_obj.keys():
            result.extend(j_obj[key])
    return result