import numpy as np
import math

from scipy.special import eval_legendre,factorial

def G(R,Theta,g0,g1,g2,g3):
    g = 0.
    for i in range(6):
        g = g + (g0[i]+g1[i]*R+g2[i]*R*R+g3[i]*R*R*R)*eval_legendre(i,math.cos(Theta))
    return g


def X(Theta,x):
    y = 0.
    for i in range(6):
        y = y + x[i]*eval_legendre(i,math.cos(Theta))
    return y


def f(n,x):
    y = 0.
    for k in range(n+1):
        y = y + (x**k)/factorial(k)
    y = 1. - math.exp(-x)*y
    return y


def V(vars, params):

    R, Theta = vars

    # Conversion des degrés en radian
    Theta_rad = math.radians(Theta)

    #  Récupération des paramètres
    b  = params[0:6]    # b0, b1, b2, b3, b4, b5
    c  = params[6:10]   # c0, c1, c2, c3
    d  = params[10:16]  # d0, d1, d2, d3, d4, d5
    g0 = params[16:22]  # g00, g01, g02, g03, g04, g05
    g1 = params[22:28]  # g10, g11, g12, g13, g14, g15
    g2 = params[28:34]  # g20, g21, g22, g23, g24, g25
    g3 = params[34:40]  # g30, g31, g32, g33, g34, g35
        
    # Variables utiles
    abs_BR = math.fabs(X(Theta_rad,b)*R)
    cosTh = math.cos(Theta_rad)
        
    # Short-Range
    V_sh = G(R,Theta_rad,g0,g1,g2,g3) * math.exp(X(Theta_rad,d)-X(Theta_rad,b)*R)
        
    # Asymptotyhic
    V_as = f(6,abs_BR) * (c[0]*eval_legendre(0,cosTh)+c[2]*eval_legendre(2,cosTh))/(R**6)\
    + f(7,abs_BR) * (c[1]*eval_legendre(1,cosTh)+c[3]*eval_legendre(3,cosTh))/(R**7)
        
    return V_sh + V_as