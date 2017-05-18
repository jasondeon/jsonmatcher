#jsonmatch_test.py
from jsonmatch import Matcher

matcher = Matcher(query="example_query.json",
                  corpus="example_targets.json")
                  

print "Query:"
print matcher.query_json
raw_input("Press Enter to continue ... ")
print
print "Tokenizing query."
q_tokens = matcher.separate_by_word(matcher.query_json)
print q_tokens
raw_input("Press Enter to continue ... ")
print
print "Correcting spelling."
q_spell = matcher.correct_spelling(q_tokens)
print q_spell
raw_input("Press Enter to continue ... ")
print
print "Removing stopwords."
q_nostop = matcher.remove_stop_words(q_spell)
print q_nostop
raw_input("Press Enter to continue ... ")
print
print "Removing dupes."
q_nodupes = matcher.remove_duplicates(q_nostop)
print q_nodupes
raw_input("Press Enter to continue ... ")
print
print "Stemming words."
q_stem = matcher.stem_tokens(q_nodupes)
print q_stem
raw_input("Press Enter to continue ... ")
print

print "Corpus:"
print matcher.corpus_json
raw_input("Press Enter to continue ... ")
print
print "Tokenizing corpus."
c_tokens = matcher.separate_by_word(matcher.corpus_json)
print c_tokens
raw_input("Press Enter to continue ... ")
print
print "Correcting spelling."
c_spell = matcher.correct_spelling(c_tokens)
print c_spell
raw_input("Press Enter to continue ... ")
print
print "Removing stopwords."
c_nostop = matcher.remove_stop_words(c_spell)
print c_nostop
raw_input("Press Enter to continue ... ")
print
print "Stemming words."
c_stem = matcher.stem_tokens(c_nostop)
print c_stem
raw_input("Press Enter to continue ... ")
print

match_matrix = matcher.match(objectq=q_stem, objectc=c_stem,
                             objectq_i=0, objectc_i=0)
print "Here is the results of the matching:"
for entry in match_matrix:
    print entry
print