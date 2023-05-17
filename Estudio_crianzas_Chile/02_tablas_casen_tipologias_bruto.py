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

tabla1_ = pd.DataFrame()
tabla2_ = pd.DataFrame()
tabla3_ = pd.DataFrame()
tabla4_ = pd.DataFrame()
tabla5_ = pd.DataFrame()
tabla6_ = pd.DataFrame()
tabla7_ = pd.DataFrame()
rutas = []
for a in anios:
    r = 'data/casen/casen' + str(a) + '.sav'
    rutas.append(r)
# Hogares con menores en su interior:
# cuantos hogares son?
# cuantos estan en situacion de pobreza?

variables = {
    1990: {
        'menores_subset': ['r', 'p', 'c', 'z', 'f', 'corte', 'qaut', 'edad', 'expr'],
    },
    1992: {
        'menores_subset': ['r', 'p', 'c', 'z', 'f', 'corte', 'qaut', 'edad', 'expr'],
    },
    1994: {
        'menores_subset': ['r', 'p', 'c', 'z', 'f', 'seg', 'corte', 'qaut', 'edad', 'expr'],
    },
    1996: {
        'menores_subset': ['r', 'p', 'c', 'z', 'f', 'corte', 'qaut', 'edad', 'expr'],
    },
    1998: {
        'menores_subset': ['r', 'p', 'z', 'seg', 'f', 'corte', 'qaut', 'edad', 'expr', 'estrato', 'segmento'],
    },
    2000: {
        'menores_subset': ['r', 'p', 'z', 'c', 'folio', 'corte', 'qaut', 'edad', 'expr', 'estrato', 'segmento'],
    },
    2003: {
        'menores_subset': ['r', 'p', 'z', 'f', 'corte', 'qaut', 'edad', 'expr', 'estrato', 'segmento'],
    },
    2006: {
        'menores_subset': ['r', 'p', 'z', 'f', 'corte', 'qaut', 'edad', 'expr', 'estrato', 'seg'],
    },
    2009: {
        'menores_subset': ['idviv', 'segmento', 'folio', 'corte', 'qaut', 'edad', 'expr', 'estrato'],
    },
    2013: {
        'menores_subset': ['folio', 'pobreza_mn', 'qaut_mn', 'edad', 'expr', 'varstrat', 'varunit'],
    },
    2015: {
        'menores_subset': ['folio', 'pobreza', 'qaut', 'edad', 'expr', 'varstrat', 'varunit'],
    },
    2017: {
        'menores_subset': ['folio', 'pobreza', 'qaut', 'edad', 'expr', 'varstrat', 'varunit'],
    },
    2020: {
        'menores_subset': ['folio', 'pobreza', 'qaut', 'edad', 'expr', 'varstrat', 'varunit'],
    },
}

vars_hogares = {
    1990: ['r', 'p', 'c', 'z', 'f'],
    1992: ['r', 'p', 'c', 'z', 'f'],
    1994: ['r', 'p', 'c', 'z', 'seg','f'],
    1996: ['r', 'p', 'c', 'z', 'seg','f'],
    1998: ['segmento','f'],
    2000: ['segmento','folio'],
    2003: ['segmento','f'],
    2006: ['seg','f'],
    2009: ['idviv', 'folio'],
    2013: ['folio'],
    2015: ['folio'],
    2017: ['folio'],
    2020: ['folio']

}

def crear_var_personas_menores(df, vars_hogar, nombre_var_edad, nombre_var_creada, n_excluyente):
    df = df.copy()
    df['aux'] = 0
    df.loc[:, nombre_var_edad] = df[nombre_var_edad].astype('int')
    df.loc[df[nombre_var_edad] < n_excluyente, 'aux'] = 1
    agrupada = df.groupby(vars_hogar)
    total_hogares = len(agrupada)
    df[nombre_var_creada] = agrupada[['aux']].transform('max')
    # validación creación variable
    df_val = pd.crosstab(df[nombre_var_edad], df[nombre_var_creada]).reset_index()
    df_val.columns = ['edad', 'mayor17', 'menor18']
    print('La validación variable edad es: {}'.format((df_val.loc[df_val.edad < 18, 'menor18'] > 0).all() & (
            df_val.loc[df_val.edad > 17, 'mayor17'] > 0).all()))
    return df

for r in range(len(rutas)):
    print('trabajando con: {}'.format(anios[r]))
    df = pd.read_spss(rutas[r])
    df.columns = df.columns.str.lower()
    if anios[r] in [1990, 1992]:
        # menores
        total_hogares = len(df.groupby(vars_hogares[anios[r]]))
        df = crear_var_personas_menores(df, vars_hogar= ['r', 'p', 'c', 'z', 'f'], nombre_var_edad='edad',
                                        nombre_var_creada='menores_18', n_excluyente=18)

        # hogares
        df['aux1'] = 0
        df.loc[(df.pco1.str.lower().str.match('^je.*')) & (df.nucleo != 0), 'aux1'] = 1
        df['nnucleo'] = agrupada[['aux1']].transform('sum')
        df.drop(columns='aux1', inplace=True)
        # se construye variable pareja para identificar si el hogar cuenta con parejas
        df['aux'] = 0
        df.loc[df.pco1.str.lower().str.match('^c[óo].*'), 'aux'] = 1
        df['pareja'] = 0
        df['pareja'] = agrupada[['aux']].transform('max')
        df['sexo_jf'] = 0
        df.loc[(df.sexo.str.match('^M')) & (df.pco1.str.lower().str.match('^je')), 'sexo_jf'] = 1
        df['sexojefat'] =  agrupada[['sexo_jf']].transform('max')
        print('Total muestral de hogares: {}'.format(total_hogares))
        df['thogar'] = 0
        df.loc[df.numper==1, 'thogar'] = 1 # unipersonal
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo == 1), 'thogar'] = 2  # nuclear monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo == 1), 'thogar'] = 3  # nuclear biparental
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo > 1), 'thogar'] = 4   # extenso monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo > 1), 'thogar'] = 5   # extenso biparental
        df.loc[(df.numper!=1) & (df.nnucleo == df.numper), 'thogar'] = 6         # sin nucle
        agrupada2 = df.groupby(['r', 'p', 'c', 'z', 'f'])
        df_filter = agrupada2.head(1)[['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr']]
        print('en el año: {}, df.thogar tiene: {}'.format(anios[r], df.thogar.unique()))
        print('en el año: {}, df_filter.thogar tiene: {}'.format(anios[r], df_filter.thogar.unique()))
    elif anios[r] in [1994, 1996]:
        df['aux'] = 0
        df.loc[df['edad'] < 18, 'aux'] = 1
        agrupada = df.groupby(['r', 'p', 'c', 'z', 'seg','f'])
        total_hogares = len(agrupada)
        df['menores_18'] = agrupada[['aux']].transform('max')

        # validación creación variable
        df_val = pd.crosstab(df.edad, df.menores_18).reset_index()
        df_val.columns = ['edad', 'mayor17', 'menor18']
        (df_val.loc[df_val.edad<18, 'menor18'] > 0).all() & (df_val.loc[df_val.edad>17, 'mayor17'] > 0).all()

        # hogares
        df['aux1'] = 0
        df.loc[(df.pco1.str.lower().str.match('^je.*')) & (df.nucleo != 0), 'aux1'] = 1
        df['nnucleo'] = agrupada[['aux1']].transform('sum')
        df.drop(columns='aux1', inplace=True)
        # se construye variable pareja para identificar si el hogar cuenta con parejas
        df['aux'] = 0
        df.loc[df.pco1.str.lower().str.match('^c[óo].*'), 'aux'] = 1
        df['pareja'] = 0
        df['pareja'] = agrupada[['aux']].transform('max')

        df['sexo_jf'] = 0
        df.loc[(df.sexo.str.match('^M')) & (df.pco1.str.lower().str.match('^je')), 'sexo_jf'] = 1
        df['sexojefat'] = agrupada[['sexo_jf']].transform('max')
        print('Total muestral de hogares: {}'.format(total_hogares))
        df['thogar'] = 0
        df.loc[df.numper==1, 'thogar'] = 1 # unipersonal
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo == 1), 'thogar'] = 2 # nuclear monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo == 1), 'thogar'] = 3 # nuclear biparental
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo > 1), 'thogar'] = 4  # extenso monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo > 1), 'thogar'] = 5  # extenso biparental
        df.loc[(df.numper!=1) & (df.nnucleo == df.numper), 'thogar'] = 6  # sin nucle
        agrupada2 = df.groupby(['r', 'p', 'c', 'z', 'seg','f'])
        df_filter = agrupada2.head(1)[['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut',
                                       'expr']]
        print('en el año: {}, df.thogar tiene: {}'.format(anios[r], df.thogar.unique()))
        print('en el año: {}, df_filter.thogar tiene: {}'.format(anios[r], df_filter.thogar.unique()))

        # if anios[r] == 1996:
        #     df_filter = df_filter.loc[df_filter.estrato != 21022.]

    elif anios[r] in [1998, 2003]:
        df['aux'] = 0
        df.loc[df['edad'] < 18, 'aux'] = 1
        agrupada = df.groupby(['segmento','f'])
        total_hogares = len(agrupada)
        df['menores_18'] = agrupada[['aux']].transform('max')

        # validación creación variable
        df_val =pd.crosstab(df.edad, df.menores_18).reset_index()
        df_val.columns=['edad', 'mayor17', 'menor18']
        (df_val.loc[df_val.edad<18, 'menor18'] > 0).all() & (df_val.loc[df_val.edad>17, 'mayor17'] > 0).all()

        # hogares
        df['aux1'] = 0
        df.loc[(df.pco1.str.lower().str.match('^je.*')) & (df.nucleo != 0), 'aux1'] = 1
        df['nnucleo'] = agrupada[['aux1']].transform('sum')
        df.drop(columns='aux1', inplace=True)
        # se construye variable pareja para identificar si el hogar cuenta con parejas
        df['aux'] = 0
        df.loc[df.pco1.str.lower().str.match('^c[oó].*'), 'aux'] = 1
        df['pareja'] = 0
        df['pareja'] = agrupada[['aux']].transform('max')

        df['sexo_jf'] = 0
        df.loc[(df.sexo.str.match('^M')) & (df.pco1.str.lower().str.match('^je')), 'sexo_jf'] = 1
        df['sexojefat'] =  agrupada[['sexo_jf']].transform('max')
        print('Total muestral de hogares: {}'.format(total_hogares))
        df['thogar'] = 0
        df.loc[df.numper==1, 'thogar'] = 1 # unipersonal
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo == 1), 'thogar'] = 2 # nuclear monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo == 1), 'thogar'] = 3 # nuclear biparental
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo > 1), 'thogar'] = 4  # extenso monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo > 1), 'thogar'] = 5  # extenso biparental
        df.loc[(df.numper!=1) & (df.nnucleo == df.numper), 'thogar'] = 6  # sin nucle
        agrupada2 = df.groupby(['segmento','f'])
        df_filter = agrupada2.head(1)[['sexojefat', 'menores_18', 'thogar', 'corte', 'estrato', 'segmento', 'qaut',
                                       'expr']]
        print('en el año: {}, df.thogar tiene: {}'.format(anios[r], df.thogar.unique()))
        print('en el año: {}, df_filter.thogar tiene: {}'.format(anios[r], df_filter.thogar.unique()))

    elif anios[r] == 2000:
        df['aux'] = 0
        df.loc[df['edad'] < 18, 'aux'] = 1
        agrupada = df.groupby(['segmento','folio'])
        total_hogares = len(agrupada)
        df['menores_18'] = agrupada[['aux']].transform('max')

        # validación creación variable
        df_val =pd.crosstab(df.edad, df.menores_18).reset_index()
        df_val.columns=['edad', 'mayor17', 'menor18']
        (df_val.loc[df_val.edad<18, 'menor18'] > 0).all() & (df_val.loc[df_val.edad>17, 'mayor17'] > 0).all()

        # hogares
        df['aux1'] = 0
        df.loc[(df.pco1.str.lower().str.match('^je.*')) & (df.nucleo != 0), 'aux1'] = 1
        df['nnucleo'] = agrupada[['aux1']].transform('sum')

        # se construye variable pareja para identificar si el hogar cuenta con parejas
        df['aux'] = 0
        df.loc[df.pco1.str.lower().str.match('^c[óo].*'), 'aux'] = 1
        df['pareja'] = 0
        df['pareja'] = agrupada[['aux']].transform('max')

        df['sexo_jf'] = 0
        df.loc[(df.sexo.str.match('^M')) & (df.pco1.str.lower().str.match('^je')), 'sexo_jf'] = 1
        df['sexojefat'] =  agrupada[['sexo_jf']].transform('max')
        print('Total muestral de hogares: {}'.format(total_hogares))
        df['thogar'] = 0
        df.loc[df.numper==1, 'thogar'] = 1 # unipersonal
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo == 1), 'thogar'] = 2 # nuclear monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo == 1), 'thogar'] = 3 # nuclear biparental
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo > 1), 'thogar'] = 4  # extenso monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo > 1), 'thogar'] = 5  # extenso biparental
        df.loc[(df.numper!=1) & (df.nnucleo == df.numper), 'thogar'] = 6  # sin nucle
        agrupada2 = df.groupby(['segmento','folio'])
        df_filter = agrupada2.head(1)[['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr', 'segmento',
                                       'estrato']]
        df_filter = df_filter.loc[df_filter.estrato != 21022.]
        print('en el año: {}, df.thogar tiene: {}'.format(anios[r], df.thogar.unique()))
        print('en el año: {}, df_filter.thogar tiene: {}'.format(anios[r], df_filter.thogar.unique()))

    elif anios[r] == 2006:
        df['aux'] = 0
        df['edad'] = df.edad.cat.codes
        df['edad'] = df.edad.astype('int64')
        df.loc[df['edad'] < 18, 'aux'] = 1
        agrupada = df.groupby(['seg','f'])
        total_hogares = len(agrupada)
        df['menores_18'] = agrupada[['aux']].transform('max')

        # validación creación variable
        df_val =pd.crosstab(df.edad, df.menores_18).reset_index()
        df_val.columns=['edad', 'mayor17', 'menor18']
        (df_val.loc[df_val.edad<18, 'menor18'] > 0).all() & (df_val.loc[df_val.edad>17, 'mayor17'] > 0).all()

        # hogares
        df['aux1'] = 0
        df.loc[(df.pco1.str.lower().str.match('^je.*')) & (df.nucleo != 0), 'aux1'] = 1
        df['nnucleo'] = agrupada[['aux1']].transform('sum')

        # se construye variable pareja para identificar si el hogar cuenta con parejas
        df['aux'] = 0
        df.loc[df.pco1.str.lower().str.match('^c[óo].*'), 'aux'] = 1
        df['pareja'] = 0
        df['pareja'] = agrupada[['aux']].transform('max')

        df['sexo_jf'] = 0
        df.loc[(df.sexo.str.match('^M')) & (df.pco1.str.lower().str.match('^je')), 'sexo_jf'] = 1
        df['sexojefat'] =  agrupada[['sexo_jf']].transform('max')
        print('Total muestral de hogares: {}'.format(total_hogares))
        df['thogar'] = 0
        df.loc[df.numper==1, 'thogar'] = 1 # unipersonal
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo == 1), 'thogar'] = 2 # nuclear monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo == 1), 'thogar'] = 3 # nuclear biparental
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo > 1), 'thogar'] = 4  # extenso monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo > 1), 'thogar'] = 5  # extenso biparental
        df.loc[(df.numper!=1) & (df.nnucleo == df.numper), 'thogar'] = 6  # sin nucle
        agrupada2 = df.groupby(['seg','f'])
        df_filter = agrupada2.head(1)[['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr',
                                       #  'seg',
                                       # 'estrato'
                                       ]]
        print('en el año: {}, df.thogar tiene: {}'.format(anios[r], df.thogar.unique()))
        print('en el año: {}, df_filter.thogar tiene: {}'.format(anios[r], df_filter.thogar.unique()))

    elif anios[r] == 2009:
        df['aux'] = 0
        df['edad'] = df.edad.cat.codes
        df['edad'] = df.edad.astype('int64')
        df.loc[df['edad'] < 18, 'aux'] = 1
        agrupada = df.groupby(['idviv', 'folio'])
        total_hogares = len(agrupada)
        df['menores_18'] = agrupada[['aux']].transform('max')

        # validación creación variable
        df_val =pd.crosstab(df.edad, df.menores_18).reset_index()
        df_val.columns=['edad', 'mayor17', 'menor18']
        (df_val.loc[df_val.edad<18, 'menor18'] > 0).all() & (df_val.loc[df_val.edad>17, 'mayor17'] > 0).all()

        # hogares
        df['aux1'] = 0
        df.loc[(df.pco1.str.lower().str.match('^je.*')) & (df.nucleo != 0), 'aux1'] = 1
        df['nnucleo'] = agrupada[['aux1']].transform('sum')

        # se construye variable pareja para identificar si el hogar cuenta con parejas
        df['aux'] = 0
        df.loc[df.pco1.str.lower().str.match('^c[óo].*'), 'aux'] = 1
        df['pareja'] = 0
        df['pareja'] = agrupada[['aux']].transform('max')

        df['sexo_jf'] = 0
        df.loc[(df.sexo.str.match('^M')) & (df.pco1.str.lower().str.match('^je')), 'sexo_jf'] = 1
        df['sexojefat'] =  agrupada[['sexo_jf']].transform('max')
        print('Total muestral de hogares: {}'.format(total_hogares))
        df['thogar'] = 0
        df.loc[df.numper==1, 'thogar'] = 1 # unipersonal
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo == 1), 'thogar'] = 2 # nuclear monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo == 1), 'thogar'] = 3 # nuclear biparental
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo > 1), 'thogar'] = 4  # extenso monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo > 1), 'thogar'] = 5  # extenso biparental
        df.loc[(df.numper!=1) & (df.nnucleo == df.numper), 'thogar'] = 6  # sin nucle
        agrupada2 = df.groupby(['idviv', 'folio'])
        df_filter = agrupada2.head(1)[['sexojefat', 'menores_18', 'thogar', 'corte', 'qaut', 'expr',
                                       #  'segmento',
                                       # 'estrato'
                                       ]]
        print('en el año: {}, df.thogar tiene: {}'.format(anios[r], df.thogar.unique()))
        print('en el año: {}, df_filter.thogar tiene: {}'.format(anios[r], df_filter.thogar.unique()))

    elif anios[r] in [2013, 2015, 2017, 2020]:
        df['aux'] = 0
        # df['edad'] = df.edad.cat.codes
        # df['edad'] = df.edad.astype('int64')
        df.loc[df['edad'] < 18, 'aux'] = 1
        agrupada = df.groupby(['folio'])
        total_hogares = len(agrupada)
        df['menores_18'] = agrupada[['aux']].transform('max')

        # validación creación variable
        df_val =pd.crosstab(df.edad, df.menores_18).reset_index()
        df_val.columns=['edad', 'mayor17', 'menor18']
        (df_val.loc[df_val.edad<18, 'menor18'] > 0).all() & (df_val.loc[df_val.edad>17, 'mayor17'] > 0).all()

        # hogares
        df['aux1'] = 0
        df.loc[(df.pco1.str.lower().str.match('^je.*')) & (df.nucleo != 0), 'aux1'] = 1
        df['nnucleo'] = agrupada[['aux1']].transform('sum')

        # se construye variable pareja para identificar si el hogar cuenta con parejas
        df['aux'] = 0
        df.loc[df.pco1.str.lower().str.match('^[ce].*xo$'), 'aux'] = 1
        df['pareja'] = 0
        df['pareja'] = agrupada[['aux']].transform('max')

        df['sexo_jf'] = 0
        df.loc[(df.sexo.str.match('^M')) & (df.pco1.str.lower().str.match('^je')), 'sexo_jf'] = 1
        df['sexojefat'] =  agrupada[['sexo_jf']].transform('max')
        print('Total muestral de hogares: {}'.format(total_hogares))
        df['thogar'] = 0
        df.loc[df.numper==1, 'thogar'] = 1 # unipersonal
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo == 1), 'thogar'] = 2 # nuclear monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo == 1), 'thogar'] = 3 # nuclear biparental
        df.loc[(df.numper>1) & (df.pareja==0) & (df.nnucleo > 1), 'thogar'] = 4  # extenso monoparental
        df.loc[(df.numper>1) & (df.pareja==1) & (df.nnucleo > 1), 'thogar'] = 5  # extenso biparental
        df.loc[(df.numper!=1) & (df.nnucleo == df.numper), 'thogar'] = 6  # sin nucle
        agrupada2 = df.groupby(['folio'])
        if df.columns.isin(['qaut_mn']).any():
            df_filter = agrupada2.head(1)[['sexojefat', 'menores_18', 'thogar',
                                           'pobreza_mn', 'qaut_mn', 'expr',
                                           'varunit', 'varstrat']]
        else:
            df_filter = agrupada2.head(1)[['sexojefat', 'menores_18', 'thogar',
                                           'pobreza', 'qaut', 'expr',
                                           'varunit', 'varstrat']]
        print('en el año: {}, df.thogar tiene: {}'.format(anios[r], df.thogar.unique()))
        print('en el año: {}, df_filter.thogar tiene: {}'.format(anios[r], df_filter.thogar.unique()))


    df_filter= df_filter.rename(columns={'qaut_mn': 'qaut', 'corte': 'pobreza','corte_mn': 'pobreza', 'pobreza_mn':
        'pobreza',
        # 'varstrat': 'estrato',
    })

    if df_filter.qaut.dtype == 'category':
        df_filter['qaut'] = df_filter.qaut.cat.codes
        df_filter['qaut'] = df_filter.qaut.astype('int64')
        df_filter.loc[df_filter.qaut == -1, 'qaut'] = np.nan
    if df_filter.pobreza.dtype == 'category':
        df_filter['pobreza'] = df_filter.pobreza.cat.codes
        df_filter['pobreza'] = df_filter.pobreza.astype('int64')
        df_filter.loc[df_filter.pobreza >= 0, 'pobreza'] = df_filter.pobreza + 1
        df_filter.loc[df_filter.pobreza == -1, 'pobreza'] = np.nan


    df_filter2 = df_filter.loc[(df_filter.thogar > 1) & (df_filter.thogar < 6)]
    if df_filter2.columns.isin(['estrato']).any():
        if df_filter2.estrato.dtype=='O':
            df_filter2['estrato'] = df_filter2.estrato.astype('int64')

    print('sigue: en el año: {}, df.thogar tiene: {}'.format(anios[r], df.thogar.unique()))
    print('sigue: en el año: {}, df_filter.thogar tiene: {}'.format(anios[r], df_filter.thogar.unique()))


    ## tabla 1 : distribucion menores 18
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

    if df_filter.columns.isin(['varstrat']).any():
        print('variables varstrat y varunit: {}'.format(anios[r]))
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

        tabla4_prop.tabulate(vars=[df_filter2.thogar, df_filter2.menores_18],
                             samp_weight=df_filter2.expr,
                             stratum=df_filter2.varstrat,
                             psu=df_filter2.varunit,
                             remove_nan=True)
        tabla4_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.menores_18],
                               samp_weight=df_filter2.expr,
                               stratum=df_filter2.varstrat,
                               psu=df_filter2.varunit,
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

    elif df_filter.columns.isin(['segmento']).any():
        print('variables segmento: {}'.format(anios[r]))
        if df_filter.estrato.dtype == 'O':
            df_filter['estrato'] = df_filter.estrato.astype('float64')
        if df_filter.segmento.dtype == 'O':
            df_filter['segmento'] = df_filter.segmento.astype('float64')
        tabla1_prop.tabulate(vars=[df_filter.sexojefat, df_filter.menores_18],
                             samp_weight=df_filter.expr,
                             stratum=df_filter.estrato,
                             psu=df_filter.segmento,
                             remove_nan=True)
        tabla1_conteo.tabulate(vars=[df_filter.sexojefat, df_filter.menores_18],
                               samp_weight=df_filter.expr,
                               stratum=df_filter.estrato,
                               psu=df_filter.segmento,
                               remove_nan=True)
        tabla2_prop.tabulate(vars=[df_filter.qaut, df_filter.menores_18],
                             samp_weight=df_filter.expr,
                             stratum=df_filter.estrato,
                             psu=df_filter.segmento,
                             remove_nan=True)
        tabla2_conteo.tabulate(vars=[df_filter.qaut, df_filter.menores_18],
                               samp_weight=df_filter.expr,
                               stratum=df_filter.estrato,
                               psu=df_filter.segmento,
                               remove_nan=True)
        tabla3_prop.tabulate(vars=[df_filter.pobreza, df_filter.menores_18],
                             samp_weight=df_filter.expr,
                             stratum=df_filter.estrato,
                             psu=df_filter.segmento,
                             remove_nan=True)
        tabla3_conteo.tabulate(vars=[df_filter.pobreza, df_filter.menores_18],
                               samp_weight=df_filter.expr,
                               stratum=df_filter.estrato,
                               psu=df_filter.segmento,
                               remove_nan=True)
        if anios[r] == 1998:
            tabla4_prop.tabulate(vars=[df_filter2.thogar, df_filter2.menores_18],
                                 samp_weight=df_filter2.expr,
                                 # stratum=df_filter2.estrato,
                                 # psu=df_filter2.segmento,
                                 remove_nan=True)
            tabla4_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.menores_18],
                                   samp_weight=df_filter2.expr,
                                   # stratum=df_filter2.estrato,
                                   # psu=df_filter2.segmento,
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
        else:
            tabla4_prop.tabulate(vars=[df_filter2.thogar, df_filter2.menores_18],
                                 samp_weight=df_filter2.expr,
                                 stratum=df_filter2.estrato,
                                 psu=df_filter2.segmento,
                                 remove_nan=True)
            tabla4_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.menores_18],
                                   samp_weight=df_filter2.expr,
                                   stratum=df_filter2.estrato,
                                   psu=df_filter2.segmento,
                                   remove_nan=True)
            tabla5_prop.tabulate(vars=[df_filter2.thogar, df_filter2.sexojefat],
                                 samp_weight=df_filter2.expr,
                                 stratum=df_filter2.estrato,
                                 psu=df_filter2.segmento,
                                 remove_nan=True)
            tabla5_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.sexojefat],
                                   samp_weight=df_filter2.expr,
                                   stratum=df_filter2.estrato,
                                   psu=df_filter2.segmento,
                                   remove_nan=True)
            tabla6_prop.tabulate(vars=[df_filter2.thogar, df_filter2.pobreza],
                                 samp_weight=df_filter2.expr,
                                 stratum=df_filter2.estrato,
                                 psu=df_filter2.segmento,
                                 remove_nan=True)
            tabla6_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.pobreza],
                                   samp_weight=df_filter2.expr,
                                   stratum=df_filter2.estrato,
                                   psu=df_filter2.segmento,
                                   remove_nan=True)
            tabla7_prop.tabulate(vars=[df_filter2.thogar, df_filter2.qaut],
                                 samp_weight=df_filter2.expr,
                                 stratum=df_filter2.estrato,
                                 psu=df_filter2.segmento,
                                 remove_nan=True)
            tabla7_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.qaut],
                                   samp_weight=df_filter2.expr,
                                   stratum=df_filter2.estrato,
                                   psu=df_filter2.segmento,
                                   remove_nan=True)
    elif (not df_filter.columns.isin(['segmento']).any()) & df_filter.columns.isin(['seg']).any():
        print('variables seg: {}'.format(anios[r]))
        if df_filter.estrato.dtype == 'O':
            df_filter['estrato'] = df_filter.estrato.astype('float64')
        if df_filter.seg.dtype == 'O':
            df_filter['seg'] = df_filter.seg.astype('float64')
        tabla1_prop.tabulate(vars=[df_filter.sexojefat, df_filter.menores_18],
                             samp_weight=df_filter.expr,
                             stratum=df_filter.estrato,
                             psu=df_filter.seg,
                             remove_nan=True)
        tabla1_conteo.tabulate(vars=[df_filter.sexojefat, df_filter.menores_18],
                               samp_weight=df_filter.expr,
                               stratum=df_filter.estrato,
                               psu=df_filter.seg,
                               remove_nan=True)
        tabla2_prop.tabulate(vars=[df_filter.qaut, df_filter.menores_18],
                             samp_weight=df_filter.expr,
                             stratum=df_filter.estrato,
                             psu=df_filter.seg,
                             remove_nan=True)
        tabla2_conteo.tabulate(vars=[df_filter.qaut, df_filter.menores_18],
                               samp_weight=df_filter.expr,
                               stratum=df_filter.estrato,
                               psu=df_filter.seg,
                               remove_nan=True)
        tabla3_prop.tabulate(vars=[df_filter.pobreza, df_filter.menores_18],
                             samp_weight=df_filter.expr,
                             stratum=df_filter.estrato,
                             psu=df_filter.seg,
                             remove_nan=True)
        tabla3_conteo.tabulate(vars=[df_filter.pobreza, df_filter.menores_18],
                               samp_weight=df_filter.expr,
                               stratum=df_filter.estrato,
                               psu=df_filter.seg,
                               remove_nan=True)
        tabla4_prop.tabulate(vars=[df_filter2.thogar, df_filter2.menores_18],
                             samp_weight=df_filter2.expr,
                             stratum=df_filter2.estrato,
                             psu=df_filter2.seg,
                             remove_nan=True)
        tabla4_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.menores_18],
                               samp_weight=df_filter2.expr,
                               stratum=df_filter2.estrato,
                               psu=df_filter2.seg,
                               remove_nan=True)
        tabla5_prop.tabulate(vars=[df_filter2.thogar, df_filter2.sexojefat],
                             samp_weight=df_filter2.expr,
                             stratum=df_filter2.estrato,
                             psu=df_filter2.seg,
                             remove_nan=True)
        tabla5_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.sexojefat],
                               samp_weight=df_filter2.expr,
                               stratum=df_filter2.estrato,
                               psu=df_filter2.seg,
                               remove_nan=True)
        tabla6_prop.tabulate(vars=[df_filter2.thogar, df_filter2.pobreza],
                             samp_weight=df_filter2.expr,
                             stratum=df_filter2.estrato,
                             psu=df_filter2.seg,
                             remove_nan=True)
        tabla6_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.pobreza],
                               samp_weight=df_filter2.expr,
                               stratum=df_filter2.estrato,
                               psu=df_filter2.seg,
                               remove_nan=True)
        tabla7_prop.tabulate(vars=[df_filter2.thogar, df_filter2.qaut],
                             samp_weight=df_filter2.expr,
                             stratum=df_filter2.estrato,
                             psu=df_filter2.seg,
                             remove_nan=True)
        tabla7_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.qaut],
                               samp_weight=df_filter2.expr,
                               stratum=df_filter2.estrato,
                               psu=df_filter2.seg,
                               remove_nan=True)
    else:
        print('variables sin muestra compleja: {}'.format(anios[r]))
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
        tabla4_prop.tabulate(vars=[df_filter2.thogar, df_filter2.menores_18],
                             samp_weight=df_filter2.expr,
                             # stratum=df_filter.estrato,
                             # psu=df_filter.seg,
                             remove_nan=True)
        tabla4_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.menores_18],
                               samp_weight=df_filter2.expr,
                               # stratum=df_filter.estrato,
                               # psu=df_filter.seg,
                               remove_nan=True)
        tabla5_prop.tabulate(vars=[df_filter2.thogar, df_filter2.sexojefat],
                             samp_weight=df_filter2.expr,
                             # stratum=df_filter2.estrato,
                             # psu=df_filter2.seg,
                             remove_nan=True)
        tabla5_conteo.tabulate(vars=[df_filter2.thogar, df_filter2.sexojefat],
                               samp_weight=df_filter2.expr,
                               # stratum=df_filter2.estrato,
                               # psu=df_filter2.seg,
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

    # tabla 1: distribucion de menores segun sexo de la jefatura de hogar
    tabla1_prop = tabla1_prop.to_dataframe()
    tabla1_prop.columns = ['sexo_jefatura', 'menor_18', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla1_prop.loc[tabla1_prop.sexo_jefatura == '1', 'sexo_jefatura'] = 'mujer'
    tabla1_prop.loc[tabla1_prop.sexo_jefatura == '0', 'sexo_jefatura'] = 'hombre'
    tabla1_prop.loc[tabla1_prop.menor_18 == '1', 'menor_18'] = 'con menores'
    tabla1_prop.loc[tabla1_prop.menor_18 == '0', 'menor_18'] = 'sin menores'
    tabla1_prop['anio'] = anios[r]
    tabla1_prop['tipo_est'] = 'proporcion'
    tabla1_prop['dato'] = round(tabla1_prop.dato*100, 1)

    tabla1_conteo = tabla1_conteo.to_dataframe()
    tabla1_conteo.columns = ['sexo_jefatura', 'menor_18', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla1_conteo.loc[tabla1_conteo.sexo_jefatura == '1', 'sexo_jefatura'] = 'mujer'
    tabla1_conteo.loc[tabla1_conteo.sexo_jefatura == '0', 'sexo_jefatura'] = 'hombre'
    tabla1_conteo.loc[tabla1_conteo.menor_18 == '1', 'menor_18'] = 'con menores'
    tabla1_conteo.loc[tabla1_conteo.menor_18 == '0', 'menor_18'] = 'sin menores'
    tabla1_conteo['anio'] = anios[r]
    tabla1_conteo['tipo_est'] = 'conteo'

    tabla1 = pd.concat([tabla1_conteo, tabla1_prop])
    tabla1.reset_index(drop=True, inplace=True)


    # tabla 2: distribucion de menores segun quintiles de ingreso
    tabla2_conteo = tabla2_conteo.to_dataframe()
    tabla2_conteo.columns = ['quintil', 'menor_18', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla2_conteo.loc[:, 'menor_18'] = tabla2_conteo.menor_18.astype('float64')
    tabla2_conteo.loc[tabla2_conteo.menor_18 == 1.0, 'menor_18'] = 'con menores'
    tabla2_conteo.loc[tabla2_conteo.menor_18 == 0.0, 'menor_18'] = 'sin menores'
    tabla2_conteo.loc[:, 'quintil'] = tabla2_conteo.quintil.astype('float64')
    tabla2_conteo.loc[:, 'quintil'] = tabla2_conteo.loc[:, 'quintil'] + 1

    tabla2_conteo['anio'] = anios[r]
    tabla2_conteo['tipo_est'] = 'conteo'

    tabla2_prop = tabla2_prop.to_dataframe()
    tabla2_prop.columns = ['quintil', 'menor_18', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla2_prop.loc[:, 'menor_18'] = tabla2_conteo.menor_18.astype('float64')
    tabla2_prop.loc[tabla2_conteo.menor_18 == 1.0, 'menor_18'] = 'con menores'
    tabla2_prop.loc[tabla2_conteo.menor_18 == 0.0, 'menor_18'] = 'sin menores'
    tabla2_prop.loc[:, 'quintil'] = tabla2_prop.quintil.astype('float64')
    tabla2_prop.loc[:, 'quintil'] = tabla2_prop.loc[:, 'quintil'] + 1
    tabla2_prop['anio'] = anios[r]
    tabla2_prop['tipo_est'] = 'proporcion'
    tabla2_prop['dato'] = round(tabla2_prop.dato*100, 1)

    tabla2 = pd.concat([tabla2_conteo, tabla2_prop])
    tabla2.reset_index(drop=True, inplace=True)


    # tabla 3: distribucion de menores segun pobreza de ingreso
    tabla3_conteo = tabla3_conteo.to_dataframe()
    tabla3_conteo.columns = ['pobreza', 'menor_18', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla3_conteo.loc[:, 'menor_18'] = tabla3_conteo.menor_18.astype('float64')
    tabla3_conteo.loc[tabla3_conteo.menor_18 == 1.0, 'menor_18'] = 'con menores'
    tabla3_conteo.loc[tabla3_conteo.menor_18 == 0.0, 'menor_18'] = 'sin menores'
    tabla3_conteo.loc[:, 'pobreza'] = tabla3_conteo.pobreza.astype('float64')
    tabla3_conteo.loc[tabla3_conteo.pobreza == 1.0, 'pobreza'] = 'no pobre'
    tabla3_conteo.loc[tabla3_conteo.pobreza == 2.0, 'pobreza'] = 'pobre extremo'
    tabla3_conteo.loc[tabla3_conteo.pobreza == 3.0, 'pobreza'] = 'pobre no extremo'
    tabla3_conteo['anio'] = anios[r]
    tabla3_conteo['tipo_est'] = 'conteo'

    tabla3_prop = tabla3_prop.to_dataframe()
    tabla3_prop.columns = ['pobreza', 'menor_18', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla3_prop.loc[:, 'menor_18'] = tabla3_prop.menor_18.astype('float64')
    tabla3_prop.loc[tabla3_prop.menor_18 == 1.0, 'menor_18'] = 'con menores'
    tabla3_prop.loc[tabla3_prop.menor_18 == 0.0, 'menor_18'] = 'sin menores'
    tabla3_prop.loc[tabla3_prop.pobreza == 1.0, 'pobreza'] = 'no pobre'
    tabla3_prop.loc[tabla3_prop.pobreza == 2.0, 'pobreza'] = 'pobre extremo'
    tabla3_prop.loc[tabla3_prop.pobreza == 3.0, 'pobreza'] = 'pobre no extremo'
    tabla3_prop['anio'] = anios[r]
    tabla3_prop['tipo_est'] = 'proporcion'
    tabla3_prop['dato'] = round(tabla3_prop.dato*100, 1)

    tabla3 = pd.concat([tabla3_conteo, tabla3_prop])
    tabla3.reset_index(drop=True, inplace=True)

    # tabla 4: distribucion de menores segun tipologia de hogar
    tabla4_conteo = tabla4_conteo.to_dataframe()
    tabla4_conteo.columns = ['thogar', 'menor_18', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla4_conteo.loc[tabla4_conteo.menor_18 == '1', 'menor_18'] = 'con menores'
    tabla4_conteo.loc[tabla4_conteo.menor_18 == '0', 'menor_18'] = 'sin menores'
    # tabla4_conteo.loc[tabla4_conteo.thogar == '1.0', 'thogar'] = 'unipersonal'
    tabla4_conteo.loc[tabla4_conteo.thogar == '2', 'thogar'] = 'nuclear monoparental'
    tabla4_conteo.loc[tabla4_conteo.thogar == '3', 'thogar'] = 'nuclear biparental'
    tabla4_conteo.loc[tabla4_conteo.thogar == '4', 'thogar'] = 'extenso monoparental'
    tabla4_conteo.loc[tabla4_conteo.thogar == '5', 'thogar'] = 'extenso biparental'
    # tabla4_conteo.loc[tabla4_conteo.thogar == '6.0', 'thogar'] = 'sin núcleo'
    tabla4_conteo['anio'] = anios[r]
    tabla4_conteo['tipo_est'] = 'conteo'

    tabla4_prop = tabla4_prop.to_dataframe()
    tabla4_prop.columns = ['thogar', 'menor_18', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla4_prop.loc[tabla4_prop.menor_18 == '1', 'menor_18'] = 'con menores'
    tabla4_prop.loc[tabla4_prop.menor_18 == '0', 'menor_18'] = 'sin menores'
    # tabla4_prop.loc[tabla4_prop.thogar == '1', 'thogar'] = 'unipersonal'
    tabla4_prop.loc[tabla4_prop.thogar == '2', 'thogar'] = 'nuclear monoparental'
    tabla4_prop.loc[tabla4_prop.thogar == '3', 'thogar'] = 'nuclear biparental'
    tabla4_prop.loc[tabla4_prop.thogar == '4', 'thogar'] = 'extenso monoparental'
    tabla4_prop.loc[tabla4_prop.thogar == '5', 'thogar'] = 'extenso biparental'
    # tabla4_prop.loc[tabla4_prop.thogar == '6', 'thogar'] = 'sin núcleo'
    tabla4_prop['anio'] = anios[r]
    tabla4_prop['tipo_est'] = 'proporcion'
    tabla4_prop['dato'] = round(tabla4_prop.dato*100, 1)

    tabla4 = pd.concat([tabla4_conteo, tabla4_prop])
    tabla4.reset_index(drop=True, inplace=True)

    # tabla 5: distribucion de menores tipologia de hogar por sexo jefatura
    tabla5_conteo = tabla5_conteo.to_dataframe()
    tabla5_conteo.columns = ['thogar', 'sexo_jefatura', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla5_conteo.loc[tabla5_conteo.sexo_jefatura == '1', 'sexo_jefatura'] = 'mujer'
    tabla5_conteo.loc[tabla5_conteo.sexo_jefatura == '0', 'sexo_jefatura'] = 'hombre'

    tabla5_conteo.loc[tabla5_conteo.thogar == '2', 'thogar'] = 'nuclear monoparental'
    tabla5_conteo.loc[tabla5_conteo.thogar == '3', 'thogar'] = 'nuclear biparental'
    tabla5_conteo.loc[tabla5_conteo.thogar == '4', 'thogar'] = 'extenso monoparental'
    tabla5_conteo.loc[tabla5_conteo.thogar == '5', 'thogar'] = 'extenso biparental'
    tabla5_conteo['anio'] = anios[r]
    tabla5_conteo['tipo_est'] = 'conteo'

    tabla5_prop = tabla5_prop.to_dataframe()
    tabla5_prop.columns = ['thogar', 'sexo_jefatura', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla5_prop.loc[tabla5_prop.sexo_jefatura == '1', 'sexo_jefatura'] = 'mujer'
    tabla5_prop.loc[tabla5_prop.sexo_jefatura == '0', 'sexo_jefatura'] = 'hombre'
    tabla5_prop.loc[tabla5_prop.thogar == '2', 'thogar'] = 'nuclear monoparental'
    tabla5_prop.loc[tabla5_prop.thogar == '3', 'thogar'] = 'nuclear biparental'
    tabla5_prop.loc[tabla5_prop.thogar == '4', 'thogar'] = 'extenso monoparental'
    tabla5_prop.loc[tabla5_prop.thogar == '5', 'thogar'] = 'extenso biparental'
    tabla5_prop['anio'] = anios[r]
    tabla5_prop['tipo_est'] = 'proporcion'
    tabla5_prop['dato'] = round(tabla5_prop.dato*100, 1)
    tabla5 = pd.concat([tabla5_conteo, tabla5_prop])
    tabla5.reset_index(drop=True, inplace=True)

    # tabla 6: distribucion de menores tipologia de hogar por sexo jefatura
    tabla6_conteo = tabla6_conteo.to_dataframe()
    tabla6_conteo.columns = ['thogar', 'pobreza', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla6_conteo.loc[tabla6_conteo.thogar == '2.0', 'thogar'] = 'nuclear monoparental'
    tabla6_conteo.loc[tabla6_conteo.thogar == '3.0', 'thogar'] = 'nuclear biparental'
    tabla6_conteo.loc[tabla6_conteo.thogar == '4.0', 'thogar'] = 'extenso monoparental'
    tabla6_conteo.loc[tabla6_conteo.thogar == '5.0', 'thogar'] = 'extenso biparental'
    tabla6_conteo.loc[tabla6_conteo.pobreza == '1.0', 'pobreza'] = 'no pobre'
    tabla6_conteo.loc[tabla6_conteo.pobreza == '2.0', 'pobreza'] = 'pobre extremo'
    tabla6_conteo.loc[tabla6_conteo.pobreza == '3.0', 'pobreza'] = 'pobre no extremo'
    tabla6_conteo['anio'] = anios[r]
    tabla6_conteo['tipo_est'] = 'conteo'

    tabla6_prop = tabla6_prop.to_dataframe()
    tabla6_prop.columns = ['thogar', 'pobreza', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla6_prop.loc[tabla6_prop.thogar == '2.0', 'thogar'] = 'nuclear monoparental'
    tabla6_prop.loc[tabla6_prop.thogar == '3.0', 'thogar'] = 'nuclear biparental'
    tabla6_prop.loc[tabla6_prop.thogar == '4.0', 'thogar'] = 'extenso monoparental'
    tabla6_prop.loc[tabla6_prop.thogar == '5.0', 'thogar'] = 'extenso biparental'
    tabla6_prop.loc[tabla6_prop.pobreza == '1.0', 'pobreza'] = 'no pobre'
    tabla6_prop.loc[tabla6_prop.pobreza == '2.0', 'pobreza'] = 'pobre extremo'
    tabla6_prop.loc[tabla6_prop.pobreza == '3.0', 'pobreza'] = 'pobre no extremo'
    tabla6_prop['anio'] = anios[r]
    tabla6_prop['tipo_est'] = 'proporcion'
    tabla6_prop['dato'] = round(tabla6_prop.dato*100, 1)
    tabla6 = pd.concat([tabla6_conteo, tabla6_prop])
    tabla6.reset_index(drop=True, inplace=True)

    # tabla 7: distribucion de menores tipologia de hogar por sexo jefatura
    tabla7_conteo = tabla7_conteo.to_dataframe()
    tabla7_conteo.columns = ['thogar', 'quintil', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla7_conteo.loc[tabla7_conteo.thogar == '2.0', 'thogar'] = 'nuclear monoparental'
    tabla7_conteo.loc[tabla7_conteo.thogar == '3.0', 'thogar'] = 'nuclear biparental'
    tabla7_conteo.loc[tabla7_conteo.thogar == '4.0', 'thogar'] = 'extenso monoparental'
    tabla7_conteo.loc[tabla7_conteo.thogar == '5.0', 'thogar'] = 'extenso biparental'
    tabla7_conteo['anio'] = anios[r]
    tabla7_conteo['tipo_est'] = 'conteo'
    tabla7_prop = tabla7_prop.to_dataframe()
    tabla7_prop.columns = ['thogar', 'quintil', 'dato', 'desviacion_s', 'ic_bajo', 'ic_alto']
    tabla7_prop.loc[tabla7_prop.thogar == '2.0', 'thogar'] = 'nuclear monoparental'
    tabla7_prop.loc[tabla7_prop.thogar == '3.0', 'thogar'] = 'nuclear biparental'
    tabla7_prop.loc[tabla7_prop.thogar == '4.0', 'thogar'] = 'extenso monoparental'
    tabla7_prop.loc[tabla7_prop.thogar == '5.0', 'thogar'] = 'extenso biparental'

    tabla7_prop['dato'] = round(tabla7_prop.dato*100, 1)
    tabla7 = pd.concat([tabla7_conteo, tabla7_prop])
    tabla7.reset_index(drop=True, inplace=True)

    tabla1_ = pd.concat([tabla1_, tabla1])
    tabla1_ = tabla1_.reset_index(drop=True)
    tabla1_.to_feather('resultados/tablas/01_jefatura_menor18.feather')
    tabla2_ = pd.concat([tabla2_, tabla2])
    tabla2_ = tabla2_.reset_index(drop=True)
    tabla2_.to_feather('resultados/tablas/02_quintil_menor_18.feather')
    tabla3_ = pd.concat([tabla3_, tabla3])
    tabla3_ = tabla3_.reset_index(drop=True)
    tabla3_.to_feather('resultados/tablas/03_pobreza_menor_18.feather')
    tabla4_ = pd.concat([tabla4_, tabla4])
    tabla4_ = tabla4_.reset_index(drop=True)
    tabla4_.to_feather('resultados/tablas/04_thogar_menor_18.feather')
    tabla5_ = pd.concat([tabla5_, tabla5])
    tabla5_ = tabla5_.reset_index(drop=True)
    tabla5_.to_feather('resultados/tablas/05_thogar_jefatura_18.feather')
    tabla6_ = pd.concat([tabla6_, tabla6])
    tabla6_ = tabla6_.reset_index(drop=True)
    tabla6_.to_feather('resultados/tablas/06_thogar_pobreza_18.feather')
    tabla7_ = pd.concat([tabla7_, tabla7])
    tabla7_ = tabla7_.reset_index(drop=True)
    tabla7_.to_feather('resultados/tablas/07_thogar_quintil_18.feather')

    gc.collect()

#%%





