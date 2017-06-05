#Export a local mysql table to a json file.
import json
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
    #Get rows
    cursor.execute("SELECT * FROM " + table_name + ";")
    row_data = cursor.fetchall()
    #Get columns
    cursor.execute("DESC " + table_name + ";")
    col_data = cursor.fetchall()
    col_names = [tup[0] for tup in col_data] 
finally:
    print "Closing the connection ... "
    cnx.close()

#Create json object for file
json_list = []
for row in row_data:
    json_obj = {}
    for i in range(len(col_names)):
        json_obj[col_names[i]] = row[i]
    json_list.append(json_obj)
#Write to file
filename = raw_input("Name the json file: ")
with open(filename, 'w') as json_out:
    json.dump(json_list, json_out)
print "Successfully wrote to json file."