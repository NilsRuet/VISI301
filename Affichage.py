import pygame
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
    ECRAN = pygame.display.set_mode(TAILLE_ECRAN)
    JEU = Affichage_jeu(Coords(0,0), (50,50))
    CARTE = Affichage_carte(Coords(550,0), (50,50))

    #Pour l'instant ce sont des constantes, mais peut etre pas dans la version finale
