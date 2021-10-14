#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 22:43:28 2020

@author: robertdenomme
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 11:46:17 2020

@author: robertdenomme
"""
from Vector import vector

import math
from math import cos
from math import sin
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go


#constants
m_ball = 1
m_cart = 3
g = 10
r = 2

e=10

#time step

N=24*10
dt = 1/24



class phase:
    def __init__(self, x=0, theta=0, x_dot=0, theta_dot=0):
        self.x=x
        self.theta=theta
        self.x_dot=x_dot
        self.theta_dot=theta_dot
        
    def get_phase(self):
        return(self.x, self.theta, self.x_dot, self.theta_dot)

        
#initial position and momentum   
initial_state = phase(0,0,0,0)



#Euler integration

def get_acceleration_ball(state):
    (x, theta, x_dot, theta_dot) = state.get_phase()
    
    theta_dot_dot =  \
    (m_ball * r**2 - (m_ball+m_cart)** -1 * m_ball**2 * r**2 * sin(theta)**2) ** -1 \
        * \
        (-m_ball * g * cos(theta) + \
         (m_ball+m_cart)** -1 * m_ball ** 2 * r**2 * sin(theta)*cos(theta)*theta_dot **2 \
            -  (m_ball+m_cart)** -1 * m_ball * r * sin(theta) * e)
    
    
    return theta_dot_dot

    
def get_acceleration_cart(state):
    (x, theta, x_dot, theta_dot) = state.get_phase()
    theta_dot_dot = get_acceleration_ball(state)
    
    x_dot_dot = (m_ball+m_cart)** -1 * (m_ball * r * (cos(theta)*theta_dot**2+sin(theta)*theta_dot_dot) - e)
    
    
    return x_dot_dot

def forward_euler_next(state, dt = dt):
    x_next = state.x + dt * state.x_dot
    x_dot_next = state.x_dot + dt * get_acceleration_cart(state)
    
    theta_next = state.theta + dt * state.theta_dot
    theta_dot_next = state.theta_dot + dt * get_acceleration_ball(state)
    
    return phase(x_next, theta_next, x_dot_next, theta_dot_next)


def midpoint_rule_next(state, dt=dt):
    
    midpoint = forward_euler_next(state, dt/2)
    
    
    
    x_next = state.x + dt * midpoint.x_dot
    x_dot_next = state.x_dot + dt * get_acceleration_cart(midpoint)
    
    theta_next = state.theta + dt * midpoint.theta_dot
    theta_dot_next = state.theta_dot + dt * get_acceleration_ball(midpoint)
    
    return phase(x_next, theta_next, x_dot_next, theta_dot_next)
    

def run_dynamics(initial_state, N):
    states = [initial_state]
    for i in range(1, N):
        next_state = midpoint_rule_next(states[-1])
        states.append(next_state)
        
    return states



states = run_dynamics(initial_state, N)

q_cart = [vector(s.x, 0) for s in states]
q_ball = [vector(s.x, 0) + r * vector(math.cos(s.theta) , math.sin(s.theta)) for s in states]

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
    N = len(items[0])
    return [go.Scatter(x=[item[t].x for t in range(N)],
                       y=[item[t].y for t in range(N)],
                       mode="lines",
                       line=dict(width=2, color="blue"),
                       ) for item in items]
    

fig = go.Figure( 
    # data=[go.Scatter(x=[0,2], y=[0,2],
    #                  mode="lines",
    #                  line=dict(width=2, color="blue"))],
    data = data(items_to_plot),
        
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