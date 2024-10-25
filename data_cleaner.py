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




