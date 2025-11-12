from dfs import generation_labyrinthe
from PIL import Image

if __name__ == "__main__":
    lab = generation_labyrinthe(15)
    
    # Taille d'une cellule en pixels
    taille_cellule = 20

    # Création d'une image RGB
    img = Image.new("RGB", (len(lab[0])*taille_cellule, len(lab)*taille_cellule), "white")

    # Remplissage des pixels
    for i, ligne in enumerate(lab):
        for j, val in enumerate(ligne):
            couleur = (0,0,0) if val == 1 else (255,255,255)  # 1 = noir (mur), 0 = blanc (passage)
            for x in range(taille_cellule):
                for y in range(taille_cellule):
                    img.putpixel((j*taille_cellule + x, i*taille_cellule + y), couleur)

    # Affichage
    img.show()
