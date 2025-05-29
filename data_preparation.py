import pandas as pd
import seaborn as sns
from datetime import date


def CalculateAge(BirthDate):
    """
    :param BirthDate:
    :return: age
    this function is to
    """
    today = date.today()
    age = today.year - BirthDate.year - ((today.month, today.day) < (BirthDate.month, BirthDate.day))

    return age


def AddAgeColumn(df, BirthDate):
    """

    :param df:

    :return:
    """
    df['Age'] = df[BirthDate].apply(CalculateAge)
    return df

def CalculateTotalProductPrice(df):
    """

    :param df:
    :return:
    """
    df['Total Product Price'] = df['Quantity'] * df['Unit Price USD']

    return df



def data_for_cust_sales_analysis(customers_data_cleaned, sales_data_cleaned, products_data_cleaned, stores_data_cleaned, exchange_rates_data_cleaned):
    """

    :param customers_data:
    :param sales_data:
    :param products_data:
    :return:
    """
    # calculating the age and adding a column to th customer data
    customers_data_cleaned['Age'] = customers_data_cleaned['Birthday'].apply(CalculateAge)
    # adding the age group column
    customers_data_cleaned['AgeGroup'] = pd.cut(customers_data_cleaned.Age,
                                                 bins=[0, 29, 40, 200], right=True,
                                                 labels=['Under 30', '30 - 40', 'Over 40'])
    # Now 'Merge' cleaned sales data and cleaned products data
    sales_details_df = sales_data_cleaned.merge(products_data_cleaned, on = 'ProductKey')
    # And then calculate 'Total Product Price', REVENUE
    sales_details_df['Total Product Price'] = sales_details_df['Quantity'] * sales_details_df['Unit Price USD']
    sales_details_df['Net Profit'] = (sales_details_df['Unit Price USD'] - sales_details_df['Unit Cost USD']) * sales_details_df['Quantity']
    sales_details_df['Net Profit Margin'] = (sales_details_df['Net Profit'] / (sales_details_df['Unit Price USD'] * sales_details_df['Quantity'])) * 100

    # Now merge the sales details with customer and product data, to get further data as, product purchase patterns
    # .... such as most ordered product by gender

    customer_products_sales_df = sales_details_df.merge(customers_data_cleaned, on = 'CustomerKey')
    customer_products_sales_df['Year'] = pd.DatetimeIndex(customer_products_sales_df['Order Date']).year
    customer_products_sales_df['Month'] = pd.DatetimeIndex(customer_products_sales_df['Order Date']).month

    # Now merge products details to help further analysis such as enough stores are there to cater to the demand:
    stores_data_prep = stores_data_cleaned[['StoreKey', 'Square Meters', 'Open Date']]
    customer_products_sales_stores_df = stores_data_prep.merge(customer_products_sales_df, on = 'StoreKey')

    # Group the customer_product_sales_df to get sales data for each order by customers
    # This data should be helpful for getting insights such as average order value,
    # average order value by gender, age-range, etc.
    customer_sales_df = (customer_products_sales_df.groupby(['Order Number', 'StoreKey', 'CustomerKey', 'Name',
                                                             'City', 'State', 'Country', 'Continent', 'Gender', 'Age',
                                                             'AgeGroup', 'Year'], observed=True, as_index=False).agg({'Total Product Price': 'sum'}))

    customer_sales_df.rename(columns={'Total Product Price': 'Order Value'}, inplace = True)

    # now creating another data for further analysis at stores level: like stores with zero sales:



    sales_stores_details_level_df = customer_sales_df.groupby(['StoreKey'] , observed=True, as_index=False).agg(
                                                                {'Order Value': 'sum', 'Order Number': 'count'})

    stores_sales_df = stores_data_prep.merge(sales_stores_details_level_df, on='StoreKey', how='left')
    stores_sales_df.fillna(0, inplace = True)

    # another data base for product analysis:

    products_profits_df = customer_products_sales_stores_df.groupby(['ProductKey', 'Country', 'Year', 'Quantity'] , observed=True, as_index=False).agg(
                                                                {'Net Profit': 'sum', 'Net Profit Margin': 'sum'})

    # testing for customers who havent made any purchase:

    customer_sales_nil_purchase = (customer_sales_df.groupby(['CustomerKey'], observed=True,
                                                            as_index=False).agg({'Order Number': 'nunique'}))
    nil_purchase_customers_df = customers_data_cleaned.merge(customer_sales_nil_purchase, on='CustomerKey', how='left')
    nil_purchase_customers_df.fillna({'Order Number': 0}, inplace=True)

    # exchange rate analysis:
    #sales_data_cleaned.rename(columns={'Order Date': 'Date for Analysis'}, inplace=True)
    exchange_rates_data_cleaned.rename(columns={'Date': 'Order Date'}, inplace=True)
    exchange_rates_data_cleaned.rename(columns={'Currency': 'Currency Code'}, inplace=True)
    #sales_exchange_rate_analysis_df = sales_data_cleaned.merge(exchange_rates_data_cleaned,
                                        #on = ['Date for Analysis', 'Currency Code'], how = 'left')
    sales_exchange_rate_analysis_df = customer_products_sales_stores_df.merge(exchange_rates_data_cleaned,
                                        on = ['Order Date', 'Currency Code'], how = 'left')

    sales_exchange_rate_analysis_df = sales_exchange_rate_analysis_df.round({'Exchange':1})

    # converting to excel for reference.
    customer_products_sales_df.to_excel('C:\\Users\\PAPPILON\\Downloads\\customer_products_sales_df_test2425AN.xlsx')
    customer_products_sales_stores_df.to_excel('C:\\Users\\PAPPILON\\Downloads\\customer_products_sales_stores_df_test2425AN.xlsx')
    customer_sales_df.to_excel('C:\\Users\\PAPPILON\\Downloads\\customer_sales_df_test2425AN.xlsx')
    stores_sales_df.to_excel('C:\\Users\\PAPPILON\\Downloads\\stores_sales_df_test2425AN.xlsx')
    products_profits_df.to_excel('C:\\Users\\PAPPILON\\Downloads\\products_profits_df_test2425AN.xlsx')
    nil_purchase_customers_df.to_excel('C:\\Users\\PAPPILON\\Downloads\\nil_purchase_customers_test2425AN.xlsx')
    sales_exchange_rate_analysis_df.to_excel('C:\\Users\\PAPPILON\\Downloads\\sales_exchange_rate_analysis_test2425AN.xlsx')

    # placing these data sets in a dictionary
    cust_sales_analysis_data_dict = {}
    cust_sales_analysis_data_dict['customer_products_sales_data'] = customer_products_sales_df
    cust_sales_analysis_data_dict['customer_products_sales_stores_data'] = customer_products_sales_stores_df
    cust_sales_analysis_data_dict['customer_sales_data'] = customer_sales_df
    cust_sales_analysis_data_dict['stores_sales_data'] = stores_sales_df
    cust_sales_analysis_data_dict['products_profits_data'] = products_profits_df
    cust_sales_analysis_data_dict['nil_purchase_customers'] = nil_purchase_customers_df
    cust_sales_analysis_data_dict['sales_exchange_rate_analysis'] = sales_exchange_rate_analysis_df
    return cust_sales_analysis_data_dict

# try #

# stores_ sales ,  --'CustomerKey': pd.Series.nunique