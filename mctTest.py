import win32api
import time
import math
import serial
import sys

#Debug Mode - No serial output
DEBUG_ = True

#Set monitor resolution here:
x_r = 1920 # set horizontal resolution in px
y_b = 1080 # set vertical resolution in px

print('Initializing mctTest script...')
if (not DEBUG_):
    time.sleep(2) #Wait 2 seconds to ensure serial output works properly
    com_port = 'ENTER_COMPORT_HERE' #Need to update port (e.g. 'com4' arduino)
    SER = serial.Serial(com_port,96810)
    #Prime motor
    SER.write(str.encode('RUN\r')) 

def invalid_input():
    print("Invalid Input.")
    return

def float_to_out(x,y):
    x_out = str(int(x*256))
    y_out = str(int(y*256))

    return [x_out,y_out]

def write_data(x_out,y_out):
    global DEBUG_
    x_print = "r=" + str(x_out) + " "
    y_print = "p=" + str(y_out) + " "
    print("Serial Output: " + str(x_print) + str(y_print))
    if (not DEBUG_):
        global SER
        SER.write(str.encode(x_print))
        SER.write(str.encode(y_print))

def keyboard_input():
    while(True):
        valid_input_flag = False
        while(not valid_input_flag):    
            print("Set Role:")
            print("Enter role angle from -45 to +45: ('q' to quit to main menu)")
            x = 0
            x_input = input()
            x = x_input

            if (x == 'q'): #Quit on user input
                return

            x = float(x)
            if (x < -45 or x > 45):
                print("Invalid angle.")
            else:
                valid_input_flag = True

        valid_input_flag = False
        while(not valid_input_flag):    
            print("Set Pitch:")
            print("Enter pitch angle from -45 to +10: ('q' to quit to main menu)")
            y = 0
            y_input = input()
            y = y_input

            if (y == 'q'): #Quit on user input
                return

            y = float(y)
            if (y < -45 or y > 10):
                print("Invalid angle.")
            else:
                valid_input_flag = True
        
        #Convert coordinates for output
        x_out,y_out = float_to_out(x,y)
        print('Raw Location: ' + str(x) + ' ' + str(y))

        #Write data out to console and serial
        write_data(x_out,y_out)

def mouse_input():
    while (True):
        print("Mouse Input Testing: \n Move mouse up and down to set pitch angle from -45 to +10 degrees. Move mouse left and right to set roll angle from -45 to +45 degrees.")
        print("Enter runtime in seconds for mouse input testing: ('q' to quit to main menu)")
        run_time_input = 0
        run_time_input = input()
        run_time = run_time_input # Set program run time in seconds

        if (run_time == 'q'): #Quit on user input
            return 

        run_time = float(run_time)

        sample_time = .05 # Set time in seconds between samples here
        
        #Get actual resolution reading from monitor manually (currently: 1080p)
        x_l = 0
        global x_r
        y_t = 0
        global y_b
        x_span = x_r - x_l
        y_span = y_b - y_t

        i = 0 # Counter for running time

        while (i < run_time/sample_time):
            x, y = win32api.GetCursorPos()
            #Scale 
            x = (x*(55/y_span)) - (x_span*(55/y_span)/2)
            y = 10 - (y*(55/y_span))
                
            #Check if coordinate is within supplied bounds - https://math.stackexchange.com/questions/76457/check-if-a-point-is-within-an-ellipse
            #If out of bounds use the ray intersection - https://math.stackexchange.com/questions/22064/calculating-a-point-that-lies-on-an-ellipse-given-an-angle
            print((x**2/(45**2)+y**2/(10**2)))
            print((x**2/(45**2)+y**2/(45**2)))
            if (y>=0): #Above
                a = 45
                b = 10
                if ((x**2/(a**2)+y**2/(b**2)) >= 1):
                    y_temp = a*b/math.sqrt(a**2 + b**2 / (y/x)**2)
                    if (x>0): #Positive
                        x_temp = a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                    else:
                        x_temp = -a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                    x = x_temp
                    y = y_temp
            else: #Below           
                a = 45
                b = 45
                if ((x**2/(a**2)+y**2/(b**2)) >= 1):
                    y_temp = -a*b/math.sqrt(a**2 + b**2 / (y/x)**2)
                    if (x>0): #Positive
                        x_temp = a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                    else:
                        x_temp = -a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                    x = x_temp
                    y = y_temp

            #Convert coordinates for output
            x_out,y_out = float_to_out(x,y)
            print('Raw Location: ' + str(x) + ' ' + str(y))

            #Write data out to console and serial
            write_data(x_out,y_out)
            
            time.sleep(sample_time) 
            i += 1

def help_():
    print("Welcome to the mctTest Script.")
    print("DESCRIPTION: \n This script is used to send custom motor angle data through serial via the mouse or keyboard.")
    print("USAGE: \n At the main menu type and enter 'k' in terminal to set a custom angle output via angle input values.")
    print("Type and enter 'm' to adjust the angle in realtime via the mouse.")
    print("Type and enter 'q' to exit the program.")
    print("KEYBOARD INPUT: \n When prompted, type in the roll (-45 to +45) and pitch (-45 to +10) angles you'd like to send to the motors. You'll be asked to reenter the angles if they are out of bounds. You can return to the main menu at any time by entering 'q'.")
    print("MOUSE INPUT: \n when prompted, type in how long you'd like to send angle data to the motors via mouse. The center of the screen sends angle data of (0 roll,0 pitch). Move the mouse up and down to move between a pitch value of -45 and +10 degrees. Move the mouse left and right to move between a roll value of -45 and 45 degreesYou can return to the main menu at any time by entering 'q'.")
    print("Note: The mouse coordinates are eliptically bound. If the mouse moves outside of these bounds, the ray-traced point on the elliptical boundary will be used as the current roll/pitch value.")
    print("CUSTOM SCREEN RESOLUTION: By default the mouse input is designed to work with 1920x1080p resolution monitors. The resolution can be changed in the code at lines 11 and 12 to any resolution.")
    print("DEBUG MODE: Debug mode is used to test the script without having working serial output. Toggle mode by changing the value of the the constant DEBUG_ to True or False on line 8.")
    print("CURRENT FILE: The latest stable python script and README documentation can be found at https://github.com/alwayzup/mctTest")
    print("TROUBLESHOOTING: For any issues with the script please see the Installation Instructions in README.md.")

    return

def quit_():
    sys.exit("Closing mctTest script \n Complete")

def input_to_method(inputType):
    switcher = {
        'k': keyboard_input,
        'm': mouse_input,
        'help': help_,
        'q': quit_
    }
    func = switcher.get(inputType, lambda: invalid_input)
    func()
    return

def main_menu():
    while (True):
        print('Awaiting input:')
        print("Please type 'k' for keyboard input, 'm' for mouse input, 'help' for help, or 'q' to quit.")
        input_type = ''
        input_type = input()
        input_to_method(input_type)

#TODO: reset motor positions to 0,0
main_menu()


