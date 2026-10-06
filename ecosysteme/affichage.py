import pygame
from environment import creer_terrain_lisse, ARIDE, PRAIRIE, FORET

COULEURS = {
    ARIDE: (210, 180, 120),   # beige
    PRAIRIE: (120, 200, 80),  # vert clair
    FORET: (30, 110, 40),     # vert foncé
}

TAILLE_CASE = 12
LARGEUR = 60
HAUTEUR = 40

terrain = creer_terrain_lisse(LARGEUR, HAUTEUR)

pygame.init()
fenetre = pygame.display.set_mode((LARGEUR * TAILLE_CASE, HAUTEUR * TAILLE_CASE))

en_cours = True
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    fenetre.fill((0, 0, 0))
    for y in range(HAUTEUR):
        for x in range(LARGEUR):
            couleur = COULEURS[terrain[y][x]]
            pygame.draw.rect(fenetre, couleur, (x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
    pygame.display.flip()

pygame.quit()

