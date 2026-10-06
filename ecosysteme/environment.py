import numpy as np

ARIDE = 0
PRAIRIE = 1
FORET = 2


def creer_terrain(largeur, hauteur):
    terrain = np.random.randint(0, 3, size=(hauteur, largeur))
    return terrain


def creer_terrain_lisse(largeur, hauteur, passes=5):
    bruit = np.random.rand(hauteur, largeur)

    for _ in range(passes):
        bruit = (
            bruit
            + np.roll(bruit, 1, axis=0)
            + np.roll(bruit, -1, axis=0)
            + np.roll(bruit, 1, axis=1)
            + np.roll(bruit, -1, axis=1)
        ) / 5

    seuil_bas = np.percentile(bruit, 30)
    seuil_haut = np.percentile(bruit, 70)

    terrain = np.zeros((hauteur, largeur), dtype=int)
    terrain[bruit > seuil_bas] = PRAIRIE
    terrain[bruit > seuil_haut] = FORET
    return terrain


#if __name__ == "__main__":
 #   print(creer_terrain_lisse(10, 5))
    
if __name__ == "__main__":
    terrain = creer_terrain_lisse(60, 40)
    print("aride  :", np.sum(terrain == ARIDE))
    print("prairie:", np.sum(terrain == PRAIRIE))
    print("forêt  :", np.sum(terrain == FORET))