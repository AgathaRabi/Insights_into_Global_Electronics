import pandas as pd
from datetime import date


def CalculateAge(BirthDate):
    """

    :param BirthDate:
    :return:
    """
    print(type(BirthDate))
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
