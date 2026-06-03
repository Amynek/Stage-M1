import numpy as np


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

def print_metriques(y_true, dict_predictions):
    """
    y : array-like
        Les valeurs réelles (ex: E_mEh)
    dict_predictions : dict
        Dictionnaire au format {"Nom du modèle": y_predise}
    """
    
    # Définition des métriques à calculer
    metriques = {"R²": rsq, "RMSE": rmse, "MAE": mae}
    
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
            print(f"{prefixe:<{longueur_max}} : {valeur}")
        print()  # Ligne vide de séparation entre les blocs de métriques