from dfs import deplacements
from random import randint
from dfs import generation_labyrinthe, choix_cellule
from dijkstra import algo_dijkstra
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

"""------------initialisation labyrinthe---------------------"""

"""Création labyrinthe 50x50"""
lab = generation_labyrinthe(50)

"""On choisit un point but au hasard"""
but = choix_cellule(0,0,lab)

"""Choix du départ avec Dijkstra pour qu'il soit assez éloigné du but"""
map_distance = algo_dijkstra(lab,but) # map distance pour évaluer la distance au but du départ
xd, yd = randint(len(lab)//2,len(lab)-1), randint(len(lab)//2,len(lab)-1) 
depart = choix_cellule(xd,yd,lab)
while map_distance[xd][yd] < 15:  # on cherche un départ loin du but
    xd, yd = randint(len(lab)//2,len(lab)-1), randint(len(lab)//2,len(lab)-1)
    depart = choix_cellule(xd,yd,lab)
    
"""----------------------------------------------------------"""

def nextCell(x,y, movement,labyrinthe):
    """
    Retourne la prochaine cellule selon le mouvement choisi.
    Si on tombe sur un mur ou hors labyrinthe, on reste sur place.
    """
    n = len(labyrinthe)
    dx , dy = deplacements[movement]
    nx, ny = x + dx, y + dy
    if 0 <= nx < n and 0 <= ny < n and labyrinthe[nx][ny] == 1:
        return (nx,ny)
    return (x,y)

def caseBloquante(x,y,labyrinthe):
    """
    Vérifie si la case est un cul-de-sac (robot n'a qu'une issue)
    """
    n = len(labyrinthe)
    cpt = 0
    for dx, dy in deplacements:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and labyrinthe[nx][ny] == 1:
            cpt += 1
        if cpt > 1:  # si plus d'une sortie, ce n'est pas bloquant
            return False
    return True


class Robot:
    """
    Un programme chemin/individu est représenté par cette classe Robot
    Elle a deux attributs: une case départ et une liste de mouvements à effectuer 
    """
    def __init__(self,depart,moves):
        self.depart = depart
        self.moves = moves.copy()  # copie des mouvements pour chaque robot
        
    def cheminParcouru(self):
        """
        Retourne le chemin réel parcouru par le robot selon ses moves
        Cette version de la méthode ne prend pas en compte les phéromones!!
        """
        chemin = [depart]
        x, y = depart
        for mv in self.moves:
            if (x, y) != nextCell(x,y,mv,lab):
                chemin.append(nextCell(x,y,mv,lab))  # ajouter nouvelle position
            x, y = nextCell(x,y,mv,lab)
        return chemin
    
    
    def ajoutPheromone(self, pheromone):
        """On ajoute la cellule dans la liste des phéromones si c'est une case bloquante"""
        for x,y in self.cheminParcouru():
            if not((x,y) in pheromone) and caseBloquante(x,y,lab):
                pheromone.append((x,y))

    def afficher(self):
        # copie du labyrinthe pour l'affichage
        M = np.array(lab, dtype=float)

        # chemin réellement parcouru par le robot
        chemin = self.cheminParcouru()

        # chemin du robot (jaune)
        for (x, y) in chemin:
            M[x][y] = 2

        # départ (vert)
        dx, dy = depart
        M[dx][dy] = 3

        # but (rouge)
        bx, by = but
        M[bx][by] = 4

        # endCell (bleu)
        ex, ey = chemin[-1]
        M[ex][ey] = 5

        # colormap :
        # 0 = mur (noir)
        # 1 = libre (blanc)
        # 2 = chemin (jaune)
        # 3 = départ (vert)
        # 4 = but (rouge)
        # 5 = endCell (bleu)
        cmap = ListedColormap([
            "black",   # mur
            "white",   # libre
            "yellow",  # chemin
            "green",   # départ
            "red",     # but
            "blue"     # endCell
        ])

        plt.figure(figsize=(6, 6))
        plt.imshow(M, cmap=cmap)
        plt.title("Chemin d'un robot")
        plt.axis("off")

        # légende
        legend_elements = [
            Patch(facecolor="green", label="Départ"),
            Patch(facecolor="red", label="But"),
            Patch(facecolor="blue", label="EndCell")
        ]
        plt.legend(handles=legend_elements, loc="upper right")

        plt.show()
        
        
    def __str__(self):
        return str(self.cheminParcouru())
    
    def __lt__(self, other):
        # Permet de trier les robots selon leur fitness
        return fitness(self, but, lab) < fitness(other, but, lab)

    def __eq__(self, other):
        # Compare les robots selon leur fitness
        return (fitness(self, but, lab) == fitness(other, but, lab))

def genese(depart, nbIndividus, longueurChemins):
    """
    Génère une population initiale de robots aléatoires
    """
    population = []
    P = 100
    for _ in range(nbIndividus):
        moves = [ randint(0,7) for _ in range(longueurChemins)]
        robot =  Robot(depart,moves)
        population.append(robot)
    return population

def endCell(robot,lab):
    """
    Retourne la dernière cellule atteinte par le robot
    """
    chemin = robot.cheminParcouru()
    return chemin[-1]

def distanceAuBut(cellule,but,lab):
    """
    Calcule la distance restante jusqu'au but
    """
    xc, yc = cellule
    map_distance = algo_dijkstra(lab,but)
    return map_distance[xc][yc]

def penalties(robot, but, lab):
    """
    Pénalités pour les mouvements inutiles et distance minimale au but
    """
    chemin = robot.cheminParcouru()
    nb_moves = len(robot.moves)
    nb_cases = len(chemin) - 1

    # mouvements inutiles (resté sur place ou mur)
    p_stagnation = nb_moves - nb_cases

    # pénalité si le robot ne bouge presque pas
    p_immobile = 0
    if nb_cases < 5:
        p_immobile = 50

    # distance minimale atteinte au cours du chemin
    map_distance = algo_dijkstra(lab, but)
    d_best = min([map_distance[x][y] for (x, y) in chemin])

    # combinaison des pénalités
    return 2*p_stagnation + p_immobile + d_best

    
def fitness(robot, but, lab):
    """
    Score global pour savoir si le robot est efficace
    """
    d_end = distanceAuBut(endCell(robot, lab), but, lab)
    pen = penalties(robot, but, lab)
    return d_end + pen

def selection(population,ts):
    """
    Garde les meilleurs robots selon le taux ts
    """
    populationTriee = sorted(population)
    k = int(len(population)*ts)
    return populationTriee[:k]

def reproduction(population,Ne):
    """
    Croisement de deux robots pour créer un enfant
    """
    newGen = []
    for _ in range(Ne):
        indexP1 = randint(0, len(population)-1)
        indexP2 = randint(0, len(population)-1)
        while indexP1 == indexP2:
            indexP2 = randint(0, len(population)-1)
        parent1 = population[indexP1]
        parent2 = population[indexP2]
        
        milieu = len(parent1.moves) // 2
        delta = len(parent1.moves) // 10
        cut = randint(milieu-delta,milieu+delta)
        moves = parent1.moves[:cut] + parent2.moves[cut:] 
        
        enfant = Robot(parent1.depart, moves)
        newGen.append(enfant)
        
    return newGen

def mutation(population,tm):
    """
    Change aléatoirement certaines directions pour garder de la diversité
    """
    nbMut = int(len(population) * tm)
    for _ in range(nbMut):
        robot = population[randint(0, len(population)-1)]
        gene = randint(0, len(robot.moves)-1)
        robot.moves[gene] = randint(0,7)
