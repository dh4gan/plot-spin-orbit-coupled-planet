# Written by D Forgan, 12/8/2013
# Reads in output dumps from spinorbit_coupled_planet (C++ code)
# Produces curves for data at specific longitude and latitude

import numpy as np
import matplotlib.pyplot as plt
from string import split
from os import system
#from sys import exit

pi = 3.1415926585

longcol = 0
latcol = 1
fluxcol = 2
Teffcol = 3
gammacol = 4 
darkcol = 5
altcol = 6
azcol = 7
hourcol = 8

# Read in input parameters

#prefix = raw_input("What is the file prefix? ")
#nfiles = input("How many files? ")
#moviechoice = raw_input("Make an animated gif at end? (y/n) ")
#deletechoice = 'n'
#if(moviechoice=='y'):
#    deletechoice = raw_input("Delete .png files? (y/n) ")

prefix = 'trial'
nfiles = 100
moviechoice = 'n'
deletechoice = 'n'

nzeros = int(np.log10(nfiles))

# Arrays to hold flux, altitude and azimuth data

time = np.zeros(nfiles)
flux = np.zeros(nfiles)
Teff = np.zeros(nfiles)
Ngamma = np.zeros(nfiles)
darkness = np.zeros(nfiles)
altitude = np.zeros(nfiles)
azimuth = np.zeros(nfiles)
hourangle = np.zeros(nfiles)

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
        for j in range (len(lat_possibles)):
            print '(',j,')', lat_possibles[j]
    
        latselect = input("Enter integer corresponding to desired value: ")        
        mylat= lat_possibles[latselect]
        
        long_possibles = np.unique(data[:,longcol])
        print "Fix value of longitude: here are the choices"
        for j in range (len(long_possibles)):
            print '(',j,')', long_possibles[j]
    
        longselect = input("Enter integer corresponding to desired value: ")
        mylong= long_possibles[longselect]
        
                        
    
    skyfile = 'skypos_'+prefix+num+'_latlong_'+str(mylat)+'_'+str(mylong)+'.png'
    
    # Select flux only from the correct latitude and longitude    
    
    myentry = data[data[:,latcol]==mylat]
    myentry = myentry[myentry[:,longcol]==mylong]        
        
    flux[i] = myentry[0,fluxcol]
    Teff[i] = myentry[0,Teffcol]
    Ngamma[i] = myentry[0,gammacol]        
    altitude[i] = myentry[0,altcol]
    azimuth[i] = myentry[0,azcol]    
    hourangle[i] = myentry[0,hourcol]*180.0/pi

    #height[i] = np.sin(altitude[i])
    #horizontal[i] = -np.cos(azimuth[i])*np.sin(altitude[i])
    horizontal[i] = np.sin(altitude[i])*np.cos(azimuth[i])
    height[i] = np.sin(altitude[i])*np.sin(azimuth[i])

    print i, hourangle[i], azimuth[i], altitude[i], horizontal[i], height[i]
    # Plot sky position for this timestep
    
    fig1 = plt.figure(1)
    ax = fig1.add_subplot(111)
    ax.set_xlabel('Horizontal Position')
    ax.set_ylabel('Height')
    ax.set_ylim(0,1)
    ax.set_xlim(0,1)    
    plt.scatter(horizontal[i],height[i], marker='o', color='red')
    if(i>0): plt.plot(horizontal[:i-1],height[:i-1], linestyle='--', color='blue')    
    plt.savefig(skyfile, format= 'png')
    plt.clf()


# end of loop

# Plot flux

fluxfile = 'latlong_'+str(mylat)+'_'+str(mylong)+'_flux_'+prefix+'_.png'    

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Time (yr)')
ax.set_ylabel('Flux (arbitrary)')
plt.plot(time,flux)

plt.savefig(fluxfile, format= 'png')

# Plot Effective Temperature

Tfile = 'latlong_'+str(mylat)+'_'+str(mylong)+'_Teff_'+prefix+'_.png'  

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Time (yr)')
ax.set_ylabel('Effective Temperature')
plt.plot(time,Teff)

plt.savefig(Tfile, format= 'png')

# Plot Ngamma

gammafile = 'latlong_'+str(mylat)+'_'+str(mylong)+'_ngamma_'+prefix+'_.png'   

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Time (yr)')
ax.set_ylabel('Maximum Photon flux ($\mu$ mol $m^{-2}s^{-1}$')
plt.plot(time,Ngamma)

plt.savefig(gammafile, format= 'png')

# Plot Ngamma

darkfile = 'latlong_'+str(mylat)+'_'+str(mylong)+'_darkness_'+prefix+'_.png'   

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Time (yr)')
ax.set_ylabel('Period of Darkness (yr)')
plt.plot(time,darkness)

plt.savefig(darkfile, format= 'png')


# Plot altitude

altfile = 'latlong_'+str(mylat)+'_'+str(mylong)+'_altitude_'+prefix+'_.png'  

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Time (yr)')
ax.set_ylabel('Altitude (degrees)')
plt.plot(time,altitude)

plt.savefig(altfile, format= 'png')

# Plot azimuth

azfile = 'latlong_'+str(mylat)+'_'+str(mylong)+'_azimuth_'+prefix+'_.png'  

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Time (yr)')
ax.set_ylabel('azimuth (degrees)')
plt.plot(time,azimuth)

plt.savefig(azfile, format= 'png')

# Hour Angle

hourfile = 'latlong_'+str(mylat)+'_'+str(mylong)+'_hourangle_'+prefix+'_.png'  

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Time (yr)')
ax.set_ylabel('Hour Angle (degrees)')
plt.plot(time,hourangle)

plt.savefig(hourfile, format= 'png')

# Plot height and horizontal on same graph

azfile = 'hh_'+prefix+'_latlong_'+str(mylat)+'_'+str(mylong)+'.png'    

fig1 = plt.figure()
ax = fig1.add_subplot(111)
ax.set_xlabel('Time (yr)')
ax.set_ylabel('x(y) position')
plt.plot(time,height, color='red', label='Height')
plt.plot(time,horizontal, color='blue', label='Horizontal')
ax.legend()
plt.savefig(azfile, format= 'png')

# Command for converting images into gifs - machine dependent

convertcommand = '/opt/ImageMagick/bin/convert '
#convertcommand = '/usr/bin/convert '

# Create movie if requested
if(moviechoice=='y'):
    print 'Creating animated gif of sky pattern, filename skymovie.gif'
    system(convertcommand +'skypos_'+prefix+'*_latlong_'+str(mylat)+'_'+str(mylong)+'.png skymovie.gif')
    
    if(deletechoice=='y'):
        print 'Deleting skypos_*.png files'
        system('rm skypos_'+prefix+'*.png')                


print 'Complete'
