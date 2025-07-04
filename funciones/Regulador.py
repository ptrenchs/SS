import pandas as pd
import numpy as np
from math import isnan
from funciones import Directorio,Fusibles_Cables
import os

def df2dict(df):
    col = df.columns
    data = df.values
    return dict(zip(col,[[float(j) for j in i if not isnan(j)] for i in np.transpose(data)]))
def transpuesta(matriz):
    return list(map(list, zip(*matriz)))



def all_reguladores(num_pan, V_co_pan, I_pan, P_pan):

    ruta_archivo = os.path.abspath(__file__)
    ruta_dir = Directorio.obtener_derectorio(directori='SS',ruta=ruta_archivo)
    
    dfs = pd.read_excel(ruta_dir + '/Excels/Reguladores.xlsx',sheet_name=None)
    V_admisible = [i for i in dfs['V_admisible']['V_admisible'].values]
    I_admisible = df2dict(dfs['I_admisible'])

    P_admisible = df2dict(dfs['P_admisible'])


    P_pan_all = num_pan * P_pan
    for v in V_admisible:
        num_string = 1
        while True:

            if num_pan % num_string == 0:
                # print(num_pan, num_string)
                n_pan_str = num_pan / num_string
                v_string = n_pan_str * V_co_pan
                if v_string <v :
                    # print(f'numero de strings {num_string}')
                    # print(v,v_string)
                    I_adm = I_admisible[[i for i in I_admisible if str(v) in i][0]]
                    # print(I_adm)
                    i_all = num_string * I_pan
                    for ia in I_adm:
                        # print(f'{v}/{ia}')
                        # print(ia,i_all)
                        if i_all < ia:

                            # print(f'{int(v)}/{int(ia)}',[i for i in P_admisible if f'{int(v)}/{int(ia)}' in i],P_pan_all)
                            # print(f'{int(v)}/{int(ia)}')
                            P_adm = P_admisible[[i for i in P_admisible if f'{int(v)}/{int(ia)}' in i][0]]
                            for pa in P_adm:
                                # print(P_pan_all,pa)
                                if pa > P_pan_all:
                                    area_a,iaf_a = Fusibles_Cables.fusibles_cables(i_all)
                                    dic_f_a = pd.DataFrame({'Fusibles(A)':[iaf_a], 'Cable (mm^2)':[area_a], 'Intensidad':[i_all]})
                                    df_sol = pd.DataFrame(dict(zip(['Variables','Tensiones','Intensidades', 'Potencias'],transpuesta([['Lo que entra en regulador',v_string,i_all,P_pan_all],['Especificaciones egulador',v,ia,pa]]))))
                                    area_d,iaf_d = Fusibles_Cables.fusibles_cables(ia)
                                    dic_f_d = pd.DataFrame({'Fusibles(A)':[iaf_d], 'Cable (mm^2)':[area_d], 'Intensidad':[ia]})
                                    try:
                                        print('Fusibles y cables antes del regulador')
                                        display(dic_f_a)
                                        print('\nCaracteristicas regulador')
                                        display(df_sol)
                                        print('\nFusibles y cables antes del regulador')
                                        display(dic_f_d)
                                    except:
                                        print('\nFusibles y cables antes del regulador')
                                        print(dic_f_a)
                                        print('\nCaracteristicas regulador')
                                        print(df_sol)
                                        print('\nFusibles y cables antes del regulador')
                                        print(dic_f_d)
                                    print(f'String {num_string} de {int(n_pan_str)} placas con un iversor de {int(v)}/{int(ia)} y potencia de {pa}')
                                    print(f'Antes del regulador se requiere de un fusible {iaf_a} y un cable de {area_a} mm^2')
                                    print(f'Despues del regulador se requiere de un fusible {iaf_d} y un cable de {area_d} mm^2')
                                    print(75*'-')
                                    print()
                                    print(75*'-')
                                    break
                        # if pa > P_pan_all:
                        #     break
                    # if pa > P_pan_all:
                    #         break
                if num_pan == num_string:
                    break
            # print(num_string)
            num_string += 1