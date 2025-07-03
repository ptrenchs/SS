import os
from PyPDF2 import PdfReader
import pandas as pd
from fillpdf import fillpdfs
from math import isnan


def quitar_espacions_in_fin(cadena):
    if cadena == None:
        return ''
    if cadena == '' or sum([1 for i in cadena if i == ' ']) == len(cadena):
        return cadena
    if cadena[-1] != ' ' and cadena[0] != ' ':
        return cadena
    while True:
        if cadena[-1] == ' ':
            cadena = cadena[:-1]
        if cadena[0] == ' ':
            cadena = cadena[1:]
        if cadena[-1] != ' ' and cadena[0] != ' ':
            break
    return cadena

def extrac_var(ruta):
    reader = PdfReader(ruta)
    fields = reader.get_fields()
    campo_dict = {}
    for name, field in fields.items():
        campo_dict[name] = {
            "tipo": field.get("/FT"),  # Tipo de campo (e.g., /Tx para texto)
            "valor_defecto": field.get("/V"),
            "opciones": field.get("/Opt")
        }

    return campo_dict




def rellenar_pdf(PDF_TEMPLATE, OUTPUT_PDF, df):


    from_fields = fillpdfs.get_form_fields(PDF_TEMPLATE)
    dic = extrac_var(PDF_TEMPLATE)

    datos = df.values
    dic_pdf = {i[0]: i[1] for i in datos}
    dic_rellenado = {}
    dic_1 = {}
    for campo, info in from_fields.items():
        tipo = dic[campo]['tipo']
        info_def = quitar_espacions_in_fin(info)
        if tipo == '/Tx':
            valor_def = quitar_espacions_in_fin(dic[campo]['valor_defecto'])
            # print(valor_def)
            for d_p in dic_pdf:
                if valor_def == quitar_espacions_in_fin(d_p):
                    break
            if valor_def == quitar_espacions_in_fin(d_p):
                if type(dic_pdf[d_p]) == str:
                    dic_rellenado = dic_rellenado | {campo: f'{dic_pdf[d_p]}'}
                elif str(dic_pdf[d_p]).lower() == 'nan':
                    dic_rellenado = dic_rellenado | {campo: f'{valor_def} vacio'}
                else:
                    dic_rellenado = dic_rellenado | {campo: f'{dic_pdf[d_p]}'}

            else:
                dic_rellenado = dic_rellenado | {campo: valor_def}





    fillpdfs.write_fillable_pdf(input_pdf_path=PDF_TEMPLATE, output_pdf_path=OUTPUT_PDF, data_dict=dic_rellenado)

    os.remove(PDF_TEMPLATE)  # Elimina el original si ya no lo necesitas



def rellenar_all(ruta_excel,rutas_pdf):
    df = pd.read_excel(ruta_excel)
    for rc in rutas_pdf:
        if rc.endswith('.pdf'):
            print(rc)
            carpeta_rellena = os.path.dirname(rc) + '/' + 'PDF_rellenado'
            if not os.path.exists(carpeta_rellena):
                os.makedirs(carpeta_rellena)

            OUTPUT_PDF = os.path.join(carpeta_rellena, os.path.basename(rc))

            rellenar_pdf(rc,OUTPUT_PDF,df)
    os.remove(ruta_excel)
    return carpeta_rellena