#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 16:03:34 2020

@author: robertdenomme
double pendulum

"""

from Vector import vector
import MatPlotRenderer
import numpy as np
import numpy.linalg as LA



m1 = 2
m2 = 1
g = 10

dt = 1/60
total_time = 5
N = int(total_time / dt )


class q_phase:
    def __init__(self, x, y, x_dot = 0, y_dot = 0):
        self.x = x
        self.y = y
        self.x_dot = x_dot
        self.y_dot = y_dot
    
    @property    
    def q(self):
        return vector(self.x, self.y)
    
    @property
    def q_dot(self):
        return vector(self.x_dot, self.y_dot)
    
    def get_variables(self):
        return(self.x, self.y, self.x_dot, self.y_dot)
        
class phase():
    def __init__(self, q1_phase, q2_phase):
        self.q1_phase = q1_phase
        self.q2_phase = q2_phase
    
    def get_q1_phase(self):
        return self.q1_phase;
    def get_q2_phase(self):
        return self.q2_phase;
    
    
    
    @property
    def q1(self):
        return self.q1_phase.q;
    @property
    def q2(self):
        return self.q2_phase.q;
    
    @property
    def q1_dot(self):
        return self.q1_phase.q_dot;
    @property
    def q2_dot(self):
        return self.q2_phase.q_dot;
    


def F1_q1 (state):
    return 2 * state.q1

def F1_q2(state):
    return vector(0,0)

def F2_q1(state):
    return 2*(state.q1 - state.q2)

def F2_q2(state):
    return 2*(state.q2 - state.q1)

def L_q1(state):
    return vector(0,-m1*g)

def L_q2(state):
    return vector(0,-m2*g)

def lambdas(state):
    (q1, q2, q1_dot, q2_dot) = (state.q1, state.q2, state.q1_dot, state.q2_dot)
    
    
    A = np.matrix([[1/m1 * F1_q1(state).dot(F1_q1(state)), 1/m1 * F1_q1(state).dot(F2_q1(state))],
                   [1/m1 * F2_q1(state).dot(F1_q1(state)), 
                    1/m1 * F2_q1(state).dot(F2_q1(state)) + 1/m2 * F2_q2(state).dot(F2_q2(state))]
                   ])

    b = np.matrix([[-2*q1_dot.dot(q1_dot)
                        - 1/m1 * F1_q1(state).dot(vector(0,-m1*g))],
                   [-2*q1_dot.dot(q1_dot) + 4*q1_dot.dot(q2_dot) - 2*q2_dot.dot(q2_dot) \
                       - 1/m1 * F2_q1(state).dot(L_q1(state)) \
                         - 1/m2 * F2_q2(state).dot(L_q2(state))
                    ]
                   ])
        
    L = LA.solve(A,b)
    lambda1 = L[0,0]
    lambda2 = L[1,0]
    return (lambda1, lambda2)



def q_dotdot(state):
    (lambda1, lambda2) = lambdas(state)
    
    q1_dotdot = 1/m1 * (L_q1(state) + lambda1 * F1_q1(state) + lambda2 * F2_q1(state))
    
    q2_dotdot = 1/m2 * (L_q2(state) + lambda1 * F1_q2(state) + lambda2 * F2_q2(state))
    
    
    return (q1_dotdot, q2_dotdot)

def forward_euler_next(state, dt=dt):
    q1 = state.q1
    q1_dot = state.q1_dot
    
    
    q2 = state.q2
    q2_dot = state.q2_dot
    
    (q1_dotdot, q2_dotdot) = q_dotdot(state)
    
    q1_next = q1 + dt * q1_dot
    q2_next = q2 + dt * q2_dot
    
    q1_dot_next = q1_dot + dt * q1_dotdot
    q2_dot_next = q2_dot + dt * q2_dotdot
    
    
    q1_phase = q_phase(q1_next.x, q1_next.y, q1_dot_next.x, q1_dot_next.y)
    q2_phase = q_phase(q2_next.x, q2_next.y, q2_dot_next.x, q2_dot_next.y)
    
    return phase(q1_phase, q2_phase)
    


def midpoint_rule_next(state, dt=dt):
    
    midpoint = forward_euler_next(state, dt/2)
    
    
    
    
    q1 = state.q1
    q1_dot = state.q1_dot
    
    
    q2 = state.q2
    q2_dot = state.q2_dot
    
    (mid_q1_dotdot, mid_q2_dotdot) = q_dotdot(midpoint)
    
    q1_next = q1 + dt * midpoint.q1_dot
    q2_next = q2 + dt * midpoint.q2_dot
    
    q1_dot_next = q1_dot + dt * mid_q1_dotdot
    q2_dot_next = q2_dot + dt * mid_q2_dotdot
    
    
    q1_phase = q_phase(q1_next.x, q1_next.y, q1_dot_next.x, q1_dot_next.y)
    q2_phase = q_phase(q2_next.x, q2_next.y, q2_dot_next.x, q2_dot_next.y)
    
    return phase(q1_phase, q2_phase)





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
    initial1 = q_phase(0,1)
    initial2 = q_phase(1,1)
    initial_state = phase(initial1, initial2)

    states = run_dynamics(initial_state, N)

    q1 = [vector(s.q1.x, s.q1.y) for s in states]
    q2 = [vector(s.q2.x, s.q2.y) for s in states]
    O = [0*v for v in q1]
    
    renderer = MatPlotRenderer.matplotrenderer(dt=dt)
    
    
    renderer.animated_scatter_set([O, q1, q2])
    renderer.display()