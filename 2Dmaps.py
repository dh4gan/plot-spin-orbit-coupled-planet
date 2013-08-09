# Written by D Forgan, 8/8/2013
# Reads in output dumps from spinorbit_coupled_planet (C++ code)
# Produces 2D maps of each timestep (PNG)

import numpy as np
import matplotlib.pyplot as plt
from string import split
from os import system
from sys import exit

pi = 3.1415926585

longcol = 0
latcol =1
fluxcol =2 

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

# Loop over files

for i in range(nfiles):

    # Create filename - how many zeros needed?
    num = str(i+1)
    k=np.log10(i+1)
    while (k<nzeros): 
        num = "0"+num
        k+=1        
    
    inputfile = prefix + '.'+num
    outputfile = prefix+num+'.png'
    # Read in header - time, position data etc



    f = open(inputfile, 'r')

    line = f.readline()

    numbers = split(line)

    time=float(numbers[0])
    nlat = int(numbers[1])
    nlong = int(numbers[2])
    
    separation=float(numbers[3])
    trueanomaly=float(numbers[4])
    x = float(numbers[5])
    y = float(numbers[6])
    z = float(numbers[7])
    
    f.close()
    
    print 'File ', str(i),' Time  ', time, 'xyz: ', x, y, z
    
    # Read in rest of file
    
    data = np.genfromtxt(inputfile, skiprows=1)
    
    
    # Reshape to fit 2D array
    
    latitude = data[:,latcol].reshape(nlat,nlong)*180.0/pi
    longitude= data[:,longcol].reshape(nlat,nlong)*180.0/pi
    flux = data[:,fluxcol].reshape(nlat,nlong)
    

    # Plot 2D map
    
    fig1 = plt.figure()
    ax = fig1.add_subplot(111)
    ax.set_xlabel('Longitude (degrees)')
    ax.set_ylabel('Latitude (degrees)')
    plt.pcolor(longitude,latitude,flux, cmap='spectral',vmin = 0.0, vmax = 0.08)
    plt.colorbar()

    plt.savefig(outputfile, format= 'png')

    #exit()
    # Save to file

# end of loop


# Create movie if requested
if(moviechoice=='y'):
    print 'Creating animated gif, filename movie.gif'
    
    system('/usr/bin/convert '+prefix+'*.png movie.gif')
    if(deletechoice=='y'):
        print 'Deleting png files'
        system('rm '+prefix+'*.png')

print 'Complete'