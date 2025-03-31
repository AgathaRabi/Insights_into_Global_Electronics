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

