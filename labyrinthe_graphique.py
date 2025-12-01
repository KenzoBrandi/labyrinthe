from dfs import generation_labyrinthe, choix_cellule
from PIL import Image

if __name__ == "__main__":
    lab = generation_labyrinthe(15)
    but = choix_cellule(0,0,lab)
    
    # Taille d'une cellule en pixels
    taille_cellule = 20

    # Création d'une image RGB
    img = Image.new("RGB", (len(lab[0])*taille_cellule, len(lab)*taille_cellule), "white")

    # Remplissage des pixels
    for i, ligne in enumerate(lab):
        for j, val in enumerate(ligne):
            if (i, j) == but:
                couleur = (255, 0, 0)      # rouge
            else:
                couleur = (0, 0, 0) if val == 0 else (255, 255, 255)
            for x in range(taille_cellule):
                for y in range(taille_cellule):
                    img.putpixel((j*taille_cellule + x, i*taille_cellule + y), couleur)

    # Affichage
    img.show()
