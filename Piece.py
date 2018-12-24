import pygame
import random
from Affichage import *
from Options import *
from Persos import *

class Piece:
    listePieces={}
            
    def __init__(self, numPieceF, typePiece, iF, jF):
    #constructeur
        self.numPiece=numPieceF
        self.typePiece=typePiece
        self.vue=False
        self.i = iF
        self.j = jF

    def initListePieces(labyF):
        #Generation temporaire de la carte globale
        for i in range(0,labyF.taille, 2):
            for j in range(0,labyF.taille, 2):
                rndm_type = random.random()
                if rndm_type<=0.5:
                    typePiece = "ennemis"
                elif rndm_type<=0.8:
                    typePiece = "grille"
                else:
                    typePiece = "vide"           
                Piece.listePieces[labyF.carte[i][j].zone] = Piece(labyF.carte[i][j].zone,typePiece, i, j)


    def revele(self, labyF):
        if not self.numPiece in CarteUnePiece.cartesChargees:
            CarteUnePiece(self.numPiece,labyF, self.typePiece)
            self.vue=True;

class CarteUnePiece:
    cartesChargees = {}
    def __init__(self,numPieceF,labyF, typePiece):
    #constructeur
        self.numPiece=numPieceF
        self.ennemis=[]
        #On initialise un tableau de NB_CASES*NB_CASES qui sera remplit de cases
        self.carte=[[0]]*OptJeu.NB_CASES
        for colonne in range(len(self.carte)):
            self.carte[colonne]=[0]*OptJeu.NB_CASES
        #Ici, initialisé avec des 0 dans toutes les cellules par défaut

        if typePiece=="ennemis":
            for colonne in range(len(self.carte)):
                for ligne in range(len(self.carte[0])):
                    self.carte[colonne][ligne] = Case(1)
                    if random.random()<=0.01:
                        self.ennemis.append(Ennemi(colonne, ligne, 10, 10))
                        #Modèle ennemi temporaire TODO
                        
        elif typePiece=="grille":
            for colonne in range(len(self.carte)):
                for ligne in range(len(self.carte[0])):
                    if colonne%2 == 1 and ligne%2 == 1:
                        self.carte[colonne][ligne] = Case(0)
                    else:
                        self.carte[colonne][ligne] = Case(1)
        else:
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
                    x_case = round(((coords_murs[0]+1)/2)*(OptJeu.NB_CASES-1))
                    y_case = round(((coords_murs[1]+1)/2)*(OptJeu.NB_CASES-1))
                    #Méthode temporaire de génération des murs
                    self.carte[x_case][y_case].typeCase = -numPieceSuiv
        
    def affiche_carte(self):
        #Méthode d'affichage de la grille
        for colonne in range(len(self.carte)):
            for ligne in range(len(self.carte[0])):
                self.carte[colonne][ligne].affiche_case(colonne, ligne)

    def affiche_ennemis(self):
        for ennemi in self.ennemis:
            ennemi.affiche()

class Case:
    def __init__(self, typeCaseF):
        self.typeCase = typeCaseF

    def affiche_case(self, colonneF, ligneF):
        #Pour l'instant on affiche un rectangle d'une certaine couleur pour représenter la case
        hauteur, largeur = Affichage.JEU.taille_case[0], Affichage.JEU.taille_case[1]
        couleur = (self.typeCase*250, self.typeCase*250, self.typeCase*250)
        x_case = hauteur*colonneF + Affichage.JEU.coords.xi
        y_case = largeur*ligneF + Affichage.JEU.coords.yi
        #On considère ici que la case vaut 0 ou 1, on affiche noir ou (presque) blanc
        if self.typeCase < 0:
            pygame.draw.rect(Affichage.ECRAN, (0,255,0), (x_case, y_case, hauteur, largeur))
        else:
            pygame.draw.rect(Affichage.ECRAN, couleur, (x_case, y_case, hauteur, largeur))
            
