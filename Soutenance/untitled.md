# Contexte

Dans l'article ... de Toczylowski, un modèle physique permettant de calculer l'énergie potentielle pour un R et un Theta donné est présenté. Il est également précisé qu'il contient 40 paramètres à calculer selon les Atomes et Molécules données

Dans la thèse de Toczylowski, les paramètres qu'il donne pour Ar-HCN ne donnent pas des résultats satisfaisants. On cherche donc à savoir pourquoi et si on peut trouver des paramètres donnent de meilleurs résultats

# Implémentation et optimisation

## Récupération des données

Il a fallut numériser les tableaux contenant les données ab-initio en fichiers de données afin de s'en servir dans nos programmes.

## Etape 1 de l'implémentation : premier jet

Implémentation du modèle physique en python. On ne s'attarde pas trop sur l'efficacité de la fonction. Elle doit seulement etre utilisable et fonctionnelle dans un premier temps.

C'est une version scalaire. On entre un R et un Theta avec les 40 paramètres et on obtient une valeur d'énergie.

Cette première version est une version "scalaire" : ```V(vars,params)``` avec vars= (Theta,R).

La fonction est testée dans un premier temps avec la méthode ```curve_fit``` de scipy afin de récupérer un premier jeu de paramètres. 

Nos fonctions renverrons des valeur en mEh (peut varier en fonction des paramètres params)

## Etape 2 de l'implémentation : optimisation des performances

On s'interesse ensuite à l'optimisation de cette fonction. Utilisation de différents LLM comme GPT, Claude, Gemini pour trouver des pistes d'amélioration avec des prompts comme : "Comment améliorer les performances de cette fonction" etc.

Les points qui ont été améliorés :

 - Piste principale : Se débarrasser des boucles et utiliser la vectorisation numpy
 - Eviter de recalculer plusieurs fois certaines variables
 - Autre choix de fonctions à utiliser. Par exemple, utiliser ```legval``` de numpy au lieu de ```eval_legendre```

Par exemple, pour calculer $B(\theta)$ que l'on appelle ```X_b``` dans le programme, on a :

**Version scalaire**
```Python

def X(Theta,x):
  y = 0.
  for i in range(6):
    y = y + x[i]*eval_legendre(i,np.cos(Theta))
  return y

def V(vars,params):
    
    ...

    X_b = X(Theta_rad,b)

    ...
```

**Version optimisée**
```Python
def V_opt(p, R, Theta):
    
    ...
    
    X_b = legval(cosTh, b)

    ...
```

La nouvelle fonction optimisée que l'on nomme ```V_opt(p, R, Theta)``` utilise à son plein potentiel l'entrée au format ndarray de R et Theta. (suppression des boucles pour des calculs vectorisés)

**On effectue des tests afin de valider les fonctions et les améliorations :**

On verifie d'abord que les deux fonctions produisent les mêmes résultats numériques : on calcule pour 500 valeurs de R et Theta aléatoires entre 2 et 10 ainsi que 0 et 180 avec p choisi aléatoirement. On récupère la différence max, la différence moyenne et l'ecart type des résultats obtenus avec les deux fonctions et on s'assure que les différences sont suffisament faible pour considérer les fonctions identiques.
- max : 1.7881393432617188e-06
- mean diff 2 : 1.2202130886608412e-08
- std  diff 2 : 1.09020624706844e-07

On teste les performances en appelant 100 fois les fonctions sur 500 R et Theta :
- V scalaire  : 3.118732e-03 s en moyenne par appel
- V optimisée : 8.047275e-04 s en moyenne par appel

V_opt est en moyenne 3.9x plus rapide.

On teste ensuite sur la fonction ```least_squares``` pour avoir une référence en application "réelle" sur 50 appels différents où on fait varier les paramètres initiaux :

- V scalaire : moyenne = 12.652s ; écart-type = 4.914s
- V optimisée : moyenne = 5.759s ; écart-type = 1.929s

# Méthodes pour les fits

On utilise 3 fonctions pour résoudre notre problème d'optimisation

## curve_fit
Typiquement faite pour l'ajustement de courbes. On entre des données (x,y) et on cherche les paramètres d'une fonction modèle qui approchent le mieux les données. Méthode des moindres carrés non linéaires.

on peux chosir parmis plusieur algorithmes : 'trf', 'lm', 'dogbox'

=> Converge vers le minimum le plus proche des paramètres initiaux p0. CAD minimum local


## least_squares
Plus flexible que curve_fit. Minimisation de la somme des carrés d'une fonction résidus que l'on fixe. Elle est donc plus générale.

On a la possibilité de choisir des bornes pour les paramètres

=> Converge aussi vers le minimum le plus proche des paramètres initiaux p0. CAD minimum local

## differential_evolution
Algorithme d'optimisation global. Il est basé sur des populations de solutions candidates qui évoluent par mutation/croisement.

On détermine une fonction de coût que la méthode cherchera à minimiser.
Elle ne nécessite pas de point de départ.
Elle a la capacité d'échapper aux minimas locaux.
Elle est beaucoup plus lente que les fonctions précédente car elle explore tous l'espace de recherche.

# Paramètres de Toczylowski

On travaille sur la molécule HCN.
On s'interesse à ses intéractions avec 3 atomes particuliers : He, Ne et Ar 

Données ab-initio :
- He-HCN : 138 points
- Ne-HCN : 151 points
- Ar-HCN : 140 points

On utilise les paramètres donnés par Toczylowski dans sa thèse comme point de départ p0.

Pour la méthode curve_fit, on fait varier les arguments : sigma, jac et method

Pour least_squares, on fait varier seulement les argument x_scale et loss. On pose la fonction résidus simplement comme l'erreur absolue (difference entre ab-initio et prediction).

parmis tous les paramètres optimaux obtnus, une première selection est faite graphiquement en affichant des coupes de la surface de potentielle obtenue avec une valeur Theta ou R fixée.

Pour chaque atome on selectionne 2 jeux de paramètres et on les compares avec les metriques suivantes : 
- R² : sans unité, exprime la capacité du modele à expliquer la tendance globale
- RMSE : même unité que la cible, racine de l'erreur quadratique moyenne, met en valeur les erreurs importantes
- MAE : même unité que la cible, erreur absolue moyenne, met en valeur l'erreur moyenne du modèle


On conclu de cette partie qu'il est possible d'obtenir de meilleurs paramètres que ceux donnés par Toczylowski particulièrement pour l'atome d'Argon qui présentait des résultats moins satisfaisants.

# Paramètres Chinois



# HNC - Données de Rennes



# Réseaux de neurones



# Conclusion
