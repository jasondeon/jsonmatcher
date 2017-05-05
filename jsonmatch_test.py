#jsonmatch_test.py
from jsonmatch import Matcher

matcher = Matcher(query="example_query.json",
                  corpus="example_targets.json")

match_matrix = matcher.match(objectq_i=0, objectc_i=0)
print "Here is the results of the matching:"
for entry in match_matrix:
    print entry
print