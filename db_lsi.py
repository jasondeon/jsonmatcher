#jsonmatch_test.py
import jsonmatch as js
import json

#Pre-coded login info
ssh_host = "dev.cs.smu.ca"
ssh_username = "j_deon"
ssh_password = ""
sql_username = "j_deon"
sql_password = ""
db_name = "j_deon"
table_name = "test"

corpus = js.dbase.read_table(
    ssh_host=ssh_host,
    ssh_username=ssh_username,
    ssh_password=ssh_password,
    sql_username=sql_username,
    sql_password=sql_password,
    db_name=db_name,
    table_name=table_name)

query = {
        "DESCRIPTION": "staff satisfaction",
        "SOURCE": "",
        "INDICATOR": "",
        "TYPE": ""
    }

#Or if you want to load the query from a file:

#query = None
#with open("name_of_query_file.json") as file:
#    query = json.load(file)
    
matcher = js.Matcher(input_type="object", query=query, corpus=corpus)

q_tokens = js.nlp.tokenize_object(matcher.query_json, matcher.tokenizer)
q_tokens = js.nlp.to_lowercase(q_tokens)
q_tokens = js.nlp.remove_stop_words(q_tokens, matcher.stop_words)
q_tokens = js.nlp.remove_special_chars(q_tokens)
q_tokens = js.nlp.remove_duplicates(q_tokens)
#Stemming optional
#q_tokens = js.nlp.stem_tokens(q_tokens, matcher.stemmer)

c_tokens = js.nlp.tokenize_object(matcher.corpus_json, matcher.tokenizer)
c_tokens = js.nlp.to_lowercase(c_tokens)
c_tokens = js.nlp.remove_stop_words(c_tokens, matcher.stop_words)
c_tokens = js.nlp.remove_special_chars(c_tokens)
#Stemming optional
#c_tokens = js.nlp.stem_tokens(c_tokens, matcher.stemmer)



## LSI search ##
'''
q_tokens[0]["DESCRIPTION"]: 0 means the first query in the file (in the
                            example there is only one). The string refers
                            to the column in the query you want to use.
c_tokens: is the corpus documents after processing.
"DESCRIPTION": is the column in the corpus you want to use.
5: is the number of topics to extract using LSI (may change results).
   Typical numbers for really large databases would be 100 to 500.
'''
sims = js.mine.lsi_search(q_tokens[0]["DESCRIPTION"],
                          c_tokens, "DESCRIPTION", 5)
#The sims variable is a list of tuples (row#, cosine similarity)
#The join function is used to print out the corpus since c_tokens
#actually contains a list of words from when we were processing them.
print "\nSearch results (best to worst cosine similarity):"
for s in sims:
    print s, "#", " ".join(c_tokens[s[0]]["INDICATOR"])
raw_input("Press Enter to continue ... ")
print