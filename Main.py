import csv
import pandas as pd
import data_cleaner as dc
import data_analyzer as da
from datetime import date

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
print(type(customers_data['Birthday']))

# clean the sales data
sales_data = dc.sales_data_clean(sales_data)


# clean the stores data
stores_data = dc.stores_data_clean(stores_data)

# clean the exchange rates data
exchange_rates_data = dc.exchange_rates_data_clean(exchange_rates_data)

# ------------------ DATA ANALYSIS ------------

# --- CUSOMER ANALYSIS ---

##-----Demographic distribution -----

###-----Analyzing the distribution of customers based on gender:

demographic_analysis_gender_M = customers_data[customers_data['Gender'] == 'Male']['CustomerKey'].count()
demographic_analysis_gender_F = customers_data[customers_data['Gender'] == 'Female']['CustomerKey'].count()
print(demographic_analysis_gender_M)
print(demographic_analysis_gender_F)

###-----Analyzing the distribution of customers based on age:

customers_data_with_age = da.AddAgeColumn(customers_data, 'Birthday')