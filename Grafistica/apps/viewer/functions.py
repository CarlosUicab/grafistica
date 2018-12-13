import pandas as pd
import json

def excel_to_json(excel_model):
    df = pd.read_excel(excel_model.file.path)
    json_table = df.to_json(orient='table')
    return json_table


def json_to_dataframe(json_value):
    """
    Convertimos el json en dataframe
    :param excel_model:
    :return:
    """
    df = pd.read_json(json_value, orient='table')
    # # #maximo
    # print(df['EDAD'].max())
    # #promedio
    # print(df['EDAD'].mean())
    # #minimo
    # print(df['EDAD'].min())
    # #mediana
    # print(df['EDAD'].median())
    # #varianza
    # print(df['EDAD'].var())
    # #desviacion estandar
    # print(df['EDAD'].std())
    # #desviacion estandar
    # print(df['EDAD'].mode())
    # #agrupación
    # print(df.groupby(['APELLIDOS',])['EDAD'].sum())
    # # print(df)
    return df

