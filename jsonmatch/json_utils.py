"""

jsonmatch.json_utils

"""
from collections import defaultdict

def get_words_by_key(input):
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
    result = defaultdict(list)
    for j_obj in input:
        for key in j_obj.keys():
            result[key].extend(j_obj[key])
    return result

def merge_by_key(input):
    """Given a list of json objects, creates a dict merging
    values under the same key into a list.
    
    'input' should be of the form:
    [ {key1:"val1", key2:...}, {key1:"val2", ...}, ... ]
    
    Return value is a dict of the form:
    {key1:["val1", "val2", ...], key2:[...], ...}
    """
    result = defaultdict(list)
    for j_obj in input:
        for key in j_obj.keys():
            result[key].append(j_obj[key])
    return result
    
def get_words_by_object(input):
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