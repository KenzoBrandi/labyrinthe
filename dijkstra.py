from dfs import generation_labyrinthe, choix_cellule, voisins
import matplotlib.pyplot as plt
import numpy as np

def initialisation_labyrinthe(n):
    labyrinthe = generation_labyrinthe(n)  # crée le labyrinthe
    but = choix_cellule(0,0,labyrinthe)  # choisit la cellule de but
    return (labyrinthe, but)  # retourne labyrinthe et but


def algo_dijkstra(labyrinthe, but):
    n = len(labyrinthe)
    # -1 = mur, None = libre non visité
    map_distance = [[-1 if labyrinthe[i][j] == 0 else None for j in range(n)] for i in range(n)]

    cpt = 0
    i_g, j_g = but
    map_distance[i_g][j_g] = 0  # la cellule de but vaut 0
    location = [but]    # liste des cellules à traiter

    while location:
        next_location = []  # cellules du prochain niveau
        for xi, yi in location:
            L = voisins(xi, yi, map_distance)  # voisins de la cellule courante
            for xj, yj in L:
                if map_distance[xj][yj] is None:
                    map_distance[xj][yj] = cpt + 1  # distance depuis la but
                    next_location.append((xj, yj))  # ajout pour le prochain tour
        location = next_location
        cpt += 1
        
    return map_distance  # retourne la map des distances

def carte_directionnelle(Map):
    n = len(Map)
    carte = [[None for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if Map[i][j] != -1:          # si ce n’est pas un mur
                if Map[i][j] == 0:       # si c’est la cellule but
                    carte[i][j] = 0
                else:
                    Lvoisins = voisins(i, j, Map)   # voisins valides
                    x, y = Lvoisins[0]
                    k = 1
                    while k < len(Lvoisins) and Map[x][y] != Map[i][j] - 1:
                        x, y = Lvoisins[k]         # trouver voisin plus proche du but
                        k += 1
                    carte[i][j] = (x, y)          # enregistrer direction
    return carte

#retourne une liste contenant les cases visitées du départ au but
def resolution_labyrinthe(depart,but,carteDir):
    x , y = depart
    chemin = [depart]
    while (x,y) != but:
        x, y = carteDir[x][y]
        chemin.append((x,y))
    return chemin
    
def afficher_carte_couleur(Map, chemin):
    
    M = np.array(Map, dtype=float)

    M_color = M.copy()
    
    # on force les cellules du chemin solution à être > vmax
    vmax = np.nanmax(M)
    valeur_chemin = vmax + 1
    
    for (x, y) in chemin:
        M_color[x][y] = valeur_chemin

    fig, ax = plt.subplots()

    # colormap vert à jaune
    cmap = plt.cm.YlGn_r   # le _r inverse YlGn → vert → jaune

    # murs en noirs
    cmap.set_under("black")
    
    #chemin en rouge
    cmap.set_over("red")
    

    # on impose les limites pour que -1 soit bien en-dessous
    cax = ax.matshow(M_color, cmap=cmap, vmin=0, vmax=vmax)

    plt.colorbar(cax)
    plt.suptitle(f"Longueur du chemin solution : {len(chemin)-1}", fontsize=14)
    plt.show()
        
        
def evolution_longueur_moyenne(taille_laby_list, nb_essais=10):
    """
    Pour chaque taille de labyrinthe dans taille_laby_list,
    génère nb_essais labyrinthes, calcule la longueur du chemin solution
    et retourne une liste des longueurs moyennes.
    """
    moyennes = []

    for N in taille_laby_list:
        longueurs = []
        for _ in range(nb_essais):
            # initialisation labyrinthe
            lab, but = initialisation_labyrinthe(N)
            n = len(lab)
            depart = (np.random.randint(n), np.random.randint(n))
            while lab[depart[0]][depart[1]] == 0:
                depart = (np.random.randint(n), np.random.randint(n))
            
            # Dijkstra
            Map = algo_dijkstra(lab, but)
            carteDir = carte_directionnelle(Map)
            chemin = resolution_labyrinthe(depart, but, carteDir)
            longueurs.append(len(chemin))
        
        moyennes.append(np.mean(longueurs))
    
    # affichage
    plt.figure(figsize=(8,5))
    plt.plot(taille_laby_list, moyennes, marker='o', linestyle='-', color='blue')
    plt.xscale('log')  # on peut garder log pour lisibilité
    plt.xticks(taille_laby_list, taille_laby_list)  # graduations exactes
    plt.xlabel("Taille du labyrinthe N")
    plt.ylabel("Longueur moyenne du chemin solution")
    plt.title(f"Évolution de la longueur moyenne du chemin solution (moyenne sur {nb_essais} labyrinthes)")
    plt.grid(True)
    plt.show()

    return moyennes

        
if __name__ == "__main__":
    lab, but = initialisation_labyrinthe(50)
    map_distance = algo_dijkstra(lab, but)
    carte = carte_directionnelle(map_distance)
    print("Labyrinthe:")
    for ligne in lab:
        print(ligne)
    print("----------\nCarte des distances:")
    for ligne in map_distance:
        print(ligne)
    print("----------\nCarte directionnelle:")
    for ligne in carte:
        print(ligne) 
    
    # ----------Résolution et affichage graphique-----
    n = len(lab)
    #on prend une cellule de départ depuis l'extrêmité opposée au but
    depart = choix_cellule(n-1,n-1,lab)
    print("De ",depart," à ", but)
    chemin = resolution_labyrinthe(depart,but,carte)
            
    afficher_carte_couleur(map_distance,chemin)
    
    # Graphique des moyennes des longueurs des chemins solutions
    # N_values = [8, 16, 32, 64, 128, 256, 512]
    # moyennes = evolution_longueur_moyenne(N_values, nb_essais=10)
    

