import torch

def f6_torch(x):
    y = (1. + x * (1. + x * (0.5 + x * (1./6. + x * (1./24. + x * (1./120. + x/720.))))))
    return 1. - torch.exp(-x) * y


def f7_torch(x):
    y = (1 + x * (1 + x * (0.5 + x * (1/6 + x * (1/24 + x * (1/120 + x * (1/720 + x/5040)))))))
    return 1 - torch.exp(-x)*y

def legendre_matrix(x):
    P0 = torch.ones_like(x)
    P1 = x
    P2 = (3*x**2 - 1)/2
    P3 = (5*x**3 - 3*x)/2
    P4 = (35*x**4 - 30*x**2 + 3)/8
    P5 = (63*x**5 - 70*x**3 + 15*x)/8

    return torch.stack([P0, P1, P2, P3, P4, P5], dim=0)

def V_torch(p, R, Theta):

    cosTh = torch.cos(torch.deg2rad(Theta))

    b  = p[0:6]
    c  = p[6:10]
    d  = p[10:16]

    g0 = p[16:22]
    g1 = p[22:28]
    g2 = p[28:34]
    g3 = p[34:40]

    Pl = legendre_matrix(cosTh)

    X_b = torch.sum(b[:,None] * Pl, dim=0)
    X_d = torch.sum(d[:,None] * Pl, dim=0)

    X_bR = X_b * R

    g = (g0[:,None] + R*(g1[:,None] + R*(g2[:,None] + R*g3[:,None])))

    exp_val = torch.clamp(X_d - X_bR, min=-200, max=200)

    V_sh = torch.sum(g * Pl, dim=0) * torch.exp(exp_val)

    inv_R = 1.0 / R
    inv_R6 = inv_R**6
    inv_R7 = inv_R**7

    P0 = Pl[0]
    P1 = Pl[1]
    P2 = Pl[2]
    P3 = Pl[3]

    C6 = c[0]*P0 + c[2]*P2
    C7 = c[1]*P1 + c[3]*P3

    abs_BR = torch.abs(X_bR)

    V_as = (f6_torch(abs_BR) * C6 * inv_R6 + f7_torch(abs_BR) * C7 * inv_R7)

    return V_sh + V_as
