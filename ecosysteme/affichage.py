import random
import numpy as np
import pygame
from environment import (
    creer_terrain_lisse, ARIDE, PRAIRIE, FORET,
    creer_nourriture, faire_repousser, NOURRITURE_MAX,
    Meteo, mettre_a_jour_meteo,
)
from agents import (
    Lapin, Renard
)

COULEURS = {
    ARIDE: (210, 180, 120),
    PRAIRIE: (120, 200, 80),
    FORET: (30, 110, 40),
}

COULEURS_VIDE = {
    ARIDE: (225, 205, 165),
    PRAIRIE: (190, 190, 140),
    FORET: (150, 160, 120),
}

TAILLE_CASE = 12
LARGEUR = 60
HAUTEUR = 40


def melanger(c1, c2, ratio):
    return (
        int(c1[0] + (c2[0] - c1[0]) * ratio),
        int(c1[1] + (c2[1] - c1[1]) * ratio),
        int(c1[2] + (c2[2] - c1[2]) * ratio),
    )


pygame.init()
horloge = pygame.time.Clock()
fenetre = pygame.display.set_mode((LARGEUR * TAILLE_CASE, HAUTEUR * TAILLE_CASE))

terrain = creer_terrain_lisse(LARGEUR, HAUTEUR)
nourriture = creer_nourriture(terrain)
eau = np.full(terrain.shape, 100.0)
temperature = 20.0
meteo = Meteo.NORMALE
police = pygame.font.Font(None, 20)

lapins = []
for _ in range(50): #changer le nombre de lapins
    lapins.append(Lapin(random.randint(0, LARGEUR - 1), random.randint(0, HAUTEUR - 1)))
    
renards = []
for _ in range(10):
    renards.append(Renard(random.randint(0, LARGEUR - 1), random.randint(0, HAUTEUR - 1)))

en_cours = True
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_1:
                meteo = Meteo.PLUIE
            elif evenement.key == pygame.K_2:
                meteo = Meteo.NORMALE
            elif evenement.key == pygame.K_3:
                meteo = Meteo.SECHERESSE

    eau, temperature = mettre_a_jour_meteo(eau, temperature, meteo)
    nourriture = faire_repousser(
        nourriture, terrain, meteo.facteur_meteo, eau, temperature
    )

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        case_x = mx // TAILLE_CASE
        case_y = my // TAILLE_CASE
        if 0 <= case_x < LARGEUR and 0 <= case_y < HAUTEUR:
            nourriture[case_y, case_x] = 0

    for lapin in lapins:
        lapin.deplacer_au_hasard(LARGEUR, HAUTEUR, temperature)
        lapin.manger(nourriture)

    for renard in renards:
        renard.agir(lapins, LARGEUR, HAUTEUR, temperature)
        renard.manger(lapins)

    lapins = [lapin for lapin in lapins if lapin.est_vivant()]
    renards = [renard for renard in renards if renard.est_vivant()]
    print(len(lapins), len(renards))

    fenetre.fill((0, 0, 0))
    for y in range(HAUTEUR):
        for x in range(LARGEUR):
            type_terrain = terrain[y, x]
            ratio = nourriture[y, x] / NOURRITURE_MAX[type_terrain]
            couleur = melanger(COULEURS_VIDE[type_terrain], COULEURS[type_terrain], ratio)
            pygame.draw.rect(fenetre, couleur, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

    for lapin in lapins:
        pixel_x = lapin.x * TAILLE_CASE + TAILLE_CASE // 2
        pixel_y = lapin.y * TAILLE_CASE + TAILLE_CASE // 2
        ratio = min(lapin.energie / 100, 1)
        couleur_lapin = melanger((220, 0, 0), (255, 255, 255), ratio)
        pygame.draw.circle(fenetre, couleur_lapin, (pixel_x, pixel_y), 4)

    for renard in renards:
        pixel_x = renard.x * TAILLE_CASE + TAILLE_CASE // 2
        pixel_y = renard.y * TAILLE_CASE + TAILLE_CASE // 2
        ratio = min(renard.energie / 100, 1)
        couleur_renard = melanger((120, 60, 0), (230, 120, 20), ratio)
        pygame.draw.circle(fenetre, couleur_renard, (pixel_x, pixel_y), 5)

    # Affichage des informations sur la météo
    meteo_texte = (
        f"{meteo.nom} - {temperature:.1f} C"
        f" - Eau moyenne : {np.mean(eau):.0f}%"
    )
    aide_texte = "1: Pluie   2: Normale   3: Secheresse"
    pygame.draw.rect(fenetre, (255, 255, 255), (4, 4, 265, 38))
    fenetre.blit(police.render(meteo_texte, True, (0, 0, 0)), (8, 6))
    fenetre.blit(police.render(aide_texte, True, (0, 0, 0)), (8, 23))

    pygame.display.flip()
    horloge.tick(30)

pygame.quit()