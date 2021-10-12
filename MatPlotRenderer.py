#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 22:25:27 2020

@author: robertdenomme
Usage:
    renderer = matplotrenderer(xlim=(-10,10),ylim=(-10,10))
    renderer.background_plot_set(F)
    #F is a function
    renderer.animated_scatter_set([q1,q2,...])
    #q1 is a time-indexed list of vector trajectories to plot
    renderer.display()    
    
"""

from Vector import vector

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np







class matplotrenderer:
    def __init__(self, xlim=(-10,10), ylim=(-10,10), dt=1/24, marker = 'ro'):
        self.animated_scatter_datum = []
        self.__animated_scatter_flag__ = False
        
        self.__background__flag__ = False
        self.__background_F__ = lambda x:0
        
        self.dt = dt
        self.xlim = xlim
        self.ylim = ylim
        self.figsize = (10,10)
        
        self.timer_flag = True
        self.marker = marker
        
        
    
    def __setup__(self):
        self.fig = plt.figure(figsize=self.figsize)
        self.ax = self.fig.add_subplot(111, autoscale_on=False, xlim=self.xlim, ylim=self.ylim)
        self.ax.set_aspect('equal')
        self.ax.grid()
        
        if self.timer_flag :
            self.time_template = 'time = %.1fs'
            self.time_text = self.ax.text(0.05, 0.9, '', transform=self.ax.transAxes)

    def manual_lim_set(self, xlim=(-10,10), ylim=(-10,10)):
        self.xlim = xlim
        self.ylim = ylim
        
    def background_plot_set(self, F):
        self.__background__flag__ = True
        self.__background_F__ = F
        
    
    def __set_auto_window__(self, datum):
        xmin = min([qi.x for q in datum for qi in q ]) - 1
        xmax = max([qi.x for q in datum for qi in q ]) + 1
        
        ymin = min([qi.y for q in datum for qi in q]) - 1
        ymax = max([qi.y for q in datum for qi in q]) + 1
        
        self.xlim = (xmin, xmax)
        self.ylim = (ymin, ymax)
        
    def animated_scatter_set(self, datum, *, autowindow = True):
        if autowindow:
            self.__set_auto_window__(datum)
        
        self.__animated_scatter_flag__ = True
        self.animated_scatter_datum = datum
        
    def __animate__(self, i):
        x_list=[q[i].x for q in self.animated_scatter_datum]
        y_list=[q[i].y for q in self.animated_scatter_datum]
        
        self.animated_scatter_plot.set_data(x_list, y_list)
    
        
        self.time_text.set_text(self.time_template % (i*self.dt))
        return self.animated_scatter_plot, self.time_text
        
    def __animated_scatter_plot__(self):
        self.animated_scatter_plot, = self.ax.plot([],[], self.marker)
        self.ani = animation.FuncAnimation(self.fig, 
                                          self.__animate__, 
                                          len(self.animated_scatter_datum[0]), 
                                          interval=self.dt*1000, 
                                          blit=True,
                                          save_count = 50)
    
    def display(self):
        self.__setup__()
        
        if self.__animated_scatter_flag__:
            self.__animated_scatter_plot__()
            
        if self.__background__flag__:
            x_inputs = np.arange(self.xlim[0], self.xlim[1], .1)
            self.ax.plot(x_inputs, self.__background_F__(x_inputs), 'b-')
        
        plt.show()






    
if __name__ =="__main__":
    renderer = matplotrenderer()
    
    def F(x):
        return ((x-3)**2 * ((x+4)**2+1)-30)/100
    
    renderer.background_plot_set(F)
    
    x_range = np.arange(-10,10,.1)
    q = [vector(x,F(x)) for x in x_range]
    
    #renderer.manual_lim_set(xlim=(-10,10), ylim = (-20,20))
    
    renderer.animated_scatter_set([q, [vector(3,3) + v for v in q]])
    renderer.display()

    
