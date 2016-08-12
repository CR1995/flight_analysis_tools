#reads log files in a targeted directory and pulls requested data when gyro data is larger then set threshold value
from pandas import Series, DataFrame
import numpy as np
import scipy as sp
import pandas as pd
import os

path = 'C:\Users\JAMES\Desktop\Soak_Test_June_2016\log_files_new' #pathway for log directory
ext  = '.log' # File extension to search for 
threshold = 0.0872665 #set radian/second threshold for gyro


data_out = DataFrame(columns=['P','Q','R', 'piccolo', 'clock','hours','minutes','seconds'])
count = 0
radtodeg = 57.2958

for i in os.listdir(path): # For each file in the directory...
    if i.endswith(ext): # Find the ones with the desired extension       
        df   = os.path.join(path,i) # Combine the path with the file name for the current log file
        data = pd.read_table(df, sep=' ', header=0, skipinitialspace=True, low_memory=False) # Read the current log file
        print i        
        for k in range(len(data)):
            if data.ix[k,'<P>[rad/s]'] > threshold or data.ix[k,'<Q>[rad/s]'] > threshold or data.ix[k,'<R>[rad/s]'] > threshold or data.ix[k,'<P>[rad/s]'] < -1*threshold or data.ix[k,'<Q>[rad/s]'] < -1*threshold or data.ix[k,'<R>[rad/s]'] < -1*threshold: 
                data_out.set_value(count,'P',data.get_value(k,'<P>[rad/s]')*radtodeg)
                data_out.set_value(count,'Q',data.get_value(k,'<Q>[rad/s]')*radtodeg)
                data_out.set_value(count,'R',data.get_value(k,'<R>[rad/s]')*radtodeg)
                data_out.set_value(count,'piccolo',i)
                data_out.set_value(count,'clock',data.get_value(k,'<Clock>[ms]'))
                data_out.set_value(count,'hours',data.get_value(k,'<Hours>'))
                data_out.set_value(count,'minutes',data.get_value(k,'<Minutes>'))
                data_out.set_value(count,'seconds',data.get_value(k,'<Seconds>'))
                count += 1

