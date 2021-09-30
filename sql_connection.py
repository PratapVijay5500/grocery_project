import mysql.connector
__mydb = None


def get_sql_connection():
    global __mydb
    if __mydb is None:
        __mydb = mysql.connector.connect(user='root', password="72841990", host='127.0.0.1', database='grocery_store')

    return __mydb