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

#Set range
range_left = -45
range_right = 45
range_top = 10
range_bottom = -45

#Set sample time in seconds here:
sample_time = .1

print('Initializing mctTest script...')
if (not DEBUG_):
    time.sleep(2) #Wait 2 seconds to ensure serial output works properly
    com_port = 'com11' #Need to update port (e.g. 'com4' arduino)
    SER = serial.Serial(com_port,9600)
    #Prime motor
    SER.write(str.encode('RUN\r')) 

def invalid_input():
    print("Invalid Input.")
    return

def float_to_out(x,y):
    x_out = str(int(x*800)) #Question: Should the scale factors change with the updated ranges?
    y_out = str(int(y*555.55))

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
    global range_left
    global range_right
    global range_top
    global range_bottom
    while(True):
        valid_input_flag = False
        while(not valid_input_flag):    
            print("Set Roll:")
            print("Enter roll angle from " + str(range_left) + " to " + str(range_right) +": ('q' to quit to main menu)")
            x = 0
            x_input = input()
            x = x_input

            if (x == 'q'): #Quit on user input
                return

            try:
                x = float(x)
                if (x < range_left or x > range_right):
                    print("Invalid angle.")
                else:
                    valid_input_flag = True
            except ValueError:
                print("Input must be numerical.")

        valid_input_flag = False
        while(not valid_input_flag):    
            print("Set Pitch:")
            print("Enter pitch angle from " + str(range_bottom) + " to " + str(range_top) +": ('q' to quit to main menu)")
            y = 0
            y_input = input()
            y = y_input

            if (y == 'q'): #Quit on user input
                return

            try:
                y = float(y)
                if (y < range_bottom or y > range_top):
                    print("Invalid angle.")
                else:
                    valid_input_flag = True
            except ValueError:
                print("Input must be numerical.")
        
        #Convert coordinates for output
        x_out,y_out = float_to_out(x,y)
        print('Raw Location: ' + str(x) + ' ' + str(y))

        #Write data out to console and serial
        write_data(x_out,y_out)

def mouse_to_file():
    global range_left
    global range_right
    global range_top
    global range_bottom
    while (True):
        print("Mouse input writen to file: \n Move mouse up and down to set pitch angle from " + str(range_bottom) + " to " + str(range_top) + "degrees. Move mouse left and right to set roll angle from " + str(range_bottom) + " to " + str(range_top) + " degrees.")
        print("Serial output data will be written to a time stamped file in working directory.")
        print("Enter runtime in seconds for mouse input writing: ('q' to quit to main menu)")
        run_time_input = 0
        run_time_input = input()
        run_time = run_time_input # Set program run time in seconds

        if (run_time == 'q'): #Quit on user input
            return 

        run_time = float(run_time)

        global sample_time # time in seconds between samples
        
        #Get actual resolution reading from monitor manually (currently: 1080p)
        x_l = 0
        global x_r
        y_t = 0
        global y_b
        x_span = x_r - x_l
        y_span = y_b - y_t

        #Create new text file with timestamp
        fileName =  str(time.strftime("%Y%m%d-%H%M%S")) + "_Serial_Data"
        f = open(fileName, "x")

        i = 0 # Counter for running time

        while (i < run_time/sample_time):
            x, y = win32api.GetCursorPos()
            #Scale 
            x = (x*((range_top-range_bottom)/y_span)) - (x_span*((range_top-range_bottom)/y_span)/2)
            y = range_top - (y*((range_top-range_bottom)/y_span))
                
            #Check if coordinate is within supplied bounds - https://math.stackexchange.com/questions/76457/check-if-a-point-is-within-an-ellipse
            #If out of bounds use the ray intersection - https://math.stackexchange.com/questions/22064/calculating-a-point-that-lies-on-an-ellipse-given-an-angle
            if (y>=0): #Above
                a = range_right
                b = range_top
                try: #Deal with divide by Zero
                    if ((x**2/(a**2)+y**2/(b**2)) >= 1):
                        y_temp = a*b/math.sqrt(a**2 + b**2 / (y/x)**2)
                        if (x>0): #Positive
                            x_temp = a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                        else:
                            x_temp = -a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                        x = x_temp
                        y = y_temp
                except ZeroDivisionError:
                    if (y>range_top):
                        y = range_top
                    elif (y<range_bottom):
                        y = range_bottom 

            else: #Below           
                a = range_right
                b = abs(range_bottom)
                try: #Deal with divide by Zero
                    if ((x**2/(a**2)+y**2/(b**2)) >= 1):
                        y_temp = -a*b/math.sqrt(a**2 + b**2 / (y/x)**2)
                        if (x>0): #Positive
                            x_temp = a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                        else:
                            x_temp = -a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                        x = x_temp
                        y = y_temp
                except ZeroDivisionError:
                    if (y>range_top):
                        y = range_top
                    elif (y<range_bottom):
                        y = range_bottom 

            #Convert coordinates for output
            x_out,y_out = float_to_out(x,y)
            print('Raw Location: ' + str(x) + ' ' + str(y))

            #Write data out to console
            x_print = "r=" + str(x_out) + " "
            y_print = "p=" + str(y_out) + " \n"
            print("Serial Output: " + str(x_print) + str(y_print))
            #Write data to text file
            f.write(str(x_print))
            f.write(str(y_print))

            #Write data out to console and serial
            write_data(x_out,y_out)
            
            time.sleep(sample_time) 
            i += 1
        #close text file
        f.close()

def mouse_input():
    global range_left
    global range_right
    global range_top
    global range_bottom

    while (True):
        print("Mouse Input Testing: \n Move mouse up and down to set pitch angle from " + str(range_bottom) + " to " + str(range_top) + "degrees. Move mouse left and right to set roll angle from " + str(range_bottom) + " to " + str(range_top) + " degrees.")
        print("Enter runtime in seconds for mouse input testing: ('q' to quit to main menu)")
        run_time_input = 0
        run_time_input = input()
        run_time = run_time_input # Set program run time in seconds

        if (run_time == 'q'): #Quit on user input
            return 

        run_time = float(run_time)

        global sample_time # time in seconds between samples
        
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
            x = (x*((range_top-range_bottom)/y_span)) - (x_span*((range_top-range_bottom)/y_span)/2)
            y = range_top - (y*((range_top-range_bottom)/y_span))
                
            #Check if coordinate is within supplied bounds - https://math.stackexchange.com/questions/76457/check-if-a-point-is-within-an-ellipse
            #If out of bounds use the ray intersection - https://math.stackexchange.com/questions/22064/calculating-a-point-that-lies-on-an-ellipse-given-an-angle
            if (y>=0): #Above
                a = range_right
                b = range_top
                try: #Deal with divide by Zero
                    if ((x**2/(a**2)+y**2/(b**2)) >= 1):
                        y_temp = a*b/math.sqrt(a**2 + b**2 / (y/x)**2)
                        if (x>0): #Positive
                            x_temp = a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                        else:
                            x_temp = -a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                        x = x_temp
                        y = y_temp
                except ZeroDivisionError:
                    if (y>range_top):
                        y = range_top
                    elif (y<range_bottom):
                        y = range_bottom 

            else: #Below           
                a = range_right
                b = abs(range_bottom)
                try: #Deal with divide by Zero
                    if ((x**2/(a**2)+y**2/(b**2)) >= 1):
                        y_temp = -a*b/math.sqrt(a**2 + b**2 / (y/x)**2)
                        if (x>0): #Positive
                            x_temp = a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                        else:
                            x_temp = -a*b/math.sqrt(b**2 + a**2 * (y/x)**2)
                        x = x_temp
                        y = y_temp
                except ZeroDivisionError:
                    if (y>range_top):
                        y = range_top
                    elif (y<range_bottom):
                        y = range_bottom

            #Convert coordinates for output
            x_out,y_out = float_to_out(x,y)
            print('Raw Location: ' + str(x) + ' ' + str(y))

            #Write data out to console and serial
            write_data(x_out,y_out)
            
            time.sleep(sample_time) 
            i += 1

def read_from_file():
    while(True):
        valid_input_flag = False
        while(not valid_input_flag):    
            print("Read and output angle data from file:")
            print("Enter the name of the data file to be read (e.g. '20190306-144312_Serial_Data'): ('q' to quit to main menu)")
            f_input = ''
            f_input = input()
            f_name = f_input

            if (f_name == 'q'): #Quit on user input
                return

            try: #attempt to open the file
                f_name = str(f_name)
                f = open(f_name,'r')
                valid_input_flag = True
            except FileNotFoundError:
                print("Wrong file or file path. Try a file name such as '20190306-144312_Serial_Data' (without the quotes) with the file located in the local directory.")

        #Read the file line by line and write to terminal/serial
        global sample_time
        global DEBUG_
        if (not DEBUG_):
            global SER
        fl = f.readlines()
        print('To Serial:')
        for l in fl:
            print(l)

            #Write data out to serial
            if (not DEBUG_):
                SER.write(str.encode(l))
            
            time.sleep(sample_time) 

def help_():
    print("Welcome to the mctTest Script.")
    print("\nDESCRIPTION: \nThis script is used to send custom motor angle data through serial via the mouse or keyboard.")
    print("\nUSAGE: \nAt the main menu type and enter 'k' in terminal to set a custom angle output via angle input values.")
    print("\nType and enter 'm' to adjust the angle in realtime via the mouse.")
    print("\nType and enter 'f' to write mouse angle data output to file.")
    print("\nType and enter 'r' to read mouse angle data from file and output to serial.")    
    print("\nType and enter 'q' to exit the program.")
    print("\nKEYBOARD INPUT: \nWhen prompted, type in the roll (e.g. -45 to +45) and pitch (e.g. -45 to +10) angles you'd like to send to the motors. You'll be asked to reenter the angles if they are out of bounds. You can return to the main menu at any time by entering 'q'.")
    print("\nMOUSE INPUT: \nWhen prompted, type in how long you'd like to send angle data to the motors via mouse. The center of the screen sends angle data of (0 roll,0 pitch). Move the mouse up and down to move between a pitch value of -45 and +10 degrees. Move the mouse left and right to move between a roll value of -45 and 45 degreesYou can return to the main menu at any time by entering 'q'.")
    print("Note: The mouse coordinates are eliptically bound. If the mouse moves outside of these bounds, the ray-traced point on the elliptical boundary will be used as the current roll/pitch value.")
    print("\nMOUSE TO FILE: \nWhen prompted, type in how long you'd like to record data for. Data is output to a time stamped txt file in the working directory.")
    print("\nREAD FROM FILE: \nWhen prompted, type in the name of the file you'd like to read from (leave off the .txt file extension). Data is written to serial at sample rate.")
    print("\nCUSTOM SCREEN RESOLUTION: By default the mouse input is designed to work with 1920x1080p resolution monitors. The resolution can be changed in the code at lines 11 and 12 to any resolution.")
    print("\nDEBUG MODE: Debug mode is used to test the script without having working serial output. Toggle mode by changing the value of the the constant DEBUG_ to True or False on line 8.")
    print("\nCURRENT FILE: The latest stable python script and README documentation can be found at https://github.com/alwayzup/mctTest")
    print("\nTROUBLESHOOTING: For any issues with the script please see the Installation Instructions in README.md.")

    return

def quit_():
    sys.exit("Closing mctTest script \n Complete")

def input_to_method(inputType):
    switcher = {
        'k': keyboard_input,
        'm': mouse_input,
        'f': mouse_to_file,
        'r': read_from_file,
        'help': help_,
        'q': quit_
    }
    func = switcher.get(inputType, lambda: invalid_input)
    func()
    return

def main_menu():
    while (True):
        print('Awaiting input:')
        print("Please type 'k' for keyboard input, 'm' for mouse input, 'f' for mouse to file, 'r' to read from file, 'help' for help, or 'q' to quit.")
        input_type = ''
        input_type = input()
        input_to_method(input_type)

main_menu()


