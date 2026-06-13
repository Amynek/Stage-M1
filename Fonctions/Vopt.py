import numpy as np
from   numpy.polynomial.legendre import legval
from   scipy.special             import eval_legendre

def f6_opt(x):
    y = 1.0 + x * (1.0 + x * (0.5 + x * (1.0/6.0 + x * (1.0/24.0 + x * (1.0/120.0 + x / 720.0)))))
    return 1.0 - np.exp(-x) * y

def f7_opt(x):
    y = 1.0 + x * (1.0 + x * (0.5 + x * (1.0/6.0 + x * (1.0/24.0 + x * (1.0/120.0 + x * (1.0/720.0 + x / 5040.0))))))
    return 1.0 - np.exp(-x) * y

def V_opt(p, R, Theta):
    R = np.asarray(R, dtype=float)
    # On calcule ces valeurs car utiles plusieurs fois
    cosTh = np.cos(np.deg2rad(np.asarray(Theta, dtype=float)))
    
    # Paramètres
    b  = p[0:6]                            # b0, b1, b2, b3, b4, b5
    c  = p[6:10]                           # c0, c1, c2, c3
    d  = p[10:16]                          # d0, d1, d2, d3, d4, d5
    g0 = np.asarray(p[16:22], dtype=float) # g00, g01, g02, g03, g04, g05
    g1 = np.asarray(p[22:28], dtype=float) # g10, g11, g12, g13, g14, g15
    g2 = np.asarray(p[28:34], dtype=float) # g20, g21, g22, g23, g24, g25
    g3 = np.asarray(p[34:40], dtype=float) # g30, g31, g32, g33, g34, g35
    
    # X(theta) ------------------------------------ #
    # --------------------------------------------- #
    X_b = legval(cosTh, b)
    X_d = legval(cosTh, d)
    
    X_bR = X_b * R
    abs_BR = np.abs(X_bR)
    # --------------------------------------------- #
    
    # G(R,theta) ---------------------------------- #
    # --------------------------------------------- #
    i = np.arange(6)
    g = g0[i, None] + R * (g1[i, None] + R * (g2[i, None] + R * g3[i, None]))
    Pl = np.array([eval_legendre(l, cosTh) for l in range(6)])
    # G = np.sum(g * Pl, axis=0)
    # ------------------------------------------- #
    
    # Short-Range
    exp_val = np.clip(X_d-X_bR,-200,200) # Bloquage des valeurs trop grandes/petites
    V_sh = np.sum(g * Pl, axis=0) * np.exp(exp_val)
    
    # Asymptotic
    inv_R = 1.0/R
    inv_R6 = inv_R * inv_R * inv_R * inv_R * inv_R * inv_R
    inv_R7 = inv_R6 * inv_R
    
    V_as = (f6_opt(abs_BR) * legval(cosTh,[c[0],0,c[2]]) * inv_R6
          + f7_opt(abs_BR) * legval(cosTh,[0,c[1],0,c[3]]) * inv_R7)
    
    V_total = V_sh + V_as
    
    # Pour ne pas renvoyer NaN en cas d'erreur
    V_total = np.nan_to_num(V_total, nan=1e100, posinf=1e100, neginf=-1e100)
    # Bloquage des valeurs trop grandes
    V_total = np.clip(V_total, -1e100, 1e100)
      
    return V_total # Energie renvoyée en mEh