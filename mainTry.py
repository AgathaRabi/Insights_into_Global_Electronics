import csv
import pandas as pd

# Read the csv file
customers_data = pd.read_csv("C:\\Users\\PAPPILON\\Downloads\\Customers.csv", encoding = 'unicode_escape')

#print(customers_data)
#print(type(customers_data))
#print(customers_data.head())
#print(customers_data["Country"])
#print(customers_data["Country"].dtype)


#print(customers_data.dtypes) # except customer id everything else is string, including pin code.
#print(customers_data.info()) # No missing information as such. # state code has missing data(10).
#print(customers_data.describe())
#print(customers_data.loc[0])
#print(customers_data.shape) # no. of rows and columns
print(customers_data.shape[0]) # no. of rows
#print(customers_data.shape[1]) # no. of columns
print(customers_data.columns)
print(customers_data.keys())
print(customers_data['CustomerKey'].count())
print(customers_data['CustomerKey'].unique())
"""a = customers_data['CustomerKey'].unique()
b = a.count()
print(b)"""
print(customers_data['CustomerKey'].nunique())
print(customers_data['CustomerKey'].value_counts())
print(customers_data.nunique())

print(customers_data.duplicated())
customers_data.drop_duplicates()  # the first step in cleaning i.e, dropping duplicates

print(customers_data.nunique())

#print(customers_data['CustomerKey'].value_counts())


#  you can drop columns that you don't need as shown below
# df.drop(columns = "the one you dont need")

# trying to change all the date entries to date format.

a = pd.to_datetime(customers_data.Birthday)
print(a)

customers_data['Birthday'] = customers_data['Birthday'].apply(lambda x : pd.to_datetime(x).strftime('%d/%m/%y'))
print(customers_data['Birthday'])

customers_data['State'] = customers_data['State'].str.replace('-', " ")
print(customers_data['State'])

# Now i want to save this data frame to excel file so that i can view the complete document:

#data_customers_excelfl = customers_data.xlsx
#customers_data.to_excel(data_customers_excelfl)

customers_data.to_excel('C:\\Users\\PAPPILON\\Downloads\\test_clean.xlsx')








