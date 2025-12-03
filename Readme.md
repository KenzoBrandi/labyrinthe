Projet Maze Runner 2025

Introduction

    Résolution et exploration de labyrinthes en 2D/3D — DFS, Dijkstra & Algorithmes génétiques

    Ce projet a pour objectif de générer, analyser et résoudre des labyrinthes en 2D/3D de manière algorithmique, en combinant plusieurs approches :

    Parcours en profondeur (DFS) pour la génération.

    Algorithme de Dijkstra pour la recherche de chemins optimaux.

    Algorithmes génétiques pour la résolution sans connaissance du labyrinthe.


Structure du projet

    Le projet est divisé en trois sous-projets indépendants mais complémentaires :

    1. Génération aléatoire de labyrinthe (DFS)

        Le labyrinthe est représenté par une matrice NxN, où les obstacles sont codés par 0 et les cellules libres par 1.

        La génération utilise une version aléatoire du parcours en profondeur (Depth-First Search) :

        Principe :

            Choisir une cellule initiale aléatoire.

            Explorer récursivement un voisin éligible non visité.

            Utiliser une pile (stack) pour gérer le backtracking.

            Continue jusqu’à ce que toutes les cellules aient été visitées.


    2. Résolution optimale via l’algorithme de Dijkstra

        L'objectif est de construire une carte directionnelle (“map”) indiquant, pour chaque cellule, la direction optimale vers le but.

        Visualisation :

        Coloration de la carte de distances.

        Coloration en rouge du chemin optimal.

        Mesure de la longueur du chemin.

        Étude de l’évolution de la longueur moyenne de la solution pour des tailles de labyrinthe dans {8, 16, 32, 64, 128, 256, 512}


    3. Résolution via algorithme génétique (GA)

        Lorsque le labyrinthe n’est pas connu du solveur, un algorithme génétique est utilisé pour approcher une solution.

        Représentation :

        Un programme/chemin = une séquence d’entiers ∈ {0..7} (directions).

        Une population initiale d’environ 100 programmes est générée aléatoirement.

    Mécanismes de l'algorithme génétique:
        Fitness

            Evaluer un programme via :

            distance au but du point atteint,

            pénalités (déplacements invalides, collisions, etc.).

        Sélection

            Conserver un pourcentage ts des meilleurs individus.

        Reproduction (crossover)

            Créer Ne = N × (1 – ts) nouveaux individus via découpage/croisement.

        Mutation

            Modifier aléatoirement certaines directions pour maintenir la diversité :

            Taux tm ∈ [0,1]

        Itérations

            Répéter :

                Fitness → Sélection → Reproduction → Mutation
                jusqu’à convergence ou nb max de générations (nG).

        Améliorations :

            Ajout d’un mécanisme de “phéromones” :
            Les branches menant à une impasse sont marquées comme interdites pour les générations suivantes, améliorant considérablement la convergence.

        Résultats :

            Visualisation de l’évolution de la fonction de perte (loss).

            Affichage des chemins trouvés par GA.

            Analyse qualitative de la convergence.