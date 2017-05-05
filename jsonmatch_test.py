#jsonmatch_test.py
from jsonmatch import Matcher

matcher = Matcher(query="example_query.json",
                  corpus="example_targets.json")
print "Query:"
print matcher.query_json
print
print "Tokenizing query."
q_tokens = matcher.separate_by_word(matcher.query_json)
print q_tokens
print
print "Removing dupes."
q_nodupes = matcher.remove_duplicates(q_tokens)
print q_nodupes
print
print "Removing stopwords."
q_nostop = matcher.remove_stop_words(q_nodupes)
print q_nostop
print

print "Corpus:"
print matcher.corpus_json
print
print "Tokenizing corpus."
c_tokens = matcher.separate_by_word(matcher.corpus_json)
print c_tokens
print
print "Removing stopwords."
c_nostop = matcher.remove_stop_words(c_tokens)
print c_nostop
print

match_matrix = matcher.match(objectq=q_nostop, objectc=c_nostop,
                             objectq_i=0, objectc_i=0)
print "Here is the results of the matching:"
for entry in match_matrix:
    print entry
print