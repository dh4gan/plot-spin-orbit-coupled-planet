# Written by D Forgan, 8/8/2013
# Reads in output dumps from spinorbit_coupled_planet (C++ code)
# Produces total darkness as a function of latitude/longitude

import numpy as np
import matplotlib.pyplot as plt
from string import split
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

# Read in input parameters

prefix = raw_input("What is the file prefix? ")

nfiles, starradius, startemp, starcolor,fluxmax = infofile.read_infofile(prefix)

nzeros = int(np.log10(nfiles))

# Loop over files

# Create filename - how many zeros needed?
num = str(nfiles)
k=np.log10(nfiles)
while (k<nzeros): 
    num = "0"+num
    k+=1        
    
inputfile = prefix + '.'+num
    
# Read in header - time, position data etc

f = open(inputfile, 'r')

line = f.readline()

numbers = split(line)

time=float(numbers[0])
nlat = int(numbers[1])
nlong = int(numbers[2])
        
f.close()
    
print 'File ', str(nfiles),' Time  ', time
    

    
data = np.genfromtxt(inputfile, skiprows=1)
        
# Reshape to fit 2D array
    
latitude = data[:,latcol].reshape(nlat,nlong)*180.0/pi
longitude= data[:,longcol].reshape(nlat,nlong)*180.0/pi
darkness = data[:,darkcol].reshape(nlat,nlong)

# Final darkness map

outputfile = 'totaldarkness'+prefix+'.png'

integratedmax = np.amax(darkness)
integratedmin = np.amin(darkness)

integratedmin = integratedmax - 0.0364 

fig1 = plt.figure(5)
ax = fig1.add_subplot(111)
ax.set_xlabel('Longitude (degrees)')
ax.set_ylabel('Latitude (degrees)')
plt.pcolor(longitude,latitude,darkness, cmap='spectral',vmin = integratedmin, vmax = integratedmax)
plt.colorbar()

plt.savefig(outputfile, format= 'png')


print 'Complete'
