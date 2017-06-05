#Load a json file into a pre-existing locally hosted mysql db
import json
import mysql.connector
from getpass import getpass

filename = raw_input("Enter the json filename: ")
with open(filename) as json_file:
    dict = json.load(json_file)
cols = []
for entry in dict:
    cols.extend(entry.keys())
cols = list(set(cols)) # remove dupes
print "Successfully loaded json file."

username = raw_input("Enter your mysql username: ")
password = getpass()
dbname = raw_input("Enter the name of the database: ")
table_name = raw_input("Enter a name for the table: ")
primary = raw_input("Enter the primary key: ")

print "Making a connection ... "
cnx = mysql.connector.connect(user=username, password=password,
                              host='127.0.0.1',
                              database=dbname)
try:
    print "Executing queries ... "
    cursor = cnx.cursor()
    #Create the table
    col_str = ""
    for c in cols:
        col_str += c
        if c == primary:
            col_str += " VARCHAR(500) NOT NULL, "
        else:
            col_str += " VARCHAR(500), "
    col_str += "PRIMARY KEY (" + primary + ")"
    col_str = "(" + col_str + ")"
    add_table = "CREATE TABLE {tbl}{cols};".format(
        tbl=table_name, cols=col_str)
    #print "Executing:\n" + add_table
    cursor.execute(add_table)
    
    #Populating the table
    col_str = val_str = ""
    for c in cols:
        col_str += (c + ", ")
        val_str += ("%s, ")
    col_str = col_str[:-2] #remove last ", "
    val_str = val_str[:-2] #remove last ", "
    add_row = "INSERT INTO {tbl} ({cols}) VALUES ({vals});".format(
        tbl=table_name, cols=col_str, vals=val_str)
    for entry in dict:
        row_data = tuple(entry[col] for col in cols)
        #print "Row entries:\n" + str(row_data)
        cursor.execute(add_row, row_data)
        
    cnx.commit()
    
finally:
    print "Closing the connection ... "
    cnx.close()