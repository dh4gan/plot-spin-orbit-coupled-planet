# Written by D Forgan, 8/8/2013
# Reads in output dumps from spinorbit_coupled_planet (C++ code)
# Produces total darkness as a function of latitude/longitude
# Produces integrated flux also

import numpy as np
import matplotlib.pyplot as plt
from string import split

pi = 3.1415926585

longcol = 0
latcol = 1
fluxcol = 2
darkcol = 3

# Read in input parameters

prefix = raw_input("What is the file prefix? ")

# Read integrated flux file

inputfile = prefix + '.integrated'
    
# Read in header - time, position data etc

f = open(inputfile, 'r')

line = f.readline()
numbers = split(line)
nlat = int(numbers[0])
nlong = int(numbers[1])

f.close()
      
print 'Integrated flux in file ',inputfile
    
data = np.genfromtxt(inputfile, skiprows=1)
        
# Reshape to fit 2D array
    
latitude = data[:,latcol].reshape(nlat,nlong)*180.0/pi
longitude= data[:,longcol].reshape(nlat,nlong)*180.0/pi
flux = data[:,fluxcol].reshape(nlat,nlong)
darkness = data[:,darkcol].reshape(nlat,nlong)

# Final darkness map

outputfile = 'integrateddarkness'+prefix+'.png'

integratedmax = np.amax(darkness)
integratedmax = np.amax(darkness)
integratedmin = np.amin(darkness)


print "Plotting darkness, limits: ",integratedmin, integratedmax

fig1 = plt.figure(1)
ax = fig1.add_subplot(111)
ax.set_xlabel('Longitude (degrees)')
ax.set_ylabel('Latitude (degrees)')
plt.contour(longitude,latitude,darkness)
plt.pcolor(longitude,latitude,darkness, cmap='spectral',vmin = integratedmin, vmax = integratedmax)
plt.colorbar()

plt.savefig(outputfile, format= 'png')

# Now plot integrated flux

outputfile = 'integratedflux'+prefix+'.png'

integratedmax = np.amax(flux)
integratedmin = np.amin(flux)

print "Plotting flux, limits: ",integratedmin, integratedmax

fig1 = plt.figure(2)
ax = fig1.add_subplot(111)
ax.set_xlabel('Longitude (degrees)')
ax.set_ylabel('Latitude (degrees)')
plt.contour(longitude,latitude,flux)
plt.pcolor(longitude,latitude,flux, cmap='spectral',vmin = integratedmin, vmax = integratedmax)
plt.colorbar()

plt.savefig(outputfile, format= 'png')




print 'Complete'
