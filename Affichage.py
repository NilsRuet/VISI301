###############################
# Contient l'ensemble des classes uniquement utilisées
# pour l'affichage des éléments du jeu

import pygame
from Options import *

class Coords:
    #Classe permettant de créer un objet contenant des coordonnées
    #En plus d'isoler cette caractéristique, permet d'accéder plus instinctivement
    #aux coordonnées selon les axes horizontaux et verticaux, en nommant les valeurs xi et yi
    def __init__(self, xF, yF):
        self.xi = xF
        self.yi = yF

class Affichage_jeu:
    #Classe regroupant les caractéristiques de l'affichage du jeu
    def __init__(self, coordsF, taille_caseF):
        self.coords = coordsF
        #Coordonnées "de départ" pour afficher le jeu
        self.taille_case = taille_caseF
        #Taille des cases du jeu

class Affichage_carte:
    #Classe regroupant les caractéristiques de la carte
    def __init__(self, coordsF, taille_pieceF):
        self.coords = coordsF
        #Coordonnées "de départ" pour afficher la carte
        self.taille_piece = taille_pieceF
        #Taille des cases de la carte
        
class Affichage:
    #Initialisation de la fenêtre
    TAILLE_ECRAN = (1000, 500) #largeur / hauteur
    ECRAN = pygame.display.set_mode(TAILLE_ECRAN)

    #Initialisation des caractéristiques d'affichage du jeu                       
    X_JEU, Y_JEU = 0, 0
    #Le jeu est affiché en haut à gauche de la fenêtre
    largeur_case = ((TAILLE_ECRAN[0]//2)//OptJeu.NB_CASES)
    #La taille d'une case est prévue pour que le jeu soit affiché sur la moitié (horizontalement) de la fenêtre
    JEU = Affichage_jeu(Coords(X_JEU, Y_JEU), (largeur_case,largeur_case))

    #Initialisation des caractéristiques d'affichage de la carte
    X_CARTE, Y_CARTE = ((TAILLE_ECRAN[0])//2)+1,0
    #La carte est affichée à partir du milieu de la fenêtre horizontalement, collée en haut de la fenêtre
    largeur_piece = (TAILLE_ECRAN[0]//2)//OptJeu.TAILLE_LABYRINTHE
    #La taille d'une case est prévue pour que l'affichage de la carte se fasse sur une moitié horizontale de la fenêtre
    CARTE = Affichage_carte(Coords(X_CARTE, Y_CARTE), (largeur_piece,largeur_piece))

    
