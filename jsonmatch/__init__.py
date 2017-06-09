"""

General text mining functions for json files.
Python 2.7+

"""

import json
from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from autocorrect import spell

from .dbase import *
from .json_utils import *
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