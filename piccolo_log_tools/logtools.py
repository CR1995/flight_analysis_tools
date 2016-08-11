# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 15:26:46 2016

@author: CR

A collection of functions used in analyzing Piccolo log files.

"""

from math import factorial
import pandas as pd
import numpy as np
import os

def import_table(path, name, delim):
    ''' 
     import_table(): imports a log file into a pandas table. Mostly just used to avoid
     remembering all of the function arguments.
    
     It takes the log path, log name, and a delimeter as arguments. The path and the
     filename have to be separated to avoid issues Python has with opening
     strings formatted a certain way. For example, if the full path of your file is
     'C:/Users/Chris/Desktop/nlog.log', then the 'n' at the beginning of the log name
     will make python interpret the '\n' as a call for a new line, messing up the script.
     
     This is avoided by using os.path.join() to formulate the full path.
    
     This function will eventually incorporate the standard log conversion function James
     is developing.
    
    '''
    fullpath = os.path.join(path,name) # Generate the full file path  
    data = pd.read_table(fullpath, sep=delim, header=0, skipinitialspace=True) # Generate a table with pandas
    return data

def isolate_ap_modes(log,modes):
    '''
     isolate_ap_modes(): returns a pandas table which only has data where AP_Mode is 
     the same as in what is in the 'modes' list. 
     
     'modes' should be a list, even if you're only lookng for a single value, but
     it can accept integers as well.
    '''
    #newlog = log.copy(deep=True)
    try:    
        for i in log['<AP_Mode>']:
            if i not in modes:
                log = log[log['<AP_Mode>'] != i]
            
    except TypeError:
        for i in log['<AP_Mode>']:
            if i != modes:
                log = log[log['<AP_Mode>'] != i]
    
    return log
        
def strip_preflight(log):
    '''
     strip_preflight(): returns a pandas table with preflight modes (modes 0 and 1, usually) removed.
     
     Useful in dead reckoning when preflight accelerations bias velocity integrations.
     
     Also useful for when you just don't want to see preflight data.
    '''
    preflight_modes = [0,1]
    
    
    for i in log['<AP_Mode>']:
            if i in preflight_modes:
                log = log[log['<AP_Mode>'] != i]

    return log

def strip_postflight(log):
    '''
     strip_postflight(): returns a pandas table with postflight modes (modes 11, 12, 13, and 14, usually) removed.
     
     Useful in dead reckoning when postflight accelerations bias velocity integrations.
     
     Also useful for when you just don't want to see postflight data. Usually used in conjunction
     with strip_preflight().
    '''    
    postflight_modes = [11,12,13,14]
    
    for i in log['<AP_Mode>']:
            if i in postflight_modes:
                log = log[log['<AP_Mode>'] != i]
        
    return log    
 
def isolate_flight(log):
    '''
     isolate_flight(): implements the strip_preflight() and strip_postflight() functions into a single package. 
     
     Useful when only flight data is required.
    ''' 
    log = strip_preflight(log)
    log = strip_postflight(log)
    
    return log
   
def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')  
    
def smooth(*args):
    '''
     smooth_acc(): implements the Savitzky smoother in the log tools library in a 
     cleaner fashion. 
     
     Smoother value correlates with level of smoothness. Higher smoother, higher smoothness.
     
     Order is the order of the smoothing. Ex: order = 3 means it uses a third order
     equation to smooth.
    ''' 
    v = []
    smoother = args[1]
    order = args[2]

    for i in args[0]:
        v.append(savitzky_golay(i,smoother,order))
        
    return v   
      
      