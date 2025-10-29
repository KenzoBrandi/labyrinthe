from random import randint

def cellule_suivante(x, y, labyrinthe):
    n = len(labyrinthe)

    voisins_non_visites = []
    
    deplacements = [
        (0, 1),
        (-1, 1), 
        (-1, 0), 
        (-1, -1), 
        (0, -1),   
        (1, -1),  
        (1, 0),  
        (1, 1)     
    ]

    for dx, dy in deplacements:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and labyrinthe[nx][ny] != 1:
            voisins_non_visites.append((nx, ny))
        
    return voisins_non_visites[randint(0,len(voisins_non_visites)-1)] if voisins_non_visites else None 
    
def generation_labyrinthe(n):
    labyrinthe = [[0 for _ in range(n)] for _ in range(n)]
    #coordonnées de départ
    x = randint(0,n-1)
    y = randint(0,n-1)
    labyrinthe[x][y] = 1 #on marque la cellule comme visitée
    stack = [(x,y)] #ajout dans la pile
    while stack != []:
        pass
    
    return labyrinthe
print(generation_labyrinthe(5))