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

# Note that these all should be loaded in save for sample_buffer
n_channels = 3
epoch_size = 200
sample_buffer = np.zeros((epoch_size, n_channels))

# Variances from other script
left_threshhold = 0.01
right_threshhold = 0.01
bicep_threshhold = 0.01

# Resolution of the monitor being used
#screen_resolution = (1920,1080) # For now will assume a standard 1080p resolution // TODO, implement optional argument, possible saveable preference

# %% Setup Commands and Methods

# Create parser to read in parameters from CMD
parser = argparse.ArgumentParser(description='Read EMG data and use it for basic GUI interfacing (mouse operation)')

# Add arguments to help text
parser.add_argument('com_port', help='Port of connected EMG device', type=str)
parser.add_argument('run_time', help='Length of time program should run for in seconds', type=float)
# Optional Arguments
parser.add_argument('--gui_scale', help='Relative speed and distance of mouse movements, default value of 1 takes 5 actions to cross a screen', default=1.0, type=float)

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
    
    if arduino_data.isOpen(): # Checks if port is already open, closes it if so // Catches dangling port errors on program unexpectedly closing
        arduino_data.close() # Closes dangling port
        time.sleep(0.001)# Time to close port
        
    arduino_data.open() # Opens the port

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

atexit.register(On_Exit) # Registers On_Exit method to call on program close // Does not catch exception closing

# %% Helper Methods

def Read_EMG_Epoch():
    ''' Read_EMG_Live
    Arguments-
    NONE
    
    Returns-
    NONE
    
    Reads a live epoch from teh 3 emg channels
    '''

    #with serial.Serial(port=com_port,baudrate=500000) as arduino_data:
    
    for sample_index in range(sample_buffer.shape[0]): # Iterates over samples in buffer
        # Extract data string to parse
        data_string = arduino_data.readline().decode('ascii')
        # Split into list of strings
        data_string = data_string.split() # First element is time of sample in ms, rest are sensor actions
        
        if(len(data_string) >= (n_channels + 1)):
        
            # Writes the output of each channel to associate column of data array
            # Converts to V
            for channel in range(n_channels): # Currently timestamp of data is ignored
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
    action = 'rest' # set the return variable to initially be rest
    
    emg_epoch_var = np.transpose(np.nanvar(acting_buffer,axis=0)) # Gets the variances of each channel in the sample epoch
    # Should be a n_channel x 1 array
    
    # Classify which muscles where tensed (Checks if variuance is greater than channel threshhold)
    is_left = emg_epoch_var[0] > left_threshhold
    is_right = emg_epoch_var[1] > right_threshhold
    is_bicep = emg_epoch_var[2] > bicep_threshhold
    
    # Decision 'tree' to assign the return action
    # Refer to manual for action combinations
    # Tree first checks if left is active, works down the branches, if not then uses deduction while checking other roots
    if is_left:
        if is_right:
            if is_bicep:
                pass # action already rest
            else:
                action = 'click' # click the mouse
        elif is_bicep:
            action = 'down' # move the cursor down
        else:
            action = 'left' # move the cursor left
    elif is_right:
        if is_bicep:
            pass # action is already rest
        else:
            action = 'right' # move cursor right
    elif is_bicep:
        action = 'up' # move the cursor up
    else:
        pass # no muscle tensing means action is rest
    
    return action
        
def Act(action, gui_scale):
    ''' Act
    Arguments-
    action ~ string of the action for GUI to do
    gui_scale ~ the amount to scale mouse speed and movement by
    
    Returns-
    NONE
    
    Executes a GUI action
    '''
    cur_pos = pyg.position() # Collect current cursor position
    
    if(action == 'up'): # Move cursor up
        pyg.moveTo(cur_pos[0],cur_pos[1]-gui_scale*(1080/5))
    if(action == 'left'): # Move cursor left
        pyg.moveTo(cur_pos[0]-gui_scale*(1920/5),cur_pos[1])
    if(action == 'down'): # Move cursor down
        pyg.moveTo(cur_pos[0],cur_pos[1]+gui_scale*(1080/5))
    if(action == 'right'): # Move cursor right
        pyg.moveTo(cur_pos[1]+gui_scale*(1920/5),cur_pos[1])
    if(action == 'click'): # Click at current curosr position
        pyg.click()
    if (action == 'rest'): # Rest
        pass # Does nothing, but included for clarity and functinoal consistency
        
    #print("Act")

def Run(com_port, run_time, gui_scale):
    '''Run
    '''
    
    start_time = time.time() # Get program start time in seconds since epoch (1970 one not local data one) // TODO change to use 1st column (timestamp of data in millisec)
    Open_Port(com_port) # Opens the COM port to read in data
    while ((time.time() - start_time) <= run_time): # Checks the difference in start_time and current time is less than run_time
        
        current_epoch = Read_EMG_Epoch() # Reads data live into current_epoch for processing
        action = Classify_EMG(current_epoch) # Calls classify on current_epoch to determine what GUI action to throw
        
        Act(action, gui_scale) # Calls act to perform GUI action
           
    print("Run_time finished")
    
# %% Main Method call

Run(args.com_port, args.run_time, args.gui_scale)