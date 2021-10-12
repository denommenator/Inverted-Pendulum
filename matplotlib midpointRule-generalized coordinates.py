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

import numpy as np
import numpy.linalg as LA
import scipy

import matplotlib.pyplot as plt
import matplotlib.animation as animation



#constants
m_ball = 1
m_cart = 10
g = 10
r = 2


#time step


dt = 1/60
total_time = 10
N = int(total_time / dt )


class phase:
    def __init__(self, x=0, theta=0, x_dot=0, theta_dot=0):
        self.x=x
        self.theta=theta
        self.x_dot=x_dot
        self.theta_dot=theta_dot
        
    def get_phase(self):
        return(self.x, self.theta, self.x_dot, self.theta_dot)

        
#initial position and momentum   
initial_state = phase(0, math.pi / 2 - .25 * math.pi, 0, 0)
equilibrium_state = phase(-5, math.pi / 2, 0, 0)




A = np.array([[0,0,1,0],
                [0,0,0,1],
                [0,m_ball/m_cart*g,0,0],
                [0,(m_ball+m_cart)/(r*m_cart)*g,0,0]])
    

B = np.array([[0],[0],[1/m_cart],[1/(r*m_cart)]])



Q = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

R=np.array([[10]])


def oscillating_force(t):
    omega = 10 * 2 * math.pi 
    print(t//1)
    if t//1 < 2 :
        return 2
    
    elif t//1 % 8  in {2,3,4,5}:
        return -2
    return 2



def lqr(A,B,Q,R):
    """Solve the continuous time lqr controller.
     
    dx/dt = A x + B u
     
    cost = integral x.T*Q*x + u.T*R*u
    """
    #ref Bertsekas, p.151
     
    #first, try to solve the ricatti equation
    X = np.matrix(scipy.linalg.solve_continuous_are(A, B, Q, R))
     
    #compute the LQR gain
    K = np.matrix(scipy.linalg.inv(R)*(B.T*X))
     
    eigVals, eigVecs = scipy.linalg.eig(A-B*K)
     
    return K, X, eigVals



def pole_place(Lambda):
    

    V = [0,0,0,0]
    for (i, v_i) in enumerate(V):
        V[i] = LA.solve(A - Lambda[i] * np.identity(4), B)
    


    V = np.column_stack(V)

    K = np.array([[1,1,1,1]])@LA.inv(V)
    return [K[0,i] for i in range(4)]


def correcting_force(state, equilibrium_state):
    l = -1.5
    Lambda = [1.1*l, 1.2*l, 1.3*l, 1.4*l]
    
    
    
    K = [ -3.16227766, 315.50629037, -11.8310435 , 139.4518508 ] #quick angle
    #K = [-31.6227766 , 702.97718422, -68.92254352, 309.88945702] #quick x
    #K = [ -0.31622777, 243.86990749,  -2.92688851, 104.49452965] #efficient
    
    
    [k_x, k_theta, k_x_dot, k_theta_dot] = K
        
        
        
    #wrote a pole placement function called get_K
    #[k_x, k_theta, k_x_dot, k_theta_dot] = pole_place(Lambda)
    
    e_x = k_x * (state.x - equilibrium_state.x)
    e_theta = k_theta * (state.theta - equilibrium_state.theta)
    e_x_dot = k_x_dot * (state.x_dot - equilibrium_state.x_dot)
    e_theta_dot = k_theta_dot * (state.theta_dot - equilibrium_state.theta_dot)
    
    return e_x + e_theta + e_x_dot + e_theta_dot


def e(state, t=0):
    #return 0
    return  - correcting_force(state, equilibrium_state)


def get_acceleration_ball(state, t=0):
    (x, theta, x_dot, theta_dot) = state.get_phase()
    
    theta_dot_dot =  \
    (m_ball * r**2 - (m_ball+m_cart)** -1 * m_ball**2 * r**2 * sin(theta)**2) ** -1 \
        * \
        (-m_ball * r * g * cos(theta) + \
         (m_ball+m_cart)** -1 * m_ball ** 2 * r**2 * sin(theta)*cos(theta)*theta_dot **2 \
            +  (m_ball+m_cart)** -1 * m_ball * r * sin(theta) * e(state, t))
    
    
    return theta_dot_dot

    
def get_acceleration_cart(state, t=0):
    (x, theta, x_dot, theta_dot) = state.get_phase()
    theta_dot_dot = get_acceleration_ball(state, t)
    
    x_dot_dot = (m_ball+m_cart)** -1 * (m_ball * r * \
                                        (cos(theta)*theta_dot**2+sin(theta)*theta_dot_dot) \
                                        + e(state, t))
    
    
    return x_dot_dot

def forward_euler_next(state, dt = dt, t=0):
    x_next = state.x + dt * state.x_dot
    x_dot_next = state.x_dot + dt * get_acceleration_cart(state, t=t)
    
    theta_next = state.theta + dt * state.theta_dot
    theta_dot_next = state.theta_dot + dt * get_acceleration_ball(state, t=t)
    
    return phase(x_next, theta_next, x_dot_next, theta_dot_next)


def midpoint_rule_next(state, dt=dt, t=0):
    
    midpoint = forward_euler_next(state, dt/2, t=t)
    
    
    
    x_next = state.x + dt * midpoint.x_dot
    x_dot_next = state.x_dot + dt * get_acceleration_cart(midpoint, t=t+dt/2)
    
    theta_next = state.theta + dt * midpoint.theta_dot
    theta_dot_next = state.theta_dot + dt * get_acceleration_ball(midpoint, t=t+dt/2)
    
    return phase(x_next, theta_next, x_dot_next, theta_dot_next)
    

def run_dynamics(initial_state, N):
    
    states = [initial_state]
    t=0+dt
    for i in range(1, N):
        next_state = forward_euler_next(states[-1], t=t)
        states.append(next_state)
        t += dt
        
    return states



states = run_dynamics(initial_state, N)

q_cart = [vector(s.x, 0) for s in states]
q_ball = [vector(s.x, 0) + r * vector(math.cos(s.theta) , math.sin(s.theta)) for s in states]

items_to_plot = [q_cart, q_ball]








fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-10, 30), ylim=(-2, 3))
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)



def animate(i):
    thisx = [items_to_plot[0][i].x, items_to_plot[1][i].x]
    thisy = [items_to_plot[0][i].y, items_to_plot[1][i].y]

    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*dt))
    return line, time_text


ani = animation.FuncAnimation(
    fig, animate, len(items_to_plot[0]), interval=dt*1000, blit=True)
plt.show()

