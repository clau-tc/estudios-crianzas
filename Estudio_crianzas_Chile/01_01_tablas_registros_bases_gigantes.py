import gc
import os
import sys
import pandas as pd

os.chdir('/home/clautc/Proyectos_/Estudios/Estudio_crianzas_Chile')
sys.path.append('/home/clautc/Proyectos_/Estudios/Estudio_crianzas_Chile')

def subset_bases_gigantes(ruta_bg, lista_var, ruta_guardar):
    size = 1000000
    lista_dfs = []
    for ruta in ruta_bg:
        df = pd.read_csv(ruta,
                         index_col=False,
                         encoding='latin-1',
                         sep=';',
                         low_memory=False, chunksize=size)
        lista_dfs.append(df)

    header = True
    for df in lista_dfs:
        for chunk in df:
            chunk.columns = chunk.columns.str.lower()
            if sum(chunk.columns.isin(lista_var))==len(lista_var):
                # chunk['grupo_etario_padre'] = chunk['grupo_etario_padre'].str.strip()
                # chunk.loc[chunk['grupo_etario_madre'] == 'MENORES 15 AÑO', 'grupo_etario_madre'] = 'MENORES 15 AÑOS'
                # chunk['ano_nac'] = pd.to_datetime(chunk['ano_nac'], format='%Y')
                chunk_filter = chunk[lista_var]
                chunk_filter = chunk_filter.reset_index(drop=True)
                chunk_filter.to_csv(ruta_guardar, header=header, mode='a')
                header = False
            else:
                print('No existen {}'.format(lista_var))
        continue
    if os.path.exists(ruta_guardar):
        print('La nueva data, se guardó con éxito en: {}'.format(ruta_guardar))
    gc.collect()


lista_var1 = ['ano_nac', 'grupo_etario_padre', 'grupo_etario_madre']
lista_var2 = ['ano_nac', 'nivel_madre', 'nivel_padre']
lista_var3 = ['ano_nac', 'activ_madre', 'activ_padre', 'ocupa_padre', 'ocupa_madre', 'categ_padre', 'categ_madre']
lista_var4 = ['ano_nac', 'est_civ_madre', 'region_residencia', 'glosa_region_residencia', 'grupo_etario_madre']
ruta1 = 'data/registros_estadisticos/df_edades.csv'
ruta2 = 'data/registros_estadisticos/df_educa.csv'
ruta3 = 'data/registros_estadisticos/df_trabajo.csv'
ruta4 = 'data/registros_estadisticos/df_geograf.csv'
ruta_bg = ['data/registros_estadisticos/Serie_Nacimientos_1992_2000.csv',
           'data/registros_estadisticos/Serie_Nacimientos_2001_2019.csv']

subset_bases_gigantes(ruta_bg=ruta_bg, lista_var=lista_var1, ruta_guardar=ruta1)
subset_bases_gigantes(ruta_bg=ruta_bg, lista_var=lista_var2, ruta_guardar=ruta2)
subset_bases_gigantes(ruta_bg=ruta_bg, lista_var=lista_var3, ruta_guardar=ruta3)
subset_bases_gigantes(ruta_bg=ruta_bg, lista_var=lista_var4, ruta_guardar=ruta4)

#
# header2 = True
# for df in lista_dfs:
#     for chunk in df:
#         chunk.columns = chunk.columns.str.lower()
#         chunk_filter = chunk[['ano_nac', 'nivel_madre', 'nivel_padre']]
#         chunk_filter = chunk_filter.reset_index()
#         chunk_filter.to_csv('data/registros_estadisticos/df_educacion.csv', header=header2, mode='a')
#         header2 = False
#
# gc.collect()
#
# header3 = True
# for df in lista_dfs:
#     for chunk in df:
#         chunk.columns = chunk.columns.str.lower()
#         chunk_filter = chunk[['ano_nac', 'activ_madre', 'activ_padre', 'ocupa_padre', 'ocupa_madre', 'categ_padre',
#                               'categ_madre']]
#         chunk_filter = chunk_filter.reset_index()
#         chunk_filter.to_csv('data/registros_estadisticos/df_trabajo.csv', header=header3, mode='a')
#         header3 = False
#
# header4 = True
# for df in lista_dfs:
#     for chunk in df:
#         chunk.columns = chunk.columns.str.lower()
#         chunk_filter = chunk[['ano_nac', 'est_civ_madre', 'region_residencia', 'glosa_region_residencia']]
#         chunk_filter = chunk_filter.reset_index()
#         chunk_filter.to_csv('data/registros_estadisticos/df_estado_civil_region.csv', header=header4, mode='a')
#         header4 = False
