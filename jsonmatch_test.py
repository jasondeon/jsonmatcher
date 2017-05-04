#jsonmatch_test.py
from jsonmatch import Matcher

matcher = Matcher(query="example_query.json",
                  corpus="example_targets.json")

print
print "1. Here are the contents of the json file:"
print matcher.corpus_json
print

sep_keys = matcher.separate_by_key(matcher.corpus_json)
print "2. Here are all the words associated with each key:"
print sep_keys
print

sep_keys = matcher.to_lowercase(sep_keys)
print "3. Now with uppercases removed:"
print sep_keys
print

sep_keys = matcher.remove_stop_words(sep_keys)
print "4. Now without stopwords:"
print sep_keys
print

sep_keys = matcher.stem_tokens(sep_keys)
print "5. Now with only word stems:"
print sep_keys
print

sep_keys = matcher.remove_duplicates(sep_keys)
print "6. Now without dupes:"
print sep_keys
print;print;print


sep_obj = matcher.separate_by_object(matcher.corpus_json)
print "1. Here are all the words associated with each object:"
print sep_obj
print

sep_obj = matcher.to_lowercase(sep_obj)
print "2. Now with uppercases removed:"
print sep_obj
print

sep_obj = matcher.remove_stop_words(sep_obj)
print "3. Now without stopwords:"
print sep_obj
print

sep_obj = matcher.stem_tokens(sep_obj)
print "4. Now with only word stems:"
print sep_obj
print

sep_obj = matcher.remove_duplicates(sep_obj)
print "5. Now without dupes:"
print sep_obj
print;print;print



tokens = matcher.separate_by_word(matcher.corpus_json)
print "1. Here is the corpus_json, with separated tokens:"
print tokens
print 