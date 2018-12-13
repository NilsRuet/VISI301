import pygame
import random
from Class_Persos import Perso, Joueur, Ennemi
from genLab import Labyrinthe, Zone
pygame.init()

TAILLE_LABYRINTHE = 3
TAILLE_ECRAN = (500, 500) #largeur / hauteur
TAILLE_CASE = (50, 50)
NB_CASES = 10
ECRAN = pygame.display.set_mode(TAILLE_ECRAN)
#Pour l'instant ce sont des constantes, mais peut etre pas dans la version finale

class Piece:
    listePieces={}
            
    def __init__(self, numPieceF, typePiece, iF, jF):
    #constructeur
        self.numPiece=numPieceF
        self.typePiece=typePiece
        self.vue=False
        self.i = iF
        self.j = jF

##    def initTempListePieces():
##        #Generation temporaire de la carte globale
##        numeroActuel=0
##        while numeroActuel != TAILLE_LABYRINTHE**2-1:
##            i_init = (numeroActuel/TAILLE_LABYRINTHE)*2
##            j_init = (numeroActuel%TAILLE_LABYRINTHE)*2
##            Piece.listePieces.append(Piece(numeroActuel, "type_test", i_init, j_init))
##            numeroActuel+=1

    def initListePieces(labyF):
        #Generation temporaire de la carte globale
        for i in range(0,labyF.taille, 2):
            for j in range(0,labyF.taille, 2):
                Piece.listePieces[labyF.carte[i][j].zone] = Piece(labyF.carte[i][j].zone,"type_test", i, j)


    def revele(self, labyF):
        if not self.numPiece in CarteUnePiece.cartesChargees:
            CarteUnePiece(self.numPiece,labyF)
            self.vue=True;

    
        


class CarteUnePiece:
    cartesChargees = {}
    def __init__(self, numPieceF,labyF):
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
        self.creer_portes(labyF)
        
        CarteUnePiece.cartesChargees[self.numPiece]=self
        
    def creer_portes(self, labyF):
        i_piece = Piece.listePieces[self.numPiece].i
        j_piece = Piece.listePieces[self.numPiece].j
        for coords_murs in ((-1,0),(1,0),(0,1),(0,-1)):
            i_mur = i_piece+coords_murs[0]
            j_mur = j_piece+coords_murs[1]
            if 0<=i_mur<labyF.taille and 0<=j_mur<labyF.taille:
                if not labyF.carte[i_mur][j_mur]:
                    numPieceSuiv = labyF.carte[i_mur+coords_murs[0]][j_mur+coords_murs[1]].zone
                    x_case = (NB_CASES-1)//2 + (coords_murs[1]*((NB_CASES-1)//2))
                    y_case = (NB_CASES-1)//2 + (coords_murs[0]*((NB_CASES-1)//2))
                    #TODO nul
                    self.carte[x_case][y_case].typeCase = -numPieceSuiv
        
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
continuer = True

laby = Labyrinthe(TAILLE_LABYRINTHE)
Piece.initListePieces(laby)

perso = Joueur(0,0,TAILLE_CASE[0],TAILLE_CASE[1])
Piece.listePieces[perso.piece_actuelle].revele(laby)

while continuer :


    #events
    for event in pygame.event.get() :
        #Fermeture de la fenêtre
        if event.type == pygame.QUIT:
            continuer = False
        if event.type == pygame.KEYDOWN:
            touche_move = False
            if event.key == pygame.K_LEFT:
                perso.direction = [-1,0]
                touche_move = True
            if event.key == pygame.K_RIGHT:
                perso.direction = [1,0]
                touche_move = True
            if event.key == pygame.K_UP:
                perso.direction = [0,-1]
                touche_move = True
            if event.key == pygame.K_DOWN:
                perso.direction = [0,1]
                touche_move = True

            if event.key == pygame.K_a:
                laby.print_lab((Piece.listePieces[perso.piece_actuelle].i, Piece.listePieces[perso.piece_actuelle].j))
                
            if touche_move:
                perso.move(NB_CASES,CarteUnePiece.cartesChargees[perso.piece_actuelle].carte)
    Piece.listePieces[perso.piece_actuelle].revele(laby)
    redrawGameWindow()
        
            
pygame.quit()
