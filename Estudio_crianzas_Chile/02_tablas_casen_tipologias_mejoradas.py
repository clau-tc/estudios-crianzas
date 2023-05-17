import pandas as pd
import numpy as np
from samplics.categorical import Tabulation, CrossTabulation
import os
import gc

os.chdir('/home/clautc/Proyectos_/CrianzasChile')

anios = []
for n in range(1990, 2000, 2):
    anios.append(n)
for n in range(2000, 2010, 3):
    anios.append(n)
for n in range(2013, 2018, 2):
    anios.append(n)

anios.append(2020)
anios.remove(2006)
# anios.remove(2000)

tabla1_ = pd.DataFrame()
tabla2_ = pd.DataFrame()
tabla3_ = pd.DataFrame()
tabla4_ = pd.DataFrame()
tabla5_ = pd.DataFrame()
tabla6_ = pd.DataFrame()
tabla7_ = pd.DataFrame()

stat1_ = pd.DataFrame()
stat2_ = pd.DataFrame()
stat3_ = pd.DataFrame()
stat4_ = pd.DataFrame()
stat5_ = pd.DataFrame()
stat6_ = pd.DataFrame()
stat7_ = pd.DataFrame()

rutas = []
for a in anios:
    ru = 'data/casen/casen' + str(a) + '.sav'
    rutas.append(ru)

vars_hogares = {
    1990: ['r', 'p', 'c', 'z', 'f'],
    1992: ['r', 'p', 'c', 'z', 'f'],
    1994: ['r', 'p', 'c', 'z', 'seg', 'f'],
    1996: ['r', 'p', 'c', 'z', 'seg', 'f'],
    1998: ['segmento', 'f'],
    2000: ['segmento', 'folio'],
    2003: ['segmento', 'f'],
    2006: ['seg', 'f'],
    2009: ['idviv', 'folio'],
    2013: ['folio'],
    2015: ['folio'],
    2017: ['folio'],
    2020: ['folio']

}

vars_filtro = {
    1990: ['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr'],
    1992: ['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr'],
    1994: ['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr'],
    1996: ['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr'],
    1998: ['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr', 'segmento', 'estrato'],
    2000: ['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr', 'segmento', 'estrato'],
    2003: ['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr', 'segmento', 'estrato'],
    2006: ['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr', 'seg', 'estrato'],
    2009: ['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr', 'segmento', 'estrato'],
    2013: ['sexojefat', 'menores_18', 'thogar', 'pobreza_mn', 'qaut_mn', 'expr', 'varunit', 'varstrat'],
    2015: ['sexojefat', 'menores_18', 'thogar', 'pobreza', 'qaut', 'expr', 'varunit', 'varstrat'],
    2017: ['sexojefat', 'menores_18', 'thogar', 'pobreza', 'qaut', 'expr', 'varunit', 'varstrat'],
    2020: ['sexojefat', 'menores_18', 'thogar', 'pobreza', 'qaut', 'expr', 'varunit', 'varstrat']

}

vars_filtro_remplazo = {
    6: ['sexojefat', 'menores_18', 'thogar', 'pobrez', 'qaut', 'expr'],
    8: ['sexojefat', 'menores_18', 'thogar', 'pobrez', 'qaut', 'expr', 'varunit', 'varstrat']
}

regex_pareja = {
    1990: '^c[oó]',
    1992: '^c[oó]',
    1994: '^c[oó]',
    1996: '^c[oó]',
    1998: '^c[oó]',
    2000: '^c[oó]',
    2003: '^c[oó]',
    2006: '^c[oó]',
    2009: '^[e]s.*',
    2013: '^[e]s.*',
    2015: '^[ce].*xo$',
    2017: '^[ce].*xo$',
    2020: '^[ce].*xo$'
}


def crear_var_personas_menores(df, vars_hogar, nombre_var_edad, nombre_var_creada, n_excluyente):
    df = df.copy()
    df['aux'] = 0
    if df[nombre_var_edad].dtype == 'category':
        df['edad'] = df.edad.cat.codes
        df.loc[:, nombre_var_edad] = df[nombre_var_edad].astype('int')
    df.loc[:, nombre_var_edad] = df[nombre_var_edad].astype('int')
    df.loc[df[nombre_var_edad] < n_excluyente, 'aux'] = 1
    agrupada = df.groupby(vars_hogar)
    total_hogares = len(agrupada)
    df[nombre_var_creada] = agrupada[['aux']].transform('max')
    # validación creación variable
    df_val = pd.crosstab(df[nombre_var_edad], df['aux']).reset_index()
    df_val.columns = ['edad', 'mayor17', 'menor18']
    df = df.drop(columns='aux')
    print('La validación variable edad es: {}'.format((df_val.loc[df_val.edad < 18, 'menor18'] > 0).all() & (
            df_val.loc[df_val.edad > 17, 'mayor17'] > 0).all()))
    return df


def crear_var_tipos_hogar(df, var_parentesco='pco1',
                          var_parentesco_nu='pco2',
                          var_nucleos='nucleo',
                          var_numero_personas='numper',
                          nombre_var_creada='thogar',
                          regex_jefatura='^je.*',
                          regex_pareja=''):
    # se crea un indicador de numero de nucleos
    df = df.copy()
    df['aux_nucleo'] = 0
    df.loc[df[var_parentesco_nu].str.lower().str.match('^jef') & (df[var_nucleos] != 0), 'aux_nucleo'] = 1
    df['nnucleo'] = df.groupby(vars_hogares[anios[r]])[['aux_nucleo']].transform('sum')
    df.drop(columns='aux_nucleo', inplace=True)
    print('este proceso crea variable cantidad de nucleos por hogar')

    # se construye variable pareja para identificar si el hogar cuenta con parejas
    df['aux_pareja'] = 0
    df.loc[df[var_parentesco].str.lower().str.match(regex_pareja), 'aux_pareja'] = 1
    df['pareja'] = 0
    df['pareja'] = df.groupby(vars_hogares[anios[r]])[['aux_pareja']].transform('max')
    print('este proceso crea variable existencia de parejas en el hogar por hogar')
    df['sexo_jf'] = 0
    df.loc[(df.sexo.str.match('^M')) & (df[var_parentesco].str.lower().str.match('^je')), 'sexo_jf'] = 1
    df['sexojefat'] = df.groupby(vars_hogares[anios[r]])[['sexo_jf']].transform('max')
    df = df.drop(columns=['aux_pareja', 'sexo_jf'])
    print('este proceso crea variable existencia jefatura femenina en el hogar')

    df[nombre_var_creada] = 0
    df.loc[df[var_numero_personas] == 1, nombre_var_creada] = 1  # unipersonal
    df.loc[(df[var_numero_personas] > 1) & (df.pareja == 0) & (
                df.nnucleo == 1), nombre_var_creada] = 2  # nuclear monoparental
    df.loc[(df[var_numero_personas] > 1) & (df.pareja == 1) & (
                df.nnucleo == 1), nombre_var_creada] = 3  # nuclear biparental
    df.loc[(df[var_numero_personas] > 1) & (df.pareja == 0) & (
                df.nnucleo > 1), nombre_var_creada] = 4  # extenso monoparental
    df.loc[(df[var_numero_personas] > 1) & (df.pareja == 1) & (
                df.nnucleo > 1), nombre_var_creada] = 5  # extenso biparental
    df.loc[(df[var_numero_personas] != 1) & (df.nnucleo == df[var_numero_personas]), nombre_var_creada] = 6  # sin nucle

    if len(df[nombre_var_creada].unique()) == 6:
        print('La tipología tiene seis valores')
    else:
        print('la tipologia tiene: {}'.format(len(df[nombre_var_creada].unique())))
    return df


def columnas_tabla(tabla, ntabla, est, a):
    tabla = tabla.copy()
    n = ntabla
    if n == 1:
        tabla.columns = ['sexo_jefatura', 'menor_18', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']

    if n == 2:
        tabla.columns = ['quintil', 'menor_18', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']

    if n == 3:
        tabla.columns = ['pobreza', 'menor_18', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']

    if n == 4:
        tabla.columns = ['thogar', 'menor_18', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']

    if n == 5:
        tabla.columns = ['thogar', 'sexo_jefatura', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']

    if n == 6:
        tabla.columns = ['thogar', 'pobreza', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']

    if n == 7:
        tabla.columns = ['thogar', 'quintil', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']

    if est == 'proporcion':
        tabla['tipo_est'] = 'proporcion'
        tabla['dato'] = round(tabla.dato * 100, 1)
    else:
        tabla['tipo_est'] = 'conteo'

    tabla['anio'] = a
    return tabla


def sexo(tabla):
    tabla.sexo_jefatura = pd.to_numeric(tabla.sexo_jefatura)
    print(tabla.sexo_jefatura.unique())
    tabla.loc[tabla.sexo_jefatura == 1, 'sexo_jefatura'] = 'mujer'
    tabla.loc[tabla.sexo_jefatura == 0, 'sexo_jefatura'] = 'hombre'



def menores(tabla):
    tabla.menor_18 = pd.to_numeric(tabla.menor_18)
    print(tabla.menor_18.unique())
    tabla.loc[tabla.menor_18 == 1, 'menor_18'] = 'con menores'
    tabla.loc[tabla.menor_18 == 0, 'menor_18'] = 'sin menores'


def quintil(tabla):
    tabla.quintil = pd.to_numeric(tabla.quintil)
    print('quintil')
    print(tabla.quintil.unique())
    if (len(tabla.quintil.unique()) == 5) & (tabla.quintil.min() == 1):
        print('tiene cinco valores unicos y comienza desde el 1')
        tabla.quintil = tabla.quintil
        tabla.loc[tabla.quintil == 1, 'quintil'] = 'I'
        tabla.loc[tabla.quintil == 2, 'quintil'] = 'II'
        tabla.loc[tabla.quintil == 3, 'quintil'] = 'III'
        tabla.loc[tabla.quintil == 4, 'quintil'] = 'IV'
        tabla.loc[tabla.quintil == 5, 'quintil'] = 'V'
    else:
        tabla.quintil = tabla.quintil + 1
        tabla.loc[tabla.quintil == 1, 'quintil'] = 'I'
        tabla.loc[tabla.quintil == 2, 'quintil'] = 'II'
        tabla.loc[tabla.quintil == 3, 'quintil'] = 'III'
        tabla.loc[tabla.quintil == 4, 'quintil'] = 'IV'
        tabla.loc[tabla.quintil == 5, 'quintil'] = 'V'

def pobreza(tabla):
    print('pobreza')
    print(tabla.pobreza.unique())
    tabla.pobreza = pd.to_numeric(tabla.pobreza)
    tabla.loc[tabla.pobreza == 0, 'pobreza'] = 'no pobre'
    tabla.loc[tabla.pobreza == 1, 'pobreza'] = 'pobre extremo'
    tabla.loc[tabla.pobreza == 2, 'pobreza'] = 'pobre no extremo'


def hogares(tabla):
    tabla.thogar = pd.to_numeric(tabla.thogar)
    tabla.loc[tabla.thogar == 1, 'thogar'] = 'unipersonal'
    tabla.loc[tabla.thogar == 2, 'thogar'] = 'nuclear monoparental'
    tabla.loc[tabla.thogar == 3, 'thogar'] = 'nuclear biparental'
    tabla.loc[tabla.thogar == 4, 'thogar'] = 'extenso monoparental'
    tabla.loc[tabla.thogar == 5, 'thogar'] = 'extenso biparental'
    tabla.loc[tabla.thogar == 6, 'thogar'] = 'sin nucleo'


def etiquetar_tablas(tabla, n):
    n = n
    tabla = tabla
    if n == 1:
        sexo(tabla)
        menores(tabla)
    elif n == 2:
        quintil(tabla)
        menores(tabla)
    elif n == 3:
        pobreza(tabla)
        menores(tabla)
    elif n == 4:
        hogares(tabla)
        menores(tabla)
    elif n == 5:
        hogares(tabla)
        sexo(tabla)
    elif n == 6:
        hogares(tabla)
        pobreza(tabla)
    elif n == 7:
        quintil(tabla)
        hogares(tabla)
    return tabla

def crear_info_stats(tabla, n, nombres_sep, ani):
    df_stat = pd.DataFrame(tabla.stats)
    df_stat['tipo_est'] = tabla.parameter
    df_stat['anio'] = ani
    df_stat['prueba'] = nombres_sep
    df_stat = df_stat.reset_index(drop=True)
    return df_stat

for r in range(len(rutas)):
    print('trabajando con: {}'.format(anios[r]))
    df = pd.read_spss(rutas[r])
    df.columns = df.columns.str.lower()
    total_hogares = len(df.groupby(vars_hogares[anios[r]]))
    print('Total muestral de hogares: {}'.format(total_hogares))
    df = crear_var_personas_menores(df, vars_hogar=vars_hogares[anios[r]], nombre_var_edad='edad',
                                    nombre_var_creada='menores_18', n_excluyente=18)
    df = crear_var_tipos_hogar(df, regex_pareja=regex_pareja[anios[r]])

    df_filter = df.loc[df.pco1.str.lower().str.match('^je'), vars_filtro[anios[r]]].reset_index(drop=True)

    df_filter.columns = vars_filtro_remplazo[len(df_filter.columns)]
    if len(df_filter.columns) == 6:
        df_filter['sexojefat'] = pd.to_numeric(df_filter.sexojefat, errors='coerce')
        df_filter['menores_18'] = pd.to_numeric(df_filter.menores_18, errors='coerce')
        df_filter['thogar'] = pd.to_numeric(df_filter.thogar, errors='coerce')
        if df_filter.pobrez.dtype == 'category':
            df_filter['pobrez'] = df_filter.pobrez.cat.codes
            df_filter['pobrez'] = df_filter.pobrez.astype('int64')
        else:
            df_filter['pobrez'] = pd.to_numeric(df_filter.pobrez, errors='coerce')
        if anios[r] < 2012:
            df_filter['pobreza'] = df_filter.pobrez.replace({0:1, 1:0})
        elif anios[r]>2012:
            df_filter['pobreza'] = df_filter.pobrez
        if df_filter.qaut.dtype == 'category':
            df_filter['qaut'] = df_filter.qaut.cat.codes
            df_filter['qaut'] = df_filter.qaut.astype('int64')
            df_filter.loc[df_filter.qaut == -1, 'qaut'] = np.nan
        elif df_filter.qaut.dtype == 'float':
            df_filter['qaut'] = pd.to_numeric(df_filter.qaut, errors='coerce')
        df_filter['expr'] = pd.to_numeric(df_filter.expr)
    if len(df_filter.columns) == 8:
        df_filter['sexojefat'] = pd.to_numeric(df_filter.sexojefat, errors='coerce')
        df_filter['menores_18'] = pd.to_numeric(df_filter.menores_18, errors='coerce')
        df_filter['thogar'] = pd.to_numeric(df_filter.thogar, errors='coerce')
        if df_filter.pobrez.dtype == 'category':
            df_filter['pobrez'] = df_filter.pobrez.cat.codes
            df_filter['pobrez'] = df_filter.pobrez.astype('int64')
        else:
            df_filter['pobrez'] = pd.to_numeric(df_filter.pobrez, errors='coerce')
        if anios[r] < 2012:
            df_filter['pobreza'] = df_filter.pobrez.replace({0:1, 1:0})
        elif anios[r]>2012:
            df_filter['pobreza'] = df_filter.pobrez
        if df_filter.qaut.dtype == 'category':
            df_filter['qaut'] = df_filter.qaut.cat.codes
            df_filter['qaut'] = df_filter.qaut.astype('int64')
            df_filter.loc[df_filter.qaut == -1, 'qaut'] = np.nan
        elif df_filter.qaut.dtype == 'float':
            df_filter['qaut'] = pd.to_numeric(df_filter.qaut, errors='coerce')
        df_filter['expr'] = pd.to_numeric(df_filter.expr)
        df_filter['varunit'] = pd.to_numeric(df_filter.varunit)
        if df_filter.varstrat.dtype == 'O':
            df_filter['varstrat'] = pd.to_numeric(df_filter.varstrat)
        df_filter['varstrat'] = pd.to_numeric(df_filter.varstrat)
    guardar = 'data_intermedia/df_filter' + str(anios[r]) + '.feather'
    df_filter = df_filter.reset_index(drop=True)
    df_filter.to_feather(guardar)
    print('en el año: {}, la distribución de tipos de hogar, se observa:'.format(anios[r]))
    print(pd.crosstab(df_filter.thogar, df_filter.menores_18))
    df_filter2 = df_filter.loc[(df_filter.thogar > 1) & (df_filter.thogar < 6) & (df_filter.menores_18 == 1)]
    df_filter3 = df_filter.loc[(df_filter.thogar > 1) & (df_filter.thogar < 6)]
    if anios[r] == 2003:
        df_filter2 = df_filter2.loc[df_filter2.varstrat != 21022.]

    print('en el año: {}, se crea df_filter2 para analizar solo los tipos familiares de hogar'.format(anios[r]))

    ## creaci'on de data frames con disenio muestral

    tabla1_prop = CrossTabulation(parameter='proportion')
    tabla1_conteo = CrossTabulation(parameter='count')
    tabla2_prop = CrossTabulation(parameter='proportion')
    tabla2_conteo = CrossTabulation(parameter='count')
    tabla3_prop = CrossTabulation(parameter='proportion')
    tabla3_conteo = CrossTabulation(parameter='count')
    tabla4_prop = CrossTabulation(parameter='proportion')
    tabla4_conteo = CrossTabulation(parameter='count')
    tabla5_prop = CrossTabulation(parameter='proportion')
    tabla5_conteo = CrossTabulation(parameter='count')
    tabla6_prop = CrossTabulation(parameter='proportion')
    tabla6_conteo = CrossTabulation(parameter='count')
    tabla7_prop = CrossTabulation(parameter='proportion')
    tabla7_conteo = CrossTabulation(parameter='count')

    if df_filter.columns.isin(['varstrat']).any() & (anios[r] != 1998) & (anios[r] != 2000) & (anios[r] != 2009):
        tabla1_prop.tabulate(vars=[df_filter.sexojefat, df_filter.menores_18],
                             samp_weight=df_filter.expr,
                             stratum=df_filter.varstrat,
                             psu=df_filter.varunit,
                             remove_nan=True)

        tabla1_conteo.tabulate(vars=[df_filter.sexojefat, df_filter.menores_18],
                               samp_weight=df_filter.expr,
                               stratum=df_filter.varstrat,
                               psu=df_filter.varunit,
                               remove_nan=True)
        tabla2_prop.tabulate(vars=[df_filter.qaut, df_filter.menores_18],
                             samp_weight=df_filter.expr,
                             stratum=df_filter.varstrat,
                             psu=df_filter.varunit,
                             remove_nan=True)
        tabla2_conteo.tabulate(vars=[df_filter.qaut, df_filter.menores_18],
                               samp_weight=df_filter.expr,
                               stratum=df_filter.varstrat,
                               psu=df_filter.varunit,
                               remove_nan=True)

        tabla3_prop.tabulate(vars=[df_filter.pobreza, df_filter.menores_18],
                             samp_weight=df_filter.expr,
                             stratum=df_filter.varstrat,
                             psu=df_filter.varunit,
                             remove_nan=True)
        tabla3_conteo.tabulate(vars=[df_filter.pobreza, df_filter.menores_18],
                               samp_weight=df_filter.expr,
                               stratum=df_filter.varstrat,
                               psu=df_filter.varunit,
                               remove_nan=True)

        tabla4_prop.tabulate(vars=[df_filter3.thogar, df_filter3.menores_18],
                             samp_weight=df_filter3.expr,
                             stratum=df_filter3.varstrat,
                             psu=df_filter3.varunit,
                             remove_nan=True)
        tabla4_conteo.tabulate(vars=[df_filter3.thogar, df_filter3.menores_18],
                               samp_weight=df_filter3.expr,
                               stratum=df_filter3.varstrat,
                               psu=df_filter3.varunit,
                               remove_nan=True)

        tabla5_prop.tabulate(vars=[df_filter2.thogar, df_filter2.sexojefat],
                             samp_weight=df_filter2.expr,
                             stratum=df_filter2.varstrat,
                             psu=df_filter2.varunit,
                             remove_nan=True)
        tabla5_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.sexojefat],
                               samp_weight=df_filter2.expr,
                               stratum=df_filter2.varstrat,
                               psu=df_filter2.varunit,
                               remove_nan=True)

        tabla6_prop.tabulate(vars=[df_filter2.thogar, df_filter2.pobreza],
                             samp_weight=df_filter2.expr,
                             stratum=df_filter2.varstrat,
                             psu=df_filter2.varunit,
                             remove_nan=True)
        tabla6_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.pobreza],
                               samp_weight=df_filter2.expr,
                               stratum=df_filter2.varstrat,
                               psu=df_filter2.varunit,
                               remove_nan=True)

        tabla7_prop.tabulate(vars=[df_filter2.thogar, df_filter2.qaut],
                             samp_weight=df_filter2.expr,
                             stratum=df_filter2.varstrat,
                             psu=df_filter2.varunit,
                             remove_nan=True)
        tabla7_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.qaut],
                               samp_weight=df_filter2.expr,
                               stratum=df_filter2.varstrat,
                               psu=df_filter2.varunit,
                               remove_nan=True)

    else:
        tabla1_prop.tabulate(vars=[df_filter.sexojefat, df_filter.menores_18],
                             samp_weight=df_filter.expr,
                             # stratum=df_filter.varstrat,
                             # psu=df_filter.varunit,
                             remove_nan=True)
        tabla1_conteo.tabulate(vars=[df_filter.sexojefat, df_filter.menores_18],
                               samp_weight=df_filter.expr,
                               # stratum=df_filter.varstrat,
                               # psu=df_filter.varunit,
                               remove_nan=True)
        tabla2_prop.tabulate(vars=[df_filter.qaut, df_filter.menores_18],
                             samp_weight=df_filter.expr,
                             # stratum=df_filter.varstrat,
                             # psu=df_filter.varunit,
                             remove_nan=True)
        tabla2_conteo.tabulate(vars=[df_filter.qaut, df_filter.menores_18],
                               samp_weight=df_filter.expr,
                               # stratum=df_filter.varstrat,
                               # psu=df_filter.varunit,
                               remove_nan=True)
        tabla3_prop.tabulate(vars=[df_filter.pobreza, df_filter.menores_18],
                             samp_weight=df_filter.expr,
                             # stratum=df_filter.varstrat,
                             # psu=df_filter.varunit,
                             remove_nan=True)
        tabla3_conteo.tabulate(vars=[df_filter.pobreza, df_filter.menores_18],
                               samp_weight=df_filter.expr,
                               # stratum=df_filter.varstrat,
                               # psu=df_filter.varunit,
                               remove_nan=True)
        tabla4_prop.tabulate(vars=[df_filter3.thogar, df_filter3.menores_18],
                             samp_weight=df_filter3.expr,
                             # stratum=df_filter2.varstrat,
                             # psu=df_filter2.varunit,
                             remove_nan=True)
        tabla4_conteo.tabulate(vars=[df_filter3.thogar, df_filter3.menores_18],
                               samp_weight=df_filter3.expr,
                               # stratum=df_filter2.varstrat,
                               # psu=df_filter2.varunit,
                               remove_nan=True)
        tabla5_prop.tabulate(vars=[df_filter2.thogar, df_filter2.sexojefat],
                             samp_weight=df_filter2.expr,
                             # stratum=df_filter2.varstrat,
                             # psu=df_filter2.varunit,
                             remove_nan=True)
        tabla5_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.sexojefat],
                               samp_weight=df_filter2.expr,
                               # stratum=df_filter2.varstrat,
                               # psu=df_filter2.varunit,
                               remove_nan=True)
        tabla6_prop.tabulate(vars=[df_filter2.thogar, df_filter2.pobreza],
                             samp_weight=df_filter2.expr,
                             # stratum=df_filter2.varstrat,
                             # psu=df_filter2.varunit,
                             remove_nan=True)
        tabla6_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.pobreza],
                               samp_weight=df_filter2.expr,
                               # stratum=df_filter2.varstrat,
                               # psu=df_filter2.varunit,
                               remove_nan=True)
        tabla7_prop.tabulate(vars=[df_filter2.thogar, df_filter2.qaut],
                             samp_weight=df_filter2.expr,
                             # stratum=df_filter2.varstrat,
                             # psu=df_filter2.varunit,
                             remove_nan=True)
        tabla7_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.qaut],
                               samp_weight=df_filter2.expr,
                               # stratum=df_filter2.varstrat,
                               # psu=df_filter2.varunit,
                               remove_nan=True)
        gc.collect()
    print('anio: {}'.format(anios[r]))

    stat1_p = crear_info_stats(tabla1_prop, 1, 'sexoj_menor18', anios[r])
    stat1_c = crear_info_stats(tabla1_conteo, 1, 'sexoj_menor18', anios[r])
    stat2_p = crear_info_stats(tabla2_prop, 2, 'qaut_menor18', anios[r])
    stat2_c = crear_info_stats(tabla2_conteo, 2, 'qaut_menor18', anios[r])
    stat3_p = crear_info_stats(tabla3_prop,   3, 'pobreza_menor18', anios[r])
    stat3_c = crear_info_stats(tabla3_conteo, 3, 'pobreza_menor18', anios[r])
    stat4_p = crear_info_stats(tabla4_prop,   4, 'thogar_menor18', anios[r])
    stat4_c = crear_info_stats(tabla4_conteo, 4, 'thogar_menor18', anios[r])
    stat5_p = crear_info_stats(tabla5_prop,   5, 'thogar_sexoj', anios[r])
    stat5_c = crear_info_stats(tabla5_conteo, 5, 'thogar_sexoj', anios[r])
    stat6_p = crear_info_stats(tabla6_prop,   6, 'pobreza_menor18', anios[r])
    stat6_c = crear_info_stats(tabla6_conteo, 6, 'pobreza_menor18', anios[r])
    stat7_p = crear_info_stats(tabla7_prop,  7, 'thogar_qaut', anios[r])
    stat7_c = crear_info_stats(tabla7_conteo,7, 'thogar_qaut', anios[r])

    stat1 = pd.concat([stat1_c, stat1_p])
    stat1.reset_index(drop=True, inplace=True)
    stat1_ = pd.concat([stat1_, stat1])
    stat1_ = stat1_.reset_index(drop=True)
    stat1_.to_csv('resultados/tablas/01_stat.csv')
    stat2 = pd.concat([stat2_c, stat2_p])
    stat2.reset_index(drop=True, inplace=True)
    stat2_ = pd.concat([stat2_, stat2])
    stat2_ = stat2_.reset_index(drop=True)
    stat2_.to_csv('resultados/tablas/02_stat.csv')
    stat3 = pd.concat([stat3_c, stat3_p])
    stat3.reset_index(drop=True, inplace=True)
    stat3_ = pd.concat([stat3_, stat3])
    stat3_ = stat3_.reset_index(drop=True)
    stat3_.to_csv('resultados/tablas/03_stat.csv')
    stat4 = pd.concat([stat4_c, stat4_p])
    stat4.reset_index(drop=True, inplace=True)
    stat4_ = pd.concat([stat4_, stat4])
    stat4_ = stat4_.reset_index(drop=True)
    stat4_.to_csv('resultados/tablas/04_stat.csv')
    stat5 = pd.concat([stat5_c, stat5_p])
    stat5.reset_index(drop=True, inplace=True)
    stat5_ = pd.concat([stat5_, stat5])
    stat5_ = stat5_.reset_index(drop=True)
    stat5_.to_csv('resultados/tablas/05_stat.csv')
    stat6 = pd.concat([stat6_c, stat6_p])
    stat6.reset_index(drop=True, inplace=True)
    stat6_ = pd.concat([stat6_, stat6])
    stat6_ = stat6_.reset_index(drop=True)
    stat6_.to_csv('resultados/tablas/06_stat.csv')

    stat7 = pd.concat([stat7_c, stat7_p])
    stat7.reset_index(drop=True, inplace=True)
    stat7_ = pd.concat([stat7_, stat7])
    stat7_ = stat7_.reset_index(drop=True)
    stat7_.to_csv('resultados/tablas/07_stat.csv')


    tabla1_conteo = tabla1_conteo.to_dataframe()
    tabla1_prop = tabla1_prop.to_dataframe()
    tabla1_conteo = columnas_tabla(tabla1_conteo, ntabla=1, est='conteo', a=anios[r])
    tabla1_prop = columnas_tabla(tabla1_prop, ntabla=1, est='proporcion', a=anios[r])
    tabla1_conteo = etiquetar_tablas(tabla1_conteo, n=1)
    tabla1_prop = etiquetar_tablas(tabla1_prop, n=1)
    tabla1 = pd.concat([tabla1_conteo, tabla1_prop])
    tabla1.reset_index(drop=True, inplace=True)


    tabla2_conteo = tabla2_conteo.to_dataframe()
    tabla2_prop = tabla2_prop.to_dataframe()
    tabla2_conteo = columnas_tabla(tabla2_conteo, ntabla=2, est='conteo', a=anios[r])
    tabla2_prop = columnas_tabla(tabla2_prop, ntabla=2, est='proporcion', a=anios[r])
    tabla2_conteo = etiquetar_tablas(tabla2_conteo, n=2)
    tabla2_prop = etiquetar_tablas(tabla2_prop, n=2)
    tabla2 = pd.concat([tabla2_conteo, tabla2_prop])
    tabla2.reset_index(drop=True, inplace=True)


    tabla3_conteo = tabla3_conteo.to_dataframe()
    tabla3_prop = tabla3_prop.to_dataframe()
    tabla3_conteo = columnas_tabla(tabla3_conteo, ntabla=3, est='conteo', a=anios[r])
    tabla3_prop = columnas_tabla(tabla3_prop, ntabla=3, est='proporcion', a=anios[r])
    tabla3_conteo = etiquetar_tablas(tabla3_conteo, n=3)
    tabla3_prop = etiquetar_tablas(tabla3_prop, n=3)
    tabla3 = pd.concat([tabla3_conteo, tabla3_prop])
    tabla3.reset_index(drop=True, inplace=True)

    tabla4_conteo = tabla4_conteo.to_dataframe()
    tabla4_prop = tabla4_prop.to_dataframe()
    tabla4_conteo = columnas_tabla(tabla4_conteo, ntabla=4, est='conteo', a=anios[r])
    tabla4_prop = columnas_tabla(tabla4_prop, ntabla=4, est='proporcion', a=anios[r])
    tabla4_conteo = etiquetar_tablas(tabla4_conteo, n=4)
    tabla4_prop = etiquetar_tablas(tabla4_prop, n=4)
    tabla4 = pd.concat([tabla4_conteo, tabla4_prop])
    tabla4.reset_index(drop=True, inplace=True)

    tabla5_conteo = tabla5_conteo.to_dataframe()
    tabla5_prop = tabla5_prop.to_dataframe()
    tabla5_conteo = columnas_tabla(tabla5_conteo, ntabla=5, est='conteo', a=anios[r])
    tabla5_prop = columnas_tabla(tabla5_prop, ntabla=5, est='proporcion', a=anios[r])
    tabla5_conteo = etiquetar_tablas(tabla5_conteo, n=5)
    tabla5_prop = etiquetar_tablas(tabla5_prop, n=5)
    tabla5 = pd.concat([tabla5_conteo, tabla5_prop])
    tabla5.reset_index(drop=True, inplace=True)

    tabla6_conteo = tabla6_conteo.to_dataframe()
    tabla6_prop = tabla6_prop.to_dataframe()
    tabla6_conteo = columnas_tabla(tabla6_conteo, ntabla=6, est='conteo', a=anios[r])
    tabla6_prop = columnas_tabla(tabla6_prop, ntabla=6, est='proporcion', a=anios[r])
    tabla6_conteo = etiquetar_tablas(tabla6_conteo, n=6)
    tabla6_prop = etiquetar_tablas(tabla6_prop, n=6)
    tabla6 = pd.concat([tabla6_conteo, tabla6_prop])
    tabla6.reset_index(drop=True, inplace=True)

    tabla7_conteo = tabla7_conteo.to_dataframe()
    tabla7_prop = tabla7_prop.to_dataframe()
    tabla7_conteo = columnas_tabla(tabla7_conteo, ntabla=7, est='conteo', a=anios[r])
    tabla7_prop = columnas_tabla(tabla7_prop, ntabla=7, est='proporcion', a=anios[r])
    tabla7_conteo = etiquetar_tablas(tabla7_conteo, n=7)
    tabla7_prop = etiquetar_tablas(tabla7_prop, n=7)
    tabla7 = pd.concat([tabla7_conteo, tabla7_prop])
    tabla7.reset_index(drop=True, inplace=True)


    tabla1_ = pd.concat([tabla1_, tabla1])
    tabla1_ = tabla1_.reset_index(drop=True)
    tabla1_.to_csv('resultados/tablas/01_jefatura_menor18.csv')
    tabla2_ = pd.concat([tabla2_, tabla2])
    tabla2_ = tabla2_.reset_index(drop=True)
    tabla2_.to_csv('resultados/tablas/02_quintil_menor_18.csv')
    tabla3_ = pd.concat([tabla3_, tabla3])
    tabla3_ = tabla3_.reset_index(drop=True)
    tabla3_.to_csv('resultados/tablas/03_pobreza_menor_18.csv')
    tabla4_ = pd.concat([tabla4_, tabla4])
    tabla4_ = tabla4_.reset_index(drop=True)
    tabla4_.to_csv('resultados/tablas/04_thogar_menor_18.csv')
    tabla5_ = pd.concat([tabla5_, tabla5])
    tabla5_ = tabla5_.reset_index(drop=True)
    tabla5_.to_csv('resultados/tablas/05_thogar_jefatura_18.csv')
    tabla6_ = pd.concat([tabla6_, tabla6])
    tabla6_ = tabla6_.reset_index(drop=True)
    tabla6_.to_csv('resultados/tablas/06_thogar_pobreza_18.csv')
    tabla7_ = pd.concat([tabla7_, tabla7])
    tabla7_ = tabla7_.reset_index(drop=True)
    tabla7_.to_csv('resultados/tablas/07_thogar_quintil_18.csv')

    gc.collect()

#%%
