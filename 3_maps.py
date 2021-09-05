# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 22:43:44 2020

@author: DavidRodrigo
"""

# PARTE 3: FOLIUM: Python, JavaScript, CSS & HTML

import folium
from folium import Map, Marker, GeoJson, LayerControl
from folium import plugins
from PIL import ImageFont
import json
from folium.plugins import MarkerCluster
from jinja2 import Template
import pandas as pd
from usrfunctions import *

# MAPA
dfGeoref = pd.read_pkl('dfGeoref.pkl')

latitude = dfGeoref['LATITUD']
longitude = dfGeoref['LONGITUD']
distrito = dfGeoref['DISTRITO']
provincia = dfGeoref['PROVINCIA']
departamento = dfGeoref['DEPARTAMENTO']
numero = dfGeoref['FECHA_CORTE']
edades = dfGeoref['EDAD']


with open("JAWGMAP API KEY.txt", 'r') as file:
    txttoken = file.read()

coor_PE = (-8.043040, -75.534517)
maPE = Map(
    coor_PE, 
    zoom_start = 5, 
    tiles='https://tile.jawg.io/jawg-matrix/{z}/{x}/{y}{r}.png?access-token='+'{token}'.format(token=txttoken),
    attr='''
    <a href="https://www.jawg.io/en/">JawgMaps</a>. 
    Fuente: <a href="https://www.datosabiertos.gob.pe/">datosabiertos.gob.pe</a>.
    Elaboración: <a href="https://www.linkedin.com/in/rodrigosanchezn/">David Sánchez</a>.
    '''
    )


contagio = MarkerCluster(icon_create_function=icon_create_function()).add_to(maPE)
font = ImageFont.truetype('times.ttf', 12)

for lat, lon, dep, pro, dis, num, edad in zip(latitude,longitude, departamento, provincia, distrito, numero, edades):
    contagio.add_child(MarkerWithProps(
        location=[lat,lon],
        icon=folium.Icon(color=colorcode(num)[0], icon=colorcode(num)[1], prefix='fa'),
        popup = folium.Popup(
            html='{}, {}, {}<br>Contagiados: {}<br>Edad promedio: {}'.format(dep,pro,dis,int(num),round(edad)),
            max_width=font.getsize(dep+pro+dis+' '*4)[0], min_width=font.getsize(dep+pro+dis+' '*4)[0],
            sticky=True),
        tooltip=folium.Tooltip('{}, {}, {}<br>Contagiados: {}<br>Edad promedio: {}'.format(dep,pro,dis,int(num),round(edad))),
        props = { 'population': num}
    ))

maPE.get_root().html.add_child(folium.Element(legend_html()))
maPE.get_root().html.add_child(folium.Element(title_html()))

maPE.save("CONTAGIOS COVID19_MORDOR.html")
maPE

import webbrowser
webbrowser.open("CONTAGIOS COVID19.html",new=2)
