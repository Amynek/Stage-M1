import numpy as np
import pandas as pd

# y : valeur exacte
# f : valeur prédite

def rsq(y, f):
  y = np.asarray(y)
  f = np.asarray(f)
  stot = np.sum((y-np.mean(y))**2)
  sres = np.sum((y-f)**2)
  return 1.0 - sres/stot

def rmse(y, f):
    y = np.asarray(y)
    f = np.asarray(f)
    return np.sqrt(np.mean((y-f)**2))

def mae(y,f):
    y = np.asarray(y)
    f = np.asarray(f)
    return np.mean(np.abs(y-f))

def mae_pondere(y, f, alpha=1.0):
    y = np.array(y)
    f = np.array(f)
    
    # Pondération : 1 / (|y| + alpha) — plus y est petit, plus le poids est grand
    poids = 1 / (np.abs(y) + alpha)
    poids_normalise = poids / np.sum(poids)
    
    erreur_absolue = np.abs(y - f)
    mae_pondere = np.sum(poids_normalise * erreur_absolue)
    
    return mae_pondere

def mae_intervalle(y_exact, y_obtenu, seuil=1):
    mask = np.abs(y_exact) < seuil
    if np.sum(mask) == 0:
        return np.nan
    
    mae_zero = np.mean(np.abs(y_exact[mask] - y_obtenu[mask]))
    return mae_zero

def mape(y,f):
    y = np.asarray(y)
    f = np.asarray(f)
    mape_value = np.mean(np.abs((y - f) / y)) * 100
    return mape_value

def erreur_rel(y,f):
    y = np.asarray(y)
    f = np.asarray(f)  
    return 100 * np.abs(f-y)/(np.abs(f) + 0.02 * np.ptp(y))
    
def erreur_abs(y,f):
    y = np.asarray(y)
    f = np.asarray(f)  
    return np.abs(f-y)

def max_rel(y,f):
    return erreur_rel(y,f).max()
def max_abs(y,f):
    return erreur_abs(y,f).max()

def mean_rel(y,f):
    return erreur_rel(y,f).mean()
def mean_abs(y,f):
    return erreur_abs(y,f).mean()



def print_metriques(y_true, dict_predictions):
    """
    y : array
        Les valeurs réelles (ex: E_mEh)
    dict_predictions : dict
        Dictionnaire au format {"Nom du modèle": y_pred}
    """
    
    # Définition des métriques à calculer
    metriques = {"R²": rsq, "RMSE": rmse, "MAE": mae, "MAE pondérée": mae_pondere,"MAE petites valeurs": mae_intervalle}
    
    # Calcul de la largeur maximale pour un alignement parfait des ":"
    longueur_max = max(len(f"{nom_metrique} ({nom_modele})") 
                       for nom_metrique in metriques 
                       for nom_modele in dict_predictions)

    # Affichage groupé par métrique
    for nom_metrique, fonction_metrique in metriques.items():
        for nom_modele, y_pred in dict_predictions.items():
            valeur = fonction_metrique(y_true, y_pred)
            
            # Construction et alignement de la ligne de texte
            prefixe = f"{nom_metrique} ({nom_modele})"
            print(f"{prefixe:<{longueur_max}} : {valeur:.12f}")
        print()  # Ligne vide de séparation entre les blocs de métriques

def calcul_metriques(y_true, dict_predictions):
    """
    Parameters
    ----------
    y_true : array-like
        Valeurs de référence.

    dict_predictions : dict
        Dictionnaire de la forme :
        {"Nom du modèle": y_pred}
    """

    metriques = {"R²": rsq,"RMSE": rmse,"MAE": mae,
                 "Relative Max (%)": max_rel, "Relative Moyenne (%)": mean_rel,
                 "Absolue Max": max_abs,  "Absolue Moyenne": mean_abs}

    data = {}

    for nom_modele, y_pred in dict_predictions.items():
        data[nom_modele] = {
            nom_metrique: fonction(y_true, y_pred)
            for nom_metrique, fonction in metriques.items()
        }

    return pd.DataFrame.from_dict(data, orient="index")