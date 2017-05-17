"""
Word based methods and functions
Author: Jonas McCallum
https://github.com/foobarmus/autocorrect
"""
from hybrid_check.utils import concat
from hybrid_check.nlp_parser import NLP_WORDS, NLP_BIGRAM_COUNTS

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

class Word(object):
    """container for word-based methods"""

    def __init__(self, word, typo_score=1):
        """
        Generate slices to assist with typo
        definitions.
        'the' => (('', 'the'), ('t', 'he'),
                  ('th', 'e'), ('the', ''))
        """
        word_ = word.lower()
        slice_range = range(len(word_) + 1)
        self.slices = tuple((word_[:i], word_[i:])
                            for i in slice_range)
        self.word = word
        self.typo_score = typo_score

    def _deletes(self):
        """th"""
        dict = {concat(a, b[1:]): bigram_score_2(a, b[1:])
               for a, b in self.slices[:-1]}
        return [Word(w, typo_score=(self.typo_score*dict[w]))
                for w in dict]

    def _transposes(self):
        """teh"""
        dict = {concat(a, (b[:2])[::-1], b[2:]): bigram_score_1((b[:2])[::-1])
                for a, b in self.slices[:-2]}
        return [Word(w, typo_score=(self.typo_score*dict[w]))
                for w in dict]

    def _replaces(self):
        """tge"""
        dict = {concat(a, c, b[1:]): bigram_score_2(c, b[1:])
                for a, b in self.slices[:-1]
                for c in ALPHABET}
        return [Word(w, typo_score=(self.typo_score*dict[w]))
                for w in dict]

    def _inserts(self):
        """thwe"""
        dict = {concat(a, c, b): bigram_score_2(c, b)
                for a, b in self.slices
                for c in ALPHABET}
        return [Word(w, typo_score=(self.typo_score*dict[w]))
                for w in dict]

    def typos(self):
        """letter combinations one typo away from word"""
        return (self._deletes() + self._transposes()
                + self._replaces() + self._inserts())

    def double_typos(self):
        """letter combinations two typos away from word"""
        typo1 = self.typos()
        typo2 = []
        for w in typo1:
            if w.typo_score > 10E-2:
                typo2.extend(w.typos())
        return typo2


def exact(words):
    """{'the', 'teh'} => {'the'}"""
    s = set([w.word for w in words])
    intersect = s & NLP_WORDS
    return [w for w in words if w.word in intersect]
  
def bigram_score_1(rev_b):
    """rev_b = 'ba' => NLP_BIGRAM_COUNTS['ba']"""
    return NLP_BIGRAM_COUNTS[rev_b]
  
def bigram_score_2(a, b):
    """(a, b) = ('fa', 'st') => NLP_BIGRAM_COUNTS['as']"""
    bi = ''
    if not a:
        if not b:
            bi = '  '
        else:
            bi = ' ' + b[0]
    else:
        if not b:
            bi = a[-1] + ' '
        else:
            bi = a[-1] + b[0]
    return NLP_BIGRAM_COUNTS[bi]