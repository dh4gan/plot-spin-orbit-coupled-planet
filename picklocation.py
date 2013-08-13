# Written by D Forgan, 12/8/2013
# Reads in output dumps from spinorbit_coupled_planet (C++ code)
# Produces flux map and movie of star position

import numpy as np
import matplotlib.pyplot as plt
from string import split
from os import system
#from sys import exit

pi = 3.1415926585

longcol = 0
latcol = 1
fluxcol = 2 
altcol = 3
azcol = 4

# Read in input parameters

#prefix = raw_input("What is the file prefix? ")
#nfiles = input("How many files? ")
#moviechoice = raw_input("Make an animated gif at end? (y/n) ")
#deletechoice = 'n'
#if(moviechoice=='y'):
#    deletechoice = raw_input("Delete .png files? (y/n) ")

prefix = 'trial'
nfiles = 100
moviechoice = 'y'
deletechoice = 'n'

nzeros = int(np.log10(nfiles))

# Arrays to hold flux, altitude and azimuth data

time = np.zeros(nfiles)
flux = np.zeros(nfiles)
altitude = np.zeros(nfiles)
azimuth = np.zeros(nfiles)
height= np.zeros(nfiles)
horizontal = np.zeros(nfiles)

# Loop over files

for i in range(nfiles):

    # Create filename - how many zeros needed?
    num = str(i+1)
    k=np.log10(i+1)
    while (k<nzeros): 
        num = "0"+num
        k+=1        
    
    inputfile = prefix + '.'+num
    
    # Read in header - time, position data etc



    f = open(inputfile, 'r')

    line = f.readline()

    numbers = split(line)

    time[i]=float(numbers[0])
    nlat = int(numbers[1])
    nlong = int(numbers[2])
    
    
    f.close()
    
    print 'File ', str(i+1),' Time  ', time[i]

    # Read in rest of file
    
    data = np.genfromtxt(inputfile, skiprows=1)
    
    if(i==0):
        # Pick from possible latitudes
        
        lat_possibles = np.unique(data[:,latcol])
                
        print "Fix value of latitude: here are the choices"
        for i in range (len(lat_possibles)):
            print '(',i,')', lat_possibles[i]
    
        latselect = input("Enter integer corresponding to desired value: ")        
        mylat= lat_possibles[latselect]
        
        long_possibles = np.unique(data[:,longcol])
        print "Fix value of longitude: here are the choices"
        for i in range (len(long_possibles)):
            print '(',i,')', long_possibles[i]
    
        longselect = input("Enter integer corresponding to desired value: ")
        mylong= long_possibles[longselect]
        
                        
    
    skyfile = 'skypos_'+prefix+num+'_latlong_'+str(mylat)+'_'+str(mylong)+'.png'
    
    # Select flux only from the correct latitude and longitude    
    
    myentry = data[data[:,latcol]==mylat]
    myentry = myentry[myentry[:,longcol]==mylong]        
        
    flux[i] = myentry[0,fluxcol]        
    altitude[i] = myentry[0,altcol]
    azimuth[i] = myentry[0,azcol]    
    
    height[i] = np.sin(altitude[i])
    horizontal[i] = -np.cos(azimuth[i])*np.sin(altitude[i])
    
    print azimuth[i], altitude[i], horizontal[i], height[i]
    # Plot sky position for this timestep
    
    fig1 = plt.figure(1)
    ax = fig1.add_subplot(111)
    ax.set_xlabel('Horizontal Position')
    ax.set_ylabel('Height')
    ax.set_ylim(-2,2)
    ax.set_xlim(-1,1)    
    plt.scatter(horizontal[i],height[i], marker='o', color='red')
    if(i>0): plt.plot(horizontal,height, linestyle='--', color='blue')    
    plt.savefig(skyfile, format= 'png')
    plt.clf()


# end of loop

# Plot flux

fluxfile = 'flux_'+prefix+'_latlong_'+str(mylat)+'_'+str(mylong)+'.png'    

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Time (yr)')
ax.set_ylabel('Flux (arbitrary)')
plt.plot(time,flux)

plt.savefig(fluxfile, format= 'png')

# Plot altitude

altfile = 'altitude_'+prefix+'_latlong_'+str(mylat)+'_'+str(mylong)+'.png'    

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Time (yr)')
ax.set_ylabel('Altitude (degrees)')
plt.plot(time,altitude)

plt.savefig(altfile, format= 'png')

# Plot azimuth

azfile = 'az_'+prefix+'_latlong_'+str(mylat)+'_'+str(mylong)+'.png'    

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Time (yr)')
ax.set_ylabel('azimuth (degrees)')
plt.plot(time,azimuth)

plt.savefig(azfile, format= 'png')

# Plot height and horizontal on same graph

azfile = 'hh_'+prefix+'_latlong_'+str(mylat)+'_'+str(mylong)+'.png'    

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Time (yr)')
ax.set_ylabel('x(y) position')
plt.plot(time,height, color='red')
plt.plot(time,horizontal, color='blue')

plt.savefig(azfile, format= 'png')

# Command for converting images into gifs - machine dependent

#convertcommand = '/opt/ImageMagick/bin/convert '
convertcommand = '/usr/bin/convert '

# Create movie if requested
if(moviechoice=='y'):
    print 'Creating animated gif of sky pattern, filename skymovie.gif'
    system(convertcommand +'skypos_'+prefix+'*_latlong_'+str(mylat)+'_'+str(mylong)+'.png skymovie.gif')
    
    if(deletechoice=='y'):
        print 'Deleting png files'
        system('rm skypos_'+prefix+'*.png')                


print 'Complete'