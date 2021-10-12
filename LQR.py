#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 09:20:28 2020

@author: robertdenomme
"""

#from __future__ import division, print_function
 
import numpy as np
import scipy.linalg
 
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
 
def dlqr(A,B,Q,R):
    """Solve the discrete time lqr controller.
     
    x[k+1] = A x[k] + B u[k]
     
    cost = sum x[k].T*Q*x[k] + u[k].T*R*u[k]
    """
    #ref Bertsekas, p.151
     
    #first, try to solve the ricatti equation
    X = np.matrix(scipy.linalg.solve_discrete_are(A, B, Q, R))
     
    #compute the LQR gain
    K = np.matrix(scipy.linalg.inv(B.T*X*B+R)*(B.T*X*A))
     
    eigVals, eigVecs = scipy.linalg.eig(A-B*K)
     
    return K, X, eigVals



m_ball = 1
m_cart = 10
g = 10
r = 2

A = np.array([[0,0,1,0],
                [0,0,0,1],
                [0,m_ball/m_cart*g,0,0],
                [0,(m_ball+m_cart)/(r*m_cart)*g,0,0]])
    

B = np.array([[0],[0],[1/m_cart],[1/(r*m_cart)]])


Q = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

R=np.array([[10]])

print(lqr(A,B,Q,R))