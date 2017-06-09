"""

jsonmatch.dbase

"""
import mysql.connector
from sshtunnel import SSHTunnelForwarder

def read_table(ssh_host,
               ssh_username,
               ssh_password,
               sql_username,
               sql_password,
               db_name,
               table_name,
               remote_port=22,
               local_port=3306):
    """Given proper credentials, exports a table from a mysql
    database hosted on a remote server as a list where each entry
    is a json-like object corresponding to a row in the table.
    """
    print "Creating an SSH tunnel ... "
    with SSHTunnelForwarder(
        (ssh_host, remote_port),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        remote_bind_address=("127.0.0.1", local_port)) as server:
        
        print "Making a connection ... "
        cnx = mysql.connector.connect(host="127.0.0.1",
                                port=server.local_bind_port,
                                user=sql_username,
                                password=sql_password,
                                database=db_name)
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