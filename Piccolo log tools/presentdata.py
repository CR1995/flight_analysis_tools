# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 09:05:18 2016



@author: CR
"""
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import pandas as pd

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filtfilt(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

files = []
data = {}

files = {
    'bsclimb': 'badsim climb.log',
    'bscruise': 'badsim cruise.log',
    'bsland': 'badsim land.log',
    'gsclimb': 'goodsim climb.log',
    'gscruise': 'goodsim cruise.log',
    'gsland': 'goodsim land.log',
    'rclimb': 'real climb.log',
    'rcruise': 'real cruise.log',
    'rland' : 'real land.log'
}

names = {
    'bs': 'Old',
    'gs': 'New',
    'r' : 'Actual'
}

for i in sorted(files):
    data[i] = pd.read_table(files[i])

x = [i for i in range(0,50)]

taslims = [10,32]

'''Plot TAS data'''
a,table = plt.subplots(3,sharex=True) 
plt.xlabel('time (s)')
#### Filtered
for k in sorted(data):
    if 'climb' in k: 
        filt = [i for i in butter_lowpass_filtfilt(data[k]['tas'],1500,25000)]
        for j in names:
            if j in k:
                lbl = names[j]
         
       
        table[0].plot(x,filt,label=lbl)
        table[0].set_title('Climb')
        table[0].set_ylabel('TAS (m/s)')
        table[0].set_ylim(taslims)
        table[0].legend(loc='best')
    
    if 'cruise' in k:
        filt = [i for i in butter_lowpass_filtfilt(data[k]['tas'],1500,25000)]
        for j in names:
            if j in k:
                lbl = names[j]
         
       
        table[1].plot(x,filt,label=lbl)
        table[1].set_title('Cruise')
        table[1].set_ylabel('TAS (m/s)')
        table[1].set_ylim(taslims)
        table[1].legend(loc='best')
        
    if 'land' in k:
        filt = [i for i in butter_lowpass_filtfilt(data[k]['tas'],1500,25000)]
        for j in names:
            if j in k:
                lbl = names[j]
         
       
        table[2].plot(x,filt,label=lbl)
        table[2].set_title('Final Approach')
        table[2].set_ylabel('TAS (m/s)')
        table[2].set_ylim(taslims)
        table[2].legend(loc='best')
plt.show()        

rpmlims = [0,8000]

'''Plot RPM data'''
a,table = plt.subplots(3,sharex=True) 
plt.xlabel('Time (s)')
#### Filtered
for k in sorted(data):
    if 'climb' in k: 
        filt = [i for i in butter_lowpass_filtfilt(data[k]['rpm'],1500,25000)]
        for j in names:
            if j in k:
                lbl = names[j]
        
        table[0].plot(x,filt,label=lbl)
        table[0].set_title('Climb')
        table[0].set_ylabel('RPM')
        table[0].set_ylim(rpmlims)
        table[0].legend(loc='best')
    
    if 'cruise' in k:
        filt = [i for i in butter_lowpass_filtfilt(data[k]['rpm'],1500,25000)]
        for j in names:
            if j in k:
                lbl = names[j]
                
        table[1].plot(x,filt,label=lbl)
        table[1].set_title('Cruise')
        table[1].set_ylabel('RPM')
        table[1].set_ylim(rpmlims)
        table[1].legend(loc='best')
        
    if 'land' in k:
        filt = [i for i in butter_lowpass_filtfilt(data[k]['rpm'],1500,25000)]
        for j in names:
            if j in k:
                lbl = names[j]
                
        table[2].plot(x,filt,label=lbl)
        table[2].set_title('Final Approach')
        table[2].set_ylabel('RPM')
        table[2].set_ylim(rpmlims)
        table[2].legend(loc='best')
plt.show()        


