import pandas as pd
import numpy as np
from math import isnan
from funciones import Directorio
import os

def df2dict(df):
    col = df.columns
    data = df.values
    return dict(zip(col,[[str_2_float(j) for j in i] for i in np.transpose(data)]))
def transpuesta(matriz):
    return list(map(list, zip(*matriz)))

def str_2_float(str_,no_nan = True):
    if type(str_) == float or type(str_) == int:
        if isnan(str_) and no_nan:
            return ''
        else:
            return float(str_)
        return str_
    if  (str_.replace(',','.')).isdigit():
        return float(str_)
    else:
        return str_

# I = 60
def fusibles_cables(I):
    ruta_archivo = os.path.abspath(__file__)
    ruta_dir = Directorio.obtener_derectorio(directori='SS',ruta=ruta_archivo)

    dfs = pd.read_excel(ruta_dir + '/Excels/cables.xlsx',sheet_name=None)
    df_f = dfs['fusibles']

    I_adm_fus = df_f['Fusibles (A)']

    for i,iaf in enumerate(I_adm_fus):
        if I < iaf:
            break
    # print(f'Se reuiqre de un fusible de {iaf} ya que hay una inteidad de {I}')
    df_c = dfs['cables']

    dic_c = df2dict(df_c)
    # display(pd.DataFrame(dic_c))
    key = 'mono'

    if 'tri' in key.lower():
        key = 'I(XLPE3)'
    if 'mono' in key.lower():
        key = 'I(XLPE2)'

    I_adm_cable = dic_c[key]

    for i,iac in enumerate(I_adm_cable):
        if iaf < iac:
            break
    area = dic_c['area (mm^2)'][i]
    # print()
    # print(f'La seccion del cable es de {area} mm^2 con una intensidad de {iac} porque el fusible no salte {iaf} ya que se trabaja {I}')
    return area,iaf