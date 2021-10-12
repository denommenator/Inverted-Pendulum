#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 21:53:01 2020

@author: robertdenomme
"""


import math
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go


mball = 1
mcart = 2
r = 2
g = 10

delta_t = .01
N = 1000
skip_frames = 10



class my_phase:
    def __init__(self, x, x_dot, theta, theta_dot):
        self.x = x
        self.x_dot = x_dot
        self.theta = theta
        self.theta_dot = theta_dot



phases = [my_phase(0,0,math.pi/4,0)]

def theta_double_dot(phase):
    return 1 / (mball * r**2 - mball/(mball+mcart) * r**2 * math.sin(phase.theta)**2)\
        * (mball / (mball+mcart)*phase.theta_dot**2 * r**2 * math.cos(phase.theta)*math.sin(phase.theta)\
          - mball * g * r * math.cos(phase.theta))

def get_next_theta(phase):
    return phase.theta + phase.theta_dot * delta_t

def get_next_x(phase):
    return phase.x + phase.x_dot * delta_t

def get_next_x_dot(phase):
    return 1/(mcart+mball) * get_next_theta_dot(phase) * r * math.sin(get_next_theta(phase))

def get_next_theta_dot(phase):
    return phase.theta_dot + theta_double_dot(phase) * delta_t

def get_next_phase(phase):
    return my_phase(get_next_x(phase) ,
                 get_next_x_dot(phase) ,
                 get_next_theta(phase) ,
                 get_next_theta_dot(phase))


for t in range(N):
    phases.append(get_next_phase(phases[-1]))



xcart = [phase.x for phase in phases[0:-1:skip_frames]]
ycart = [0 for phase in phases[0:-1:skip_frames]]

xball = [phase.x + r * math.cos(phase.theta) for phase in phases[0:-1:skip_frames]]
yball = [r * math.sin(phase.theta) for phase in phases[0:-1:skip_frames]]



fig = go.Figure( 
    data=[go.Scatter(x=xcart, y=ycart,
                     mode="markers",
                     line=dict(width=2, color="blue")),
          go.Scatter(x=xball, y=yball,
                     mode="markers",
                     line=dict(width=2, color="blue"))],

    layout=go.Layout(
        xaxis=dict(range=[-1, 1], autorange=False, zeroline=False),
        yaxis=dict(range=[-1, 1], autorange=False, zeroline=False),
        title_text="cart and rod", hovermode="closest",
        updatemenus=[dict(type="buttons",
                          buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None])])]),
    frames=[go.Frame(
        data=[go.Scatter(
            x=[xcart[k]],
            y=[ycart[k]],
            mode="markers",
            marker=dict(color="red", size=10)),
        go.Scatter(
            x=[xball[k]],
            y=[yball[k]],
            mode="markers",
            marker=dict(color="red", size=10))
            ])

        for k in range(len(xcart))]
    )
plot(fig)





