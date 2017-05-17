"""
Spell function
Author: Jonas McCallum
https://github.com/foobarmus/autocorrect
"""
from hybrid_check.nlp_parser import NLP_WORD_COUNTS
from hybrid_check.word import Word, exact
from hybrid_check.utils import add_words

def spell(word):
    """most likely correction for everything up to a double typo"""
    w = Word(word.lower())
    candidates = []
    candidates = add_words(candidates, exact([w]))
    candidates = add_words(candidates, exact(w.typos()))
    candidates = add_words(candidates, exact(w.double_typos()))
    candidates = add_words(candidates, [Word(word, typo_score=0)])
    can_dict = {w.word: NLP_WORD_COUNTS[w.word] * w.typo_score
                for w in candidates}
    correction = max(can_dict, key=can_dict.get)
    return correction