# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 13:16:56 2016

@author: CR


 The main script which runs the dead reckoning logic.


"""

import logtools as lt 
import drfuncs  as dr
import matplotlib.pyplot as plt
import numpy as np


'''
 Import the log file 

'''
logpath = 'C:\Users\CR\Desktop' ## Location of the log file
logname = 'simlog.log' ## Name of the log file
delim   = ' ' ## The character that is used to deliminate the log file . Usually a space. 

log = lt.import_table(logpath,logname,delim) ## Import the log file as a pandas table

## Depending on what envelope of flight we are looking at, pull only data we are interested in
log = lt.isolate_ap_modes(log,[9,10])

## Extract what we need from the pandas table into lists
[time,p,q,r,xaccel,yaccel,zaccel,roll,pitch,yaw,maghdg] = dr.pull_att_data(log) 
zaccel = [i + 9.8065 for i in zaccel]

## We are going to estimate a timestamp here. Divide the total time 
## recorded by the number of entries to estimate a timestep. 
timestep = dr.timestep(time)

## Pull the NED velocities reported by the Piccolo for comparison.
[vnorth, veast, vdown] = dr.pull_ned_vel(log)

## Estimate the NED accelerations from the NED velocities.
[tay,tax,taz] = dr.generate_true_acc(vnorth, veast, vdown, timestep)

## Filter with a filter I found on the internet
smoother = 111
order = 4
#[xaccel, yaccel, zaccel, yaw, pitch, roll] = lt.smooth([xaccel,yaccel,zaccel,yaw,pitch,roll],smoother,order)

smoother = 111
order = 3
#[tay, tax, taz] = lt.smooth([tay, tax, taz], smoother, order)

'''
 Use the pulled data to generate a list of estimated accelerations in the inertial x, y, and z
 directions

'''
## Generate lists of the accelerations in each axis at each step in time
## by converting the body accelerations reported by the piccolo into
## inertial accelerations. 
[ay,ax,az] = dr.acc_body_to_inertial(roll,pitch,yaw,xaccel,yaccel,zaccel)

## Use an offset to try and remove some bias from the recorded values.
#[ax,ay,az] = dr.acc_bias_offset(ax,ay,az) 

'''
 Generate a list of velocities in each axis using the accelerations, and a known(?) timestep

'''
threshold = .2
[ax, ay, az] = dr.acc_filter(ax, ay, az, threshold)

## Convert the accelerations into velocities. The NED velocities are the initial conditions.
#[vx, vy, vz] = dr.acc_to_vel_newton_cotes([-i for i in ax], [-i for i in ay], [-i for i in az], veast[0], vnorth[0], vdown[0], time, 0)
#[vx, vy, vz] = dr.acc_to_vel_midpoint([-i for i in ax], [-i for i in ay], [-i for i in az], veast[0], vnorth[0], vdown[0], timestep, 0)
[vx, vy, vz] = dr.acc_to_vel_linear([-i for i in ax], [-i for i in ay], [-i for i in az], veast[0], vnorth[0], vdown[0], timestep, 0)

## Convert the directional velocities into velocity magnitudes
dr_vel = dr.magnitude(vy,vx,vz)[:-10]
true_vel = dr.magnitude(vnorth,veast,vdown)[:-10]


 