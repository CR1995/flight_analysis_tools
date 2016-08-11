# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 13:26:02 2016

@author: Ramos

Get data from log file, narrow it down, calculate stuff and plot as a function of time in seconds

Also writes recorded data to text file for processing in presentdata.py


LANDING considered during final
CLIMB considered immediately after liftoff
CRUISE considered constant altitude flight
SAMPLE TIME is 50 seconds


"""
#### Import everything
import pandas as pd
import matplotlib.pyplot as plt
import math as m
import numpy as np
import os

####
## Config
####

#### Toggle legend/AP_Mode markers
sl = True

#### Toggle saving images
save = False

#### Toggle flight modes (doesn't do anything currently)
takeoff = False
cruise  = False
landing = False

#### Toggle recording modes
autotime = 0  # Finds when AP_Mode switches to desired mode, then records x seconds after that
findapmode = 0 # Records specific AP_Mode's only
timerange = 1 # Records a set time range

#### Data file path
fpath = 'C:\Users\CR\Cloud Cap\Piccolo Command Center 2.1.4\Telemetry' 

#### Log file name
fsname = 'goodsim'
fname = fsname + '.log'

#### Log location
df = os.path.join(fpath,fname)

#### Initialize data variable
data = pd.read_table(df, sep=' ', header=0, skip_blank_lines=True)

#### Convert time from [ms] to [s]
data['<Clock>[ms]'] = data['<Clock>[ms]'] / 1000

#### List of AP_Modes for legend
apmodes = ['0 - Prelaunch', '1 - Transition', '2 - Liftoff', '3 - Climbout', 
           '4 - Flying', '5 - Landing', '6 - Downwind', '7 - Base', '8 - Final', 
           '9 - Short Final', '10 - Touchdown', '11 - Rollout', '12 - Final T&G',
           '13 - Short Final T&G', '14 - T&G']

#### autotime detect settings
automode = 2     # Refer to apmodes list. This mode triggers the recorder 
rectime  = 500  # Time to record (seconds)
toffset  = -10    # Time of offset recording (Used for fine tuning data)

#### findapmode settings
findmode1 = 0
findmode2 = 1

#### timerange settings
if timerange:
    start = 63 # Time(s) to start recording
    end =   113 # Time(s) to end recording

####
## Retrieve the data (these lists have the full data)
####
dapmode = data['<AP_Mode>']       # Autopilot mode
drpm = data['<LeftRPM>']          # Engine RPM
dtime = data['<Clock>[ms]']       # Time (s)
dvdown = data['<VDown>[m/s]']     # Downwards velocity
dalt = data['<Height>[m]']        # Atitude
dthrottle = data['<Surface2>']    # Throttle setting
dtas = data['<TAS>[m/s]']         # True air speed
ddynpress = data['<Dynamic>[Pa]'] # Dynamic pressure
dax = data['<Xaccel>[m/s/s]']      # X Acceleration
daz = data['<Zaccel>[m/s/s]']      # Z Acceleration

dltime = []
dlapmode = []
dlstatpress = []
for i in dtime: dltime.append(m.floor(i))   # Make a useable list of total time
for i in dapmode: dlapmode.append(i)        # Make a useable list of total apmodes

#### Create lists to store refined data
apmode = []
rpm = []
vdown = []
throttle = []
time = []
alt = []
tas = []
dynpress= []
ax = []
az = []

########
#### Use AP_Mode to refine data. This probably isn't very useful now, but I'll leave it here just in case.
########
if findapmode:
    start = dltime[dlapmode.index(findmode1)]
    end = dltime[dlapmode.index(findmode2)]
    ttime = start - end
    mttime = ttime/60

elif autotime:
    start = dltime[dlapmode.index(automode)] + toffset
    end = start + rectime
    ttime = rectime+toffset
    mttime = ttime/60
elif timerange:
    ttime  = end-start # Length of recording
    mttime = ttime/60  # Convert to minutes

rstime = dltime.index(start) # Real start time
retime = dltime.index(end)   # Real end time

print '\nShowing data in range from %f seconds to %f seconds (%i seconds/%i mins total)' % (dtime[rstime], dtime[retime], ttime,mttime)
print '\nAP_Mode at start = %i' % dapmode[rstime]


for i in range(dltime.index(start), dltime.index(end), 1):
    #### Create refined lists
    apmode.append(int(dapmode[i])) 
    rpm.append(drpm[i])
    vdown.append(dvdown[i])
    time.append(dtime[i])
    alt.append(dalt[i])
    throttle.append(dthrottle[i])
    tas.append(dtas[i])
    dynpress.append(ddynpress[i])
    ax.append(dax[i])
    az.append(daz[i] + 9.81)
    
########
#### Marking times when AP_Mode changes
########
    
aptime = [[],[]]         
for i in range(len(apmode)-1):
    old = apmode[i]
    new = apmode[i+1]
    if old != new:
        aptime[0].append(time[i+1])
        aptime[1].append(new)
        
for i in aptime[0]:
    print 'AP_Mode changes to %i at time=%f, index=%i' % (aptime[1][aptime[0].index(i)], i, dltime.index(m.floor(i)))

print 'AP_Mode at end   = %i' % dapmode[retime]

########
#### Calculating stuff using collected data
########

pvdown = [] # List to store inverted vdown,az info since we want positive velocity upwards
for i in vdown: pvdown.append(-i)  

mass   = 219      # Plane mass (kg)
g      = 9.81     # Acceleration due to gravity (m/s/s)
weight = mass*g   # Plane weight(newtons)
cdp    = .05      # Profile CD
s      = 4.444    # Reference area(m^2)
ar     = 9.45     # Wing aspect ratio
e      = .8       # Oswald efficiency factor for the wing

avgrpm = np.mean(rpm)
avgvz  = np.mean(pvdown)
avgalt = np.mean(alt)
prat   = np.exp(-avgalt/7000)
avgtas = np.mean(tas)
avgdps = np.mean(dynpress)
avgax  = np.mean(ax)
avgaz  = np.mean(az)

aoc = []
for i in range(len(tas)):
    aoc.append(m.sin(pvdown[i]/tas[i]))

aaoc = m.sin(avgvz/avgtas) # Average angle of climb
cl = []    
cdt = []        
for i in aoc:
    cl.append((weight*m.cos(i))/(dynpress[aoc.index(i)]*s)) # CL for cdt calculation. Should probably find in xml instead
    cdt.append(cdp + (cl[aoc.index(i)]**2)/(m.pi*e*ar))     # Total drag

thrust = []
drag = []
for i in dynpress:
    drag.append(i*cdt[dynpress.index(i)]*s)

for i in range(len(pvdown)):
    val = ((pvdown[i]*weight)/tas[i]) + drag[i]
    if not landing: thrust.append(val)

avgdrag = np.mean(drag)
avgcl = np.mean(cl)

for i in range(len(ax)):
    if landing:
        a = ax[i]**2 + az[i]**2
        a = -np.sqrt(a)
        t = abs(mass*a + drag[i] - weight*m.sin(aoc[i]))
        thrust.append(t)
    
avgthr = np.mean(thrust)
    

print 'Average RPM: %f' % avgrpm
print 'Average Vz: %f(m/s)' % avgvz
print 'Average TAS: %f(m/s)' % avgtas 
#print 'Average Alt: %f(m)' % avgalt
#print 'Press. Rat.: %f\n' % prat
                      
########
#### Plotting data 
########

colors = ['k','g','r','c','m','y','b', '#FFA500', '#808080', '#2F4F4F', '#A52A2A', '#FF00FF'] # List of colors 

#### Set figure sizes
fh = 10   # figure height
fw = 13  # figure width
plt.rcParams['figure.figsize'] = [fw,fh]
                     
'''
#### Plotting data. Copied this from two_axis_plot.py
#### Plots RPM and VDown vs time (s) on same graph       
fig, ax1 = plt.subplots()
ax1.plot(time,rpm, 'b-')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('RPM', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')

ax2 = ax1.twinx()
ax2.plot(time, vdown, 'r')
ax2.set_ylabel('Vz', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
plt.show()

sf = 'C:\Users\Ramos\Desktop\graph.png'
plt.savefig(sf,dpi=300)  
'''      

#### Plot RPM vs time (s)
plt.plot(time, rpm)
plt.title('RPM vs. Time(s)')
plt.xlabel('Time (s)')
plt.ylabel('RPM')
plt.grid(True)
q = 0
for i in aptime[0]:
    mode = aptime[1][aptime[0].index(i)]
    if sl: plt.axvline(x=i, color=colors[mode], hold=None, label=apmodes[mode], linewidth=2)
    q+=1
if sl: plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
if save: plt.savefig('rpmvstime.png', bbox_inches='tight')
plt.show()


'''
#### Plot VDown vs time (s)
plt.plot(time, pvdown)
plt.title('Vz(m/s) vs. Time(s)')
plt.xlabel('Time (s)')
plt.ylabel('Vz(m/s)')
plt.grid(True)
q = 0
for i in aptime[0]:
    mode = aptime[1][aptime[0].index(i)]
    if sl: plt.axvline(x=i, color=colors[mode], hold=None, label=apmodes[mode], linewidth=2)
    q+=1
plt.axhline(y=0, color='k', hold=None, linewidth=1)    
if sl: plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
if save: plt.savefig('vdownvstime.png', bbox_inches='tight')
plt.show()
'''

#### Plot throttle vs time (s)
plt.plot(time, throttle)
plt.title('Throttle vs. Time(s)')
plt.xlabel('Time (s)')
plt.ylabel('Throttle')
plt.ylim(0,1.2)
plt.grid(True)
q = 0
for i in aptime[0]:
    mode = aptime[1][aptime[0].index(i)]
    if sl: plt.axvline(x=i, color=colors[mode], hold=None, label=apmodes[mode], linewidth=2)
    q+=1
if sl: plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
if save: plt.savefig('throttlevstime.png', bbox_inches='tight')
#plt.legend(loc=0)
plt.show()


#### Plot True Air Speed vs time (s)
plt.plot(time, tas)
plt.title('True Air Speed (m/s) vs. Time(s)')
plt.xlabel('Time (s)')
plt.ylabel('TAS(m/s)')
plt.grid(True)
q = 0
for i in aptime[0]:
    mode = aptime[1][aptime[0].index(i)]
    if sl: plt.axvline(x=i, color=colors[mode], hold=None, label=apmodes[mode], linewidth=2)
    q+=1
if sl: plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
if save: plt.savefig('tasvstime.png', bbox_inches='tight')
plt.show() 


#### Plot alt vs time (s)
plt.plot(time, alt)
plt.title('Altitude(m) vs. Time(s)')
plt.xlabel('Time (s)')
plt.ylabel('Altitude(m)')
plt.grid(True)
q = 0
for i in aptime[0]:
    mode = aptime[1][aptime[0].index(i)]
    if sl: plt.axvline(x=i, color=colors[mode], hold=None, label=apmodes[mode], linewidth=2)
    q+=1
if sl: plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
if save: plt.savefig('altvstime.png', bbox_inches='tight')
plt.show()

print 'Average thrust: %f pounds\n' % (avgthr*.224809) 

print avgtas
print avgvz

power = [i * thrust[tas.index(i)] for i in tas]

pa = avgtas * avgthr
pu = avgvz  * weight
p  = np.sqrt(pa**2 - pu**2)
print p

txtname = '%s log.log' % fsname
text_file = open(txtname,'w')
text_file.write('index\talt\trpm\ttas\n')
for i in range(len(time)):
    string = '%i\t%f\t%i\t%f\n' % (i,alt[i],rpm[i],tas[i])
    text_file.write(string)
text_file.close()   
  
    
    


