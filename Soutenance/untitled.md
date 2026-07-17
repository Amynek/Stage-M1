# Contexte

On s'interesse à un système composé d'un atome A et d'une molécule B linéaire de longueure fixe.
La structure et dynamique moléculaire sont décrites par la mécanique quantique. De ce fait le système est décrit par une fonction d'onde qui est solution de l'équation de Schrödinger $\Psi(\vec{r}, \vec{\rho})$ 


- Le système est décrit par une fonction d’onde $\Psi(\vec{r}, \vec{\rho})$, qui est une solution de l’équation de Schrödinger.
    - $\vec{r}$ est la position du centre de masse de A par rapport au centre de masse de B
    - $\vec{\rho}$ sont les coordonnées internes de A et B (électrons, ...)

- Approximation de Born-Oppenheimer :
    - masse de l’électron $\ll$ masse du proton
    - les électrons réagissent presque instantanément à de faibles variations des positions nucléaires
    - la fonction d’onde s’écrit comme le produit d’une fonction décrivant le mouvement relatif et d’une autre représentant le mouvement électronique, qui dépend paramétriquement de $\vec{r}$:

        $\Psi(\vec{r}, \vec{\rho}) = F(\vec{r})\chi(\vec{\rho}; \vec{r})$

    - Algorithme :
        - fixer les positions nucléaires $\vec{r}$ et résoudre l'équation de Schrödinger électronique correspondant pour retrouver $\chi(\vec{\rho}; \vec{r})$
        -  faire varier la géométrie nucléaire => l’énergie électronique en fonction de la géométrie nucléaire, appelé surface d’énergie potentielle (PES).
        - résoudre l'équation pour le mouvement nucléaire pour obtenir $F(\vec{r})$

- La PES est obtenue à l'aide de techniques de chimie quantique et de programmes informatiques associés
    - les calculs sont coûteux et sont effectués pour un (petit) ensemble de géométries nucléaires
    - Les points de données ab initio ainsi obtenus sont généralement ajustés à un modèle analytique qui sert à interpoler la fonction potentielle d'énergie (PES) pour d'autres géométries


Voici une proposition condensée pour tenir sur **une seule slide**, en gardant l'essentiel et en évitant la surcharge de texte (le jury a juste besoin du contexte, pas d'un cours) :

Titre : Contexte théorique — surfaces d'énergie potentielle (PES)

**Système étudié**
Atome A + molécule linéaire rigide B, décrits par une fonction d'onde $\Psi(\vec{r},\vec{\rho})$ solution de l'équation de Schrödinger ($\vec{r}$ : position relative A–B ; $\vec{\rho}$ : coordonnées internes/électroniques).

**Approximation de Born-Oppenheimer**
Les électrons étant beaucoup plus légers que les noyaux, on sépare les mouvements :
$$\Psi(\vec{r},\vec{\rho}) = F(\vec{r})\,\chi(\vec{\rho};\vec{r})$$
→ à géométrie nucléaire $\vec{r}$ fixée, on résout le problème électronique ; en faisant varier $\vec{r}$, on obtient l'énergie électronique comme fonction de la géométrie : **la PES**.

**De l'ab initio au modèle analytique**
- Calculs de chimie quantique coûteux → un nombre limité de points $(\vec{r}, E)$
- **Ajustement (fit)** de ces points à une fonction analytique → PES continue, exploitable pour toute géométrie (dynamique, spectroscopie, etc.)
___

**Sujet du stage :**

On s'interesse à l'article : _Theoretical study of the He–HCN, Ne–HCN, Ar–HCN,
and Kr–HCN complexes_ écrit par Toczyłowski, Doloresco et Cybulski en 2000.
On y retrouve des tableaux de données ab-initio pour les systèmes présents dans le titre. Ainsi qu'un modèle physique permettant de calculer l'énergie potentielle pour un R et un Theta donné. Il est également précisé qu'il contient 40 paramètres à calculer selon le système étudié.

Dans un article ultérieur Toczylowski, donne pour chacun de ces sytèmes un jeu de paramètres pour calculer les Energies potentielles. Il se trouve que ces paramètres n'apportent pas des résultats satisfaisants particulièrement pour le système avec l'atome d'Argon.

La première étape de ce stage est donc de déterminer s'il est possible de calculer de "meilleurs" paramètres à partir des données ab-initio présentes dans l'article 

les paramètres qu'il donne pour Ar-HCN ne donnent pas des résultats satisfaisants. On cherche donc à savoir pourquoi et si on peut trouver des paramètres donnent de meilleurs résultats

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

parmis tous les paramètres optimaux obtenus, une première selection est faite graphiquement en affichant des coupes de la surface de potentielle obtenue avec une valeur Theta ou R fixée.

Pour chaque atome on selectionne 2 jeux de paramètres et on les compares avec les metriques suivantes : 
- R² : sans unité, exprime la capacité du modele à expliquer la tendance globale



- RMSE : même unité que la cible, racine de l'erreur quadratique moyenne, met en valeur les erreurs importantes
- MAE : même unité que la cible, erreur absolue moyenne, met en valeur l'erreur moyenne du modèle


On conclu de cette partie qu'il est possible d'obtenir de meilleurs paramètres que ceux donnés par Toczylowski particulièrement pour l'atome d'Argon qui présentait des résultats moins satisfaisants.

# Paramètres Chinois

On s'interresse à un nouvel article plus récent du journal chinois de ... qui traite spécifiquement de l'Argon. A celui ci est ajouté un nouveau jeu de données ab-initio plus grand pour Ar-HCN.
il est plus grand tant dans le nombre de points calculés que dans la plage de valeurs que prend R.

- 1767 points
- R de 2 à 25 Angstrom avec un pas de 0.05 (soit 3.77945225 à 47.243153125 bohr)
- Theta de 0° à 180° avec un pas de 10

Pas la meme géométrie que Toczylowski pour theta donc il faut inverser.
Il y a beaucoup plus de données, les fit deviennent plus complexes.


Meme méthodologie que les données précedentes à quelques différences pres :

- On prend p0 le meilleur jeu de paramètres que l'on a obtenu pour les données Ar-HCN de Toczylowski
- curve_fit est apppliquée de la même manière
- Pour least_squares on met en place 3 fonctions résidus :
    - residus 1 : erreur absolue
    - residus 2 : (y_ref-y_pred)/sqrt(abs(y_ref)+1)
    - residus 3 : mean(((y_ref-y_pred)/sqrt(abs(y_ref) + eps))**2)
- Pour differential evolution on effectue plus de test avec des fonctions de couts différentes 

En utilisant toutes les données, il est plutot difficile d'obtenir un fit satisfaisant:
- Probleme d'une forte variation d'échelle (zone répulsive, puits, zone ou R est tres grand)

On obtient des premiers resultats

puis on refait des calculs en réduisant l'ensemble et en prenant R entre 2.5 et 10 Angstrom (4.7 et 18.9 bohr) avec la meme procédure.

La selection des meilleurs paramètres se fait graphiquement et avec les métrique. J'ai aussi ajouté ici une metrique MAE pondérée qui donne plus de poids aux erreurs dans la zone du puit. Et une MAE qui n'est calculée que sur les valeurs entre -1 et 1 mEh.


# Comparaison des methodes sur les données

Efficacité, temps d'execution, meilleurs résutats, flexibilité

Comparaison des Paramètres obtenus

C

# HNC - Données de Rennes

On travaille maintenant sur un grand dataset qui comporte des données ab-initio mélangées à des données calculées. Celui ci contient 25000 points. 

La molécule a changé, ce n'est plus HCN mais HNC. Le grand nombre de points rend plus difficile le fit.

On réduit l'intervalle des valeurs et on prend les points entre 2.5 et 10 Angstrom (4.7 et 18.9 bohr). 

contour plot HCN HNC

# Réseaux de neurones

Dans un dernier temps on s'interesse brievement à l'utilisation de réseaux de neuronnes pour l'ajustement de surface.

Utilisation de la Bibliothèque PyTorch. On oublie le modèle physique est on cherche à obtenir les coefficients d'une somme de polynomes de legendre de degré n.

Pour aller plus vite, comme on est dans une phase exploratoire, je demande à Gemini de me mettre en place le réseau.

Architecture : 
- Entree du NN : Distance R
- Sortie du NN : Les coefficients $c_0(R),\,\dots\,,\,c_{L_{max}}$
- Couche de fusion (forward) : modele prend $(R,\theta)$ en entrée du forward. $R$ passe dans le réseau pour obtenir les $c_l(R)$ l'énergie finale est le produit scalaire entre les $c_l$ et les $P_l$

Gemini préconise aussi de normaliser les R à l'entrée pour éviter les instabilités numériques et de redimensionner les énergies.


On choisis la loss-L1 dans un premier temps, sur les données de Rennes de 2.5 à 10 Angstrom


Les résultats sont plutot satisfaisants dans la zone répulsive et la zone du puit (sans etre meilleur que les méthodes classiques d'optimisation), 

Probleme à longue distance : l'énergie tend à passer au dessus de 0.


pas aussi bien que analytique



probleme contexte avec plus de degrés de liberté peut etre meilleur?

# Conclusion


