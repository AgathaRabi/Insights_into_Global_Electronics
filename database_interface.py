"""
Module with functions to perform Create, Read, Update, Delete operations on the database
"""

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session

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

    for table_name, df in cust_products_details_dict.items():
        # TEST :print(df.head())
        df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)


def drop_and_create_customers_data_table(db_conn):
    """
        Function to drop the customers_data table, if it exists
        and create a new empty table.

        Parameters:
        ----------
        db_conn:
            The database connection object
        """

    cursor = db_conn.cursor()

    drop_query = '''drop table if exists customers_data'''
    cursor.execute(drop_query)

    try:
        create_query = '''create table if not exists customers_data(customer_key varchar(100) primary key,
                                                                    gender text,
                                                                    name varchar(200),
                                                                    city varchar(200),
                                                                    state_code varchar(100),
                                                                    state varchar(200),
                                                                    zip_code varchar(100),
                                                                    country text,
                                                                    continent text,
                                                                    birthday date)'''
        cursor.execute(create_query)

        db_conn.commit()

    except:
        print("Error in creating customers table!")



def drop_and_create_stores_data_table(db_conn):
    """
        Function to drop the stores_data table, if it exists
        and create a new empty table.

        Parameters:
        ----------
        db_conn:
            The database connection object
        """

    cursor = db_conn.cursor()

    drop_query = '''drop table if exists customers_data'''
    cursor.execute(drop_query)

    try:
        create_query = '''create table if not exists customers_data(customer_key varchar(100) primary key,
                                                                    gender text,
                                                                    name varchar(200),
                                                                    city varchar(200),
                                                                    state_code varchar(100),
                                                                    state varchar(200),
                                                                    zip_code varchar(100),
                                                                    country text,
                                                                    continent text,
                                                                    birthday date)'''
        cursor.execute(create_query)

        db_conn.commit()

    except:
        print("Error in creating stores table!")


def add_data_to_customers_data_table(customers_data, db_conn):
    """
    Function to add/ insert  customer details as a new row of data to
    the customers_data table.

    Parameters:
    ----------
    customers_data:
        Pandas DataFrame object of the customer details
    """

    cursor = db_conn.cursor()

    for index, row in customers_data.iterrows():
        insert_into_sql = '''insert into customers_data (customer_key,
                                                        gender,
                                                        name,
                                                        city,
                                                        state_code,
                                                        state,
                                                        zip_code,
                                                        country,
                                                        continent,
                                                        birthday) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        value_customers = (row['CustomerKey'],
                           row['Gender'],
                           row['Name'],
                           row['City'],
                           row['State Code'],
                           row['State'],
                           row['Zip Code'],
                           row['Country'],
                           row['Continent'],
                           row['Birthday'])

        cursor.execute(insert_into_sql, value_customers)

        db_conn.commit()