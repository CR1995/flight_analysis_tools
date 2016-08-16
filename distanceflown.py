# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 13:35:41 2016

@author: CR
"""
from flight_analysis_library import *
from math import radians, sin, cos, sqrt, asin

logpath = 'C:\Users\CR\Desktop\distlog.log'

## Import the log file. This takes a while.
log = import_log(logpath,0,0)

## Remove unnecessary flight modes
log = isolate_flight(log)

def haversine(lat1, lon1, lat2, lon2):
 
    R = 6372.8 # Earth radius in kilometers
     
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c

dist = []
time = []
for i in range(log.index[0] + 1, log.index[-1]+1):
    lat1 = log.latitude[i-1]
    lat2 = log.latitude[i]
    lon1 = log.longitude[i-1]
    lon2 = log.longitude[i]
    
    dist.append(haversine(lat1,lon1,lat2,lon2))
    time.append(float(log.time[i]))
    
print sum(dist) * .621371
print 'Time elapsed: %f (s)' % (time[-1] - time[0])
    


