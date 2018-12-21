import pygame
from Options import *
class Coords:
    def __init__(self, xF, yF):
        self.xi = xF
        self.yi = yF

class Affichage_jeu:
    def __init__(self, coordsF, taille_caseF):
        self.coords = coordsF
        self.taille_case = taille_caseF

class Affichage_carte:
    def __init__(self, coordsF, taille_pieceF):
        self.coords = coordsF
        self.taille_piece = taille_pieceF

class Affichage:
    TAILLE_ECRAN = (1000, 500) #largeur / hauteur    
    X_JEU, Y_JEU = 0, 0
    #Pour l'instant ce sont des constantes

    ECRAN = pygame.display.set_mode(TAILLE_ECRAN)
    
    largeur_case = ((TAILLE_ECRAN[0]//2)//OptJeu.NB_CASES)   
    JEU = Affichage_jeu(Coords(X_JEU, Y_JEU), (largeur_case,largeur_case))

    X_CARTE, Y_CARTE = ((TAILLE_ECRAN[0])//2)+1,0
    largeur_piece = (TAILLE_ECRAN[0]//2)//OptJeu.TAILLE_LABYRINTHE
    CARTE = Affichage_carte(Coords(X_CARTE, Y_CARTE), (largeur_piece,largeur_piece))

    
