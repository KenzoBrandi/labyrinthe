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

def voisins(x,y, labyrinthe):
    voisins = []
    n = len(labyrinthe)
    for dx, dy in deplacements:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n:
            voisins.append((nx,ny))
    return voisins
        
def voisin_eligible(x, y, labyrinthe):
    cpt = 0
    for xc, yc in voisins(x, y, labyrinthe):
        if labyrinthe[xc][yc] == 1:
            cpt += 1
            if cpt > 1:
                return False  #trop de voisins visités

    return cpt == 1  #exactement 1 voisin visité

def voisins_non_visites(x, y, labyrinthe):
    voisins_non_visites = []
    for xc, yc in voisins(x, y, labyrinthe):
        if labyrinthe[xc][yc] == 0 and voisin_eligible(xc, yc,labyrinthe):
            voisins_non_visites.append((xc, yc))
        
    return voisins_non_visites 



def point_valide(x, y, labyrinthe):
    """Déplace (x,y) vers un voisin aléatoire tant que la cellule vaut 0."""
    while labyrinthe[x][y] == 0:
        voisins_liste = voisins(x, y, labyrinthe)
        x, y = voisins_liste[randint(0, len(voisins_liste)-1)]
    return x, y

def choix_debut_fin(labyrinthe):
    n = len(labyrinthe)

    # Début : en bas à droite (n-1, n-1)
    xd, yd = point_valide(n-1, n-1, labyrinthe)

    # Fin : en haut à gauche (0, 0)
    xf, yf = point_valide(0, 0, labyrinthe)

    return (xd, yd), (xf, yf)


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
