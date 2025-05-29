import pandas as pd
import psycopg2
import pyodbc



def get_local_db_conn():
    """
    Function to connect to the local database and return
    the connection object.

    Retuns:
    ------
    Database connectionn object
    """
    my_data_base_conn = psycopg2.connect(host="localhost",
                                         user="postgres",
                                         password="phoenix275",
                                         database="global_electronics",
                                         port="5432")
    my_data_base_conn.autocommit = True

    return my_data_base_conn



