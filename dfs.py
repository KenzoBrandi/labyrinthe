from random import randint

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
def voisin_eligible(x, y, labyrinthe):
    cpt = 0
    n = len(labyrinthe)
    for dx, dy in deplacements:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and labyrinthe[nx][ny] == 1:
            cpt += 1
            if cpt > 1:
                return False  # plus d’un voisin visité : pas éligible

    # éligible si exactement 1 voisin visité
    return cpt == 1

def voisins_non_visites(x, y, labyrinthe):
    n = len(labyrinthe)
    voisins_non_visites = []
    for dx, dy in deplacements:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and labyrinthe[nx][ny] == 0:
            if voisin_eligible(nx, ny,labyrinthe):
                voisins_non_visites.append((nx, ny))
        
    return voisins_non_visites 



def generation_labyrinthe(n):
    labyrinthe = [[0 for _ in range(n)] for _ in range(n)]
    #coordonnées de départ
    x = randint(0,n-1)
    y = randint(0,n-1)
    labyrinthe[x][y] = 1 #on marque la cellule comme visitée
    stack = [(x,y)] #ajout dans la pile

    while stack:
        x, y = stack[-1]
        voisins = voisins_non_visites(x,y,labyrinthe)
        if voisins:
            nx, ny = voisins[randint(0, len(voisins)-1)]
            labyrinthe[nx][ny] = 1
            stack.append((nx, ny))
        else:
            stack.pop()
    
    return labyrinthe

if __name__ == "__main__":
    for ligne in generation_labyrinthe(15):
        print(ligne)
