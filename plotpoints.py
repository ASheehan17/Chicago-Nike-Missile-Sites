#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 17:52:54 2022

@author: alexsheehan
"""
import pandas as pd
import folium
import re
from statistics import mean
sites = pd.read_csv("sites.csv")

#Jackson Park Coordiantes need adjustment
jp = sites.iloc[6,:]
sites = sites.drop(index = 6)
lats = []
longs = []


#Change format of coordinates
def to_degree_decimal(lat,long):
    #adjust lat
    deg, minutes, seconds, direction =  re.split('[°\′″]', lat)
    y = (float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1)
    lats.append(y)
    
    #adjust long
    deg, minutes, seconds, direction =  re.split('[°\′″]', long)
    y = (float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1)
    longs.append(y)
    
for i in range(0,len(sites.iloc[:,0])):
    lat = sites.iloc[i,0]
    lat = lat.split()[0]
    
    long = sites.iloc[i,0]
    long = long.split()[1]
    
    to_degree_decimal(lat,long)
    
#Jackson Park Coordinates need adjustment
jpcoord = jp[0]
jplat = jpcoord.split()[0]
jplong = jpcoord.split()[1]
jplat = jplat[0:-2]
jplong = jplong[0:-2]
names = list(sites.iloc[:,1])
names.append("Jackson Park")
lats.append(float(jplat))
longs.append(float(jplong)*-1)


map = folium.Map(location=[mean(lats), mean(longs)], zoom_start=10, control_scale=True)
for i in range(0,len(lats)):
    folium.Marker([lats[i],longs[i]], popup=names[i]).add_to(map)
map.save("map.html")
