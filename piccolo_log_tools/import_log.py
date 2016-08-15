# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 14:31:09 2016

Collection of functions used to import log files.

@author: CR
"""

def import_log(logpath, config, version):
    from pandas import *
    import numpy as np
    
    data_import = import_table(logpath, ' ')

    data = DataFrame(columns=['time', 'tas', 'velocity_north', 'velocity_east', 
                          'velocity_down', 'beta', 'alpha', 'roll_rate', 
                          'pitch_rate', 'yaw_rate', 'roll', 'pitch', 'yaw', 
                          'a_x', 'a_y', 'a_z', 'alt_gps', 'alt_baro', 'agl', 
                          'longitude', 'latitude', 'dynamic_pressure', 'static_pressure', 
                          'density_air', 'oat', 'ap_mode', 'alt_ctrl', 'alt_track', 
                          'x_track', 'y_track', 'z_track', 'velocity_track', 'surface_0', 
                          'surface_1', 'surface_2', 'surface_3', 'surface_4', 'surface_5', 
                          'surface_6', 'surface_7', 'surface_8', 'surface_9', 'surface_10', 
                          'surface_11', 'surface_12', 'surface_13', 'surface_14', 'surface_15'])
    
    
    #unit converstions
    mstos = .001
    
    #importing data fields and performing unit conversions 
    data['time'] = (data_import['<Clock>[ms]'] - data_import.ix[0,'<Clock>[ms]']) * mstos
    data['tas'] = data_import['<TAS>[m/s]']
    data['velocity_north'] = data_import['<VNorth>[m/s]']
    data['velocity_east'] = data_import['<VEast>[m/s]']
    data['velocity_down'] = data_import['<VDown>[m/s]']
    data['alpha'] = np.rad2deg(data_import['<Pitch>[rad]'])
    data['roll_rate'] = np.rad2deg(data_import['<P>[rad/s]'])
    data['pitch_rate'] = np.rad2deg(data_import['<Q>[rad/s]'])
    data['yaw_rate'] = np.rad2deg(data_import['<R>[rad/s]'])
    data['roll'] = np.rad2deg(data_import['<Roll>[rad]'])
    data['pitch'] = np.rad2deg(data_import['<Pitch>[rad]'])
    data['yaw'] = np.rad2deg(data_import['<Yaw>[rad]'])
    data['a_x'] = data_import['<Xaccel>[m/s/s]']
    data['a_y'] = data_import['<Yaccel>[m/s/s]']
    data['a_z'] = data_import['<Zaccel>[m/s/s]']
    data['alt_gps'] = data_import['<Height>[m]']
    #data['alt_baro'] = data_import['<BaroAlt>[m]']
    data['agl'] = data_import['<AGL>[m]']
    data['longitude'] = np.rad2deg(data_import['<Lat>[rad]'])
    data['latitude'] = np.rad2deg(data_import['<Lon>[rad]'])
    data['dynamic_pressure'] = data_import['<Dynamic>[Pa]']
    data['static_pressure'] = data_import['<Static>[Pa]']
    data['oat'] = data_import['<OAT>[C]']
    data['ap_mode'] = data_import['<AP_Mode>']
    data['alt_ctrl'] = data_import['<AltCtrl>']
    data['alt_track'] = data_import['<LoopTarget1>']
    data['x_track'] = data_import['<Track_X>[m]']
    data['y_track'] = data_import['<Track_Y>[m]']
    data['z_track'] = data_import['<Track_Z>[m]']
    data['velocity_track'] = data_import['<LoopTarget0>']
 
    
    #importing surface data from piccolo. Eventually write function to match surfaces data with surface name
    data['surface_0'] = data_import['<Surface0>']
    data['surface_1'] = data_import['<Surface1>']
    data['surface_2'] = data_import['<Surface2>']
    data['surface_3'] = data_import['<Surface3>']
    data['surface_4'] = data_import['<Surface4>']
    data['surface_5'] = data_import['<Surface5>']
    data['surface_6'] = data_import['<Surface6>']
    data['surface_7'] = data_import['<Surface7>']
    data['surface_8'] = data_import['<Surface8>']
    data['surface_9'] = data_import['<Surface9>']
    data['surface_10'] = data_import['<Surface10>']
    data['surface_11'] = data_import['<Surface11>']
    data['surface_12'] = data_import['<Surface12>']
    data['surface_13'] = data_import['<Surface13>']
    data['surface_14'] = data_import['<Surface14>']
    data['surface_15'] = data_import['<Surface15>']
    
    
    #calculating air density using oat and static pressure data from piccolo
    t = data['oat'] + 273
    data['density_air'] = data['static_pressure'] / (t * 287)
    
    #Rough beta approximation. Slip from the difference between heading and yaw   
    data['beta'] = np.rad2deg(data_import['<Direction>[rad]'] - data_import['<Yaw>[rad]'])
    for i in range(len(data)):
        beta = data.ix[i, 'beta']
        if beta > 30:
            data.ix[i,'beta'] = beta - 360;
        elif beta < -30:
            data.ix[i,'beta'] = beta + 360;
    
    return data
    
def import_table(path, delim):
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
    import pandas as pd    
    import os
    
    fullpath = os.path.normpath(path) # Generate the full file path  
    data = pd.read_table(fullpath, sep=delim, header=0, skipinitialspace=True, low_memory = False) # Generate a table with pandas
    return data    
        
    