##############################################################################################
# Fichiers contenant les classes relatives aux personnages du jeu comme le joueur, les ennemis

import pygame
from Options import *
from Affichage import *
from Piece import *

class Perso():
    #Classe de base pour tous les personnages mobiles
    directions={"BAS":[0,1],"DROITE":[1,0],"HAUT":[0,-1],"GAUCHE":[-1,0]}
    
    def __init__(self,x,y,width,height,vitesse):
        self.x = x
        self.y = y
        self.direction = "BAS"
        self.width = width
        self.height = height
        self.last_mvt = 0
        #stockage du temps du dernier mouvement pour gestion de la vitesse de dépacement
        self.vitesse = vitesse #nombre de millisecondes entre chaque déplacement

        #Chaque personnage mobile possède des coordonnées dans une pièce, une direction, une largeur et une hauteur (affichage) (à déplacer)
        #On connaît moment où son dernier mouvement a été effectué ainsi que sa vitesse

    def case_valide(x, y, piece):
        #Méthode permettant de savoir si une case dans une pièce autorise des personnages à se déplacer dessus
        autoriser_mouvement=True
        if not 0 <= x < OptJeu.NB_CASES:
            autoriser_mouvement = False
            
        elif not 0 <= y < OptJeu.NB_CASES:
            autoriser_mouvement = False

        else:
            if piece.carte[x][y].collision: 
                autoriser_mouvement = False
        
        #On vérifie que la case ne contient pas un ennemi
        i=0
        while i<len(piece.ennemis) and autoriser_mouvement:
            autoriser_mouvement = not (piece.ennemis[i].x==x and piece.ennemis[i].y==y)
            i+=1
            
        return autoriser_mouvement

class Joueur(Perso):
    #Personnage joué par l'utilisateur
    
    VIE_DEPART=100
    VITESSE=100
    #Vie de départ du joueur

    def __init__(self,x,y,width,height,pieceF=1):
        Perso.__init__(self,x,y,width,height,Joueur.VITESSE)
        #Un joueur les mêmes caractéristiques que tous les personages mobiles
        self.max_vie = Joueur.VIE_DEPART
        self.vie = Joueur.VIE_DEPART
        #En plus d'un nombre de points de vie
        self.piece_actuelle = pieceF
        #Et du numéro de la pièce dans laquelle il se trouve
    
    def move(self,piece):
        #Méthode permettant de bouger le personnage
        autoriser_mouvement = True
        #Booléen mis à faux si le déplacement est impossible
        
        dx=Perso.directions[self.direction][0]
        dy=Perso.directions[self.direction][1]
        #dx et dy représentent la position relative au joueur de la case vers laquelle il veut se déplacer
        
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
        #Méthode qui détecte si le joueur a atteint la sortie du labyrinthe
        return self.piece_actuelle==num_sortie

    def affichage_vie(self):
        rect_vie=(Affichage.VIE.coords.xi, Affichage.VIE.coords.yi, int(Affichage.VIE.largeur*(self.vie/self.max_vie)), Affichage.VIE.hauteur)
        pygame.draw.rect(Affichage.ECRAN, (0, 127, 0), rect_vie)
        
    def affichage(self):
        #Méthode d'affichage du joueur
        rectangle = (self.x*Affichage.JEU.taille_case[0] + Affichage.JEU.coords.xi, self.y*Affichage.JEU.taille_case[1] + Affichage.JEU.coords.yi, self.width, self.height)
        pygame.draw.rect(Affichage.ECRAN, (255, 0, 0), rectangle)
    

class Ennemi(Perso):
    #Classe représentant un ennemi, qui attaque le joueur
    VIE_DEPART=10
    ATTAQUE=10
    VITESSE_ATTAQUE=1000
    VITESSE=500
    def case_valide(x,y,piece,joueur):
        #Gestion du déplacement d'un ennemi
        return Perso.case_valide(x,y,piece) and not (joueur.x == x and joueur.y == y)
        #Même conditions que tous les personnages mobiles, mais ne peut pas aller sur la même case qu'un joueur

    
    def __init__(self,x,y,width=Affichage.JEU.taille_case[0],height=Affichage.JEU.taille_case[1]):
        #Création d'un ennemi, avec des valeurs par défaut pour la largeur et la hauteur
        
        Perso.__init__(self,x,y,width,height,Ennemi.VITESSE)
        self.vie = Ennemi.VIE_DEPART
        self.attaque = Ennemi.ATTAQUE
        self.vitesse_attaque = Ennemi.VITESSE_ATTAQUE
        self.last_attaque = 0

    def action(self, piece, joueur):
        #Gestionnaire des actions réalisées par un ennemi
        self.attaquer(joueur)
        self.move(piece, joueur)
        

    def move(self,piece, joueur):
        #Méthode bougeant si possible l'ennemi vers le joueur
        autoriser_mouvement = True

        #Calcul de la direction à prendre pour aller vers le joueur
        distance_x = joueur.x - self.x
        distance_y = joueur.y - self.y

        #On réduit la distance en x si elle est plus élevée que celle en y, et inversement
        if abs(distance_x)>abs(distance_y):
            if distance_x == 0:
                #TODO ce test existe car la génération actuelle des ennemis a une probabilité d'en créer un sous le joueur
                dx=0
            else:                   
                dx = round(distance_x/abs(distance_x))
            dy = 0
        else:
            dx = 0
            if distance_y==0:
                dy=0
            else:
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

    def attaquer(self, joueur):
        if (joueur.x-self.x,joueur.y-self.y) in ((0,1),(0,-1),(1,0),(-1,0)):
            #Si le joueur est sur une case adjacente
            if not ((pygame.time.get_ticks() - self.last_attaque) < self.vitesse_attaque):
                joueur.vie-=self.attaque
                self.last_attaque = pygame.time.get_ticks()

    def affiche(self):
        #Méthode d'affichage d'un ennemi
        rectangle = (self.x*Affichage.JEU.taille_case[0] + Affichage.JEU.coords.xi, self.y*Affichage.JEU.taille_case[1] + Affichage.JEU.coords.yi, self.width, self.height)
        pygame.draw.rect(Affichage.ECRAN, (0, 127, 0), rectangle)
