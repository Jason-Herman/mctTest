Python test script for Enginuity Works and MCT. 
The latest stable python script and README documentation can be found at https://github.com/alwayzup/mctTest

# Platform
This script will ONLY work for Windows Environments.

# Installation Instructions
1. Install VSCode for Windows - https://code.visualstudio.com/download
2. Install Anaconda 2018.12 Python 3.7 version for Windows (our Python Platform) - https://www.anaconda.com/distribution/
3. Set global path variables for python and anaconda.
- Open Anaconda Prompt (WindowsKey, "Anaconda Prompt")
- In Anaconda Prompt, enter the commands "where python" and "where conda" to determine their install locations. 
- Open Command Prompt (WindowsKey, "Command Prompt")
- In Command Prompt, set the path variables form python and anaconda with the following commands: "set PATH=%PATH%;C:\your\path\here\" using the conda and python paths in 2 separate commands
4. Open VSCode and choose to enable python from the welcome screen. 
5. Set the current Python interpretter by clicking the Python 3.7... text in the bottom left of the screen and choosing Python 3.7.1 ('base':Conda)
6. In the VSCode Terminal type the following commands to install the necessary dependencies:
- "pip install pyserial"
- "pip install pypiwin32"
7. Update the comport on line 17 and change debug mode to False on line 8 if you'd like to test the serial output. 
Note: A step by step video setup can be created on request. 

# Running the Script in VSCode
- Open the mctTest.py file in VSCode (assumes installation instructions were followed).
- Right click the text of the script and select the command 'Run Python File in Terminal'. 
- By Default the terminal will be nested at the bottom of the screen. Click into the terminal to enter commands via keyboard. 

# Usage instructions/commands
## Main Menu
At the main menu type and enter 'k' in terminal to set a custom angle output via angle input values.
Type and enter 'm' to adjust the angle in realtime via the mouse.
Type and enter 'help' to see help documentation.
Type and enter 'f' to write mouse data to file. 
Type and enter 'r' to read mouse angle data from file and output to serial.
Type and enter 'q' to exit the program.
## Keyboard Input
When prompted, type in the roll (-45 to +45) and pitch (-45 to +10) angles you'd like to send to the motors. You'll be asked to reenter the angles if they are out of bounds. You can return to the main menu at any time by entering 'q'.
## Mouse Input
When prompted, type in how long you'd like to send angle data to the motors via mouse. The center of the screen sends angle data of (0 roll,0 pitch). Move the mouse up and down to move between a pitch value of -45 and +10 degrees. Move the mouse left and right to move between a roll value of -45 and 45 degreesYou can return to the main menu at any time by entering 'q'.
Note: The mouse coordinates are eliptically bound. If the mouse moves outside of these bounds, the ray-traced point on the elliptical boundary will be used as the current roll/pitch value.
## Mouse to File
When prompted, type in how long you'd like to record data for. Data is output to a time stamped txt file in the working directory.
## Read from File
When prompted, type in the name of the file you'd like to read from (leave off the .txt file extension). Data is written to serial at sample rate.
# Advanced Instructions
## Custom Screen resolution
By default the mouse input is designed to work with 1920x1080p resolution monitors. The resolution can be changed in the code at lines 11 and 12 to any resolution. 
## Debug Mode
Debug mode is used to test the script without having working serial output. Toggle mode by changing the value of the the constant DEBUG_ to True or False on line 8. 