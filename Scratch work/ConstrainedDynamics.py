#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 13:07:49 2020

@author: robertdenomme

demo of a constrained dynamics where the potential field is simply gravity,
and the constraint is of the form y=f(x)

Using formula for arbitrary constraints...
"""

from Vector import vector
import MatPlotRenderer
import numpy as np


m = 2
g = 10

dt = 1/60
total_time = 10
N = int(total_time / dt )


def f(x):
    return ((x-3)**2 * ((x+4)**2+1)-30)/100

def f_prime(x):
    return __f_prime_N__(x)
    #return __F_prime_exact__(x)



def __f_prime_N__(x):
    return (f(x+.001) - f(x-.001))/(2*.001)


def __f_prime_exact__(x):
    return 1/50*(2*x**3 + 3*x**2 - 22*x -15)

def f_primeprime(x):
    #return 1/25*(3*x**2 + 3*x - 11)
    return (f_prime(x+.001) - f_prime(x-.001))/(2*.001)

class phase:
    def __init__(self, x=0, y = f(0), x_dot = 0, y_dot = 0):
        self.x=x
        self.y = y
        self.x_dot=x_dot
        self.y_dot = y_dot
        
    def get_phase(self):
        return(self.x, self.y, self.x_dot, self.y_dot)
    
    def get_velocity_vector(self):
        return vector(self.x_dot, self.y_dot)

def get_initial_phase(x, *, x_dot=0):
    return phase(x=x, y=f(x), x_dot=x_dot, y_dot = f_prime(x) * x_dot)













############ equations for acceleration



def F(state):
    return state.y - f(state.x)

def F_q(state):
    return vector(- f_prime(state.x), 1)

def F_qq(state):
    return np.matrix([[-f_primeprime(state.x), 0],
                      [0, 0]])

def L_q(state):
    return vector(0,-m*g)

def lambda_1(state):
    q_dot = state.get_velocity_vector()
    result =  (1/m * F_q(state).dot(F_q(state)))**-1 \
        * ( 
            - q_dot.get_transpose_matrix() @ F_qq(state) @ q_dot.get_matrix() \
            -1/m * F_q(state).dot(L_q(state))
          )
    return result[0,0]
    #return max(result[0,0], 0)
    

def q_dotdot (state):
    return 1/m * (L_q(state) + lambda_1(state)*F_q(state))






#######integration scheme (midpoint)


def forward_euler_next(state, dt=dt):
    x, y, x_dot, y_dot = state.get_phase()
    
    x_next = x + dt * x_dot
    y_next = y + dt * y_dot

    x_dot_next = x_dot + dt * q_dotdot(state).x
    y_dot_next = y_dot + dt * q_dotdot(state).y

    return phase(x_next, y_next, x_dot_next, y_dot_next)


def midpoint_rule_next(state, dt=dt):
    x, y, x_dot, y_dot = state.get_phase()
    midpoint = forward_euler_next(state, dt/2)
    
    
    
    x_next = x + dt * midpoint.x_dot
    x_dot_next = x_dot + dt * q_dotdot(midpoint).x
    
    y_next = y + dt * midpoint.y_dot
    y_dot_next = y_dot + dt * q_dotdot(midpoint).y
    
    return phase(x_next, y_next, x_dot_next, y_dot_next)





def run_dynamics(initial_state, N):
    
    states = [initial_state]
    t=0+dt
    for i in range(1, N):
        next_state = midpoint_rule_next(states[-1])
        states.append(next_state)
        t += dt
        
    return states




if __name__ == "__main__":

    #initial position and momentum   
    initial_state = get_initial_phase(
        x=-6)

    states = run_dynamics(initial_state, N)

    q = [vector(s.x, s.y) for s in states]
    
    renderer = MatPlotRenderer.matplotrenderer(dt=dt)
    
    renderer.background_plot_set(f)
    
    renderer.animated_scatter_set([q])
    renderer.display()