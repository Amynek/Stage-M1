# Contexte théorique : Slide 3

On s'interesse à un système composé d'un atome A et d'une molécule B linéaire **rigide** de longueure fixe.
La structure et dynamique moléculaire sont décrites par la mécanique quantique. De ce fait le système est décrit par une fonction d'onde qui est solution de l'équation de Schrödinger $\Psi(\vec{r}, \vec{\rho})$ 

Approximation de Born-Oppenheimer : 
- FCT d'onde : Fonction decrivant le mvt relatif et fct décrivant le mvt electronique
- électrons réagissent presque instantanément à de faibles variations des positions nucléaires (seulement en R et \theta car rigide)
- calcul de l'énergie électronique pour chaque geometrie fixe du noyau => PES
- PES obtenue avec calculs de chimie quantique et programmes informatiques :
    - calculs tres couteux
    - pts ab-initio obtenus ajustés avec un modèle analytique pour interpoler la fct de potentiel sur d'autres geométries
    - 

# Sujet du stage : Slide 4

On s'interesse à l'article : ...

Il y a : 
- 4 systemes et leurs données ab-initio
- Un modele analytique proposé datant de 1973 : calcul de l'énergie potentielle pour $\theta$ et R donnés.
    - Contient 40 paramètres à determiner selon le systeme

Thèse de Toczylowski : paramètres pour chacun de ces systèmes
Parametres utilisés pour des calculs de propriétés des molécules composés les résultats sont bons sauf pour l'Argon + les résultats ne correspondent pas à ceux qu'ils présentent dans l'article de 2000

# Modèle physique : Slide 5

- Partie short range s'annule à grande distance : 
- Partie asymptotique s'annule à courte distance role de fonctions de switch joué par f6 et f7 : Impose le comportement physique avec 1/R⁶ et 1/R⁷ => energie tend vers 0 en restant négative
- Presenter 40 paramètres

# Implémentation du modèle : Slide 6

- Numérisation des tableaux : grilles de point avec des trous + répartition non uniforme des R et theta
- Objectif premier faire une fonction qui marche
- Temps passé à l'optimiser pour améliorer les performances. Important car nombreux appels

# Implémentation plus performante : Slide 7
- points d'amélioration
- tests : memes fonctions ? Plus performantes?

# Méthodes ajustement de surface : Slide 8
...

# Premières données - Surface 1 Slide 9

# Contours plot : Slide 10 :

Comparer les paramètres 

# Coupes de surfaces : Slide 11

comparer + conclure : Paramètres peuvent etres recalculés, le modele fonctionne pour l'argon + Validation supplémentaire par franck lors de ses calculs d'états vibrationnels

# Nouvelles données - Surface 2 : Slide 12 à 14

dérouler

# Nouveau système HNC : Slide 15 

Apres selection de meilleurs paramètres, on affiche juste des coupes pour differents theta pour HCN et HNC à titre de comparaison.

CCl de cette partie : fit de qualité comme pour HCN meme avec un tres grand nombre de données à condition de travailler sur le dataset

# Reseaux de neurones : Slide 16

- Modèle semi analytique
- L_max = 18


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



# Conclusion


