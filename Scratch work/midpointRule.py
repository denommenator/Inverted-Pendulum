#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 11:46:17 2020

@author: robertdenomme
"""
import math
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
recursion_depth = 4



#should make these vector classes...

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
    
    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    
    
class position(vector):
    pass
class velocity(vector):
    pass
class acceleration(vector):
    pass
        
#initial position and momentum   
initial_position = position(1,0)
initial_velocity = velocity(0,0)



#Euler integration

def get_acceleration(position, velocity):
    x = position.x
    y = position.y
    
    x_dot = velocity.x
    y_dot = velocity.y
    
    lagrange_lambda = (-2*(x_dot**2+y_dot**2)*m + 2*m*g*y)/(4*(x**2+y**2))
    
    # dL/dt = dL/dq + lambda * grad F
    return (1/m) * (vector(0, -m * g) + lagrange_lambda * vector(2*x, 2*y))

    


def forward_euler_next(position, velocity, dt = dt):
    position_next = position + dt * velocity
    velocity_next = velocity + dt * get_acceleration(position, velocity)
    return (position_next, velocity_next)

def backward_euler_next(position, velocity):
    position_next = [position]
    velocity_next = [velocity]
    
    position_next.append(position + dt * velocity_next[-1])
    velocity_next.append(velocity + dt * get_acceleration(position_next[-1], velocity_next[-1]))
    n = 1
    
    while (abs(position_next[-1] - position_next[-2]) + 
           abs(velocity_next[-1] - velocity_next[-2]) > recursion_tolerance 
           and n < recursion_depth):
        position_next.append(position + dt * velocity_next[-1])
        velocity_next.append(velocity + dt * get_acceleration(position_next[-1], velocity_next[-1]))
        n += 1
        
    if n == recursion_depth:
        print("hit recursion depth!")
    return (position_next[-1], velocity_next[-1])


def semi_implicit_robert_next(position, velocity):
    position_next = position + dt * velocity
    velocity_next = velocity + dt * get_acceleration(position_next, velocity)
    return (position_next, velocity_next)


def midpoint_rule_next(position, velocity):
    (midpoint_position, midpoint_velocity) = forward_euler_next(position, velocity, dt/2)
    
    position_next = position + dt * midpoint_velocity
    velocity_next = velocity + dt * get_acceleration(midpoint_position, midpoint_velocity)
    return (position_next, velocity_next)



def get_N_steps(initial_position, initial_velocity, N):
    positions = [initial_position]
    velocities = [initial_velocity]
    for i in range(1, N):
        (next_position, next_velocity) = midpoint_rule_next(positions[-1], velocities[-1])
        positions.append(next_position)
        velocities.append(next_velocity)
        
    return (positions, velocities)

(positions, velocities) = get_N_steps(initial_position, initial_velocity, N)


x = [position.x for position in positions]
y = [position.y for position in positions]






fig = go.Figure( 
    data=[go.Scatter(x=x, y=y,
                     mode="lines",
                     line=dict(width=2, color="blue")),
          go.Scatter(x=x, y=y,
                     mode="lines",
                     line=dict(width=2, color="blue"))],

    layout=go.Layout(
        xaxis=dict(range=[-1, 1], autorange=False, zeroline=False),
        yaxis=dict(range=[-1, 1], autorange=False, zeroline=False),
        title_text="Pendulum", hovermode="closest",
        updatemenus=[dict(type="buttons",
                          buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None])])]),
    frames=[go.Frame(
        data=[go.Scatter(
            x=[x[k]],
            y=[y[k]],
            mode="markers",
            marker=dict(color="red", size=10))])

        for k in range(len(x))]
    )

fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1))

plot(fig)