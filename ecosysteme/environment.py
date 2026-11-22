from enum import Enum
import numpy as np


ARIDE = 0
PRAIRIE = 1
FORET = 2

NOURRITURE_MAX = np.array([20, 60, 100])   # aride, prairie, forêt
VITESSE_REPOUSSE = np.array([0.1, 0.3, 0.6])  # vitesse de repousse initiale : ([0.5, 1, 2]), je change pour les tests

## Classe Meteo pour gerer les variations selon un type de météo (pluie, normale, sécheresse)
class Meteo(Enum):
    PLUIE = ("Pluie", 1.5, 0.1, -0.005)
    NORMALE = ("Normale", 1.0, 0.0, 0.0)
    SECHERESSE = ("Secheresse", 0.25, -0.3, 0.01)

    def __init__(self, nom, facteur_meteo, variation_eau, variation_temperature):
        self.nom = nom
        self.facteur_meteo = facteur_meteo
        self.variation_eau = variation_eau
        self.variation_temperature = variation_temperature

EAU_MAX = 100.0
TEMPERATURE_MIN = -10.0
TEMPERATURE_MAX = 50.0
TEMPERATURE_OPTIMALE = 20.0
ECART_TEMPERATURE_CONFORTE = 5.0


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

# Mise à jour de la météo
# Applique les variations selon le type de méteo choisi
def mettre_a_jour_meteo(eau, temperature, meteo):
    if not isinstance(meteo, Meteo):
        raise ValueError(f"Meteo inconnue : {meteo}")

    eau = np.clip(eau + meteo.variation_eau, 0, EAU_MAX)
    temperature = np.clip(
        temperature + meteo.variation_temperature,
        TEMPERATURE_MIN,
        TEMPERATURE_MAX,
    )
    return eau, float(temperature)

# Calcul le facteur de croissance de la végétation en fonction de la température
# Plus la température est proche de la température optimale, plus le facteur est élevé
# Par exemple, si la température est de 20°C, le facteur est de 1.0
# Si la température est de 10°C ou 30°C, le facteur est de 0.75
# Si la température est de 0°C ou 40°C, le facteur est de 0.5
def calcul_facteur_temperature_vegetation(temperature):
    ecart = abs(temperature - TEMPERATURE_OPTIMALE)
    reduction = max(0, ecart - ECART_TEMPERATURE_CONFORTE) / 20
    return np.clip(1 - reduction, 0, 1)

# Calcul la penalité energie à donner aux angents en fonction de la température actulle
# En dehors de la zone de confort, l'energie diminue plus vite
def calcul_penalite_energie_temperature(temperature):
    ecart = abs(temperature - TEMPERATURE_OPTIMALE)
    depassement = max(0, ecart - ECART_TEMPERATURE_CONFORTE)
    return depassement * 0.05

# En prenant en compte les facteurs de météo, d'eau et de température, cette fonction fait repousser la nourriture sur le terrain
def faire_repousser(
    nourriture,
    terrain,
    facteur_meteo=1.0,
    eau=None,
    temperature=TEMPERATURE_OPTIMALE,
):
    maximums = NOURRITURE_MAX[terrain]
    vitesse = (
        VITESSE_REPOUSSE[terrain]
        * facteur_meteo
        * calcul_facteur_temperature_vegetation(temperature)
    )
    if eau is not None:
        vitesse = vitesse * (eau / EAU_MAX)
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