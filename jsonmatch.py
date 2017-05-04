"""General text mining functions for json files."""

import json
import re
import types
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


class Matcher:
    """This class implements various methods for matching text.
    
    Here I will explain more.
    
    """
    
    def __init__(self, input_type="filename", query=None, corpus=None,
                 tokenizer=word_tokenize, stemmer=PorterStemmer.stem,
                 stop_words=str(stopwords.words('english'))):
        """
        
        Some explanation
        
        """
        self.query_arr = None
        self.corpus_arr = None
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.stop_words = stop_words
        self.query_vocabulary = []
        self.corpus_vocabulary = []
        self.corpus_arr = []
        self.query_arr = self._extract_arr(input_type, query)
        self.corpus_arr = self._extract_arr(input_type, corpus)

    @staticmethod
    def _extract_arr(input_type, object):
        """Some explanation"""
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
        if not isinstance(json_object, types.ListType):
            json_object = list(json_object)
        print json_object
        return [[[json_object[i][k]]
                for k in json_object[i].keys()]
                for i in range(len(json_object))]
    
    @staticmethod
    def _remove_special_chars(str):
        """Accepts a single string."""
        return re.sub('[^\w\s]', ' ', str)

    @staticmethod
    def _to_lowercase(str):
        """Accepts a single string."""
        return str.lower()
    
    def _tokenize(self, str):
        """Accepts a single string."""
        return self.tokenizer(str)
    
    @staticmethod
    def _remove_duplicates(lst):
        """Accepts a list."""
        return list(set(lst))
        
    def _remove_stop_words(self, input):
        """Accepts a list."""
        return [word for word in input if word not in self.stop_words]
                    
    def _stem_tokens(self, input):
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
