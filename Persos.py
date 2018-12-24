import pygame
import time
from Options import *
from Affichage import *


class Perso():
    directions={"BAS":[0,1],"DROITE":[1,0],"HAUT":[0,-1],"GAUCHE":[-1,0]}
    
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.direction = "BAS"
        self.width = width
        self.height = height
        self.last_mvt = 0
        #stockage du temps du dernier mouvement pour gestion de la vitesse de dépacement
        self.vitesse = 100 #nombre de millisecondes entre chaque déplacement

class Joueur(Perso):
    VIE_DEPART=100
    def __init__(self,x,y,width,height,pieceF=1):
        Perso.__init__(self,x,y,width,height)
        self.vie = Joueur.VIE_DEPART
        self.piece_actuelle = pieceF

    def move(self,piece):
        autoriser_mouvement = True
        dx=Perso.directions[self.direction][0]
        dy=Perso.directions[self.direction][1]
        
        #Gestion de la vitesse de déplacement
        if (pygame.time.get_ticks() - self.last_mvt) < self.vitesse:
            autoriser_mouvement = False
        
        #Gestion des collisions
        if not 0 <= self.x+dx < OptJeu.NB_CASES:
            autoriser_mouvement = False
            
        elif not 0 <= self.y+dy < OptJeu.NB_CASES:
            autoriser_mouvement = False

        else:
            if piece[self.x+dx][self.y+dy].typeCase == 0: 
                autoriser_mouvement = False

        #Deplacement du personnage
        if autoriser_mouvement:
             self.x = self.x + dx
             self.y = self.y + dy             
             self.last_mvt = pygame.time.get_ticks()

             #Gestion des changements de pièce
             if piece[self.x][self.y].typeCase<0:
                 self.piece_actuelle = -piece[self.x][self.y].typeCase
                 self.x = (OptJeu.NB_CASES-1)-self.x
                 self.y = (OptJeu.NB_CASES-1)-self.y

    def sortie_atteinte(self, num_sortie):
        return self.piece_actuelle==num_sortie

    def affichage(self):
        rectangle = (self.x*Affichage.JEU.taille_case[0] + Affichage.JEU.coords.xi, self.y*Affichage.JEU.taille_case[1] + Affichage.JEU.coords.yi, self.width, self.height)
        pygame.draw.rect(Affichage.ECRAN, (255, 0, 0), rectangle)

class Ennemi(Perso):
    VIE_DEPART=10
    def __init__(self,x,y,width,height):
        Perso.__init__(self,x,y,width,height)
        self.vie = Ennemi.VIE_DEPART

    def affiche(self):
        rectangle = (self.x*Affichage.JEU.taille_case[0] + Affichage.JEU.coords.xi, self.y*Affichage.JEU.taille_case[1] + Affichage.JEU.coords.yi, self.width, self.height)
        pygame.draw.rect(Affichage.ECRAN, (0, 127, 0), rectangle)
