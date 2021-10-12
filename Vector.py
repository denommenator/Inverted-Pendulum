#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 19:56:44 2020

The vector module!


@author: robertdenomme
"""

import math
import numpy as np

class vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, v):
        x= self.x + v.x
        y = self.y + v.y
        return vector(x, y)
    
    def __sub__(self, v):
        x= self.x - v.x
        y = self.y - v.y
        return vector(x, y)
    
    #scalar multiplication
    def __rmul__(self, scalar):
        x = scalar * self.x
        y = scalar * self.y
        return  vector(x, y)
    
    def __neg__(self):
        x = self.x
        y = self.y
        return  vector(-x, -y)
    
    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def dot(self, vec):
        return self.x * vec.x + self.y * vec.y
    
    def get_matrix(self):
        return np.matrix([[self.x],[self.y]])
    
    def get_transpose_matrix(self):
        return np.matrix([[self.x, self.y]])
    
    