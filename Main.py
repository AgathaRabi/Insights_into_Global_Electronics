import csv
import pandas as pd
import data_cleaner as dc
import data_preparation as da
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
print(type(customers_data['Birthday']))

# clean the sales data
sales_data = dc.sales_data_clean(sales_data)

# clean the products data
products_data = dc.products_data_clean(products_data)
products_data.to_excel('C:\\Users\\PAPPILON\\Downloads\\products_data_test.xlsx')

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
customers_data_with_age.to_excel('C:\\Users\\PAPPILON\\Downloads\\cust_data_age.xlsx')
#customers_data_with_age.Age.hist()   # not seen
#plt.show()  # have to use this for the graph to be seen
customers_data_with_age['AgeGroup'] = pd.cut(customers_data_with_age.Age,
                                             bins = [0, 29, 40, 200], right = True,
                                             labels = ['Under 30', '30 - 40', 'Over 40'])
plt.figure(figsize = (14, 12))
sns.countplot(x = 'Country', data = customers_data_with_age, hue = 'AgeGroup')
#plt.show()

###-----Analyzing the distribution of customers based on age:

# this part we can directly do in power BI using data in SQL


##-----Purchase Patterns -----


###------Average order value:

#.....first i need a data frame having the following data....CUSTOMER ID, ORDER AMOUNT, ORDER DATE

#data_frame_average_order_value = pd.concat([sales_data, products_data], axis = 1, ignore_index = False)
#print('Merged Table using concat()')

#data_frame_average_order_value = pd.merge(sales_data, products_data, left_on=['ProductKey'],
                                          #right_on = ['Unit Price USD'], how = 'left')
#data_frame_average_order_value.to_excel('C:\\Users\\PAPPILON\\Downloads\\average_order_value_test.xlsx')

#data_frame_average_order_value = sales_data.merge(products_data, left_index = True, right_index = True,
                                                  #how = 'outer', suffixes = ('', '_DROP')).filter(regex = '^(?!.*_DROP)')
#data_frame_average_order_value = pd.merge(sales_data, products_data,left_on = True, right_on = True, how = 'outer')
#print("hello")
sales_summary = sales_data.merge(products_data, on = 'ProductKey')
customer_analysis_data_frame = sales_summary.merge(customers_data_with_age, on = 'CustomerKey')
#print("hi")
sales_summary.to_excel('C:\\Users\\PAPPILON\\Downloads\\sales_summary_before_group_test.xlsx')
customer_analysis_data_frame.to_excel('C:\\Users\\PAPPILON\\Downloads\\customer_analysis_df_test.xlsx')


#data_frame_aov_group = data_frame_average_order_value.groupby('CustomerKey')['Unit Price USD'].sum()
#print(data_frame_aov_group)
#demographic_analysis_new_df = pd.DataFrame()
#demographic_analysis_new_df = customers_data[['CustomerKey']].copy()
#demographic_analysis_new_df.insert(2, 'Purchase Amount', data_frame_aov_group, True)
#demographic_analysis_new_df.to_excel('C:\\Users\\PAPPILON\\Downloads\\demographic_analysis_new_df_test.xlsx')

#data_frame_average_order_value.merge(data_frame_aov_group, on = 'CustomerKey')

#sales_summary['Total Purchase'] = sales_summary.groupby('CustomerKey')['Unit Price USD'].sum()
sales_summary = sales_summary.groupby(['Order Number', 'CustomerKey'])['Unit Price USD'].sum()
sales_summary.to_excel('C:\\Users\\PAPPILON\\Downloads\\sales_summary_test.xlsx')
# Iam trying to build a data frame to cover the entire customer analysis (demographic distribution and purchase patterns)
customer_analysis_data_frame = customer_analysis_data_frame.groupby(['CustomerKey', 'City', 'State',
                                                                     'Continent', 'Age']).agg({'Order Number': ['count'],
                                                                                        'Unit Price USD': ['sum']})
customer_analysis_data_frame.to_excel('C:\\Users\\PAPPILON\\Downloads\\cust_df_multiple_grbys.xlsx')