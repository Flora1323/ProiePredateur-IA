import random

def distance(x1, y1, x2, y2): #distance de Manhattan
    return abs(x1 - x2) + abs(y1 - y2)

def signe(n):
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0

class Lapin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energie = 100

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
    
class Renard:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energie = 100
        self.vision = 5

    def agir(self, lapins, largeur, hauteur):
        proches = [l for l in lapins if distance(self.x, self.y, l.x, l.y) <= self.vision]

        if proches:
            cible = min(proches, key=lambda l: distance(self.x, self.y, l.x, l.y))
            self.x += signe(cible.x - self.x)
            self.y += signe(cible.y - self.y)
        else:
            self.x += random.choice([-1, 0, 1])
            self.y += random.choice([-1, 0, 1])

        self.x = max(0, min(self.x, largeur - 1))
        self.y = max(0, min(self.y, hauteur - 1))
        self.energie -= 1

    def manger(self, lapins):
        for lapin in lapins:
            if lapin.x == self.x and lapin.y == self.y:
                self.energie += 40
                lapin.energie = 0

    def est_vivant(self):
        return self.energie > 0

if __name__ == "__main__":
    lapin = Lapin(30, 20)
    for _ in range(10):
        lapin.deplacer_au_hasard(60, 40)
        print(lapin.x, lapin.y)