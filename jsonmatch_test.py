#jsonmatch_test.py
from jsonmatch import Matcher

matcher = Matcher(query="example_query.json",
                  corpus="example_targets.json")

print "Here are the contents of the json file:"
print matcher.corpus_json
print

print "Here are all the words associated with each key:"
print matcher.separate_by_key(matcher.corpus_json)
print

print "Here are all the words associated with each object:"
print matcher.separate_by_object(matcher.corpus_json)