"""
File reader, concat function and dict wrapper
Author: Jonas McCallum
https://github.com/foobarmus/autocorrect
"""
from itertools import chain

def concat(*args):
    """reversed('th'), 'e' => 'hte'"""
    try:
        return ''.join(args)
    except TypeError:
        return ''.join(chain.from_iterable(args))
    
def bigram_word(word):
    """list of adjacent letters: 'fast' => [' f', 'fa', 'as', 'st', 't ']"""
    word = ' ' + word + ' '
    return [word[i:i+2] for i in range(len(word) - 1)]
    
def add_words(main_list, sub_list):
    """Concatenate to a list of Word objects, updating duplicates"""
    word_list = [w.word for w in main_list]
    for w in sub_list:
        found = False
        for i in range(len(main_list)):
            if w.word == main_list[i].word and w.typo_score > main_list[i].typo_score:
                #Update the main list.
                main_list[i] = w
                found = True
        if not found:
            main_list.append(w)
    return main_list
    
class Zero(dict):
    """dict with a zero default"""

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key):
        try:
            return super(Zero, self).__getitem__(key)
        except KeyError:
            return 0

zero_default_dict = Zero