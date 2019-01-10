###################################################################
#Contient les classes qui gèrent les pièces que contient le labyrinthe

import pygame
import random
from Affichage import *
from Options import *
from Persos import *

class Piece:
    #Classe contenant les caractéristiques d'une pièce dans le labyrinthe
    listePieces={}
    
    def __init__(self, numPieceF, typePiece, iF, jF):
        self.numPiece=numPieceF
        self.typePiece=typePiece
        #Numéro de la pièce dans le labyrinthe et son stype
        self.vue=False
        #Booléen vrai si le joueur est déjà entré dans la pièce (=si la pièce a été générée pour l'instant)
        self.i = iF
        self.j = jF
        #Coordonnées de la pièce dans le labyrinthe

    def initListePieces(labyF):
        nbTypeRepos = 0
        #nombre de pièces de type "repos"
        
        #Generation temporaire de la carte globale
        for i in range(0,labyF.taille, 2):
            for j in range(0,labyF.taille, 2):
                #Pour chaque pièce
                numPiece = labyF.carte[i][j].zone
                if labyF.depart == numPiece:
                    typePiece = "depart"
                elif labyF.arrivee == numPiece:
                    typePiece = "arrivee"
                else:
                    rndm_type = random.random()
                    if rndm_type<=0.1 and nbTypeRepos<2:
                        #Limitation du nombre maximal de pièces de repos
                        #(en plus de la pièce de départ)
                        typePiece = "repos"
                        nbTypeRepos = nbTypeRepos+1       
                    elif rndm_type<=0.4:
                        typePiece = "ennemi01"
                    elif rndm_type<=0.7:
                        typePiece = "ennemi02"
                    else:
                        typePiece = "ennemi03"
                #On choisit son type "aléatoirement" et on la crée ensuite
                Piece.listePieces[numPiece] = Piece(numPiece,typePiece, i, j)

    def revele(self, labyF):
        #Permet de charger la carte d'une pièce si elle n'a jamais été chargée
        if not self.numPiece in CarteUnePiece.cartesChargees:
            CarteUnePiece(self.numPiece,labyF, self.typePiece)
            self.vue=True;

class CarteUnePiece:
    #Classe représentant la carte d'une pièce
    cartesChargees = {}
    #Liste des cartes déjà chargées
    
    def __init__(self,numPieceF,labyF, typePiece):
        self.numPiece=numPieceF

        
        self.ennemis={}
        
        self.carte=[]
        for colonne in range(OptJeu.NB_CASES):
            cases_colonne=[]
            for ligne in range(OptJeu.NB_CASES):
                cases_colonne.append(Case(1,False))
            self.carte.append(cases_colonne)
        #On initialise un tableau de NB_CASES*NB_CASES qui sera remplit d'objets case
        #Ici, initialisé avec des cases vides dans toutes les cellules par défaut

        self.init_depuis_fichier("niveaux/{}.lvl".format(typePiece))
        #On intitialise la pièce en fonction de son type
            
        self.creer_portes(labyF)
        #On créé les ouvertures avec les pièces voisines dans le labyrinthe
        
        CarteUnePiece.cartesChargees[self.numPiece]=self
        #On ajoute la pièce actuelle aux cartes chargées

    def init_depuis_fichier(self, nom_fichier):
        #Initialisation d'une pièce depuis le contenu d'un fichier
        fichier = open(nom_fichier, "r")
        
        num_ligne = 0
        ligne = fichier.readline()
        while num_ligne<OptJeu.NB_CASES and ligne!="":
            #On lit le fichier ligne par ligne
            num_col=0
            while num_col<OptJeu.NB_CASES and ligne[num_col]!="\n":
                #On lit chaque ligne caractère par caractère
                val = ligne[num_col]
                if val=="e":
                    if random.random()<0.25:#Constante jusqu'à l'augmentation de difficulté
                        self.ennemis[num_col, num_ligne] = Ennemi(num_col, num_ligne, self)
                elif val=="a":
                    val = random.choice(["0","1"])
                self.carte[num_col][num_ligne]=Case(val,val in Case.CASES_SOLIDES)
                num_col+=1
            num_ligne+=1
            ligne = fichier.readline()
        fichier.close()

    def init_piece_vide(self):
        #Initialisation d'une pièce en pièce vide
        for colonne in range(len(self.carte)):
            for ligne in range(len(self.carte[0])):
                self.carte[colonne][ligne] = Case(1, False)

                        
    def creer_portes(self, labyF):
        #Méthode de création des ouvertures
        i_piece = Piece.listePieces[self.numPiece].i
        j_piece = Piece.listePieces[self.numPiece].j
        #Coordonnée de la pièce
        
        for coords_murs in ((-1,0),(1,0),(0,1),(0,-1)):
            #On regarde tous les coordonnées des murs potentiels autour de la pièce
            i_mur = i_piece+coords_murs[0]
            j_mur = j_piece+coords_murs[1]
            
            if 0<=i_mur<labyF.taille and 0<=j_mur<labyF.taille:
                #On regarde si ce mur potentiel est dans le labyrinthe (pour les pièces au bord)
                if not labyF.carte[i_mur][j_mur]:
                    #On vérifie que ce mur potentiel n'existe pas
                    
                    numPieceSuiv = labyF.carte[i_mur+coords_murs[0]][j_mur+coords_murs[1]].zone
                    #On regarde le numéro de la pièce de l'autre côté de l'ouverture
                    
                    x_case = round(((coords_murs[0]+1)/2)*(OptJeu.NB_CASES-1))
                    y_case = round(((coords_murs[1]+1)/2)*(OptJeu.NB_CASES-1))
                    #On choisit les coordonnées de la case permettant de changer de pièce dans la pièce
                    
                    self.carte[x_case][y_case].typeCase = -numPieceSuiv
                    self.carte[x_case][y_case].collision = False
                    #On crée la porte dans la pièce, avec une case dont la valeur est négative. Cette valeur indique le numéro de la pièce vers laquelle la porte mène.

    def action_ennemis(self, joueur):
        #Méthode appelée pour faire bouger tous les ennemis d'une pièce
        for coords_ennemi in self.ennemis:
            self.ennemis[coords_ennemi].action(joueur)
            
    def affiche_carte(self):
        #Méthode d'affichage de la carte de la pièce
        for colonne in range(len(self.carte)):
            for ligne in range(len(self.carte[0])):
                self.carte[colonne][ligne].affiche_case(colonne, ligne)

    def affiche_ennemis(self):
        #Méthode d'affichage des ennemis situés dans la pièce
        for coords_ennemi in self.ennemis:
            self.ennemis[coords_ennemi].affiche()

class Case:
    #Classe contenant les informations d'une case dans une pièce
    CASES_SOLIDES=["f","1"]
    
    def __init__(self, typeCaseF, collisionF):
        self.typeCase = typeCaseF
        self.collision = collisionF
        #Chaque case possède un type et peut ou non être "solide", c'est à dire que les personnages entrent en collision avec
        
    def affiche_case(self, colonneF, ligneF):
        #Affichage d'une case
        
        hauteur = Affichage.JEU.taille_case[0]
        largeur = Affichage.JEU.taille_case[1]
        #Dimensions de la case
        
        couleur = (self.typeCase*250, self.typeCase*250, self.typeCase*250)
        #Couleur (ou image) correspondant à la case
        
        x_case = hauteur*colonneF + Affichage.JEU.coords.xi
        y_case = largeur*ligneF + Affichage.JEU.coords.yi
        #Position de la case
        
        #On considère ici que la case vaut 0 ou 1, on affiche noir ou blanc
##        if isinstance(self.typeCase, int):
##            pygame.draw.rect(Affichage.ECRAN, (0,255,0), (x_case, y_case, hauteur, largeur))
##        else:
        if self.typeCase == "1":
            Affichage.ECRAN.blit(Sprite.liste["sapin"].image,(x_case+Sprite.liste["sapin"].xi, y_case+Sprite.liste["sapin"].yi))
        if self.typeCase == "f":
            Affichage.ECRAN.blit(Sprite.liste["feudecamp"].image,(x_case+Sprite.liste["feudecamp"].xi, y_case+Sprite.liste["feudecamp"].yi))
            
