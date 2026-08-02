

# Contexte théorique
On considère un système composé d'un Atome A et d'une molécule linéaire B de longueur fixe (rotateur rigide).
La structure et la dynamique du système sont décrites par la mécanique quantique via une fonction d'onde 
$\Psi(\vec{R}, \vec{\rho})$,solution de l'équation de Schrödinger : 
- $\vec{R}$ est la position du centre de masse de A par rapport au centre de masse de B
- $\vec{\rho}$ sont les coordonnées internes de A et B (électrons, etc.)

Par l'approximation de Born-Oppenheimer,la masse de l'électron est beaucoup plus faible que celle du noyau.
Les électrons s'adaptent donc presque instantanément à de faibles variations des positions nucléaires. On peut alors séparer la 
fonction d'onde sous la forme : $\Psi(\vec{R}, \vec{\rho}) = F(\vec{R})\chi(\vec{\rho}; \vec{R})$
- $F(\vec{R})$ : qui décrit le mouvement relatif
- $\chi(\vec{\rho}; \vec{R})$ : qui décrit le mouvement électronique

Cette approche permet de résoudre le problème en trois étapes : 
1. On fixe la géométrie nucléaire $\vec{R}$ et on résout l'équation de Schrödinger électronique pour obtenir $\chi(\vec{\rho}; \vec{r})$
2. En faisant varier $\vec{R}$, on obtient l'énergie électronique en fonction de cette géométrie : c'est la **surface d'énergie potentielle (PES)**
3. On résoud l'équation du mouvement nucléaire pour d'obtenir $F(\vec{R})$.

La surface d'énergie potentielle est obtenue par des techniques de chimie quantique et des programmes informatiques
associés. Les calculs étant particulièrement coûteux, ceux-ci sont effectués sur un ensemble réduit de géométries nucléaires (**points ab-initio**). 
On utilise ensuite un modèle analytique pour interpoler la fonction de potentiel $V(R,\theta)$.

Pour notre système, la symétrie axiale de la molécule B (potentiel indépendant de l'angle d'azimut) et son caractère rigide font que la surface de potentel
 ne dépend que de $R$ et $\theta$ où :
- R distance entre les centres de masse de A et B
- $\theta$ angle entre l'axe de la molécule B et le vecteur $\vec{R}$
par symétrie cylindrique autour de l'axe moléculaire de B, on se place seulement dans le contexte d'un plan (2 dimensions).

En pratique, en fixant une variable (par exemple $\theta=90$°) on réalise des coupes de la surface d'énergie potentielle.
- Le signe de l'énergie potentielle informe sur la nature de l'interaction entre A et B. 
	- $V > 0$ : Répulsive
	- $V < 0$ : Attractive
- A courte distance $V(R,\theta)$ prend de grandes valeurs (mur répulsif)
- A grande distance $V(R,\theta) \to 0$ par valeurs négatives (région asymptotique)
- Entre ces deux régions il y a le puits de potentiel. Il correspond à une configuration stable du système

La surface d'énergie potentelle est notamment utilisée pour étudier la dynamique des collisions ou la formation d'états liés. 



# Sujet du stage 

La problématique de ce stage trouve son origine dans l'article de référence publié en 2000 par R.R. Toczylowski, F. Dolorest S.M. Cybulski : 
Theoretical study of the He–HCN, Ne–HCN, Ar–HCN, and Kr–HCN complexes.Cet article présente des données ab initio pour ces quatre systèmes, 
ainsi qu'un modèle analytique permettant de calculer la surface d'énergie potentielle $V(R,\theta)$. Ce modèle repose sur 40 paramètres qui 
doivent être ajustés en fonction du système étudié. Toutefois, les auteurs ne mentionnent pas les valeurs numériques de ces paramètres, y compris 
ceux utilisés pour générer les figures de leur publication.

Quatre ans plus tard, la thèse de doctorat de R.R. Toczylowski (2004) propose un jeu de paramètres pour chacun des systèmes étudiés. 
Cependant, une incohérence majeure est apparue : l'utilisation des paramètres fournis pour l'Argon conduit à des calculs d'états liés insatisfaisants, 
qui ne parviennent pas à reproduire les résultats présentés dans l'article initial.

**Afficher des contour plots?**

L'objectif de ce travail est d'une part de réaliser de nouveaux ajustements de la surface d'énergie potentielle (fits) afin 
de déterminer des jeux de paramètres qui conduisent à des résultats physiquement cohérents. D'autre part, de définir des critères 
pertinents pour évaluer et quantifier la qualité de ces ajustements.

 
Dans un second temps on s'interesse à d'autres Surfaces de potentiel issues de traveaux plus récents : 
- Le complexe Ar–HCN, à partir de données ab-initio publiées dans le Chinese Journal of Chemical Physics (T. Liman et al., 2026).
- Le complexe Ar–HNC, à l'aide d'un jeu de données produit à l'Institut de Physique de Rennes (IPR). Qui comprend à la fois des 
points ab-initio et les résultats d'un premier ajustement de surface.


# Le modèle physique et ses paramètres

Notre modèle décrivant $V(R,\theta)$ s'exprime comme la somme d'un terme qui décrit les interactions à courte portée ($V_{sh}$)
et d'un terme asymptotique régissant les phénomènes à longue portée ($V_{as}$)
$$V(R,\theta)=V_{\mathrm{sh}}(R,\theta) + V_{\mathrm{as}}(R,\theta)$$ 

## Courte portée : $V_{\mathrm{sh}}$

$$V_{\mathrm{sh}}=G(R,\theta)e^{D(\theta)+B(\theta)R}$$

avec $G(R,\theta) = \sum_{l=0}^{5} (g_{0,l}+g_{1,l}R+g_{2,l}R^2+g_{3,l}R^3) P_l(\cos\theta)$

et $D(\theta)=\sum\limits_{l=0}^{5}d_lP_l(\cos\theta)\;$ $\;B(\theta)=\sum\limits_{l=0}^{5}b_lP_l(\cos\theta)$

## Longue portée : $V_{\mathrm{as}}$

$$V_{as}&=f_6(\lvert B(\theta)R\rvert)\frac{c_0P_0(\cos\theta)+c_2P_2(\cos\theta)}{R^6}
		 +f_7(\lvert B(\theta)R\rvert)\frac{c_1P_1(\cos\theta)+c_3P_3(\cos\theta)}{R^7}$$

avec $f_n(x)=1-e^{-x}\sum_{k=0}^{n}\frac{x^k}{k!}$



# Implémentation du modèle analytique

La première étape - après avoir converti les tableaux de données en fichiers utilisables - est de produire un programme python













___

Comportement physique de la PES :
	- Une valeur d'énergie positive décrit une force de répulsion entre les molécules tandis qu'une valeur négative décrit une force d'attraction
    - à grand $R$ : $V(R,\theta) \to 0$ negativement
    - à courte distance : mur répulsif : grandes valeurs d'énergie
    - entre la zone à grand $R$ et le mur répulsif à courte distance, on observe un **puits de potentiel** : une région où $V(R,\theta) < 0$ passe par un minimum local avant de remonter



- La structure et la dynamique moléculaires sont décrites par la mécanique quantique.

- Considère un système composé d’un atome A et d’une molécule linéaire B de longueur fixe (un rotateur rigide).

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
        - faire varier la géométrie nucléaire => l’énergie électronique en fonction de la géométrie nucléaire, appelé surface d’énergie potentielle (PES).
        - résoudre l'équation pour le mouvement nucléaire pour obtenir $F(\vec{r})$

- La PES est obtenue à l'aide de techniques de chimie quantique et de programmes informatiques associés
    - les calculs sont coûteux et sont effectués pour un (petit) ensemble de géométries nucléaires que l'on appelle "points ab-initio"
    - Les points de données ab initio ainsi obtenus sont généralement ajustés à un modèle analytique qui sert à interpoler la fonction potentielle d'énergie (PES) pour d'autres géométries

- Coordonnées adaptées au système Atome–rotateur rigide :
    - on utilise typiquement des coordonnées  : $R$ (distance entre les centres de masse de A et B) et $\theta$ (angle entre l'axe de la molécule B et le vecteur $\vec{R}$)
    - comme B est un rotateur rigide (longueur de liaison fixe), la PES ne dépend que de $(R, \theta)$, au lieu des 3 coordonnées internes nécessaires pour un système à 3 atomes libres
    - par symétrie cylindrique autour de l'axe moléculaire de B, on se place seulement dans le contexte d'un plan (2 dimensions)

- Comportement physique de la PES :
	- Positif = repulsif, negatif=attractif
    - à grand $R$ : $V(R,\theta) \to 0$ negativement
    - à courte distance : mur répulsif : grandes valeurs d'énergie
    - _parler de la zone du puits pour les coupes à theta fixé?_

- Utilisation de la PES pour la dynamique nucléaire :
	- Etats liés :
	- Etats de diffusion :
