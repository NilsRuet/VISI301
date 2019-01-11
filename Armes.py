##################################################################################################
# Fichier contenant les classes correspondant aux armes que peut posséder le joueur
import pygame
from math import sqrt
from Persos import *
from Piece import *

class Arme():
    #Classe de base des armes
    def __init__(self, persoF, attaqueF, vit_attaqueF):
        self.owner = persoF
        self.attaque = attaqueF
        self.vitesse_attaque = vit_attaqueF
        #La vitesse d'attaque représente le temps entre chaque coup, si elle augmente l'arme peut attaquer moins souvent
        self.last_attaque = 0
        #Permet de savoir quand a eu lieu la dernière attaque
        
class Melee(Arme):
    #Classe des armes de mélée possèdant une durabilité
    MAX_ATTAQUE_INIT = round(sqrt(1000))
    MIN_ATTAQUE_INIT = 1
    DURABILITE_INIT = 2000
    
    def __init__(self, persoF, attaqueF, vit_attaqueF):
        Arme.__init__(self, persoF, attaqueF, vit_attaqueF)
        self.max_attaque = Melee.MAX_ATTAQUE_INIT
        self.min_attaque = Melee.MIN_ATTAQUE_INIT
        self.durabilite = Melee.DURABILITE_INIT
        self.max_durabilite = Melee.DURABILITE_INIT

    def modifier_attaque(self, montant):
        #Méthode permettant de modifier l'attaque de l'arme
        if self.durabilite>0:
            self.attaque+=montant
            if self.attaque>self.max_attaque:
                #On limite l'attaque à une attaque maximale
                self.attaque=self.max_attaque
            
            if self.attaque<self.min_attaque:
                #On limite l'attaque à une attaque minimale
                self.attaque=self.min_attaque

    def enlever_durabilite(self, attaque):
        #Méthode permettant de réduire la durabilité d'une arme
        #et de gérer les statistiques quand la durabilité atteint 0
        #Chaque fois qu'on attaque et qu'il reste de la durabilité, l'arme perd en durabilité
        if self.durabilite>0:
            self.durabilite -= attaque**2
            #On veut que le cout en durabilité augmente plus rapidement que la puissance d'attaque
            if self.durabilite<=0:
                #Si on a plus de durabilite, l'attaque de l'arme passe au minimum
                #Et la vitesse d'attaque est fortement diminuée
                self.durabilite=0
                self.vitesse_attaque*=2
                self.attaque=self.min_attaque

    def restaurer_durabilite(self):
        #Méthode permettant de restaurer la durabilité de l'arme
        #et de remettre ses statistiques normales si sa durabilité était nulle
        if self.durabilite<=0:
            self.vitesse_attaque=self.vitesse_attaque//2
        self.durabilite = self.max_durabilite
        self.attaque = (self.max_attaque+self.min_attaque)//4
        
    def attaquer(self):
        #Méthode les effets d'une attaque
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
                self.enlever_durabilite(self.attaque)
                if ennemi.vie<=0:
                    ennemi.meurt()
                    self.owner.points+=1

        
    def afficher_statistiques(self):
        #Méthode d'affichage des caractéristiques de l'arme
        x_dura,y_dura,largeur_dura,hauteur_dura=Affichage.DURABILITE.coords.xi, Affichage.DURABILITE.coords.yi, Affichage.DURABILITE.largeur, Affichage.DURABILITE.hauteur
        pygame.draw.rect(Affichage.ECRAN, (200, 64, 0),Affichage.rectangle_barre_progressive(x_dura, y_dura, largeur_dura, hauteur_dura, self.durabilite, self.max_durabilite))

        x_att,y_att,largeur_att,hauteur_att=Affichage.ATTAQUE.coords.xi, Affichage.ATTAQUE.coords.yi, Affichage.ATTAQUE.largeur, Affichage.ATTAQUE.hauteur
        pygame.draw.rect(Affichage.ECRAN, (200, 0, 0),Affichage.rectangle_barre_progressive(x_att,y_att,largeur_att,hauteur_att, self.attaque, self.max_attaque, self.min_attaque))
    
