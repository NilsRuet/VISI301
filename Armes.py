##################################################################################################
# Fichier contenant les classes correspondant aux armes que peut posséder ke joueur
import pygame

from Persos import *
from Piece import *

class Arme():
    #Classe de base des armes
    def __init__(self, persoF, attaqueF, vit_attaqueF):
        self.owner = persoF
        self.attaque = attaqueF
        self.vitesse_attaque = vit_attaqueF
        self.last_attaque = 0

class Melee(Arme):
    #Classe correspondant à une arme à courte portée
    def __init__(self, persoF, attaqueF, vit_attaqueF):
        Arme.__init__(self, persoF, attaqueF, vit_attaqueF)

    def attaquer(self):
        if pygame.time.get_ticks() - self.last_attaque > self.vitesse_attaque:
            x_case_att = self.owner.x + Perso.directions[self.owner.direction][0]
            y_case_att = self.owner.y + Perso.directions[self.owner.direction][1]
            #On récupère les coordonnées de la case vers laquelle est tournée le joueur
            piece = CarteUnePiece.cartesChargees[self.owner.piece_actuelle]
            #On récupère la pièce dans laquelle se trouve le perso qui possède l'arme

            ennemi = piece.ennemis.get((x_case_att, y_case_att))
            if ennemi!=None:
                ennemi.vie-=self.attaque
                self.last_attaque = pygame.time.get_ticks()
                if ennemi.vie<=0:
                    ennemi.meurt()
    
