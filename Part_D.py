# %% Imports

import Part_B
import Part_C
import serial
import argparse
import numpy as np
import pyautogui as pyg

# %% Dummy variables, will figure origin later
com_port = 'COM3'

# Note that these all should be loaded in save for sample_buffer
n_channels = 3
epoch_size = 200
sample_buffer = np.zeros((epoch_size, n_channels))

# %% Live Reading Main Method

def Read_EMG_Live():
    ''' Read_EMG_Live
    
    to add docstring
    
    '''

    with serial.Serial(port=com_port,baudrate=500000) as arduino_data:
    
        for sample_index in range(sample_buffer.shape[0]): # Iterates over samples in buffer
            # Extract data string to parse
            data_string = arduino_data.readline().decode('ascii')
            # Split into list of strings
            data_string = data_string.split() # First element is time of sample in ms, rest are sensor values
            
            # Uses short circuit logic and to avoid indexing errors when read line empty or short
            if(len(data_string) >= (n_channels + 1) and (st[sample_index] >= int(data_string[0]))):
                st[sample_index] = int(data_string[0])
            
                # Writes the output of each channel to associate column of data array
                # Converts to V
                for channel in range(n_channels):
                    # Write collected data point from each channel to associated position in sd
                    sample_buffer[sample_index, channel] = int(data_string[channel+1])*5.0/1024
            
            else: # If data readline is not full, consider it a dropped point and increase time sample index
                st[sample_index] = int(data_string[0])
            
            # Seperate check and loop for plot updates reduces net operations per cycle
            if((sample_index % 50) == 0):
                for channel in range(n_channels):                
                    # Update the buffer?
                    pass
                    
    
    # Close the port // Define exit condition?
    arduino_data.close()