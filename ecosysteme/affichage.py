import pygame
from environment import (
    creer_terrain_lisse, ARIDE, PRAIRIE, FORET,
    creer_nourriture, faire_repousser, NOURRITURE_MAX,
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

en_cours = True
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    nourriture = faire_repousser(nourriture, terrain)

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        case_x = mx // TAILLE_CASE
        case_y = my // TAILLE_CASE
        if 0 <= case_x < LARGEUR and 0 <= case_y < HAUTEUR:
            nourriture[case_y, case_x] = 0

    fenetre.fill((0, 0, 0))
    for y in range(HAUTEUR):
        for x in range(LARGEUR):
            type_terrain = terrain[y, x]
            ratio = nourriture[y, x] / NOURRITURE_MAX[type_terrain]
            couleur = melanger(COULEURS_VIDE[type_terrain], COULEURS[type_terrain], ratio)
            pygame.draw.rect(fenetre, couleur, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

    pygame.display.flip()
    horloge.tick(30)

pygame.quit()