from autocorrect.word_lists import LOWERCASE
import os, itertools

VOWELS = "aoeiu"
DEFAULT_DICTIONARY = "big.txt"
NOT_FOUND = "NO SUGGESTION"
GENERIC_MESSAGE = "Please enter a word to spell-check (ie. ignorence) \n--verify to generate a list of possible mis-spellings (ie. sheep --verify)\n--exit to quit\n"

def initialize_dictionary():
    """
    Returns a set of words contained in a large list of English words

    """
    return LOWERCASE
    #word_set = set()
    #filename = DEFAULT_DICTIONARY
    #if os.path.isfile(filename):
    #    with open(filename, 'r') as f:
    #        for line in iter(f):
    #            word_set.add(line.strip('\n'))
    #else:
    #    print "There's seems to be a problem loading in the word list, ensure availability of /usr/share/dict/words"
    #return word_set

def spell_check(word, dictionary):
    """
    Returns True if valid suggestion can be found, False otherwise

    *function used in --verify only
    """
    unduplicated = eliminate_duplicate(word)
    for elem in unduplicated:
        if elem in dictionary or isinstance(permutate_vowels(elem, dictionary, complete = False), str):
            return True
    return False

def permutate_vowels(word, dictionary, complete = True):
    """
    Returns a list of strings, where instances of vowel characters are permutated
    between every possible vowel, setting complete to False will return a string
    immediately if a suggestion is found in the dictionary

    >>> permutate_vowels('cat', initialize_dictionary())
    ['cat', 'cot', 'cet', 'cit', 'cut']

    >>> permutate_vowels('cat', initialize_dictionary(), complete=False)
    'cat'

    *function used in --verify only
    """
    rtn = []
    vowel_locations = [index for index in range(len(word)) if word[index] in VOWELS]
    vowel_permutations = itertools.product(VOWELS, repeat = len(vowel_locations))
    for permutation in vowel_permutations:
        tmp = ""
        vowel_index = 0
        for index in range(len(word)):
            if word[index] in VOWELS:
                tmp += permutation[vowel_index]
                vowel_index += 1
            else:
                tmp += word[index]
        if not complete and tmp in dictionary:
            return tmp
        rtn.append(tmp)
    return rtn

def eliminate_duplicate(word):
    """
    Returns a list of strings, where instances of consecutive duplicate characters
    in string parameter, word are permutated between one and two

    >>> eliminate_duplicate("teepee")
    ['tepe', 'tepee', 'teepe', 'teepee']

    >>> eliminate_duplicate("sheeeeep")
    ['shep', 'sheep']

    """
    rtn = []
    enumerated_word = [[k, 2] if len(list(v)) >= 2 else [k, 1] for k,v in itertools.groupby(word)]
    duplicate_count = len(filter(lambda elem: elem[1] == 2, enumerated_word))
    permutations = itertools.product("12", repeat = duplicate_count)
    for elem in permutations:
        tmp = ""
        duplicate_index = 0
        for char in enumerated_word:
            if char[1] == 2:
                tmp += char[0] * int(elem[duplicate_index])
                duplicate_index += 1
            else:
                tmp += char[0]
        rtn.append(tmp)
    return rtn

def spawn_duplicate(word):
    """
    Returns a list of strings, where each character in string input, word is permutated
    to contain a consecutive duplicate value

    """
    rtn = []
    permutations = itertools.product("12", repeat = len(word))
    for elem in permutations:
        rtn.append("".join(map(lambda index: word[index] * int(elem[index]), range(len(word)))))
    return rtn
    
def test(word):
    """Added by Jason.
    Pass a single word and return the correction.
    """
    dictionary = initialize_dictionary()
    word = word.strip().lower()
    found = False
    unduplicated = eliminate_duplicate(word)
    for elem in unduplicated:
        if elem in dictionary:
            return elem
    if not found:
        for elem in unduplicated:
            rst = permutate_vowels(elem, dictionary, complete = False)
            if isinstance(rst, str):
                return rst
    if not found:
        return word

def main():
    print "SpellChecker: Note on implementation at https://github.com/yuxinzhu/spellchecker\n"
    print GENERIC_MESSAGE
    dictionary = initialize_dictionary()
    while True:
        word = raw_input("> ")
        if "--verify" in word:
            success = True
            word = word.split("--verify")[0].strip().lower()
            if word not in dictionary:
                print "word to verify must already exist in dictionary"
                continue
            tmp = permutate_vowels(word, dictionary)
            possible_words = itertools.chain(*map(spawn_duplicate, tmp))
            num_possible_words = len(list(itertools.chain(*map(spawn_duplicate, tmp)))) #just for fun
            for misspelling in possible_words:
                print misspelling
                if not spell_check(misspelling, dictionary):
                    print ("\nThe following mis-spelling: \"" + misspelling + "\" was not found in the dictionary")
                    success = False
                    break
            if success:
                print "\n\nSuccess! All " + str(num_possible_words) + " possible mis-spellings were successfully generated and spell-checked."

        elif "--exit" in word:
            print "See you next time!"
            break

        else:
            word = word.strip().lower()
            if word == "":
                print GENERIC_MESSAGE
            else:
                found = False
                unduplicated = eliminate_duplicate(word)
                for elem in unduplicated:
                    if elem in dictionary:
                        print elem
                        found = True
                        break
                if not found:
                    for elem in unduplicated:
                        rst = permutate_vowels(elem, dictionary, complete = False)
                        if isinstance(rst, str):
                            print rst
                            found = True
                            break
                if not found:
                    print NOT_FOUND

if __name__ == "__main__":
    main()
