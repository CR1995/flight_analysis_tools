# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 08:40:57 2016

A collection of functions related to calculating the distance flown. Not sure
this really needs its own library but I don't know what else to do with it.

@author: CR
"""

def haversine(lat1, lon1, lat2, lon2):
    '''
     haversine(): a function which implements the Haversine formula to
     calculate the distance between two locations given their latitude 
     and longitude. 
     
     Source: https://rosettacode.org/wiki/Haversine_formula#Python
     
    '''
 
    from math import radians, sin, cos, sqrt, asin 
 
    R = 6372.8 # Earth radius in kilometers
     
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c
    
def distance_flown(log):
    '''
     distance_flown(): calculates the total distance flown during the portion 
     of flight recorded in the log file. Sums the incremental differences in 
     longitude and lattiude using the haversine() function to determine total
     distance flown. Also returns total time flown.
     
     Takes a Pandas table as input, but it returns the distance over the entire 
     log, so make sure the log is reduced to the region of interest before
     implementing this function.
     
     Returns:
         - Distance flown (miles)
         - Time flown (seconds)
     
    '''    
    dist = []
    time = []
    for i in range(log.index[0] + 1, log.index[-1]+1):
        lat1 = log.latitude[i-1]
        lat2 = log.latitude[i]
        lon1 = log.longitude[i-1]
        lon2 = log.longitude[i]
        
        dist.append(haversine(lat1,lon1,lat2,lon2))
        time.append(float(log.time[i]))
        
    dist = sum(dist) * .621371
    time = time[-1] - time[0]
    
    return dist, time
    