"""
Module with functions to perform Create, Read, Update, Delete operations on the database
"""

import psycopg2
from sqlalchemy import create_engine



def get_local_engine():
    """
    Function to connect to the local database and return
    the connection object.

    Retuns:
    ------
    Database connectionn object
    """
    """my_data_base_conn = psycopg2.connect(host="localhost",
                                         user="postgres",
                                         password="phoenix275",
                                         database="insights_global_electronics",
                                         port="5432")"""
    engine = create_engine('postgresql+psycopg2://postgres:phoenix275@localhost/global_electronics')
    #engine.autocommit = True

    return engine


def drop_and_create_cust_prodts_sales_dets_table(cust_products_details_dict, engine):
    """
    Function to drop the current channel table, if it exists
    and create a new empty table.

    Parameters:
    ----------
    cust_products_details_dict:
        The database connection object
    """
    #engine = get_local_engine()

    for table_name, df in cust_products_details_dict.items():
        print(df.head())
        df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)



