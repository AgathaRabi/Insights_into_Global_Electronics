import pandas as pd


def clean_data(df, fill_values_dict):

    """
    Fumction to perform standard clean operations on the data.

    :param df:
        The data to clean
    :param fill_value:
        The value to fill in NA values
    :return:
    """

    # Drop duplicates in data
    df.drop_duplicates(inplace=True)

    # Fill the NA values
    df.fillna(value=fill_values_dict, inplace=True)

    # return the cleaned data
    return df

def customer_data_clean(df):

    """

    :param df (data frame) - (customers_data)
            is the data frame on which the following specific cleaning steps are done.

    birthday : the date format is not uniform. The format is to be made uniform. the format is to
            be such that, age can be calculated
    state_name:
            some state names have gaps others '-', replacing '-' with ' '.
    :return: returns cleaned data
    """

    #df['Birthday'] = df['Birthday'].apply(lambda x: pd.to_datetime(x).strftime('%d/%m/%y'))
    #df['Birthday'] = df['Birthday'].apply(lambda x: pd.to_datetime(x, format = "%d/%m/%Y"))
    #df['Birthday'] = df['Birthday'].apply(lambda x: pd.to_datetime(x, format= "ISO8601" ))
    df['Birthday'] = df['Birthday'].apply(lambda x: pd.to_datetime(x, format="mixed"))
    df['State'] = df['State'].str.replace('-', " ")
    #df.to_excel('test_clean_cust.xlsx')
    #df.to_excel('C:\\Users\\PAPPILON\\Downloads\\test_clean_cust.xlsx')

    return df

def sales_data_clean(df):
    """

    :param : df:
    :return:
    """

    df['Order Date'] = df['Order Date'].apply(lambda x: pd.to_datetime(x).strftime('%d/%m/%y'))
    df['Delivery Date'] = df['Delivery Date'].fillna(0)
    df['Delivery Date'] = df['Delivery Date'].apply(
        lambda x: pd.to_datetime(x).strftime('%d/%m/%y') if x != 0 else x)

    return df

def products_data_clean(df):
    """

    :param df:
    :return:
    """
    #df['Unit Cost USD'] = df['Unit Cost USD'].str.replace('$', "", ',',"").astype(float)
    df['Unit Cost USD'] = df['Unit Cost USD'].apply(lambda x: x.replace('$', '').replace(',', ''))
    df['Unit Cost USD'] = df['Unit Cost USD'].astype(float)

    #df['Unit Price USD'] = df['Unit Price USD'].str.replace('$', "").astype(float)
    df['Unit Price USD'] = df['Unit Price USD'].apply(lambda x: x.replace('$', '').replace(',', ''))
    df['Unit Price USD'] = df['Unit Price USD'].astype(float)

    return df

def stores_data_clean(df):
    """

    :param df:

    :return:
    """
    df['Open Date'] = df['Open Date'].apply(lambda x : pd.to_datetime(x).strftime('%d/%m/%y'))

    return df

def exchange_rates_data_clean(df):
    """

    :param df:
    :return:
    """

    df['Date'] = df['Date'].apply(lambda x: pd.to_datetime(x).strftime('%d/%m/%y'))

    return df


