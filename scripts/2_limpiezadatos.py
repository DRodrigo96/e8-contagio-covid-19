

# PARTE 2: PANDAS y SHAPEFILES

import pandas as pd
import os

os.chdir('../')

# 2.1) CSV: Datos de contagiados
dataFile = pd.read_csv('data/positivos_covid.csv', sep=';')
dataFile.info()
dataFile.head(10)

# Problemas con CSV
# Problema 1: Lima y Lima-Región
dataFile['DEPARTAMENTO'].unique()
dataFile.loc[dataFile['DEPARTAMENTO'] == 'LIMA REGION', 'DEPARTAMENTO'] = 'LIMA'

len(dataFile['DEPARTAMENTO'].unique()) # Corregido

# Problema 2: Casos "EN INVESTIGACIÓN"
dataFile['PROVINCIA'].unique()
dataFile['DISTRITO'].unique()

for x in ['PROVINCIA', 'DISTRITO']:
    condition = dataFile[x] == 'EN INVESTIGACIÓN'
    dataFile = dataFile[~condition]

len(dataFile['PROVINCIA'].unique()) # Corregido
len(dataFile['DISTRITO'].unique()) # Corregido

dataFile.sort_values(by=['DEPARTAMENTO','PROVINCIA','DISTRITO'], inplace=True)
dataFile['INDEX'] = list(zip(dataFile['DEPARTAMENTO'], dataFile['PROVINCIA'], dataFile['DISTRITO']))

# 2.2) UBICACION GEOGRAFICA: LIMITE DISTRITAL Y COORDENADAS
import matplotlib.pyplot as plt

# Configuraciones
%matplotlib inline
%config InlineBackend.figure_format='retina'

# Información para el mapa
coor_link = 'https://raw.githubusercontent.com/DRodrigo96/e8-contagio-covid-19/main/data/COORDENADAS%20DISTRITAL.csv'
shapef = pd.read_csv(coor_link, sep=';', encoding='utf-8-sig')
shapef.shape

shapef.sort_values(by=['DEPARTAMENTO','PROVINCIA','DISTRITO'], inplace=True)
shapef['INDEX'] = list(zip(shapef['DEPARTAMENTO'], shapef['PROVINCIA'], shapef['DISTRITO']))

# STRING MATCHING - FUZZY WUZZY
dataFile_index = list(dataFile['INDEX'].unique())
shapef_index = list(shapef['INDEX'].unique())

len(dataFile_index)
len(shapef_index)

not_in_shp = list()
for x in shapef_index:
    if x not in dataFile_index:
        not_in_shp.append(x)

print(len(not_in_shp) - (len(shapef_index) - len(dataFile_index)))

# 2.3) FUZZY WUZZY 
from fuzzywuzzy import fuzz

x = fuzz.ratio("LIMA PORTILLO MANANTAY", 'LIMA PORTIYO MANANTAI')
if x > 80:
    print("Score: {}. It's a match!".format(x))

# Con threshold de score 95
for x, y, z in not_in_shp:
    for a, b, c in dataFile_index:
        ratio = fuzz.ratio(str(y + ' ' + z), str(b + ' ' + c))
        if ratio >= 95:
            dataFile.loc[dataFile['PROVINCIA'] == b, 'PROVINCIA'] = y
            dataFile.loc[dataFile['DISTRITO'] == c, 'DISTRITO'] = z
            #print(ratio, str(y + ' ' + z), '---', str(b + ' ' + c))
        else:
            pass

dataFile['INDEX'] = list(zip(dataFile['DEPARTAMENTO'], dataFile['PROVINCIA'], dataFile['DISTRITO']))

dataFile_index = list(dataFile['INDEX'].unique())
shapef_index = list(shapef['INDEX'].unique())

not_in_shp = list()
for x in shapef_index:
    if x not in dataFile_index:
        not_in_shp.append(x)

# Correción manual
for x, y, z in not_in_shp:
    for a, b, c in dataFile_index:
        ratio = fuzz.ratio(str(y + ' ' + z), str(b + ' ' + c))
        if ratio >= 85:
            print(ratio, str(y + ' ' + z), '---', str(b + ' ' + c))
        else:
            pass

dataFile.loc[dataFile['PROVINCIA'] == 'NAZCA', 'PROVINCIA'] = 'NASCA'
dataFile.loc[dataFile['DISTRITO'] == 'HUAY HUAY', 'DISTRITO'] = 'HUAY-HUAY'
dataFile.loc[dataFile['DISTRITO'] == 'SAN FCO DE ASIS DE YARUSYACAN', 'DISTRITO'] = 'SAN FRANCISCO DE ASIS DE YARUSYACAN'
dataFile.loc[dataFile['DISTRITO'] == 'SONDOR', 'DISTRITO'] = 'SONDORILLO'
dataFile.loc[dataFile['DISTRITO'] == 'CORONEL GREGORIO ALBARRACIN L.', 'DISTRITO'] = 'CORONEL GREGORIO ALBARRACIN LANCHIPA'
dataFile.loc[dataFile['DISTRITO'] == 'NAZCA', 'DISTRITO'] = 'NASCA'
dataFile.loc[dataFile['DISTRITO'] == 'ANDRES AVELINO CACERES D.', 'DISTRITO'] = 'ANDRES AVELINO CACERES DORREGARAY'

# dataFile corregido en nombres
dataFile['INDEX'] = list(zip(dataFile['DEPARTAMENTO'], dataFile['PROVINCIA'], dataFile['DISTRITO']))

dataFile_index = list(dataFile['INDEX'].unique())
shapef_index = list(shapef['INDEX'].unique())

not_in_shp = list()
for x in shapef_index:
    if x not in dataFile_index:
        not_in_shp.append(x)

print(len(not_in_shp) - (len(shapef_index) - len(dataFile_index)))

# 2.3) INFORMACIÓN GEORREFERENCIADA A NIVEL DISTRITAL
# Número de casos por distrito e index setting
collapseData = dataFile.groupby(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']).agg({'FECHA_CORTE': 'count', 'EDAD': 'mean'})
collapseData.reset_index(inplace=True)

collapseData['INDEX'] = collapseData['DEPARTAMENTO'] + ' ' + collapseData['PROVINCIA'] + ' ' + collapseData['DISTRITO'] 
collapseData.set_index('INDEX', inplace=True)
collapseData.drop(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'], axis=1, inplace=True)

# Shapefile e index setting
shapef['INDEX'] = shapef['DEPARTAMENTO'] + ' ' + shapef['PROVINCIA'] + ' '+ shapef['DISTRITO'] 
shapef.set_index('INDEX', inplace=True)

dfGeoref = shapef.join(collapseData, how='left')

# Drop distritos sin datos
dfGeoref.dropna(inplace=True)

# Saving
dfGeoref.to_pickle('temp/dfGeoref.pkl')

print('CLEANING DONE')
