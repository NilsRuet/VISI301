import pygame
import random
pygame.init()

TAILLE_ECRAN = (1000, 1000)
TAILLE_CASE = (100, 100)
NB_CASES = 10
ECRAN = pygame.display.set_mode(TAILLE_ECRAN)
#Pour l'instant ce sont des constantes, mais peut etre pas dans la version finale

continuer = True #Mis à faux quand on ferme la fenêtre



class CarteUnePiece:
    def __init__(self, numPieceF):
    #constructeur
        self.numPiece=numPieceF

        #On initialise un tableau de NB_CASES*NB_CASES qui sera remplit de cases
        self.carte=[[0]]*NB_CASES
        for colonne in range(len(self.carte)):
            self.carte[colonne]=[0]*NB_CASES
        #Ici, initialisé avec des 0 dans toutes les cellules parce que je ne sais pas comment initialiser une liste vide
            
        for colonne in range(len(self.carte)):
            for ligne in range(len(self.carte[0])):
                self.carte[colonne][ligne] = Case(random.randint(0,1))
                #Chaque cellule de la carte est une case
                #Ici, pour l'exemple, on appelle le constructeur de la case avec 0 ou 1
        
    def affiche_carte(self):
        #Méthode d'affichage de la grille
        for colonne in range(len(self.carte)):
            for ligne in range(len(self.carte[0])):
                self.carte[colonne][ligne].affiche_case(colonne, ligne)

class Case:
    def __init__(self, typeCaseF):
        self.typeCase = typeCaseF

    def affiche_case(self, colonneF, ligneF):
        #Pour l'instant on affiche un rectangle d'une certaine couleur pour représenter la case
        hauteur, largeur = TAILLE_CASE[0], TAILLE_CASE[1]
        couleur = (self.typeCase*250, self.typeCase*250, self.typeCase*250)
        #On considère ici que la case vaut 0 ou 1, on affiche noir ou (presque) blanc
        pygame.draw.rect(ECRAN, couleur, (hauteur*colonneF, largeur*ligneF, hauteur, largeur))


#########################################################################################
# Programme principal
carte_test=CarteUnePiece(0)
while continuer:
    carte_test.affiche_carte()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0
    pygame.display.flip()
     
pygame.quit()
