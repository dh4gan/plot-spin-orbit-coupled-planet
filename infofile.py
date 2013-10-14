# Useful functions for reading info file, etc

from string import split

def wavelengthToRGB(wavelength):
    '''Function converts a wavelength (nm)in the visible spectrum to an RGB colour'''
    red =0.0
    green = 0.0
    blue = 0.0
    
    # If wavelength in UV or beyond, make it blue
    if(wavelength<380.0):
        red = 0.0
        green = 0.0
        blue = 1.0
        print "Wavelength ", wavelength, " too blue for visible RGB!"

    if(wavelength>781.0):
        red = 1.0
        green = 0.0
        blue = 0.0
        print "Wavelength ", wavelength, " too red for visible RGB!"


    if(wavelength>=380.0 and wavelength < 440.0):
        red = (wavelength -440)/(440-380)
        green = 0.0
        blue =1.0
    elif(wavelength >=440 and wavelength < 490):
        red = 0.0
        green = ((wavelength)-440)/(490-440)        
        blue = 1.0            
    elif(wavelength>=490 and wavelength < 510):
        red = 0.0
        green = 1.0
        blue = -(wavelength-510)/(510-490)
    elif(wavelength>=510 and wavelength < 580):
        red = (wavelength-510)/(580-510)
        green=1.0
        blue= 0.0
    elif(wavelength>=580 and wavelength < 645):
        red = 1.0
        green = -(wavelength-645)/(645-580)
        blue = 0.0
    elif(wavelength>=645 and wavelength< 781):
        red = 1.0
        green = 0.0
        blue = 0.0

    rgb = (red,green,blue)

    return rgb


def read_infofile(prefix):
    infofile = prefix +'.info'

    print "Reading information file ",infofile
    f =  open(infofile, 'r')

    line = f.readline()
    nfiles=int(line)

    print "There are ", nfiles, " files"

    line = f.readline()
    numbers = split(line)
    
    starradius = float(numbers[0])
    startemp = float(numbers[1])
    wavelength = float(numbers[2])*1e7
    starcolor = wavelengthToRGB(wavelength)    

    
    line = f.readline()
    fluxmax = float(line)
        
    f.close()
        
    print "Star Radius: ", starradius
    print "Effective Temperature: ", startemp
    print "Colour ", starcolor
    print "Maximum Flux: ", fluxmax
    
    return nfiles, starradius, startemp, starcolor, fluxmax