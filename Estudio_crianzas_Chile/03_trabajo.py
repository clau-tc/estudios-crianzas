import pandas as pd
import os
import re
# os.getcwd()
os.chdir('/home/clautc/Proyectos_/CrianzasChile')

columnas = ['ano_trimestre', 'mes_central', 'ano_encuesta', 'estrato', 'id_directorio', 'id_identificacion',
            'hogar', 'idrph', 'nro_linea', 'edad', 'sexo', 'parentesco', 'cine', 'est_conyugal', 'proveedor',
            'habituales', 'efectivas', 'e17',  'activ', 'cae_especifico', 'categoria_ocupacion',
            'fact', 'fact_cal']

col_2017 = ['ano_trimestre', 'mes_central', 'ano_encuesta', 'estrato', 'conglomerado', 'id_identificacion',
            'hogar', 'idrph', 'nro_linea', 'edad', 'sexo', 'parentesco', 'cine', 'est_conyugal', 'proveedor',
            'habituales', 'efectivas', 'e17', 'activ', 'cae_especifico', 'categoria_ocupacion',
            'fact_cal']
anios = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
finrut = ['-02-efm.sav', '-05-amj.sav', '-08-jas.sav', '-11-ond.sav']
for a in anios:
    ru = str(a)
    if re.search('201[789]', ru) or re.search('202[012]', ru):
        print('verdadero')
    else:
        print('falso')
    # Creando rutas
rutas = []
for a in anios:
    for f in finrut:
        r = 'data/ene/ene-' + str(a) + f
        rutas.append(r)

# Comprobando que las variables se nombren igual en todas las bd
for ru in rutas:
    if re.search('201[789]', ru) or re.search('202[012]', ru):
        df = pd.read_spss(ru)
        print(ru)
        print((df.columns.intersection(col_2017).to_list() == col_2017))
    else:
        df = pd.read_spss(ru)
        print(ru)
        print((df.columns.intersection(columnas).to_list() == columnas))



