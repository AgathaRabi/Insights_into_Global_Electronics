import pandas as pd
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

def customer_analysis_details(customers_data, sales_data, products_data):
    """

    :param customers_data:
    :param sales_data:
    :param products_data:
    :return:
    """
    customers_data['Age'] = customers_data['BirthDate'].apply(CalculateAge)
    sales_data.merge(products_data, on='ProductKey')
    sales_data['Total Product Price'] = sales_data['Quantity'] * sales_data['Unit Price USD']
    df = sales_data.merge(customers_data, on = 'CustomerKey')
    df = df.groupby(['CustomerKey', 'City', 'State', 'Continent', 'Age']).agg({'Order Number': ['nunique'],
                                                                               'Total Product Price': ['sum']})

    return df