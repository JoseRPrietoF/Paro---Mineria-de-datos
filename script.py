import pandas as pd
import numpy as np
import os, datetime, json, time, io
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

path = "data/"
codificacion = 'cp1252'
index = ['cod_mes',
             'mes',
             'cod_CA', # 2
             'CA',
             'cod_prov',
             'prov',
             'cod_mun', #6
             'mun', # 7
             'tot_paro_registrado',
             'paro_edad_hombre25',
             'paro_edad_hombre25_45',
             'paro_edad_hombre45M',
             'paro_edad_mujer25',
             'paro_edad_mujer25_45',
             'paro_edad_mujer45M',
             'paro_agro',
             'paro_industria',
             'paro_construccion',
             'paro_servicios',
             'paro_sin_empleo_anterior',
             ]
"""Cada columna es un mes a partir del 2006"""
# el dataset actual llega hasta mayo de 2017, este incluido
def merge_csv(path, dato="tot_paro_registrado", dir = "results",file_name_dest=None):
    if file_name_dest is None:
        path_destino  = os.path.join(dir, dato+".csv")
    else:
        path_destino  = os.path.join(dir, file_name_dest+".csv")
    cod_com_valenciana = 10

    lst = os.listdir(path)
    lst.sort()
    res_municipios_total = dict()
    mes = []
    for file_name in lst:
        if not file_name.endswith(".csv"):
            continue
        filepath = os.path.join(path, file_name)
        print("Filepath %s " % filepath)
        df = pd.read_csv(filepath, sep=';', encoding=codificacion, error_bad_lines=False)
        df.columns = index
        df = df[df['cod_CA'] == cod_com_valenciana]

        total_paro_reg = df[['mun',dato,'mes']]

        paro =  total_paro_reg[dato]
        municipios = total_paro_reg['mun']
        meses = total_paro_reg['mes']
        mes.extend(meses.tolist())
        res_municipios_total = copy_into_dict(res_municipios_total, municipios.tolist(), paro.tolist())

    print(res_municipios_total)
    print(len(res_municipios_total["Cullera"]))
    res_municipios_total = create_dataframe(res_municipios_total)
    print(res_municipios_total)
    if not os.path.isdir(dir):
        os.mkdir(dir)
    res_municipios_total_csv = res_municipios_total.to_csv(path_destino, sep=',', encoding='utf-8',header=True)

    return res_municipios_total_csv,res_municipios_total,df

"""Se Espera un dict:
keys = municipio
value = lista de enteros que indican su paro, cada valor es un mes a partir del 2006"""
def create_dataframe(d={}):
    m = datetime.datetime(2006, 1, 1)
    array_months = []
    name_random = list(d.keys())[0]
    long = d[name_random]
    for i in range(len(long)):
        #print(m)
        array_months.append(m)
        m = m + relativedelta(months=1)

    df = pd.DataFrame(columns=array_months)
    print(array_months)
    print(len(array_months))
    for k in d.keys():
        a = d[k]
        df.loc[k] = a

    print(df)
    return df

"""Mezcla los K / V en el diccionario
keys = lista de municipios
values = lista de paro por municipio, tienen que coincidir con los municipios y su posicion
los valores del diccionario son listas
resultado: {"Municipio_1": [12,14,15,01,98],
            "Municipio_2": [14,52, 3, 4, 5]}"""
def copy_into_dict(d=dict(), keys="",values=[]):
    for i in range(len(keys)):
        arr = d.get(keys[i],[])
        # arr = array de municipios
        arr.append(values[i])
        d[keys[i]] = arr
    return d

"""Creacion de csv con codigo_municipio:municipio"""
def codigos_municipios(df, dir = "results",file_name_dest=None):
    if file_name_dest is None:
        path_destino  = os.path.join(dir, "codigos_municipios.csv")
    else:
        path_destino  = os.path.join(dir, file_name_dest+".csv")
    interes = df[['cod_mun','mun']]
    print("-"*100)
    print(interes)
    interes.to_csv(path_destino, sep=',', encoding='utf-8', header=True,index=False)

csv, df, df_all = merge_csv(path, file_name_dest="tot_paro_registrado_comas")

codigos_municipios(df_all)
"""
row = df.loc['Ondara']
row.plot(kind='bar')
plt.legend(loc=4)
plt.xlabel('Fechas')
plt.ylabel('Paro total registrado')
plt.show()
"""