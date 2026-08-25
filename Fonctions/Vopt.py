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
    """
    p     : vecteur de taille 40
    R     : vecteur de taille N
    Theta : vecteur de taille N
    """
    
    R = np.asarray(R, dtype=float)
    # On calcule ces valeurs car utiles plusieurs fois
    cosTh = np.cos(np.deg2rad(np.asarray(Theta, dtype=float)))
    
    # Paramètres
    b  = p[0:6]                                  # b0, b1, b2, b3, b4, b5
    c  = p[6:10]                                 # c0, c1, c2, c3
    d  = p[10:16]                                # d0, d1, d2, d3, d4, d5
    g0 = np.asarray(p[16:22], dtype=float)       # g00, g01, g02, g03, g04, g05
    g1 = np.asarray(p[22:28], dtype=float)       # g10, g11, g12, g13, g14, g15
    g2 = np.asarray(p[28:34], dtype=float)       # g20, g21, g22, g23, g24, g25
    g3 = np.asarray(p[34:40], dtype=float)       # g30, g31, g32, g33, g34, g35
    
    # ----------------- X(theta) ------------------ #
    # --------------------------------------------- #
    X_b = legval(cosTh, b)                          # ndarray -> shape (N,)
    X_d = legval(cosTh, d)                          # ndarray -> shape (N,)
    
    X_bR = X_b * R                                  # ndarray -> shape (N,)
    abs_BR = np.abs(X_bR)                           # ndarray -> shape (N,)
    # --------------------------------------------- #

    
    # ----------------- G(R,theta) ---------------- #
    # --------------------------------------------- #               
    
    # Pl : ndarray -> shape (6,N)
    Pl = eval_legendre(np.arange(6)[:,None],cosTh)
    
    # g : ndarray -> shape (6,1)
    g = g0[:, None] + R * (g1[:, None] + R * (g2[:, None] + R *  g3[:, None]))  
    
    # mult = g * Pl  -> g[i,0] * Pl[i,x]  (x=0,..N-1 ; i=0,..5)
    # mult : ndarray -> shape (6,N)
    #
    # G = np.sum(mult, axis=0) -> axis=0 : pour chaque colonne x, 
    #                             on somme tous les éléments entre eux
    # G : ndarray -> shape (N,)
    # --------------------------------------------- #


    
    # ---------------- Short-Range ---------------- #
    
    exp_val = np.clip(X_d-X_bR,-200,200)            # Bloquage des valeurs 
                                                    # trop petites/grandes
                                                    
                                                    # V_sh = G * exp(...)
    V_sh = np.sum(g * Pl, axis=0) * np.exp(exp_val) # ndarray -> shape (N,)

    # --------------------------------------------- #
    
    # ---------------- Asymptotic ----------------- #
    inv_R = 1.0/R
    inv_R6 = inv_R * inv_R * inv_R * inv_R * inv_R * inv_R
    inv_R7 = inv_R6 * inv_R
    
    V_as = (f6_opt(abs_BR) * legval(cosTh,[c[0],0,c[2]]) * inv_R6
          + f7_opt(abs_BR) * legval(cosTh,[0,c[1],0,c[3]]) * inv_R7)

    # --------------------------------------------- #
    
    V_total = V_sh + V_as # ndarray -> shape (N,)
    
    # Pour ne pas renvoyer NaN en cas d'erreur
    V_total = np.nan_to_num(V_total, nan=1e100, posinf=1e100, neginf=-1e100)
    # Bloquage des valeurs trop grandes
    V_total = np.clip(V_total, -1e100, 1e100)
      
    return V_total # Energie renvoyée en mEh (selon les parametres p donnés)

def V_opt_de(p, R, Theta):
    """
    VERSION ADAPTEE POUR OPTIMISATION

    p : vecteur (40,)
        p[6:10] = u  (log-params)
        c = -10^u
    """

    R = np.asarray(R, dtype=float)
    cosTh = np.cos(np.deg2rad(np.asarray(Theta, dtype=float)))

    # ----------------- paramètres ----------------- #
    b  = p[0:6]
    u  = p[6:10]          # transformation
    d  = p[10:16]

    g0 = np.asarray(p[16:22], dtype=float)
    g1 = np.asarray(p[22:28], dtype=float)
    g2 = np.asarray(p[28:34], dtype=float)
    g3 = np.asarray(p[34:40], dtype=float)

    # reconstruction physique
    c = -10.0 ** u

    # ----------------- X(theta) ------------------ #
    X_b = legval(cosTh, b)
    X_d = legval(cosTh, d)

    X_bR = X_b * R
    abs_BR = np.abs(X_bR)

    # ----------------- Legendre ------------------ #
    Pl = eval_legendre(np.arange(6)[:, None], cosTh)

    # ----------------- short-range ---------------- #
    g = g0[:, None] + R * (g1[:, None] + R * (g2[:, None] + R * g3[:, None]))

    exp_val = np.clip(X_d - X_bR, -200, 200)

    V_sh = np.sum(g * Pl, axis=0) * np.exp(exp_val)

    # ----------------- asymptotique --------------- #
    inv_R = 1.0 / R
    inv_R6 = inv_R**6
    inv_R7 = inv_R6 * inv_R

    C6 = c[0] * (1.0) + c[2] * (0.5 * (3*cosTh**2 - 1))
    C7 = c[1] * (cosTh) + c[3] * (0.5 * (5*cosTh**3 - 3*cosTh))

    V_as = (
        f6_opt(abs_BR) * C6 * inv_R6 +
        f7_opt(abs_BR) * C7 * inv_R7
    )

    # ----------------- total ---------------------- #
    V_total = V_sh + V_as

    return np.nan_to_num(
        V_total,
        nan=1e100,
        posinf=1e100,
        neginf=-1e100
    )

# Fonction qui converti les paramètres obtenus via V_opt_de en paramètres compatibles avec V_opt
def de_to_opt(p_de):
    p = p_de.copy()
    p[6:10] = -10.0 ** p_de[6:10]   # u → c
    return p

# Fonction qui converti les paramètres obtenus via V_opt en paramètres compatibles avec V_opt_de
def opt_to_de(p_opt):
    p = p_opt.copy().astype(float)
    c = p_opt[6:10]
    # c doit être négatif pour que log10(-c) soit défini
    if np.any(c >= 0):
        raise ValueError(f"c doit être négatif, got {c}")
    p[6:10] = np.log10(-c)   # c → u
    return p