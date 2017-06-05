#jsonmatch_test.py
import jsonmatch as js
from getpass import getpass

#Read sql tables
username = raw_input("Enter your mysql username: ")
password = getpass()
dbname = raw_input("Enter the name of the database: ")
table_name = raw_input("Enter the name of the table: ")

corpus = js.dbase.read_table(username, password, "127.0.0.1", dbname, table_name)
query = {
        "DESCRIPTION": "staff satisfaction",
        "SOURCE": "",
        "INDICATOR": "",
        "TYPE": ""
    }

matcher = js.Matcher(input_type="object", query=query, corpus=corpus)
c_index = 16

## Handling the query ##

#query_json holds all the queries (just 1 in this case)
print "\nQuery:"
for dict in matcher.query_json:
    for key,val in dict.iteritems():
        print key,": ",val
raw_input("Press Enter to continue ... ")
print

print "Tokenizing query." #Using the matcher's default tokenizing function
q_tokens = js.nlp.tokenize_object(matcher.query_json, matcher.tokenizer)
for dict in q_tokens:
    for key,val in dict.iteritems():
        print key,": ",val
raw_input("Press Enter to continue ... ")
print

print "Correcting spelling." #Using the matcher's default autocorrector
q_spell = js.nlp.correct_spelling(q_tokens, matcher.speller)
for dict in q_spell:
    for key,val in dict.iteritems():
        print key,": ",val
raw_input("Press Enter to continue ... ")
print

#Removing stopwords (using the matcher's default set of words)
q_nostop = js.nlp.remove_stop_words(q_spell, matcher.stop_words)

#Removing duplicates
q_nodupes = js.nlp.remove_duplicates(q_nostop)

#Stemming words (using the matcher's default stemming function)
q_stem = js.nlp.stem_tokens(q_nodupes, matcher.stemmer)

## Handling the corpus ##

#corpus_json holds all the search documents
#c_index is referring to a specific document
print "Corpus:"
for k,v in matcher.corpus_json[c_index].iteritems():
    print k,": ",v
raw_input("Press Enter to continue ... ")
print

print "Tokenizing corpus."
c_tokens = js.nlp.tokenize_object(matcher.corpus_json, matcher.tokenizer)
for k,v in c_tokens[c_index].iteritems():
    print k,": ",v
raw_input("Press Enter to continue ... ")
print

print "Correcting spelling."
c_spell = js.nlp.correct_spelling(c_tokens, matcher.speller)
for k,v in c_spell[c_index].iteritems():
    print k,": ",v
raw_input("Press Enter to continue ... ")
print

#Removing stopwords
c_nostop = js.nlp.remove_stop_words(c_spell, matcher.stop_words)

#Stemming words
c_stem = js.nlp.stem_tokens(c_nostop, matcher.stemmer)

#This function requires the query and corpus lists, plus the indices
#of the objects you want to compare in those lists
match_matrix = js.mine.match(query=q_stem, corpus=c_stem,
                             query_i=0, corpus_i=c_index)
print "Here is the results of the matching:"
for entry in match_matrix:
    if entry[0] == entry[1]: #Here I only look at entries with matching keys
        print entry
print