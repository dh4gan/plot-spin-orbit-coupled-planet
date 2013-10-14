# Written by D Forgan, 8/8/2013
# Reads in output dumps from spinorbit_coupled_planet (C++ code)
# Produces 2D maps of each timestep (PNG)

import numpy as np
import matplotlib.pyplot as plt
from string import split
from os import system
import infofile

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

# Read in input parameters

prefix = raw_input("What is the file prefix? ")

nfiles, starradius, startemp, starcolor,fluxmax = infofile.read_infofile(prefix)

moviechoice = raw_input("Make an animated gif at end? (y/n) ")
deletechoice = 'n'
if(moviechoice=='y'):
    deletechoice = raw_input("Delete .png files? (y/n) ")

nzeros = int(np.log10(nfiles))

# Loop over files

for i in range(nfiles):

    # Create filename - how many zeros needed?
    num = str(i+1)
    k=np.log10(i+1)
    while (k<nzeros): 
        num = "0"+num
        k+=1        
    
    inputfile = prefix + '.'+num
    fluxfile = 'flux_'+prefix+num+'.png'
    Tfile = 'Teff_'+prefix+num+'.png'
    gammafile = 'ngamma_'+prefix+num+'.png'
    azfile = 'azimuth_'+prefix+num+'.png'
    darkfile = 'darkness_'+prefix+num+'.png'
    altfile = 'altitude_'+prefix+num+'.png'
    
    # Read in header - time, position data etc

    f = open(inputfile, 'r')

    line = f.readline()

    numbers = split(line)

    time=float(numbers[0])
    nlat = int(numbers[1])
    nlong = int(numbers[2])
        
    f.close()
    
    print 'File ', str(i+1),' Time  ', time
    
    if(i==0):
        # Create array to hold integrated flux data
        integrated = np.zeros((nlat,nlong))
    
    # Read in rest of file
    
    data = np.genfromtxt(inputfile, skiprows=1)
        
    # Reshape to fit 2D array
    
    latitude = data[:,latcol].reshape(nlat,nlong)*180.0/pi
    longitude= data[:,longcol].reshape(nlat,nlong)*180.0/pi
    flux = data[:,fluxcol].reshape(nlat,nlong)
    Teff = data[:,Teffcol].reshape(nlat,nlong)
    ngamma = data[:,gammacol].reshape(nlat,nlong)
    darkness = data[:,darkcol].reshape(nlat,nlong)
    altitude = data[:,altcol].reshape(nlat,nlong)*180.0/pi
    azimuth = data[:,azcol].reshape(nlat,nlong)*180.0/pi
    
    # Add flux to integrated map
    integrated = integrated + flux/float(nfiles)
    
    # Plot 2D maps of this timestep
    
    if(moviechoice=='y'):
        # Flux
    
        fig1 = plt.figure(1)
        ax = fig1.add_subplot(111)
        ax.set_xlabel('Longitude (degrees)')
        ax.set_ylabel('Latitude (degrees)')
        plt.pcolor(longitude,latitude,flux, cmap='spectral',vmin = 0.0, vmax = 2000.0)
        plt.colorbar()

        plt.savefig(fluxfile, format= 'png')
        plt.clf()
    
        # Effective Temperature
        fig1 = plt.figure(2)
        ax = fig1.add_subplot(111)
        ax.set_xlabel('Longitude (degrees)')
        ax.set_ylabel('Latitude (degrees)')
        plt.pcolor(longitude,latitude,Teff, cmap='spectral',vmin = 0.0, vmax = 500.0)
        plt.colorbar()

        plt.savefig(Tfile, format= 'png')
        plt.clf()

        # N Gamma
        fig1 = plt.figure(3)
        ax = fig1.add_subplot(111)
        ax.set_xlabel('Longitude (degrees)')
        ax.set_ylabel('Latitude (degrees)')
        plt.pcolor(longitude,latitude,np.log10(ngamma), cmap='spectral',vmin = 0.0, vmax = 4.0)
        plt.colorbar()

        plt.savefig(gammafile, format= 'png')
        plt.clf()

        # Darkness
        fig1 = plt.figure(4)
        ax = fig1.add_subplot(111)
        ax.set_xlabel('Longitude (degrees)')
        ax.set_ylabel('Latitude (degrees)')
        plt.pcolor(longitude,latitude,darkness, cmap='spectral',vmin = 0.0, vmax = 1.0)
        plt.colorbar()

        plt.savefig(darkfile, format= 'png')
        plt.clf()

        
    
        fig1 = plt.figure(5)
        ax = fig1.add_subplot(111)
        ax.set_xlabel('Longitude (degrees)')
        ax.set_ylabel('Latitude (degrees)')
        plt.pcolor(longitude,latitude,altitude, cmap='spectral',vmin = 0.0, vmax = 90.0)
        plt.colorbar()

        plt.savefig(altfile, format= 'png')
        plt.clf()
    
        fig1 = plt.figure(6)
        ax = fig1.add_subplot(111)
        ax.set_xlabel('Longitude (degrees)')
        ax.set_ylabel('Latitude (degrees)')
        plt.pcolor(longitude,latitude,azimuth, cmap='spectral',vmin = 0.0, vmax = 360.0)
        plt.colorbar()

        plt.savefig(azfile, format= 'png')
        plt.clf()

    # Save to file

# end of loop

# Plot 2D map of integrated flux

integratedmax = np.amax(integrated)
integratedmin = np.amin(integrated)
    
outputfile = 'integrated'+prefix+'.png'

fig1 = plt.figure(4)
ax = fig1.add_subplot(111)
ax.set_xlabel('Longitude (degrees)')
ax.set_ylabel('Latitude (degrees)')
plt.pcolor(longitude,latitude,integrated, cmap='spectral',vmin = integratedmin, vmax= integratedmax)
plt.colorbar()

plt.savefig(outputfile, format= 'png')

# Final darkness map

outputfile = 'totaldarkness'+prefix+'.png'

integratedmax = np.amax(darkness)
integratedmin = np.amin(darkness)
fig1 = plt.figure(5)
ax = fig1.add_subplot(111)
ax.set_xlabel('Longitude (degrees)')
ax.set_ylabel('Latitude (degrees)')
plt.pcolor(longitude,latitude,darkness, cmap='spectral',vmin = integratedmin, vmax = integratedmax)
plt.colorbar()

plt.savefig(outputfile, format= 'png')

# Command for converting images into gifs - machine dependent

#convertcommand = '/opt/ImageMagick/bin/convert '
convertcommand = '/usr/bin/convert '

# Create movie if requested
if(moviechoice=='y'):
    print 'Creating animated gif of flux pattern, filename fluxmovie.gif'
    system(convertcommand +'flux_'+prefix+'*.png fluxmovie.gif')
    print 'Creating animated gif of Teff pattern, filename Teffmovie.gif'
    system(convertcommand +'Teff_'+prefix+'*.png Teffmovie.gif')
    print 'Creating animated gif of Ngamma pattern, filename ngammamovie.gif'
    system(convertcommand +'ngamma_'+prefix+'*.png ngammamovie.gif')
    print 'Creating animated gif of darkness pattern, filename darkmovie.gif'
    system(convertcommand +'darkness_'+prefix+'*.png darkmovie.gif')
    print 'Creating animated gif of altitude pattern, altname altmovie.gif'
    system(convertcommand +'altitude_'+prefix+'*.png altmovie.gif')
    print 'Creating animated gif of azimuth pattern, filename azmovie.gif'
    system(convertcommand +'azimuth_'+prefix+'*.png azmovie.gif')

    if(deletechoice=='y'):
        print 'Deleting png files'
        system('rm flux_'+prefix+'*.png')
        system('rm altitude_'+prefix+'*.png')
        system('rm Teff_'+prefix+'*.png')
        system('rm ngamma_'+prefix+'*.png')
        system('rm darkness_'+prefix+'*.png')
        system('rm azimuth_'+prefix+'*.png')


print 'Complete'
