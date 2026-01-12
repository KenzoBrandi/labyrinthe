import argparse
from algo_genetique import *
from copy import deepcopy
import matplotlib.pyplot as plt

lab_copy = deepcopy(lab) # copie du labyrinthe initial qui ne sera pas modifié par les ajouts de phéromone


"""Préparation des arguments"""
parser = argparse.ArgumentParser()
parser.add_argument('--N', type=int, default=100, help="Nombre d'individus")
parser.add_argument('--L', type=int, default=50, help="Longueur des programmes/chemins")
parser.add_argument('--nG', type=int, default=5, help="Nombre maximal de générations")
parser.add_argument('--ts', type=float, default=0.4, help="Taux de sélection des individus les plus adaptés")
parser.add_argument('--tm', type=float, default=0.3, help="Taux de mutation")
args = parser.parse_args()
Ne =  int(args.N * (1 - args.ts))

population = genese(depart, args.N, args.L)

"""------------------------- ÉVOLUTION -----------------------------"""
pheromone = [] # Liste des cases où il y aura des phéromones 
fitness_history = [] #là où on stocke toutes les fitness

for _ in range(args.nG):
    """1. i) Fitness et tri des individus et 2. ii) Sélection des individus les plus adaptés"""
    selected = selection(population, args.ts) # les robots sont triés dans l'ordre croissant du fitness dans la fonction selection
    
    fitness_history.append(fitness(selected[0], but, lab)) # Sauvegarder la meilleure fitness de la génération

    """Étape de phéromone"""
    for robot in population:
        robot.ajoutPheromone(pheromone) # on met les phéromones
    for x, y in pheromone:
        lab[x][y] = 0 # on change les cellules concernées en mur


    """3. iii) Reproduction : construction des nouveaux individus"""
    newGen = reproduction(selected, Ne) # seuls les individus sélectionnés peuvent se reproduire
    population = selected + newGen

    """4. iv) Mutation"""
    mutation(population, args.tm)


"""------------------------- Affichage de la fonction de fitness -----------------------------"""
plt.plot(fitness_history, marker='o')
plt.xlabel("Génération")
plt.ylabel("Fitness du meilleur robot")
plt.title("Évolution de la fitness")
plt.show()
    
selected[0].afficher()
