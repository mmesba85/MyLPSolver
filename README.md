# LP SOLVER

Implémentation de l'algorithme du Simplex.

- Version de python >= 3
- Auteur: Mesbahi Maroua

# Use
**Execution**: python3 LP.py
### Input
- A partir d'un programme linéaire pré-enregistré
	> Le programme demandera le nom du fichier en entrée
- A partir d'un programme linéaire donné en entrée.
	> Il vous sera demandé d'entrer le nom et l'heuristique de l'algorithme, les coefficients de la fonction objectif, la matrice des contraintes ainsi que les coefficients à droite de l'inégalité. Le programme peut prendre en entrée des entiers ou des fractions (exemple: 5, 6/7...)
	Remarque:
	Entrées de la matrice: un coefficient/ligne
	Entrées des vecteurs (fonction objectif/coefficients à droite des contraintes): tous les elements sur une meme ligne.
- A partir d'un programme linéaire aléatoire généré.
	> Il vous sera demandé d'entrer un intervalle pour le choix de la taille de la matrice sous la forme beggining/end. Une taille aléatoire sera choisi parmis l'intervalle

**Execution**: python3 LP.py -gen low_boundary high_boundary

- Dans ce cas, si -gen est spécifiée suivie de deux entiers correspondants aux bornes de l'interval, un programme aléatoire est généré avec une taille choisie aléatoirement dans l'interval.
- Cette méthode d'éxécution est utile dans le cas de lancement de script de tests.


### Output:
- Solution de base
- Valeur objective
- Nombre de récursions du pivot
- Temps de résolution
> Il est aussi possible d'enregistrer le programme linéaire à la fin de l'éxecution afin de pouvoir le relancer à la prochaine éxecution (cf partie Input)

# Test
Exécution: python3 test.py [arg] value

- **[arg]** peut prendre les valeurs suivantes:
		- **-rec** : déscription selon le nombre de récursions.
		- **-time**: description selon le temps d'execution.
- **value** correspond à la taille maximale que le programme linéaire peut prendre.
- Ainsi, le script de test, pour des tailles dif   férentes et inférieurs à la taille maximal donnée, créer un programme linéaire aléatoire de cet taille, execute l'algorithme du Simplex et décris les résultat grace à matplotlib.

```
