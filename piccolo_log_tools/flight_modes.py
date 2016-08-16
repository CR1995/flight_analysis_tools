# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 09:45:41 2016

Library of flight mode isolation functions.


@author: CR
"""

def list_ap_modes(log):
    '''
     list_ap_modes(): print out a list of all the AP modes present in a log file
    ''' 
    return list(log.ap_mode.unique())
    
def isolate_ap_modes(log,modes):
    '''
     isolate_ap_modes(): returns a pandas table which only has data where AP_Mode is 
     the same as in what is in the 'modes' list. 
     
     'modes' should be a list, even if you're only lookng for a single value, but
     it can accept integers as well.
    '''
    try:    
        for i in log['<ap_mode>']:
            if i not in modes:
                log = log[log['<ap_mode>'] != i]
            
    except TypeError:
        for i in log['<ap_mode>']:
            if i != modes:
                log = log[log['<ap_mode>'] != i]
    
    return log
        
def strip_preflight(log):
    '''
     strip_preflight(): returns a pandas table with preflight modes (modes 0 and 1, usually) removed.
     
     Useful in dead reckoning when preflight accelerations bias velocity integrations.
     
     Also useful for when you just don't want to see preflight data.
    '''
    preflight_modes = [0,1]
    
    
    for i in log['<ap_mode>']:
            if i in preflight_modes:
                log = log[log['<ap_mode>'] != i]

    return log

def strip_postflight(log):
    '''
     strip_postflight(): returns a pandas table with postflight modes (modes 11, 12, 13, and 14, usually) removed.
     
     Useful in dead reckoning when postflight accelerations bias velocity integrations.
     
     Also useful for when you just don't want to see postflight data. Usually used in conjunction
     with strip_preflight().
    '''    
    postflight_modes = [11,12,13,14]
    
    for i in log['<ap_mode>']:
            if i in postflight_modes:
                log = log[log['<ap_mode>'] != i]
        
    return log    
 
def isolate_flight(log):
    '''
     isolate_flight(): implements the strip_preflight() and strip_postflight() functions into a single package. 
     
     Useful when only flight data is required.
    ''' 
    log = strip_preflight(log)
    log = strip_postflight(log)
    
    return log