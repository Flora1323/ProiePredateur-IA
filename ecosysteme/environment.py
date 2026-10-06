import numpy as np



ARIDE = 0
PRAIRIE = 1
FORET = 2 

def creer_terrain(largeur, hauteur):
    terrain = np.random.randint(0, 3, size=(hauteur, largeur)) #on met 3 pour avoir 2 au max
    return terrain


# Test
print(creer_terrain(10, 5))
