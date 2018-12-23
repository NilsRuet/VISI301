import pygame
import time
from Affichage import *


class Perso():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.direction = [0,0]
        self.width = width
        self.height = height
        self.last_mvt = time.time()
        #stockage du temps du dernier mouvement pour gestion de la vitesse de dépacement
        self.vitesse = 0.1 #nombre de secondes entre chaque déplacement

    def affichage(self):
        rectangle = (self.x*Affichage.JEU.taille_case[0] + Affichage.JEU.coords.xi, self.y*Affichage.JEU.taille_case[1] + Affichage.JEU.coords.yi, self.width, self.height)
        pygame.draw.rect(Affichage.ECRAN, (255, 0, 0), rectangle)

    def move(self,nb_cases,piece):
        autoriser_mouvement = True
        dx=self.direction[0]
        dy=self.direction[1]
        
        #Gestion des collisions
        if not 0 <= self.x+dx < nb_cases:
            autoriser_mouvement = False
            
        elif not 0 <= self.y+dy < nb_cases:
            autoriser_mouvement = False

        else:
            if piece[self.x+dx][self.y+dy].typeCase == 0: 
                autoriser_mouvement = False

            if piece[self.x+dx][self.y+dy].typeCase<0:
                self.piece_actuelle = -piece[self.x+dx][self.y+dy].typeCase
                
        #Gestion de la vitesse de déplacement
        if (time.time() - self.last_mvt) < self.vitesse:
            autoriser_mouvement = False

        if autoriser_mouvement:
             self.y = self.y + dy
             self.x = self.x + dx
             self.last_mvt = time.time()

    def sortie_atteinte(self, num_sortie):
        return self.piece_actuelle==num_sortie

class Joueur(Perso):
    def __init__(self,x,y,width,height,pieceF=1):
        Perso.__init__(self,x,y,width,height)
        self.piece_actuelle = pieceF

class Ennemi(Perso):
    def __init__(self,x,y,width,height):
        Perso.__init__(self,x,y,width,height)
