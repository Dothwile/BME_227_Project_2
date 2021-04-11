#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 13:32:36 2021

@author: Kai
"""



def evaluate_and_plot_confusion(path_of_data):
    # import packages
    import numpy as np
    import datetime as dt
    from matplotlib import pyplot as plt
    
    #globals
    path_string='Arduino_data'
    now=dt.datetime.now() #get time 
    
    def load_data(path=path_of_data):
        '''
        

        Parameters
        ----------
        path : string
            The path of the datafile recorded in part B

        Returns
        -------
        emg_epoch : TYPE
            array of 300 epochs that contain 100 samples each

        '''
        emg_voltage=np.load(path)
        #initialise epoch size variables
        fs=float(500) # sampling frequency
        epoch_time=float(0.2) # time to record each epoch
        recording_duration=float(60) # time of recoding
        epoch_sample_count=int(fs*epoch_time) #number of samples per epoch
        row_count,channel_count=np.shape(emg_voltage) # get number of channels 
        epoch_count=int((fs/epoch_sample_count)*recording_duration) # number of epochs in array
    
        # use reshape to index data into epochs
        emg_epoch=np.reshape(emg_voltage,(epoch_count, epoch_sample_count, channel_count))
        return emg_epoch
    

    def var_and_true_arrays(emg_epoch):
        '''
        

        Parameters
        ----------
        emg_epoch : array
            array of epochs made in the previous funciton

        Returns
        -------
        emg_epoch_var : 300,3 array
            array of the variance of each epoch from emg_epoch
        proper_fake_epoch_var : 300,3 array
            array of fake data to test the rest of the script
        is_true_left : 300,1 array
            boolean array of true when the left arm was supposed to be squeezed 
        is_true_right : 300,1 array
            boolean array of true when right arm was supposed to be squeezed
        is_true_bicep : 300,1 array
            boolean array of true when bicep was supposed to be squeezed

        '''
        # get varience of epochs
        emg_epoch_var=np.var(emg_epoch,1)
        
        fake_epoch_var=np.array([[.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,\
                                  .0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,\
                                      .0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,\
                                          .0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,\
                                          .0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,\
                                              .0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,]*5,\
                                 [.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,\
                                  .0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,\
                                      .0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,\
                                          .0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,\
                                              .0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,
                                          .0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003]*5,\
                                     [.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,\
                                      .0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,\
                                          .0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,\
                                              .0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,\
                                                  .0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,.0003,\
                                                      .0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,.0001,]*5])
        proper_fake_epoch_var=fake_epoch_var.T # transpose fake epoch array
        
        # create boolean arrays 
        
        #create array of 1s when left and both should be squezed
        is_true_left=np.array([0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,\
                               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                                   1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]*5,dtype=bool)
        
        # create array of 1s when right and both should be squezed 
        is_true_right=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                                1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,\
                                    0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1]*5,dtype=bool)
        # create bicp array
        is_true_bicep=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                                0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,\
                                    1,1,1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0,0,0]*5,dtype=bool)
        return emg_epoch_var, proper_fake_epoch_var, is_true_left, is_true_right, is_true_bicep
        
    def left_hist_plot(emg_epoch_var, is_true_left):
        '''
        

        Parameters
        ----------
        emg_epoch_var : array 
            array of epoch variances
        is_true_left : boolean array
            array of true when left arm was supposed to be squeezed

        Returns
        -------
        plot of true left and not true left

        '''
        #left hand 
        
        plt.hist(emg_epoch_var[is_true_left==1,0],bins=60,alpha=0.5)
        plt.hist(emg_epoch_var[is_true_left==0,0],bins=60, alpha=0.5) # create plot
        #plt.axvline(x=0.0002)
        plt.xlim([0,0.003])
        plt.xlabel('Variance of left arm') # add x axis label
        plt.ylabel('number of trials') # add y axis label
        plt.title('Var of left arm true vs not true') # add title 
        plt.legend(('true left','not true left')) # add legend with data from A0 as ch1, A2 as ch2, A3 as ch3
       
        now.isoformat()
        plt.savefig(f'{path_string}/ArduinoData_{now}_leftHist.png') #save figure
        return 
    
    def right_hist_plot(emg_epoch_var, is_true_right):
        '''
        

        Parameters
        ----------
        emg_epoch_var : array
            array of epoch variances 
        is_true_right : boolean array
            boolean array of true when right arm was supposed to be squeezed

        Returns
        -------
        plot of true right and not true right

        '''
        #right arm
        plt.hist(emg_epoch_var[is_true_right==1,1],bins=40,alpha=0.5)
        plt.hist(emg_epoch_var[is_true_right==0,1],bins=40, alpha=0.5) # create plot
        #plt.axvline(x=0.00019)
        plt.xlim([0,0.002])
        plt.xlabel('Variance of right arm') # add x axis label
        plt.ylabel('number of trials') # add y axis label
        plt.title('Variance of right arm of true right and not true right') # add title 
        plt.legend(('true right','not true right')) # add legend 
        now.isoformat()
        plt.savefig(f'{path_string}/ArduinoData_{now}_RightHist.png') #save figure
        return
    
    def bicep_hist_plot(emg_epoch_var, is_true_bicep):
        '''
        

        Parameters
        ----------
        emg_epoch_var : array
            array of epoch variances 
        is_true_bicep : boolean array
            boolean array of true when the bicep was supposed to be squeezed

        Returns
        -------
        plot of true bicep and not true bicep

        '''
        plt.hist(emg_epoch_var[is_true_bicep==1,2],bins=60,alpha=0.5)
        plt.hist(emg_epoch_var[is_true_bicep==0,1],bins=40, alpha=0.5) # create plot
        #plt.axvline(x=0.00019)
        plt.xlim([0,0.003])
        plt.xlabel('Variance of bicep') # add x axis label
        plt.ylabel('number of trials') # add y axis label
        plt.title('Variance of bicep of true and not true') # add title 
        plt.legend(('true bicep','not true bicep')) # add legend 
        now.isoformat()
        plt.savefig(f'{path_string}/ArduinoData_{now}_bicepHist.png') #save figure
    
    def boolean_arrays(emg_epoch_var, is_true_left, is_true_right, is_true_bicep, left_var, right_var, bicep_var):
        '''
        

        Parameters
        ----------
        emg_epoch_var : array
            array of epoch variances
        is_true_left : boolean array
            boolean array of tue when left was supposed to be squeezed
        is_true_right : boolean array
            boolean array of true when right was supposed to be squeezed
        is_true_bicep : boolean array
            boolean array of true when bicep was supposed to be squeezed
        left_var : float
            threshold determined from plot of left arm. enterd as a string to the command line
        right_var : foat
            threshold determined from plot of right arm. enterd as a string to the command line
        bicep_var : float
            threshold determined from plot of bicep. enterd as a string to the command line

        Returns
        -------
        is_predicted_left : boolean array
            boolean array created by setting values in emg_epoch_var to true if they are 
            greater than the threshold that was entered
        is_predicted_right : boolean array
            boolean array created by setting values in emg_epoch_var to true if they are 
            greater than the threshold that was entered
        is_predicted_bicep : boolean array
            boolean array created by setting values in emg_epoch_var to true if they are 
            greater than the threshold that was entered

        '''
        
        #create boolean arrarys
        is_predicted_left=emg_epoch_var[:,0]>left_var #from the graph, set threshhold to 0.0002
        is_predicted_right=emg_epoch_var[:,1]>right_var# from graph, set threshold to 0.00019
        is_predicted_bicep=emg_epoch_var[:,2]>bicep_var
        return is_predicted_left, is_predicted_right, is_predicted_bicep
    
    def hmi_eval(is_predicted_left, is_predicted_right, is_predicted_bicep, is_true_left, is_true_right, is_true_bicep):
        '''
        

        Parameters
        ----------
        is_predicted_left : boolean array
            boolean array created by setting values in emg_epoch_var to true if they are 
            greater than the threshold that was entered
        is_predicted_right : boolean array
            boolean array created by setting values in emg_epoch_var to true if they are 
            greater than the threshold that was entered
        is_predicted_bicep : boolean array
            boolean array created by setting values in emg_epoch_var to true if they are 
            greater than the threshold that was entered
        is_true_left : boolean array
            array of true when left was was supposed to be squeezed
        is_true_right : boolean array
            array of true when right are was supposed to be squeezed
        is_true_bicep : boolean array
            array of true when bicep was supposed to be squeezed

        Returns
        -------
        accuracy_left : float
            accuracy of left arm perdictions calculated using true positives and true 
            negatives. 
        accuracy_right : float
             accuracy of right arm perdictions calculated using true positives and true 
            negatives.
        accuracy_bicep : float
             accuracy of bicep perdictions calculated using true positives and true 
            negatives.
        itr_time_left : flaot
            Information transfer rate in bits per second for left arm
        itr_time_right : float
             Information transfer rate in bits per second for right arm
        itr_time_bicep : float
             Information transfer rate in bits per second for bicep

        '''
        # for left hand
        tp_left = np.count_nonzero(is_predicted_left[is_true_left==1]) # calculate true positives 
        tn_left = np.size(is_predicted_left[is_true_left==0])-np.count_nonzero(is_predicted_left[is_true_left==0]) # calculate true negatives
        fp_left = np.count_nonzero(is_predicted_left[is_true_left==0]) #calculate false positive
        fn_left = np.size(is_predicted_left[is_true_left==0])-np.count_nonzero(is_predicted_left[is_true_left==1])# calculate false negatives
        
        accuracy_left= (tp_left+tn_left)/(tp_left+tn_left+fp_left+fn_left) #calculate accuracy
        sensitivity_left= tp_left/(tp_left+fn_left) # calculate sensitivity 
        specificity_left= tn_left/(fp_left+tn_left) # calculate specificity
        n=6 #set class to 6. right, left, rest, click, up, down
        p_left=accuracy_left
        itr_trial_left=np.log2(n)+p_left*np.log2(p_left)+(1-p_left)*np.log2((1-p_left)/(n-1))
        itr_time_left=itr_trial_left*5 #information transfer rate in bits/sec
        
        #for right hand
        tp_right = np.count_nonzero(is_predicted_right[is_true_right==1])
        tn_right = np.size(is_predicted_right[is_true_right==0])-np.count_nonzero(is_predicted_right[is_true_right==0])
        fp_right = np.count_nonzero(is_predicted_right[is_true_right==0])
        fn_right = np.size(is_predicted_right[is_true_right==0])-np.count_nonzero(is_predicted_right[is_true_right==1])
        
        accuracy_right= (tp_right+tn_right)/(tp_right+tn_right+fp_right+fn_right)
        sensitivity_right= tp_right/(tp_right+fn_right)
        specificity_right= tn_right/(fp_right+tn_right)
        
        p_right=accuracy_right
        itr_trial_right=np.log2(n)+p_right*np.log2(p_right)+(1-p_right)*np.log2((1-p_right)/(n-1))
        itr_time_right=itr_trial_right*5
        
        
        # bicep
        
        tp_bicep = np.count_nonzero(is_predicted_bicep[is_true_bicep==1]) # calculate true positives 
        tn_bicep = np.size(is_predicted_bicep[is_true_bicep==0])-np.count_nonzero(is_predicted_bicep[is_true_bicep==0]) # calculate true negatives
        fp_bicep = np.count_nonzero(is_predicted_bicep[is_true_bicep==0]) #calculate false positive
        fn_bicep = np.size(is_predicted_bicep[is_true_bicep==0])-np.count_nonzero(is_predicted_bicep[is_true_bicep==1])# calculate false negatives
        
        accuracy_bicep= (tp_bicep+tn_bicep)/(tp_bicep+tn_bicep+fp_bicep+fn_bicep) #calculate accuracy
        sensitivity_bicep= tp_bicep/(tp_bicep+fn_bicep) # calculate sensitivity 
        specificity_bicep= tn_bicep/(fp_bicep+tn_bicep) # calculate specificity
       
        p_bicep=accuracy_bicep
        itr_trial_bicep=np.log2(n)+p_bicep*np.log2(p_bicep)+(1-p_bicep)*np.log2((1-p_bicep)/(n-1))
        itr_time_bicep=itr_trial_bicep*5 #information transfer rate in bits/sec
        return accuracy_left, accuracy_right, accuracy_bicep, itr_time_left, itr_time_right, itr_time_bicep
    
    def plot_confusion(is_predicted_left, is_predicted_right, is_predicted_bicep, is_true_left, is_true_right, is_true_bicep):
        '''
        

        Parameters
        ----------
        is_predicted_left : boolean array
            boolean array created by setting values in emg_epoch_var to true if they are 
            greater than the threshold that was entered
        is_predicted_right : boolean array
            boolean array created by setting values in emg_epoch_var to true if they are 
            greater than the threshold that was entered
        is_predicted_bicep : boolean array
            boolean array created by setting values in emg_epoch_var to true if they are 
            greater than the threshold that was entered
        is_true_left : boolean array
            array of true when left was was supposed to be squeezed
        is_true_right : boolean array
            array of true when right are was supposed to be squeezed
        is_true_bicep : boolean array
            array of true when bicep was supposed to be squeezed

        Returns
        -------
        true_actions : array
            array filled in with 'left','right','rest','up','down','click' depending 
            on what action was supposed to be happening at the corresponding time
        predicted_actions : array
             array filled in with 'left','right','rest','up','down','click' depending 
            on what action was predicted using the variance of the epochs

        '''
        is_predicted_6_left=(is_predicted_right==0) & (is_predicted_left==1) & (is_predicted_bicep==0) # creat array of true for when left is predicted
        is_predicted_6_right=(is_predicted_right==1)&(is_predicted_left==0)& (is_predicted_bicep==0) # creat array  of true for when right is predicted 
        is_predicted_6_click=(is_predicted_right==1)&(is_predicted_left==1)& (is_predicted_bicep==0) # creat array of true for when click (both) is predicted
        is_predicted_6_rest=(is_predicted_right==0)&(is_predicted_left==0)& (is_predicted_bicep==0) # creat array of true for when rst (none) is predicted
        is_predicted_6_up=(is_predicted_right==0)&(is_predicted_left==0)& (is_predicted_bicep==1)
        is_predicted_6_down=(is_predicted_right==0)&(is_predicted_left==1)& (is_predicted_bicep==1)
        
        
        is_true_6_left=(is_true_left==1)&(is_true_right==0) & (is_true_bicep==0) # creat array of true for when left is actully squeezed
        is_true_6_right=(is_true_left==0)&(is_true_right==1)& (is_true_bicep==0) # creat array of true for when right is actully squeezed
        is_true_6_click=(is_true_left==1)&(is_true_right==1)& (is_true_bicep==0) # creat array of true for when click (both) is actully squeezed
        is_true_6_rest=(is_true_left==0)&(is_true_right==0)& (is_true_bicep==0) # creat array of true for when rest (none) is actully squeezed
        is_true_6_up=(is_true_left==0)&(is_true_right==0)& (is_true_bicep==1)
        is_true_6_down=(is_true_left==1)&(is_true_right==0)& (is_true_bicep==1)
        
        
        epoch_count=len(is_true_6_left)
        # create array of true actions
        true_actions=np.array(['rest']*epoch_count,dtype='object')
        true_actions[is_true_6_left]='left'
        true_actions[is_true_6_right]='right'
        true_actions[is_true_6_rest]='rest'
        true_actions[is_true_6_up]='up'
        true_actions[is_true_6_down]='down'
        true_actions[is_true_6_click]='click'
        
        # create array of predicted actions
        predicted_actions=np.array(['rest']*epoch_count,dtype='object')
        predicted_actions[is_predicted_6_left]='left'
        predicted_actions[is_predicted_6_right]='right'
        predicted_actions[is_predicted_6_rest]='rest'
        predicted_actions[is_predicted_6_up]='up'
        predicted_actions[is_predicted_6_down]='down'
        predicted_actions[is_predicted_6_click]='click'
        
        
        
        possible_actions=['left','right','rest','up','down','click'] # array of all possible actions
        action_count=len(possible_actions) # get length to crate array of proper size
        
        confusion_matrix=np.zeros([action_count,action_count]) # initialize array
        
        # fill in confusion matrix
        for predicted_action_index, predicted_action in enumerate(possible_actions):
            for true_action_index, true_action in enumerate(possible_actions):
                confusion_matrix[predicted_action_index, true_action_index]= \
                    np.sum((predicted_actions==predicted_action)&(true_actions==true_action))
                    
        
        
        plt.figure() # set up figure
        plt.pcolor(confusion_matrix) #plot
        plt.title('HMI Confusion Matrix') #title
        plt.xticks([0.5,1.5,2.5,3.5,4.5,5.5],labels=possible_actions) # set coordinates for x lables
        plt.xlabel('actual action') # set x axis title
        plt.yticks([0.5,1.5,2.5,3.5,4.5,5.5],labels=possible_actions) # set coordinates for y lables
        plt.ylabel('predicted action') # set y axis title
        plt.colorbar(label='# trials') # creat color bar 
        plt.savefig(f'{path_string}/ArduinoData_{now}_confusionmatrix.png') #save figure
        print(true_actions) # for debugging
        print(predicted_actions) # for debugging 
        return true_actions, predicted_actions
  
    print('Loading saved data...')
    print('epoching data...')
    # call function to load data and seperate the data into epochs
    emg_epoch=load_data(path=path_of_data)
    
    # call function to create is_true arrays
    emg_epoch_var, proper_fake_epoch_var, is_true_left, is_true_right, is_true_bicep=var_and_true_arrays(emg_epoch)
    
    # call functions to plot histograms of data
    print('plotting histograms to choose threshold')
    
    # left arm
    left_hist_plot(emg_epoch_var, is_true_left)
    plt.show()
    # right arm
    right_hist_plot(emg_epoch_var, is_true_right)
    plt.show()
    # bicep
    bicep_hist_plot(emg_epoch_var, is_true_bicep)
    plt.show()
    
    # add input prompt to ask for varience thresholds 
    prompt=input('enter the thresholds as a comma seperated list:')
    # split list after each comma
    left_var, right_var, bicep_var= prompt.split(',')
    
    #save variables to files for part D
    left_var_edit = open('left_var.txt','w+')
    left_var_edit.write(left_var)
    left_var_edit.close()
    
    right_var_edit = open('right_var.txt','w+')
    right_var_edit.write(right_var)
    right_var_edit.close()
    
    bicep_var_edit = open('bicep_var.txt','w+')
    bicep_var_edit.write(bicep_var)
    bicep_var_edit.close()
    
    
    # conver inputs from str to float 
    left=float(left_var)
    right=float(right_var)
    bicep=float(bicep_var)
    
    #call boolean_arrays function to create is_predicted arrays using the thresholds that were entered above
    is_predicted_left, is_predicted_right, is_predicted_bicep=boolean_arrays(emg_epoch_var, is_true_left, is_true_right, is_true_bicep, left, right, bicep)
    
    #evalute the paramaters of the HMI
    accuracy_left, accuracy_right, accuracy_bicep, itr_time_left, itr_time_right, itr_time_bicep = hmi_eval(is_predicted_left, is_predicted_right, is_predicted_bicep, is_true_left, is_true_right, is_true_bicep)
    
    # plot confusion matrix
    plot_confusion(is_predicted_left, is_predicted_right, is_predicted_bicep, is_true_left, is_true_right, is_true_bicep)
    # print accuracy
    print(f'accuracy for left arm:{accuracy_left}')
    print(f'accuracy for right arm:{accuracy_right}')
    print(f'accuracy for bicep:{accuracy_bicep}')
    # print ITR
    print(f'ITR left:{itr_time_left}')
    print(f'ITR right:{itr_time_right}')
    print(f'ITR bicep:{itr_time_bicep}')
    return emg_epoch, emg_epoch_var


file='Arduino_Data/ArduinoData_2021-04-10T11_02_31.460505-0400.npy'  # data file to use   

emg_epoch, emg_epoch_var=evaluate_and_plot_confusion(file)  # call main function

