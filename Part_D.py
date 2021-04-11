'''
Part_D.py

@author: Artur Smiechowski

A program that:
    
'''

# %% Imports

'''

import Part_B.py
import Part_C.py
'''
import time
import serial
import argparse
import numpy as np
import pyautogui as pyg
import atexit # To handle closing Serial port on program exit


# %% Dummy variables, will figure origin later
com_port = 'COM3'

gui_scale = 1 # Amount to scale speed of mouse movements

# Note that these all should be loaded in save for sample_buffer
n_channels = 3
epoch_size = 200
sample_buffer = np.zeros((epoch_size, n_channels))
full_buffer = np.zeros((epoch_size, n_channels))

# Variances from other script
v1 = 0.01
v2 = 0.01
v3 = 0.01

# %% Setup Commands and Methods

# Create parser to read in parameters from CMD
parser = argparse.ArgumentParser(description='Read EMG data and use it for basic GUI interfacing (mouse operation)')

# Add arguments to help text
parser.add_argument('com_port', help='Port of connected EMG device', type=str)
parser.add_argument('run_time', help='Length of time program should run for in seconds', type=float)
parser.add_argument('gui_scale', help='Relative speed and distance of mouse movements to account for different screen size', type=float)

# Collect arguments into an accessible object
args = parser.parse_args()

arduino_data = serial.Serial() # Give the Serial process an appropriate alias

def Open_Port(port):
    '''Open_Port
    Arguments-
    port ~ String of the COM port to open to
    
    Returns-
    NONE
    
    Opens the Serial port to read in data
    '''
    arduino_data.baudrate = 500_000 # Set baudrate
    arduino_data.port = port # Sets the port to use
    arduino_data.open()

def On_Exit():
    '''On_Exit
    Arguments-
    NONE
    
    Returns-
    NONE
    
    Closes the COM port
    '''
    arduino_data.close()
    print("Closing EMG Interface")

atexit.register(On_Exit) # Registers On_Exit method to call on program close

# %% Helper Methods

def Read_EMG_Epoch():
    ''' Read_EMG_Live
    
    
    '''

    #with serial.Serial(port=com_port,baudrate=500000) as arduino_data:
    
    for sample_index in range(sample_buffer.shape[0]): # Iterates over samples in buffer
        # Extract data string to parse
        data_string = arduino_data.readline().decode('ascii')
        # Split into list of strings
        data_string = data_string.split() # First element is time of sample in ms, rest are sensor values
        
        if(len(data_string) >= (n_channels + 1)):
        
            # Writes the output of each channel to associate column of data array
            # Converts to V
            for channel in range(n_channels):
                # Write collected data point from each channel to associated position in sd
                sample_buffer[sample_index, channel] = int(data_string[channel+1])*5.0/1024
        
        else:
            pass # figure out what to do in drop cases // Could enclose whole if in a while loop to only ever read if full-line available??
            
    return sample_buffer # Returns a full epoch

def Classify_EMG(acting_buffer):
    ''' Classify_EMG
    Arguments-
    acting_buffer ~ array of the data to make action decisions on
    
    Returns-
    action ~ string of the GUI action to complete
    
    Classifies the EMG data of an epoch
    '''    
    pass

def Act(action, gui_scale):
    ''' Act
    Arguments-
    action ~ string of the action for GUI to do
    gui_scale ~ the amount to scale mouse speed and movement by
    
    Returns-
    NONE
    
    Executes a GUI action
    '''
    pass

def Run(com_port, run_time, gui_scale):
    '''Run
    '''
    
    start_time = time.time() # Get program start time in seconds since epoch (1970 one not local data one)
    Open_Port(com_port) # Opens the COM port to read in data
    while ((time.time() - start_time) <= run_time): # Checks the difference in start_time and current time is less than run_time
        
        current_epoch = Read_EMG_Epoch() # Reads data live into current_epoch for processing
        action = Classify_EMG(current_epoch) # Calls classify on current_epoch to determine what GUI action to throw
        
        Act(action, gui_scale) # Calls act to perform GUI action
        
    print("Run_time finished")
    exit() # End program (redundant but habit, ensures On_Exit fires)
    
# %% Main Method call

Run(args.com_port, args.run_time, args.gui_scale)