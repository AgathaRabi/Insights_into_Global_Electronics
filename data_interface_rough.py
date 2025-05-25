"""
Module with functions to perform Create, Read, Update, Delete operations on the database
"""

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session


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

    with engine.connect() as connection:
        connection.execute()
        for table_name, df in cust_products_details_dict.items():

            cursor = db_conn.cursor()

            drop_query = '''drop table if exists channels'''
            cursor.execute(drop_query)

            try:
                create_query = '''create table if not exists channels(Order_Number varchar(100),
                                                                            Line_Item int,
                                                                            Order_Date datetime,
                                                                            Delivery_Date datetime, 
                                                                        Customer_Key varchar(80) primary key,
                                                                        Store_Key varchar(80),
                                                                        Product_Key varchar(80),
                                                                        Quantity int,
                                                                        Currency_Code varchar(80),
                                                                        Product_Name varchar(400),
                                                                        Brand varchar(250),
                                                                        Color varchar(100),
                                                                        Unit_Cost_USD float(100),
                                                                        Unit_Price_USD float(200),
                                                                        Sub_Category_Key varchar(50),
                                                                        Sub_Category varchar(300),
                                                                        Category_Key varchar(100),
                                                                        Category varchar(200),
                                                                        Total_Product_Price float(100),
                                                                        Gender text(50),
                                                                        Name varchar(100),
                                                                        City varchar(200),


                                                                        Subscribers_Count bigint,
                                                                        Views_Channel bigint,
                                                                        Total_Videos int,
                                                                        Channel_Description text,
                                                                        Playlist_Id varchar(80))'''
            cursor.execute(create_query)

            db_conn.commit()
        # engine = get_local_engine()

        """ for table_name, df in cust_products_details_dict.items():
             print(df.head())
             df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)"""