import numpy as np

ARIDE = 0
PRAIRIE = 1
FORET = 2

NOURRITURE_MAX = np.array([20, 60, 100])   # aride, prairie, forêt
VITESSE_REPOUSSE = np.array([0.1, 0.3, 0.6])  # vitesse de repousse initiale : ([0.5, 1, 2]), je change pour les tests


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


def creer_nourriture(terrain):
    maximums = NOURRITURE_MAX[terrain]
    return maximums


def faire_repousser(nourriture, terrain, facteur_meteo=1.0):
    maximums = NOURRITURE_MAX[terrain]
    vitesse = VITESSE_REPOUSSE[terrain] * facteur_meteo
    nourriture = np.minimum(nourriture + vitesse, maximums)
    return nourriture


if __name__ == "__main__":
    terrain = creer_terrain_lisse(10, 5)
    nourriture = creer_nourriture(terrain)
    nourriture[:, :] = 0   # on vide toute la carte
    for tour in range(10):
        nourriture = faire_repousser(nourriture, terrain)
    print(terrain)
    print(nourriture)