#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 20:08:37 2020

@author: robertdenomme
"""

from Vector import vector

import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go


#constants
m = 3
g = 10
r = 1

#time step

N=24*10
dt = 1/24
recursion_tolerance = 0.01
recursion_depth = 5


class phase:
    def __init__(self, q = vector(0,0), q_dot = vector(0,0)):
        self.q = q
        self.q_dot = q_dot




phase_cart_initial = phase(q = vector(1,0), q_dot = vector(1,1))
phase_ball_initial = phase(q = vector(1,0), q_dot = vector(1,1))





def get_ball_acceleration(phase_cart, phase_ball, t=0):
    
    
    # dL/dt = dL/dq + lambda * grad F
    return vector(0,-.1)



def get_cart_acceleration(phase_cart, phase_ball, t=0):
    
    
    # dL/dt = dL/dq + lambda * grad F
    return vector(0,-.1)


def get_next_ball_position(phase_ball, phase_cart, t=0):
    pass


def get_next_cart_position(phase_ball, phase_cart, t=0):
    pass

def get_next_ball_velocity(phase_ball, phase_cart, t=0):
    pass


def get_next_cart_velocity(phase_ball, phase_cart, t=0):
    pass

def run_dynamics(phase_ball_initial, phase_cart_initial):
    pass






# y[n+1] = y[n] + dt * f(y[n] + dt / 2 * f(y[n]))

# since f(q, q_dot) = (q_dot, accel(q, q_dot))









q_cart = [vector(k * .5, k * .5) for k in range(10)]
q_ball = [vector(k * .5, k * .5) + vector(0,1) for k in range(10)]


# scatter_cart = go.scatter(x=[q_cart[k].x , q_ball[k].y]
#                           y=[q_cart[k].y , q_ball[k].y],
#                           mode="markers",
#                           marker=dict(color="red", size=10)
#                           )
                          

items_to_plot = [q_cart, q_ball]




def frames(items):
    return [go.Frame(
        data = [go.Scatter(x=[item[t].x for item in items],
                           y=[item[t].y for item in items],
                           mode="markers",
                           marker=dict(color="red", size=10)
                           )]
        ) 
        for t in range(len(items[0]))]
    
def data(items):
    [go.Scatter(x=[item[t].x for t in range(len(items[0])]],
                           y=[item[t].y for item in items],
                           mode="markers",
                           marker=dict(color="red", size=10)
                           )

fig = go.Figure( 
    # data=[go.Scatter(x=[0,2], y=[0,2],
    #                  mode="lines",
    #                  line=dict(width=2, color="blue"))],
        data = [go.Scatter()],
        
    layout=go.Layout(
        xaxis=dict(range=[-1, 1], autorange=False, zeroline=False),
        yaxis=dict(range=[-1, 1], autorange=False, zeroline=False),
        title_text="Pendulum", hovermode="closest",
        updatemenus=[dict(type="buttons",
                          buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None])])]),
    frames = frames(items_to_plot)
 
    )

fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1))

plot(fig)