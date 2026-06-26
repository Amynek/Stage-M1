import numpy as np
from   numpy.polynomial.legendre import legval, legval2d
from   scipy.special             import eval_legendre

def f6_opt(x):
    y = 1.0 + x * (1.0 + x 
                * (0.5 + x 
                * (1.0/6.0 + x 
                * (1.0/24.0 + x 
                * (1.0/120.0 + x / 720.0)))))
    return 1.0 - np.exp(-x) * y

def f7_opt(x):
    y = 1.0 + x * (1.0 + x 
                * (0.5 + x 
                * (1.0/6.0 + x
                * (1.0/24.0 + x 
                * (1.0/120.0 + x 
                * (1.0/720.0 + x / 5040.0))))))
    return 1.0 - np.exp(-x) * y

    
def V_opt_vec(all_params, R, Theta):
    """
    all_params : ndarray (40,M)
    R          : ndarray (N,)
    Theta      : ndarray (N,)

    Retour :
        ndarray (M,N)
    """
    R      = np.asarray(R, dtype=float)
    cosTh  = np.cos(np.deg2rad(np.asarray(Theta, dtype=float)))

    all_params = np.asarray(all_params, dtype=float)
    
    if all_params.ndim == 1:
        all_params = all_params[:, None]   # (40,1)
        
    p = all_params.T      # (M,40)

    b  = p[:, 0:6]
    c  = p[:, 6:10]
    d  = p[:, 10:16]

    g0 = p[:, 16:22]
    g1 = p[:, 22:28]
    g2 = p[:, 28:34]
    g3 = p[:, 34:40]

    # ---------------------------------------------------------
    # Polynômes de Legendre
    # ---------------------------------------------------------

    Pl = eval_legendre(np.arange(6)[:, None], cosTh)  # (6,N)

    # ---------------------------------------------------------
    # X_b et X_d
    # ---------------------------------------------------------

    X_b = b @ Pl                                       # (M,N)
    X_d = d @ Pl                                       # (M,N)

    X_bR  = X_b * R[None, :]                           # (M,N)
    absBR = np.abs(X_bR)

    # ---------------------------------------------------------
    # G(R,theta)
    # ---------------------------------------------------------

    R1 = R[None, :]
    R2 = R1 * R1
    R3 = R2 * R1

    g = (
        g0[:, :, None]
        + g1[:, :, None] * R1
        + g2[:, :, None] * R2
        + g3[:, :, None] * R3
    )                                                  # (M,6,N)

    G = np.sum(g * Pl[None, :, :], axis=1)            # (M,N)

    # ---------------------------------------------------------
    # Short-range
    # ---------------------------------------------------------

    exp_val = np.clip(X_d - X_bR, -200, 200)

    V_sh = G * np.exp(exp_val)

    # ---------------------------------------------------------
    # Asymptotique
    # ---------------------------------------------------------

    P0 = np.ones_like(cosTh)
    P1 = cosTh
    P2 = 0.5 * (3.0 * cosTh**2 - 1.0)
    P3 = 0.5 * (5.0 * cosTh**3 - 3.0 * cosTh)

    C6 = c[:, 0, None] * P0 + c[:, 2, None] * P2
    C7 = c[:, 1, None] * P1 + c[:, 3, None] * P3

    inv_R  = 1.0 / R1
    inv_R6 = inv_R**6
    inv_R7 = inv_R6 * inv_R

    V_as = (
        f6_opt(absBR) * C6 * inv_R6
        + f7_opt(absBR) * C7 * inv_R7
    )

    # ---------------------------------------------------------
    # Total
    # ---------------------------------------------------------

    V = V_sh + V_as

    V = np.nan_to_num(
        V,
        nan=1e100,
        posinf=1e100,
        neginf=-1e100
    )

    return np.clip(V, -1e100, 1e100)