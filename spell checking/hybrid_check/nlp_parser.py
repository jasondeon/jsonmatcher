"""
NLP parser
Author: Jonas McCallum
https://github.com/foobarmus/autocorrect
"""
from hybrid_check.utils import zero_default_dict
from hybrid_check.utils import bigram_word
from nltk.corpus import brown
import re

def filter(s):
    """takes a string and converts to lowercase and removes
    punctuation and special characters
    """
    return re.sub('[^a-zA-Z]', '', s).lower()

def parse(filename):
    """tally word popularity using novel extracts, etc"""
    words = []
    bigrams = []
    
    with open(filename, "r") as file:
        for line in file:
            line_words = [filter(w) for w in line.split()]
            words.extend(line_words)
            for w in line_words:
                bigrams.extend(bigram_word(w))
                
    with open("english.txt", "r") as file:
        for line in file:
            line_words = [filter(w) for w in line.split()]
            words.extend(line_words)
            for w in line_words:
                bigrams.extend(bigram_word(w))
    
    for w in brown.words():
        words.append(w.lower())
        bigrams.extend(bigram_word(w))
    
    #Count words and bigrams.
    word_counts = zero_default_dict()
    bi_counts = zero_default_dict()
    for word in words:
        word_counts[word] += 1
    for bi in bigrams:
        bi_counts[bi] += 1
    #Normalize.
    for word in word_counts:
        word_counts[word] = word_counts[word] / float(len(words))
    for bi in bi_counts:
        bi_counts[bi] = bi_counts[bi] / float(len(bigrams))
    return set(words), word_counts, set(bigrams), bi_counts

NLP_WORDS, NLP_WORD_COUNTS, NLP_BIGRAMS, NLP_BIGRAM_COUNTS = parse('big.txt')