import csv
import pandas as pd
import data_cleaner as dc
import data_preparation as dp
import database_interface as db_int
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns

# Read the csv files
customers_data = pd.read_csv("C:\\Users\\PAPPILON\\Downloads\\Customers.csv", encoding = 'unicode_escape')
sales_data = pd.read_csv("C:\\Users\\PAPPILON\\Downloads\\Sales.csv", encoding = 'unicode_escape')
products_data = pd.read_csv("C:\\Users\\PAPPILON\\Downloads\\Products.csv", encoding = 'unicode_escape')
stores_data = pd.read_csv("C:\\Users\\PAPPILON\\Downloads\\Stores.csv", encoding = 'unicode_escape')
exchange_rates_data = pd.read_csv("C:\\Users\\PAPPILON\\Downloads\\Exchange_Rates.csv", encoding = 'unicode_escape')

# basic clean of all the data
customers_data = dc.clean_data(customers_data, 0)
sales_data = dc.clean_data(sales_data, 0)
products_data = dc.clean_data(products_data, 0)
stores_data = dc.clean_data(stores_data, 0)
exchange_rates_data = dc.clean_data(exchange_rates_data, 0)


# clean the customer data
customers_data = dc.customer_data_clean(customers_data)

# test :print(type(customers_data['Birthday']))
# test :customers_data.to_excel('C:\\Users\\PAPPILON\\Downloads\\test_clean.xlsx')

# clean the sales data
sales_data = dc.sales_data_clean(sales_data)

# clean the products data
products_data = dc.products_data_clean(products_data)
#test :products_data.to_excel('C:\\Users\\PAPPILON\\Downloads\\products_data_test.xlsx')

# clean the stores data
stores_data = dc.stores_data_clean(stores_data)

# clean the exchange rates data
exchange_rates_data = dc.exchange_rates_data_clean(exchange_rates_data)

# set the index for each df
#customers_data.reset_index(drop=True, inplace = True)

# test:customers_data.to_excel('C:\\Users\\PAPPILON\\Downloads\\test_clean.xlsx')
# test:print('Hi')

# Get the local DB connection
db_conn = db_int.get_local_db_conn()

# Drop and create the respective fresh SQL tables
db_int.drop_and_create_customers_data_table(db_conn) # for customer analysis

# Add data to the created SQL tables
db_int.add_data_to_customers_data_table(customers_data,db_conn) # for customer analysis


# Main run

cust_sales_analysis_data_dictionary = dp.data_for_cust_sales_analysis(customers_data, sales_data, products_data, stores_data, exchange_rates_data)
engine = db_int.get_local_engine()
db_int.drop_and_create_cust_prodts_sales_dets_table(cust_sales_analysis_data_dictionary, engine)
