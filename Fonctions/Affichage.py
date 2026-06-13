import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt


def plot_interactif(model, params, fixed_vals, x, data, fixed_col, x_col,
                    y_col, title="Graphique interactif", fixed_first=True):
    """
    model       :  V_opt
    params      :  40 paramètres en argument de V_opt
    fixed_vals  :  ensemble des valeurs fixées
    x           :  variable en abscisse (si R est fixé, theta est en abscisse et inversement)
    data        :  jeu de données 
    fixed_col   :  nom de fixed_vals dans data
    x_col       :  nom de x dans data
    y_col       :  nom de la variable à afficher en ordonnée dans data
    title       :  titre du graphe
    fixed_first :  pour model(p,a,b), fixed_first=True => a variable fixée | fixed_first=False => b variable fixée
    """
    fig = go.Figure()

    for i, val in enumerate(fixed_vals):

        # ordre des variables
        if fixed_first:
            y_model = model(params, np.full_like(x, val), x)
        else:
            y_model = model(params, x, np.full_like(x, val))

        # données
        mask = np.isclose(data[fixed_col], val)

        x_data = data[x_col][mask]
        y_data = data[y_col][mask]

        order = np.argsort(x_data)
        
        visible = (i == 0)

        fig.add_trace(go.Scatter(x=x, y=y_model, mode='lines', name='Modèle', visible=visible))

        fig.add_trace(go.Scatter(x=x_data[order],y=y_data[order],mode='markers',name='Données',visible=visible))

    steps = []

    for i, val in enumerate(fixed_vals):

        vis = [False] * (2 * len(fixed_vals))

        vis[2*i] = True
        vis[2*i+1] = True

        steps.append(
            dict(
                method="update",
                args=[
                    {"visible": vis},
                    {"title": f"{fixed_col} = {val}"}
                ],
                label=str(val)
            )
        )

    fig.update_layout(
        title=title,
        sliders=[dict(steps=steps)],
        template="plotly_white",
        width=600,
        height=400,
        uirevision=True
    )

    fig.show()

############################################################################
############################################################################

def multi_plot_interactif(model, list_params, fixed_vals, x, data, fixed_col, x_col, y_col, 
                          title="Graphique interactif", fixed_first=True, nom_courbe=None):
    """
    model       :  V_opt
    list_params :  liste des paramètres qui seront comparés
    fixed_vals  :  ensemble des valeurs fixées
    x           :  variable en abscisse (si R est fixé, theta est en abscisse et inversement)
    data        :  jeu de données 
    fixed_col   :  nom de fixed_vals dans data
    x_col       :  nom de x dans data
    y_col       :  nom de la variable à afficher en ordonnée dans data
    title       :  titre du graphe
    fixed_first :  pour model(p,a,b), fixed_first=True => a variable fixée | fixed_first=False => b variable fixée
    nom_courbe  :  nom associé à chaque paramètre pour la légende
    """    
    
    fig = go.Figure()
    
    num_models = len(list_params)
    if nom_courbe is None:
        nom_courbe = [f"Modèle (Params {i+1})" for i in range(num_models)]

    val_initiale = fixed_vals[0]

    # 1. Courbes de modèles initiales
    for j in range(num_models):
        params = list_params[j]
        
        if fixed_first:
            y_model = model(params, np.full_like(x, val_initiale), x)
        else:
            y_model = model(params, x, np.full_like(x, val_initiale))
            
        fig.add_trace(go.Scatter(x=x, y=y_model, 
                                 mode='lines', name=nom_courbe[j],
                                 visible=True))

    # 2. Points de données initiales
    data_init = data[data[fixed_col] == val_initiale]
    x_data = np.asarray(data_init[x_col])
    y_data = np.asarray(data_init[y_col])
    order = np.argsort(x_data)
    
    fig.add_trace(go.Scatter(x=x_data[order], y=y_data[order], 
                             mode='markers', name='Données', 
                             visible=True,
                             marker=dict(size=8)))

    # 3. Etapes du Slider
    steps = []
    
    for val in fixed_vals:
        x_updates = []
        y_updates = []
        
        # A. Mise à jour des courbes de modèles
        for j in range(num_models):
            params = list_params[j]
            
            if fixed_first:
                y_model = model(params, np.full_like(x, val), x)
            else:
                y_model = model(params, x, np.full_like(x, val))
                
            x_updates.append(x.tolist())
            y_updates.append(y_model.tolist())
            
        # B. Mise à jour des données fournies filtrées
        data_filtree = data[data[fixed_col] == val]
        x_data_f = np.asarray(data_filtree[x_col])
        y_data_f = np.asarray(data_filtree[y_col])
        ordre_f = np.argsort(x_data_f)
        
        x_updates.append(x_data_f[ordre_f].tolist())
        y_updates.append(y_data_f[ordre_f].tolist())
        
        steps.append(dict(
            method="update",
            args=[
                {
                    "x": x_updates,
                    "y": y_updates
                },
                {"title": {"text": f"{title} - {fixed_col} = {val}"}}
            ],
            label=str(val)
        ))

    # 4. Layout
    fig.update_layout(
        title={"text": f"{title} - {fixed_col} = {val_initiale}"},
        sliders=[dict(
            active=0,
            steps=steps
        )],
        template="plotly_white",
        width=750, height=500,
        uirevision=True
    )

    fig.show()

##########################################################################################
##########################################################################################

def to_grid(R, T, E, R_unique, T_unique):
    """
    Création d'un tableau :
        | T1  T2  T3 ...
    ----|----------------------
     R1 | E11 ...
     R2 | ... ...
    """
    
    grid = np.empty((len(R_unique), len(T_unique)))

    for i, r in enumerate(R_unique):
        for j, t in enumerate(T_unique):
            mask = (R == r) & (T == t)
            grid[i, j] = E[mask][0]

    return grid

def plot_Theta_fix_zoom(Val_fixee, params, R_a0, Theta_deg, E,
                        V_opt, xlim=[6,15], ylim=[-1,1], data=True):
    """
    Val_fixee : entier (adresse du tableau des Theta : Theta[Val_fixee])
    params    : dict {"nom courbe": param_array}
    """
    Thet = np.unique(Theta_deg)
    R_unique = np.unique(R_a0)
    R_dense = np.linspace(np.min(R_unique),np.max(R_unique), 500)
    
    fig, ax = plt.subplots()

    ax.axhline(0, color='k', ls='--', lw=1)
    
    for nom, par in params.items():
        courbe = V_opt(par,R_dense, np.full_like(R_dense,Thet[Val_fixee]))
        ax.plot(R_dense, courbe, label=nom)   
    if data:
        E_chinois = to_grid(R_a0, Theta_deg, E, R_unique, Thet)
        ax.plot(R_unique,E_chinois[:,Val_fixee],"o", mec="1.0",color='r', ms=4, lw=1, label="Données ab initio")
    ax.set_ylim(ylim[0],ylim[1])
    ax.set_xlim(xlim[0],xlim[1])
    ax.set_yticks(np.linspace(ylim[0], ylim[1], 10))

    ax.legend()
    ax.grid(alpha=0.3)

    plt.title(f"Energie potentielle en fonction de R pour Theta={Thet[Val_fixee]:.0f}°")
    plt.xlabel("R (bohr)")
    plt.ylabel("Energie potentielle (mEh)")
    
    plt.tight_layout()
    plt.show()

def plot_Theta_fix_zoom_cmm1(Val_fixee, params, R_a0, Theta_deg, E,
                             V_opt, xlim=[0,25], ylim=[-5,500], data=True):
    """
    Val_fixee : entier de 0 à 18
    params    : dict {"nom courbe": param_array}
    """
    Thet = np.linspace(0,180,19)
    R_unique = np.unique(R_a0)
    R_dense = np.linspace(np.min(R_unique),np.max(R_unique), 500)

    R_dense_A = R_dense * 1/1.889726125
    R_unique_A = R_unique * 1/1.889726125
    
    fig, ax = plt.subplots()

    ax.axhline(0, color='k', ls='--', lw=1)
    
    for nom, par in params.items():
        courbe = V_opt(par,R_dense, np.full_like(R_dense,Thet[Val_fixee])) * 219474.6313705 / 1000.0
        ax.plot(R_dense_A, courbe, label=nom)   

    if data:
        E_chinois = to_grid(R_a0, Theta_deg, E, R_unique, Thet)    
        ax.plot(R_unique_A,E_chinois[:,Val_fixee],"o", mec="1.0",color='r', ms=4, lw=1, label="Données ab initio")
    ax.set_ylim(ylim[0],ylim[1])
    ax.set_xlim(xlim[0],xlim[1])

    ax.legend()
    ax.grid(alpha=0.3)

    plt.title(f"Energie potentielle en fonction de R pour Theta={Thet[Val_fixee]:.0f}°")
    plt.xlabel(r"R ($\AA$)")
    plt.ylabel(r"Energie potentielle ($cm^{-1}$)")
    
    plt.tight_layout()
    plt.show()

##########################################################################################
##########################################################################################

def plot_R_fix(Val_fixee, params, R_a0, Theta_deg, E, V_opt):
    """
    Val_fixee : entier de 0 à len(R_unique)-1
    params    : dict {"nom courbe": param_array}
    """
    Thet = np.linspace(0,180,19)
    Thet_dense = np.linspace(0, 180, 500)
    R_unique = np.unique(R_a0)
    R_dense = np.linspace(np.min(R_unique),np.max(R_unique), 500)

    fig, ax = plt.subplots()
    for nom, par in params.items():
        courbe = V_opt(par,np.full_like(Thet_dense,R_unique[Val_fixee]), Thet_dense)
        ax.plot(Thet_dense, courbe, label=nom)   

    
    E_chinois = to_grid(R_a0, Theta_deg, E, R_unique, Thet)   
    ax.plot(Thet,E_chinois[Val_fixee,:],"o", 
                mec="1.0",color='r', ms=4, lw=1, label="Données ab initio")

    ax.legend()
    ax.grid(alpha=0.3)

    plt.title(f"Energie potentielle en fonction de Theta pour R={R_unique[Val_fixee]:.4f} bohr")
    plt.xlabel("Theta en °")
    plt.xticks(Thet, rotation=45)
    plt.ylabel("Energie potentielle (mEh)")
    
    plt.tight_layout()
    plt.show()

def plot_R_fix_cmm1(Val_fixee, params, R_a0, Theta_deg, E, V_opt):
    """
    Val_fixee : entier de 0 à len(R_unique)-1
    params    : dict {"nom courbe": param_array}
    """
    Thet = np.linspace(0,180,19)
    Thet_dense = np.linspace(0, 180, 500)
    R_unique = np.unique(R_a0)
    R_dense = np.linspace(np.min(R_unique),np.max(R_unique), 500)
    E_chinois = to_grid(R_a0, Theta_deg, E, R_unique, Thet)

    fig, ax = plt.subplots()
    for nom, par in params.items():
        courbe = V_opt(par,np.full_like(Thet_dense,R_unique[Val_fixee]), Thet_dense) * 219474.6313705 / 1000.0
        ax.plot(Thet_dense, courbe, label=nom)   

    ax.plot(Thet,E_chinois[Val_fixee,:],"o", 
            mec="1.0",color='r', ms=4, lw=1, label="Données ab initio")

    ax.legend()
    ax.grid(alpha=0.3)

    R_ang = R_unique[Val_fixee] * 1/1.889726125
    
    plt.title(f"Energie potentielle en fonction de Theta pour R={R_ang:.4f} bohr")
    plt.xlabel("Theta en °")
    plt.xticks(Thet, rotation=45)
    plt.ylabel(r"Energie potentielle ($cm^{-1}$)")
    
    plt.tight_layout()
    plt.show()

############################################################################################################################
############################################################################################################################

def erreur_rel_Theta_fix(theta_fix, Theta_deg, R_a0, E, params, V_opt):
    """
    theta_fix : valeur de theta fixée
    Theta_deg : valeurs de theta possible
    R_a0      : valeurs de R
    E         : energie ab initio en cm-1
    params    : dict {"nom courbe": param_array}
    """
    i_theta = np.argmin(np.abs(Theta_deg - theta_fix))

    Thet = np.unique(Theta_deg)
    R_unique = np.unique(R_a0)
    E_grid = to_grid(R_a0, Theta_deg, E, R_unique, Thet)

    
    fig, ax = plt.subplots()

    for nom, p in params.items():

        V_fit = V_opt(p, R_a0, Theta_deg) * 219474.6313705 / 1000.0
        V_grid = to_grid(R_a0, Theta_deg, V_fit, R_unique, Thet)
        erreur = 100 * np.abs(V_grid[:, i_theta] - E_grid[:, i_theta]) / np.abs(E_grid[:, i_theta])

        ax.plot(R_unique * 0.529177210903, erreur, label=nom) # Affichage en Angstrom

    plt.xlabel(r"R ($\AA$)")
    plt.ylabel("Erreur relative (%)")
    plt.title(f"Erreur relative pour θ = {Theta_deg[i_theta]:.0f}°")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def erreur_abs_Theta_fix(theta_fix, Theta_deg, R_a0, E, params, V_opt):
    """
    theta_fix : valeur de theta fixée
    Theta_deg : valeurs de theta possible
    R_a0      : valeurs de R
    E         : energie ab initio en cm-1
    params    : dict {"nom courbe": param_array}
    """
    i_theta = np.argmin(np.abs(Theta_deg - theta_fix))

    Thet = np.unique(Theta_deg)
    R_unique = np.unique(R_a0)
    E_grid = to_grid(R_a0, Theta_deg, E, R_unique, Thet)

    
    fig, ax = plt.subplots()

    for nom, p in params.items():

        V_fit = V_opt(p, R_a0, Theta_deg) * 219474.6313705 / 1000.0
        V_grid = to_grid(R_a0, Theta_deg, V_fit, R_unique, Thet)
        erreur = 100 * np.abs(V_grid[:, i_theta] - E_grid[:, i_theta])

        ax.plot(R_unique * 0.529177210903, erreur, label=nom) # Affichage en Angstrom

    plt.xlabel(r"R ($\AA$)")
    plt.ylabel("Erreur absolue ($cm^{-1}$)")
    plt.title(f"Erreur absolue pour θ = {Theta_deg[i_theta]:.0f}°")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


def erreur_rel_contour(Theta_deg, R_a0, E, params, V_opt):
    """
    theta_fix : valeur de theta fixée
    Theta_deg : valeurs de theta possible
    R_a0      : valeurs de R
    E         : energie ab initio en cm-1
    params    : dict {"nom courbe": param_array}
    """
    Thet = np.unique(Theta_deg)
    R_unique = np.unique(R_a0)
    E_grid = to_grid(R_a0, Theta_deg, E, R_unique, Thet)

    
    fig, ax = plt.subplots()

    (nom, p), = params.items()
    V_fit = V_opt(p, R_a0, Theta_deg) * 219474.6313705 / 1000.0
    V_grid = to_grid(R_a0, Theta_deg, V_fit, R_unique, Thet)
    erreur = 100 * np.abs(V_grid - E_grid) / np.abs(E_grid)

    c = ax.contourf(Thet, R_unique * 0.529177210903, erreur, levels=50, cmap="coolwarm")
    plt.colorbar(c, ax=ax, label="Erreur")

    ax.set_xlabel("Theta (deg)")
    ax.set_ylabel(r"R ($\AA$)")

    plt.title(f"Erreur relative pour les paramètres optimaux = {nom}")
    plt.tight_layout()
    plt.show()
