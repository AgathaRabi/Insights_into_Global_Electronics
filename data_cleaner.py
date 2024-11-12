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

def customer_data_clean(df, date_format, state_name):

    """

    :param customers_data:
            is the data frame on which the following specific cleaning steps are done.
    :param date_format:
            the date format is not uniform. The format is to be made uniform.
    :param state_name:
            some state names have gaps others '-', replacing '-' with ' '.
    :return:
    """

    df['Birthday'] = df['Birthday'].apply(lambda x: pd.to_datetime(x).strftime('%d/%m/%y'))
    df['State'] = df['State'].str.replace('-', " ")

