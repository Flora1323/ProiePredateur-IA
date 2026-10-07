import random


class Lapin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energie = 50

    def deplacer_au_hasard(self, largeur, hauteur):
        self.x = self.x + random.choice([-1, 0, 1])
        self.y = self.y + random.choice([-1, 0, 1])
        self.x = max(0, min(self.x, largeur - 1))
        self.y = max(0, min(self.y, hauteur - 1))
        self.energie -= 2
    
    def manger(self, nourriture):
        quantite = min(10, nourriture[self.y, self.x])   # il mange 10 maximum, ou ce qu'il reste
        nourriture[self.y, self.x] -= quantite           # la case perd ce qu'il a mangé
        self.energie += quantite                         # le lapin le gagne      

    def est_vivant(self):
        return self.energie > 0

if __name__ == "__main__":
    lapin = Lapin(30, 20)
    for _ in range(10):
        lapin.deplacer_au_hasard(60, 40)
        print(lapin.x, lapin.y)