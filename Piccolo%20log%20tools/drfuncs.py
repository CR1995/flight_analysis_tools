# -*- coding: utf-8 -*-
"""
Created on Mon Aug 01 14:15:19 2016

@author: CR

A collection of functions used for the dead reckoning project.

"""

import numpy as np
import logtools as lt

def pull_att_data(log):
    '''
     pull_att_data(): returns a normal Python list of relevant log values. It 
     takes a pandas table as input.
    
     Returns the list-converted log data
    '''
    #time = [(float(i) - log['<Clock>[ms]'][0])/1000 for i in log['<Clock>[ms]']] # Converts the <Clock> field to seconds, always starting from 0
    time = [float(i)/1000.0 for i in log['<Clock>[ms]']]    
    
    p = [i for i in log['<P>[rad/s]']]
    q = [i for i in log['<Q>[rad/s]']]
    r = [i for i in log['<R>[rad/s]']]
    
    xaccel = [i for i in log['<Xaccel>[m/s/s]']]
    yaccel = [i for i in log['<Yaccel>[m/s/s]']]
    zaccel = [i for i in log['<Zaccel>[m/s/s]']]
    
    roll =  [i for i in log['<Roll>[rad]']]
    pitch = [i for i in log['<Pitch>[rad]']]
    yaw =   [i for i in log['<Yaw>[rad]']]
    
    maghdg = [i for i in log['<MagHdg>[rad]']]
    
    return time,p,q,r,xaccel,yaccel,zaccel,roll,pitch,yaw,maghdg

def pull_ned_vel(log):
    '''
     pull_ned_vel(): pulls the VNorth, VEast, and VDown velocities from a log file.
     
     Used generally to just save space make scripts look nicer.
    ''' 
    veast = [i for i in log['<VEast>[m/s]']]
    vnorth = [i for i in log['<VNorth>[m/s]']]
    vdown = [i for i in log['<VDown>[m/s]']]
    
    return vnorth, veast, vdown

def acc_body_to_inertial(roll,pitch,yaw,xaccel,yaccel,zaccel):    
    '''
     acc_body_to_inertial(): takes body accelerations reported by the Piccolo (after 
     being pushed to list form) and converts them to accelerations in the inertial 
     reference frame. 
    
     Returns 3 values (or normal python lists, if given lists) for the x, y, and 
     z accelerations in the inertial reference frame.
    
     The logic here is to break down the accelerations into their different components 
     in the desired directions.
    
    '''    
    ax_x = np.cos(pitch)*np.cos(yaw)
    ax_y = np.cos(pitch)*np.sin(yaw)
    ax_z = -np.sin(pitch)
    
    ay_x = np.sin(roll)*np.sin(pitch)*np.cos(yaw) - np.cos(roll)*np.sin(yaw)
    ay_y = np.sin(roll)*np.sin(pitch)*np.sin(yaw) + np.cos(roll)*np.cos(yaw)
    ay_z = np.sin(roll)*np.cos(pitch)
    
    az_x = np.cos(roll)*np.sin(pitch)*np.cos(yaw) + np.sin(roll)*np.sin(yaw)
    az_y = np.cos(roll)*np.sin(pitch)*np.sin(yaw) - np.sin(roll)*np.cos(yaw)
    az_z = np.cos(roll)*np.cos(pitch)
    
    ax = (ax_x * xaccel) + (ax_y * yaccel) + (ax_z * zaccel)
    ay = (ay_x * xaccel) + (ay_y * yaccel) + (ay_z * zaccel)
    az = (az_x * xaccel) + (az_y * yaccel) + (az_z * zaccel)
    
    return ax,ay,az

def acc_bias_offset(ax,ay,az):
    '''
     acc_bias_offset(): finds the mean of each acceleration and subtracts that
     value from every datapoint. Forces the average acceleration to be zero,
     when you know that the velocity at the beginning and end of the data should
     be equal.
     
    ''' 
    xoffset = np.mean(ax)
    yoffset = np.mean(ay)
    zoffset = np.mean(az)
    
    ax = [i - xoffset for i in ax]
    ay = [i - yoffset for i in ay]
    az = [i - zoffset for i in az]
    return ax,ay,az

def acc_filter(a,threshold):
    '''
     acc_filter(): sets accelerations below a certain threshold to 0 to avoid
     changes in velocity when accelerations are very low.
     
    '''
    if np.abs(a) < threshold:
        a = 0
    return a    

def acc_to_vel(ax,ay,az,vx0,vy0,vz0,dt):
    '''
     acc_to_vel(): takes in three lists of accelerations plus a constant timestep 
     and returns three lists of velocities. 
    '''
    
    ## The threshold for acceleration filtering.
    threshold = .5
    
    vx = [vx0 for i in range(len(ax) + 1)]
    vy = [vy0 for i in range(len(ay) + 1)]
    vz = [vz0 for i in range(len(az) + 1)]  

    for i in range(1,len(ax)):
        
        acc_filter(ax[i], threshold)
        
        vx[i] = vx[i-1] + ax[i]*dt
        vy[i] = vy[i-1] + ay[i]*dt
        vz[i] = vz[i-1] + az[i]*dt
        
    vx[-1] = vx[-2]
    vy[-1] = vy[-2]
    vz[-1] = vz[-2] 
    
    return vx,vy,vz

def vel_magnitude(vn,ve,vd):
    '''
     vel_magnitude(): generates a velocity magnitude for a given set of directional
     velocities.
     
    '''
    v = []
    for i in range(len(vn)):
        val = vn[i]**2 + ve[i]**2 + vd[i]**2
        v.append(np.sqrt(val))
    return v        
    
    