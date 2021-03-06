import json
import jsonmatch as js
import mysql.connector
from getpass import getpass

username = raw_input("Enter your mysql username: ")
password = getpass()
dbname = raw_input("Enter the name of the database: ")
table_name = raw_input("Enter the name of the table: ")

print "Making a connection ... "
cnx = mysql.connector.connect(user=username, password=password,
                              host='127.0.0.1',
                              database=dbname)
try:
    print "Executing queries ... "
    cursor = cnx.cursor()
    #Get columns
    cursor.execute("DESC " + table_name + ";")
    col_data = cursor.fetchall()
    col_names = [tup[0] for tup in col_data] 
    #Get rows
    cursor.execute("SELECT * FROM " + table_name + ";")
    row_data = cursor.fetchall()
finally:
    print "Closing the connection ... "
    cnx.close()

#Create json object for file
corpus = []
for row in row_data:
    json_obj = {}
    for i in range(len(col_names)):
        json_obj[col_names[i]] = row[i]
    corpus.append(json_obj)

query = {
        "DESCRIPTION": "staff satisfaction",
        "SOURCE": "",
        "INDICATOR": "",
        "TYPE": ""
    }
matcher = js.Matcher(input_type="object", query=query, corpus=corpus)

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

#To lowercase
q_tokens = js.nlp.to_lowercase(q_tokens)
#Removing stopwords (using the matcher's default set of words)
q_tokens = js.nlp.remove_stop_words(q_tokens, matcher.stop_words)
#Removing punctuation
q_tokens = js.nlp.remove_special_chars(q_tokens)
#Removing duplicates
q_tokens = js.nlp.remove_duplicates(q_tokens)
#Stemming words (using the matcher's default stemming function)
#q_tokens = js.nlp.stem_tokens(q_tokens, matcher.stemmer)

## Handling the corpus ##
#corpus_json holds all the search documents
print "Corpus:"
for k,v in matcher.corpus_json[16].iteritems():
    print k,": ",v
raw_input("Press Enter to continue ... ")
print

print "Tokenizing corpus."
c_tokens = js.nlp.tokenize_object(matcher.corpus_json, matcher.tokenizer)

for k,v in c_tokens[16].iteritems():
    print k,": ",v
raw_input("Press Enter to continue ... ")
print

#To lowercase
c_tokens = js.nlp.to_lowercase(c_tokens)
#Removing stopwords
c_tokens = js.nlp.remove_stop_words(c_tokens, matcher.stop_words)
#Removing punctuation
c_tokens = js.nlp.remove_special_chars(c_tokens)
#Stemming words
#c_tokens = js.nlp.stem_tokens(c_tokens, matcher.stemmer)

## LSI search ##
sims = js.mine.lsi_search(q_tokens[0]["DESCRIPTION"],
                          c_tokens, "DESCRIPTION", 5)
print "\nSearch results (best to worst cosine similarity):"
for s in sims:
    print s, "#", " ".join(c_tokens[s[0]]["INDICATOR"])
raw_input("Press Enter to continue ... ")
print