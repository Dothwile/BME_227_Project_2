"""
Created on Apr 7 2021

@author:  
Part C
Evaluate your predictions
BME227 Project 2

"""
#%% 
from Project1_submit import read_and_plot_serial_data
import numpy as np
from matplotlib import pyplot as plt

#%% Cell One: Import data

out_folder = '/BME227_code'
com_port = '/dev/cu.usbserial-1420'
read_and_plot_serial_data(com_port,60,3,500,"./Project1_submit_Data/") 

#%% Cell Two: Epoch the data

# load the ArduinoTime and ArduinoData into part C
emg_time = np.load('/Users/callankennedy/Desktop/ArduinoTime_2021-03-17_00:59:47.npy')
emg_voltage = np.load('/Users/callankennedy/Desktop/ArduinoData_2021-03-17_00:59:47.npy')

# epoch_sample_count = number of EMG samples in each 200ms chunk
# channel_count = number of channels, in this case 2
# epoch_count = number of 200ms epochs in your data, 10/.2 
# begin = start at 0
epoch_sample_count = 100
channel_count = 3
epoch_count = 50 
begin = 0

emg_epoch = np.zeros((epoch_count,epoch_sample_count,channel_count))

for epoch in range(epoch_count):
    for channel in range(channel_count):
        for sample in range(epoch_sample_count):
            emg_epoch[epoch,sample,channel] = emg_voltage[sample+begin,channel]
    begin = begin + 100


# save the epochs    
np.save("ArduinoData_2021-03-17_00/59/47_epochs.npy",emg_epoch)