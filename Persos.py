import pygame
import time
from Options import *
from Affichage import *
from Piece import *

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

    def case_valide(x, y, piece):
        autoriser_mouvement=True
        if not 0 <= x < OptJeu.NB_CASES:
            autoriser_mouvement = False
            
        elif not 0 <= y < OptJeu.NB_CASES:
            autoriser_mouvement = False

        else:
            if piece.carte[x][y].collision: 
                autoriser_mouvement = False
        return autoriser_mouvement

class Joueur(Perso):
    VIE_DEPART=100
    def case_valide(x, y, piece):
        est_ennemi = False
        i=0
        #On vérifie que la case ne contient pas un ennemi
        while i<len(piece.ennemis) and not est_ennemi:
            est_ennemi = (piece.ennemis[i].x==x and piece.ennemis[i].y==y)
            i+=1
        return Perso.case_valide(x, y, piece) and not est_ennemi
    
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
        
        else:
            #Gestion des collisions
            autoriser_mouvement = Joueur.case_valide(self.x+dx, self.y+dy,piece)
            
        #Deplacement du personnage
        if autoriser_mouvement:
            self.x = self.x + dx
            self.y = self.y + dy             
            self.last_mvt = pygame.time.get_ticks()

            #Gestion des changements de pièce
            if piece.carte[self.x][self.y].typeCase<0:
                self.piece_actuelle = -piece.carte[self.x][self.y].typeCase
                self.x = (OptJeu.NB_CASES-1)-self.x
                self.y = (OptJeu.NB_CASES-1)-self.y

    def sortie_atteinte(self, num_sortie):
        return self.piece_actuelle==num_sortie

    def affichage(self):
        rectangle = (self.x*Affichage.JEU.taille_case[0] + Affichage.JEU.coords.xi, self.y*Affichage.JEU.taille_case[1] + Affichage.JEU.coords.yi, self.width, self.height)
        pygame.draw.rect(Affichage.ECRAN, (255, 0, 0), rectangle)

class Ennemi(Perso):
    VIE_DEPART=10
    def __init__(self,x,y,width=Affichage.JEU.taille_case[0],height=Affichage.JEU.taille_case[1]):
        Perso.__init__(self,x,y,width,height)
        self.vie = Ennemi.VIE_DEPART
        self.vitesse = 500

    def move(self,piece, joueur):
        autoriser_mouvement = True

        #Calcul de la direction à prendre pour aller vers le joueur
        distance_x = joueur.x - self.x
        distance_y = joueur.y - self.y
        if abs(distance_x)>abs(distance_y):
            dx = round(distance_x/abs(distance_x))
            dy = 0
        else:
            dx = 0
            dy = round(distance_y/abs(distance_y))
            
        #Gestion de la vitesse de déplacement
        if (pygame.time.get_ticks() - self.last_mvt) < self.vitesse:
            autoriser_mouvement = False       
        
        else:
            #Gestion des collisions
            autoriser_mouvement = Ennemi.case_valide(self.x+dx,self.y+dy,piece,joueur)
            
        #Deplacement du personnage
        if autoriser_mouvement:
            self.x = self.x + dx
            self.y = self.y + dy             
            self.last_mvt = pygame.time.get_ticks()

    def case_valide(x,y,piece,joueur):
        return Perso.case_valide(x,y,piece) and not (joueur.x == x and joueur.y == y)

    def affiche(self):
        rectangle = (self.x*Affichage.JEU.taille_case[0] + Affichage.JEU.coords.xi, self.y*Affichage.JEU.taille_case[1] + Affichage.JEU.coords.yi, self.width, self.height)
        pygame.draw.rect(Affichage.ECRAN, (0, 127, 0), rectangle)
