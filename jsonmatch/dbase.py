"""

jsonmatch.dbase

Depends on external libraries:
mysql-connector-python-rf

"""
import mysql.connector

def read_table(username, password, host, dbname, table_name):
    """Given proper credentials, exports a table from a mysql
    database as a list where each entry is a json-like object
    corresponding to a row in the table.
    """
    print "Making a connection ... "
    cnx = mysql.connector.connect(user=username, password=password,
                                host=host, database=dbname)
    try:
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM " + table_name + ";") #Get rows
        row_data = cursor.fetchall()
        cursor.execute("DESC " + table_name + ";") #Get columns
        col_data = cursor.fetchall()
        col_names = [tup[0] for tup in col_data] 
    finally:
        print "Closing the connection ... "
        cnx.close()
    #Create json object
    json_list = []
    for row in row_data:
        json_obj = {}
        for i in range(len(col_names)):
            json_obj[col_names[i]] = row[i]
        json_list.append(json_obj)
    return json_list