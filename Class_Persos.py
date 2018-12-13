import pygame

class Perso():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.direction = [0,0]
        self.width = width
        self.height = height
        self.vitesse = 5

    def affichage(self,ECRAN,TAILLE_CASE):
        pygame.draw.rect(ECRAN, (255, 0, 0), (self.x*TAILLE_CASE[0], self.y*TAILLE_CASE[1], self.width, self.height))

    def move(self,NB_CASES,piece):
        autoriser_mouvement = True
        dx=self.direction[0]
        dy=self.direction[1]
        if not 0 <= self.x+dx < NB_CASES:
            autoriser_mouvement = False
            
        elif not 0 <= self.y+dy < NB_CASES:
            autoriser_mouvement = False

        else:
            if piece[self.x+dx][self.y+dy].typeCase == 0: 
                autoriser_mouvement = False

            if piece[self.x+dx][self.y+dy].typeCase<0:
                self.piece_actuelle = -piece[self.x+dx][self.y+dy].typeCase
        
        if autoriser_mouvement:
             self.y = self.y + dy
             self.x = self.x + dx

class Joueur(Perso):
    def __init__(self,x,y,width,height,pieceF=1):
        Perso.__init__(self,x,y,width,height)
        self.piece_actuelle = pieceF

class Ennemi(Perso):
    def __init__(self,x,y,width,height):
        Perso.__init__(self,x,y,width,height)
