import pygame
import random
from Class_Persos import Perso, Joueur, Ennemi
pygame.init()

TAILLE_LABYRINTHE = 3
TAILLE_ECRAN = (500, 500) #largeur / hauteur
TAILLE_CASE = (50, 50)
NB_CASES = 10
ECRAN = pygame.display.set_mode(TAILLE_ECRAN)
#Pour l'instant ce sont des constantes, mais peut etre pas dans la version finale


class Piece:
    listePieces=[]
            
    def __init__(self, numPieceF, typePiece, iF, jF):
    #constructeur
        self.numPiece=numPieceF
        self.typePiece=typePiece
        self.vue=False
        self.i = iF
        self.j = jF

    def initTempListePieces():
        #Generation temporaire de la carte globale
        numeroActuel=0
        while numeroActuel != TAILLE_LABYRINTHE**2-1:
            i_init = (numeroActuel/TAILLE_LABYRINTHE)*2
            j_init = (numeroActuel%TAILLE_LABYRINTHE)*2
            Piece.listePieces.append(Piece(numeroActuel, "type_test", i_init, j_init))
            numeroActuel+=1


    def revele(self):
        if not self.numPiece in CarteUnePiece.cartesChargees:
            CarteUnePiece(self.numPiece)
            self.vue=True;

    
        


class CarteUnePiece:
    cartesChargees = {}
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
                self.carte[colonne][ligne] = Case(1)
                #Chaque cellule de la carte est une case
                #Ici, pour l'exemple, on appelle le constructeur de la case avec 0 ou 1

        #Lecture des murs
        self.carte[1][1].typeCase = -((self.numPiece+1)%TAILLE_LABYRINTHE**2)
        
        CarteUnePiece.cartesChargees[self.numPiece]=self
        
        
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
        if self.typeCase < 0:
            pygame.draw.rect(ECRAN, (0,255,0), (hauteur*colonneF, largeur*ligneF, hauteur, largeur))
        else:
            pygame.draw.rect(ECRAN, couleur, (hauteur*colonneF, largeur*ligneF, hauteur, largeur))
    



def redrawGameWindow():
    #affichage carte
    CarteUnePiece.cartesChargees[perso.piece_actuelle].affiche_carte()
    #affichage perso
    perso.affichage(ECRAN,TAILLE_CASE)
    
    pygame.display.update()






####################################################################################
#boucle principale
perso = Joueur(0,0,TAILLE_CASE[0],TAILLE_CASE[1])
continuer = True

testCarteGlobale = Piece.initTempListePieces()

Piece.listePieces[perso.piece_actuelle].revele()

while continuer :


    #events
    for event in pygame.event.get() :
        #Fermeture de la fenêtre
        if event.type == pygame.QUIT:
            continuer = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = (-1,0)
            if event.key == pygame.K_RIGHT:
                direction = (1,0)
            if event.key == pygame.K_UP:
                direction = (0,-1)
            if event.key == pygame.K_DOWN:
                direction = (0,1)
            perso.move(direction[0],direction[1],NB_CASES,CarteUnePiece.cartesChargees[perso.piece_actuelle].carte)

    redrawGameWindow()
        
            
pygame.quit()
