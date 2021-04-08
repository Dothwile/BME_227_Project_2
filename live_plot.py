#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 22:13:18 2021

@author: Kai
"""
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')


fig = plt.figure()
ax = plt.axes(xlim=(0, 60), ylim=(0, 8))
line, = ax.step([], [], lw=3)
actions=['Rest','Left','Right','Bicep','Bicep & Left','Right & Left']
plt.yticks([0,1,2,3,4,5],labels=actions)
 
display_data_y=np.array([0,0,1,1,2,2,3,3,4,4,5,5]*5)
display_data_x=np.arange(0,60)

xdata=[]
ydata=[]
def init():
    line.set_data([], [])
    return line,
def animate(i):
    x = display_data_x[i]
    y = display_data_y[i]
    xdata.append(x)
    ydata.append(y)             
    line.set_data(xdata, ydata)
    return line,

anim = FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=1000, blit=True)
