import matplotlib.pyplot as plt
import numpy as np
from dfs import deplacements
from random import randint
from dfs import generation_labyrinthe, choix_cellule
from dijkstra import algo_dijkstra

"""Retourne les indices des déplacements possibles (0..7)."""
def deplacements_possibles(x, y, pheromone, labyrinthe):
    moves = []
    n = len(labyrinthe)

    for i, (dx, dy) in enumerate(deplacements):
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n:
            if labyrinthe[nx][ny] == 1 and (nx, ny) not in pheromone:
                moves.append(i)
    return moves

"""Crée un individu : une liste de déplacements (0..7)."""
def creationIndividu(depart, but, longueurChemin, labyrinthe):
    chemin = []
    pheromone = []
    x, y = depart
    
    for _ in range(longueurChemin):
        if but  == (x,y): # si l'individu atteint l'objectif, il arrête son parcours
            return chemin
        
        deplacements_valides = deplacements_possibles(x, y, pheromone, labyrinthe)

        if deplacements_valides:
            choix = randint(0, len(deplacements_valides)-1)
            nextStep = deplacements_valides[choix]
            dx, dy = deplacements[nextStep]
            x, y = x + dx, y + dy

        else: # Si on est bloqué , on met un phéromone et on retourne en arrière
            
            pheromone.append((x, y))

            # Retour arrière si possible
            if len(chemin) >= 1:
                lastStep = chemin[-1]
                dx, dy = deplacements[lastStep]
                x, y = x - dx, y - dy
            else:
                # si aucune direction précédente, on reste sur place
                nextStep = None

        chemin.append(nextStep)

    return chemin


def afficher_individu(labyrinthe, depart, individu):
    n = len(labyrinthe)

    # copie en float pour pouvoir changer certaines cases
    M = np.array(labyrinthe, dtype=float)

    # coordonnées du robot
    x, y = depart

    for d in individu:
        if d is None:
            break
        dx, dy = deplacements[d]
        x, y = x + dx, y + dy
        M[x][y] = 2 # colore le chemin : valeur spéciale (2)

    plt.figure(figsize=(6, 6))

    # colormap : 0 = noir (mur), 1 = blanc (labyrinthe), 2 = jaune (chemin)
    cmap = plt.cm.gray
    cmap = cmap.copy()
    cmap.set_over('yellow')

    # affichage
    plt.imshow(M, cmap=cmap, vmin=0, vmax=1)
    plt.title("Chemin de l'individu")
    plt.axis('off')
    plt.show()


def genese(depart, but,longueurChemin,labyrinthe):
    population = []
    P = randint(100,200)
    for _ in range(P):
        individu = creationIndividu(depart,but,longueurChemin,lab)
        population.append(individu)
    return population

if __name__ == "__main__":
    lab = generation_labyrinthe(10)
    but = choix_cellule(0,0,lab)
    
    """Choix du départ avec dijkstra"""
    map_distance = algo_dijkstra(lab,but)
    xd, yd = randint(len(lab)//2,len(lab)-1), randint(len(lab)//2,len(lab)-1) #depart doit au plus proche être au milieu du labyrinthe
    depart = choix_cellule(xd,yd,lab)
    while map_distance[xd][yd] < 8: #tant que la distance au but est peu élevé, on cherche un autre point de départ
        xd, yd = randint(len(lab)//2,len(lab)-1), randint(len(lab)//2,len(lab)-1)
        depart = choix_cellule(xd,yd,lab)
        
    longChemins = randint(10,25)
    population = genese(depart,but,longChemins,lab)
    for ligne in population:
        print(ligne)

