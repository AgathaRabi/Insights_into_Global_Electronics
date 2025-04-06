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


def AverageOrderValue():
    """
    :return:
    """

## trying one function for customer analysis dataframe

def data_for_cust_sales_analysis(customers_data_cleaned, sales_data_cleaned, products_data_cleaned):
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
    # And then calculate 'Total Product Price'
    sales_details_df['Total Product Price'] = sales_details_df['Quantity'] * sales_details_df['Unit Price USD']

    # Now merge the sales details with customer and product data, to get further data as, product purchase patterns
    # .... such as most ordered product by gender
    customer_products_sales_df = sales_details_df.merge(customers_data_cleaned, on = 'CustomerKey')

    # Group the customer_product_sales_df to get sales data for each order by customers
    # This data should be helpful for getting insights such as average order value,
    # average order value by gender, age-range, etc.
    customer_sales_df = (customer_products_sales_df.groupby(['Order Number', 'CustomerKey', 'City', 'State',
                                                                         'Country', 'Continent', 'Gender', 'Age',
                                                             'AgeGroup'], observed=True, as_index=False).agg({'Total Product Price': 'sum'}))

    customer_sales_df.rename(columns={'Total Product Price': 'Order Value'}, inplace = True)

    # converting to excel for reference.
    customer_products_sales_df.to_excel('C:\\Users\\PAPPILON\\Downloads\\customer_products_sales_df_test2425AN.xlsx')
    customer_sales_df.to_excel('C:\\Users\\PAPPILON\\Downloads\\customer_sales_df_test2425AN.xlsx')

    # placing these data sets in a dictionary
    cust_sales_analysis_data_dict = {}
    cust_sales_analysis_data_dict['customer_products_sales_data'] = customer_products_sales_df
    cust_sales_analysis_data_dict['customer_sales_data'] = customer_sales_df

    return cust_sales_analysis_data_dict

# try #