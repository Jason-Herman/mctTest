#NOTE: Must change comport name on line 15 for serial output to work. 

import win32api
import time
import math
import serial

def floatToOut(x,y):
    xOut = str(int(x*256))
    yOut = str(int(y*256))

    return [xOut,yOut]

def printMouseCoordinates():
    comPort = 'ENTER_COMPORT_HERE' #Need to update port (e.g. 'com4' arduino)
    serialData = serial.Serial(comPort,96810) 
    runTime = 20 # Set program run time in seconds
    sampleTime = .05 # Set time in seconds between samples here
    
    i = 0
    
    #Get actual resolution reading from monitor manually (currently: 1080p)
    xL = 0
    xR = 1920
    yT = 0
    yB = 1080
    xSpan = xR - xL
    ySpan = yB - yT

    #Prime motor
    serialData.write(str.encode('RUN\r'))

    while (i < runTime/sampleTime):
        x, y = win32api.GetCursorPos()
        #Scale 
        x = (x*(55/ySpan)) - (xSpan*(55/ySpan)/2)
        y = 10 - (y*(55/ySpan))
               
        #Check if coordinate is within supplied bounds - https://math.stackexchange.com/questions/76457/check-if-a-point-is-within-an-ellipse
        #TODO: Update to ray method (Get angle with trig and figure out how to get point on elipse)
        print((x**2/(45**2)+y**2/(10**2)))
        print((x**2/(45**2)+y**2/(45**2)))
        if (y>=0): #Above
            a = 45
            b = 10
            if ((x**2/(a**2)+y**2/(b**2)) >= 1):
                yTemp = a*b/math.sqrt(a**2 + b**2 / (y/x)**2)
                if (x>0): #Positive
                    xTemp = a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                else:
                    xTemp = -a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                x = xTemp
                y = yTemp
        else: #Below           
            a = 45
            b = 45
            if ((x**2/(a**2)+y**2/(b**2)) >= 1):
                yTemp = -a*b/math.sqrt(a**2 + b**2 / (y/x)**2)
                if (x>0): #Positive
                    xTemp = a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                else:
                    xTemp = -a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                x = xTemp
                y = yTemp

        #Convert coordinates for output
        xOut,yOut = floatToOut(x,y)

        xPrint = "r=" + str(xOut) + " "
        yPrint = "p=" + str(yOut) + " "

        #Write data out to console
        print('Raw Location: ' + str(x) + ' ' + str(y))
        print(xPrint)
        print(yPrint)


        #Write data out to serial
        serialData.write(str.encode(xPrint))
        serialData.write(str.encode(yPrint))
        
        time.sleep(sampleTime) 
        i += 1
    #serialData.close()

time.sleep(2) #Wait 2 seconds to ensure serial output works properly

printMouseCoordinates() 