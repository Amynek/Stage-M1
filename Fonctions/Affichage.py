import plotly.graph_objects as go
import numpy as np


def plot_interactif(model, params, fixed_vals, x, data, fixed_col, x_col,
                    y_col, title="Graphique interactif", fixed_first=True):

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

def contour_plot(ax, params, niveaux, niveaux_label, title):
    # Niveaux à plot
    niveaux = np.asarray(niveaux)
    # Niveaux avec un label
    niveaux_label = np.asarray(niveaux_label)
    
    # Axes
    theta_grid = np.linspace(0, 180, 250)
    r_grid = np.linspace(6, 10, 250)
    
    Theta_mesh, R_mesh = np.meshgrid(theta_grid, r_grid)
    
    # Calcul de Z
    Z = np.array([V_opt(params, np.full_like(theta_grid, r), theta_grid) for r in r_grid])
    
    # Niveaux intermédiaires
    niveaux_inter = []
    for i in range(len(niveaux) - 1):
        a, b = niveaux[i], niveaux[i + 1]
        inter = np.linspace(a, b, 6)
        niveaux_inter.extend(inter[1:-1])
    
    niveaux_inter = np.sort(np.unique(niveaux_inter))
    ax.contour(Theta_mesh, R_mesh, Z, levels=niveaux_inter, colors='gray', linewidths=0.7) # Contours gris
    
    # Contours principaux
    all_contours = []
    for level in niveaux:
        cp = ax.contour(Theta_mesh, R_mesh, Z,levels=[level],colors='black',linewidths=1.5,linestyles='--')
        all_contours.append(cp)
    
    # Labels
    for cp in all_contours:
        level = cp.levels[0]
        if np.isclose(niveaux_label, level).any():
            ax.clabel(cp, fmt='%.3f', fontsize=10, inline=True)

    # Affichage des Max et Min selon le R
    theta_values = np.arange(0,181,20)
    r_dense = np.linspace(6,10,300)
    
    for th_val in theta_values:
        energies = V_opt(params, r_dense, np.full_like(r_dense,th_val))

        # Minimum
        min_idx = np.argmin(energies)
        min_E = energies[min_idx]
        min_r = r_dense[min_idx]
        
        # Affichage du point
        ax.plot(th_val, min_r, marker='v', color='red', markersize=5)
        
        # Affichage de la valeur
        offset = -15 if th_val > 150 else 3 # Si on est proche du bord droit
        ax.text(th_val + offset, min_r, f"{min_E:.3f}", color='red', fontsize=9, verticalalignment='center')

    
    ax.set_title(f"He-HCN - Energie potentielle (mEh)\n{title}")
    ax.set_xlabel("Theta (°)")
    ax.set_ylabel("R")
    
    ax.set_yticks(np.arange(6, 10.5, 0.5))
    ax.set_xticks(np.arange(0, 181, 20))
    
    ax.grid(True, linestyle='--', alpha=0.3)

    legende_point = Line2D([0], [0], linestyle='None', marker='v', color='red', markersize=5, label="Energie min")
    ax.legend(handles=[legende_point],loc='upper right', fontsize=10, framealpha=0.9)