"""

jsonmatch.nlp

"""
import re
import autocomplete

def tokenize_object(input, tokenizer):
    """Accepts a list of json objects and returns a new list
    where the string values are tokenized.
    'tokenizer' is the handle for the function used for tokenizing.
    """
    if not input or input is None:
        return input
    elif isinstance(input, list):
        return [{key: (tokenizer(val)
                if isinstance(val, basestring)
                else val)
                for key, val in input[i].iteritems()}
                for i in range(len(input))]
    else:
        print ("Error: input must be a list. "
            "Actual type: {}".format(type(input)))
            
def untokenize_object(input):
    """Accepts a list of json objects and returns a new list
    where the list/tuple values are joined with spaces to form
    strings.
    """
    if not input or input is None:
        return input
    elif isinstance(input, list):
        return [{key: (" ".join(val)
                if isinstance(val, (list, tuple))
                else val)
                for key, val in input[i].iteritems()}
                for i in range(len(input))]
    else:
        print ("Error: input must be a list. "
            "Actual type: {}".format(type(input)))

def remove_special_chars(input):
    """Accepts a single string, list, or dict.
    Iterables may be multidimensional. Returns the structure
    where all strings have had punctuation removed.
    """
    if isinstance(input, basestring):
        return re.sub('[^\w\s]', ' ', input)
    elif isinstance(input, list):
        return [remove_special_chars(w) for w in input]
    elif isinstance(input, dict):
        return {key: remove_special_chars(val)
                for key, val in input.iteritems()}
    else:
        print ("Error: input must be a string, list, or dict. "
            "Actual type: {}".format(type(input)))
            

def to_lowercase(input):
    """Accepts a single string, list, or dict.
    Iterables may be multidimensional. Returns the structure
    where all strings are converted to lowercase.
    """
    if isinstance(input, basestring):
        return input.lower()
    elif isinstance(input, list):
        return [to_lowercase(w) for w in input]
    elif isinstance(input, dict):
        return {key: to_lowercase(val)
                for key, val in input.iteritems()}
    else:
        print ("Error: input must be a string, list, or dict. "
            "Actual type: {}".format(type(input)))
            
def remove_duplicates(input):
    """Removes duplicate tokens from iterable structures.
    Accepts a simple list or a list/dict of lists. 
    """
    if not input or input is None:
        return input
    if isinstance(input, list):
        #List of lists.
        if isinstance(input[0], (list, dict)):
            return [remove_duplicates(input[i])
                    for i in range(len(input))]
        #Simple list.
        else:
            return list(set(input))
    elif isinstance(input, dict):
        #Dict of lists.
        return {key: remove_duplicates(val)
                for key, val in input.iteritems()}
    else:
        print ("Error: input must be a simple list or a "
            "list/dict of lists.")
        
def remove_stop_words(input, stop_words):
    """Removes specific words from iterable structures.
    Accepts a simple list or a list/dict of lists.
    'stop_words' contains the blacklisted words.
    
    This should only be called AFTER tokenizing the strings,
    since it looks for values that are lists or tuples and
    will ignore complete, untokenized strings.
    """
    if not input or input is None:
        return input
    if isinstance(input, list):
        #List of lists.
        if isinstance(input[0], (list, dict)):
            return [remove_stop_words(input[i], stop_words)
                    for i in range(len(input))]
        #Simple list.
        else:
            return [word for word in input
                    if word not in stop_words]
    elif isinstance(input, dict):
        #Dict of lists.
        return {key: remove_stop_words(val, stop_words)
                for key, val in input.iteritems()}
    else:
        print ("Error: input must be a simple list or a "
            "list/dict of lists.")
            
def correct_spelling(input, speller):
    """Converts a string or all strings in an iterable
    structure to their closest correct spelling using a
    spell-correcting model.
    Accepts a simple list or a list/dict of lists.
    'speller' is a handle for the spell-correcting model function.
    """
    if not input or input is None:
        return input
    elif isinstance(input, list):
        #List of lists.
        if isinstance(input[0], (list, dict)):
            return [correct_spelling(input[i], speller)
                    for i in range(len(input))]
        #Simple list.
        else:
            return [speller(w) for w in input]
    elif isinstance(input, dict):
        #Dict of lists.
        return {key: correct_spelling(val, speller)
                for key, val in input.iteritems()}
    elif isinstance (input, basestring):
        return speller(input)
    else:
        print ("Error: input must be a simple list or a "
            "list/dict of lists.")
            
def suggest_word(previous, current):
    """Given the previous word and the current partially typed
    word, suggest some possibilities for the word being typed.
    Returns a list of tuples containing the suggested word and
    the number of times it showed up as a followup in the training
    corpus.
    """
    if not suggest_word.is_loaded: #Don't train more than once
        autocomplete.load()
        suggest_word.is_loaded = True
    return autocomplete.predict(previous, current)
            
def stem_tokens(input, stemmer):
    """Converts all strings in an iterable structure
    to their stem form.
    Accepts a simple list or a list/dict of lists.
    'stemmer' is a handle for a function that stems words.
    """
    if not input or input is None:
        return input
    if isinstance(input, list):
        #List of lists.
        if isinstance(input[0], (list, dict)):
            return [stem_tokens(input[i], stemmer)
                    for i in range(len(input))]
        #Simple list.
        else:
            return [stemmer(w) for w in input]
    elif isinstance(input, dict):
        #Dict of lists.
        return {key: stem_tokens(val, stemmer)
                for key, val in input.iteritems()}
    else:
        print ("Error: input must be a simple list or a "
            "list/dict of lists.")
            
suggest_word.is_loaded = False