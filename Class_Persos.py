import pygame

class Perso():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5

    def affichage(self,ECRAN):
        pygame.draw.rect(ECRAN, (255, 0, 0), (x, y, width, height))

class Joueur(Perso):
    def __init__(self,x,y,width,height):
        Perso.__init__(self,x,y,width,height)

class Ennemi(Perso):
    def __init__(self,x,y,width,height):
        Perso.__init__(self,x,y,width,height)
