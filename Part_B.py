#%% import packages
import numpy as np
import matplotlib.pyplot as plt
import serial
import datetime as dt
import os
import argparse
from matplotlib.animation import FuncAnimation
#%%

data_path = 'Arduino_Data'
com = 'COM3'

 # main function
def record_data(com_port=com, recording_duration=60, n_channels=3, fs=500, out_string=data_path):  
    
 #initialize array


    def initialize_arrays(recording_duration,n_channels,fs):
            '''
            this function initializes two arrays. sample_time is a 1d array that holds the 
            time of each sample recorded. sample_data is a 2D array with n_channels. Each 
            column is a seperate channels. the channels correspond to sensors on the Arduino
    
            Parameters
            ----------
            recording_duration : int
                Length of time to run the recording
            n_channels : int
                number of sensors hooked up to the Arduino
            fs : int
                the sampeling frequency of the arduino 
    
            Returns
            -------
            sample_time : 1D array
                holds the time of each sample
            sample_data: 2D array
                Holds the reading from each sample in each column
    
            '''
            sample_time=np.zeros([recording_duration*fs,1])*np.nan # create #sample by 1 array
            sample_data=np.zeros([recording_duration*fs,n_channels])*np.nan # create #sample by number of channels array
            
            
            
            return sample_time, sample_data # return the sample time and sample data as variables
        
    #Create plot for display
        
    # #rest, left, right, bicep-up, bicep&left-down, right&left-click
    # 2 second intervals 
    #create data
    def initialize_plot():
         #create display plot arrays
        display_data_y=np.array([0,0,1,1,2,2,3,3,4,4,5,5]*5)
        display_data_x=np.arange(0,60)  
        plot=plt.step(display_data_x,display_data_y) # create plot
        actions=['Rest','Left','Right','Bicep','Bicep & Left','Right & Left']
        plt.xlim([0,60]) # set the x axis limits
        plt.ylim([0,8]) # set the y axis limits 
        
        plt.xlabel('time') # add x axis label
        plt.yticks([0,1,2,3,4,5],labels=actions)
        plt.title('Time Plot of Actions') # add title 
        #plt.legend(('ch1','ch2','ch3')) # add legend with data from A0 as ch1, A2 as ch2, A3 as ch3
        
    
        return plot
    
    
    
    
    
    #Read data and save
    print('rest, squeez left arm, then right armn then bicep, then bicep & left, then right &left') 
    print('Hold each action for 2s')
    
   
   
    sample_time, sample_data= initialize_arrays(recording_duration, n_channels, fs) # call array function
    initialize_plot() # initialize plot function
    
    prompt=input('enter s to start:').lower()
    
    
    if prompt=='s':  
        
        with serial.Serial(port=com_port, baudrate=500000) as arduino_data: #open connection to serial monitor. takes input com_port form main function
            
                
                n_channel=len(sample_data[0]) #create variable that is the number of columns in sample_data
                for data_index in range(len(sample_data)): # for loop to index data into arrays
                    try:
                                
                        arduino_string=arduino_data.readline().decode('ascii') # read line from serial
                                        
                        arduino_list=arduino_string.split() # split string into list at space
                                        
                        sample_time[data_index]=int(arduino_list[0])/1000 # put 1st piece of data into time array
                           
                        for channel_index in range(n_channel): # for loop to index data into the corrct column of sample_data and data_line
                            sample_data[data_index,channel_index]=int(arduino_list[channel_index+1])*5/1024
                        
                               
                    
                    except:
                        pass
                               
    arduino_data.close() # close searial port
            
    
        
    #Save data 
        
    path_string = out_string # create path for folder
    try:
            os.mkdir(path_string)
    except OSError:
            print('save failed')
    else:
            print('folder created')
        
    now=dt.datetime.now() #get time 
    now.isoformat()
        
    np.save(f'{path_string}/ArduinoData_{now}',sample_data) #save sample_data
    np.save(f'{path_string}/ArduinoTime_{now}',sample_time) #save sample_time
        
            
    return 

record_data(com_port='/dev/cu.usbserial-1440', recording_duration=60, n_channels=3, fs=500, out_string=data_path)


