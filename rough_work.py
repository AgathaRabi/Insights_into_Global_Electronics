demographic_analysis_gender_M = customers_data[customers_data['Gender'] == 'Male']['CustomerKey'].count()
demographic_analysis_gender_F = customers_data[customers_data['Gender'] == 'Female']['CustomerKey'].count()
print(demographic_analysis_gender_M)
print(demographic_analysis_gender_F)

###-----Analyzing the distribution of customers based on age:

customers_data_with_age = dp.AddAgeColumn(customers_data, 'Birthday')

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
dp.CalculateTotalProductPrice(sales_summary)  # calculating Total Product price
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
                                                                     'Continent', 'Age']).agg({'Order Number': ['nunique'],
                                                                                        'Total Product Price': ['sum']})
customer_analysis_data_frame.to_excel('C:\\Users\\PAPPILON\\Downloads\\cust_df_multiple_grbys.xlsx')