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

def multi_plot_interactif(model, list_params, fixed_vals, x, data, fixed_col, x_col, y_col, 
                          title="Graphique interactif", fixed_first=True, nom_courbe=None):
    
    fig = go.Figure()
    
    num_models = len(list_params)
    if nom_courbe is None:
        nom_courbe = [f"Modèle (Params {i+1})" for i in range(num_models)]

    val_initiale = fixed_vals[0]

    # 1. Courbes de modèles INITIALES (Arrière-plan)
    for j in range(num_models):
        params = list_params[j]
        
        if fixed_first:
            y_model = model(params, np.full_like(x, val_initiale), x)
        else:
            y_model = model(params, x, np.full_like(x, val_initiale))
            
        fig.add_trace(go.Scatter(x=x, y=y_model, 
                                 mode='lines', name=nom_courbe[j],
                                 visible=True))

    # 2. Points de données INITIALES (Premier plan)
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
            
        # B. Mise à jour des données réelles filtrées
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





