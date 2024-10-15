import csv
import pandas as pd

# Read the csv file
data_customers = pd.read_csv("C:\\Users\\PAPPILON\\Downloads\\Customers.csv", encoding = 'unicode_escape')

#print(data_customers)
#print(type(data_customers))
#print(data_customers.head())
#print(data_customers["Country"])
#print(data_customers["Country"].dtype)

#print(data_customers.dtypes) # except customer id everything else is string, including pin code.
#print(data_customers.info()) # No missing information as such. # state code has missing data(10).
#print(data_customers.describe())
#print(data_customers.loc[0])
#print(data_customers.shape) # no. of rows and columns
print(data_customers.shape[0]) # no. of rows
#print(data_customers.shape[1]) # no. of columns
print(data_customers.columns)
print(data_customers.keys())
print(data_customers['CustomerKey'].count())
print(data_customers['CustomerKey'].value_counts())


