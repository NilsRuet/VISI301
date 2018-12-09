import pygame
import random
from Class_Persos import Perso, Joueur, Ennemi
pygame.init()
clock = pygame.time.Clock()

TAILLE_ECRAN = (1000, 1000) #largeur / hauteur
TAILLE_CASE = (100, 100)
NB_CASES = 10
ECRAN = pygame.display.set_mode(TAILLE_ECRAN)
#Pour l'instant ce sont des constantes, mais peut etre pas dans la version finale

#ajout d'1 titre
pygame.display.set_caption("Jeu")

class Piece:
    listePieces=[]
            
    def __init__(self, numPieceF, typePiece):
    #constructeur
        self.numPiece=numPieceF
        self.typePiece=typePiece
        self.vue=False
        self.connexions = []

    def initTempListePieces():
        #Generation temporaire de la carte globale
        numeroActuel=0
        while numeroActuel != 16:
            Piece.listePieces.append(Piece(numeroActuel, "type_test"))
            Piece.listePieces[numeroActuel].ajout_connexion(numeroActuel//4,numeroActuel%4, (numeroActuel+1)%16)
            numeroActuel+=1

    def ajout_connexion(self, xCase, yCase, numPieceConnectee):
        self.connexions.append([xCase, yCase, numPieceConnectee])

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
                self.carte[colonne][ligne] = Case(random.randint(0,1))
                #Chaque cellule de la carte est une case
                #Ici, pour l'exemple, on appelle le constructeur de la case avec 0 ou 1

        CarteUnePiece.cartesChargees[self.numPiece]=self
        
        
    def affiche_carte(self):
        #Méthode d'affichage de la grille
        for colonne in range(len(self.carte)):
            for ligne in range(len(self.carte[0])):
                self.carte[colonne][ligne].affiche_case(colonne, ligne)
##        for cases_connexions in Piece.listePieces[self.numPiece].connexions:
##            #Afficher temporairement les cases de connexion
##            x, y = cases_connexions[0],cases_connexions[1]
##            pygame.draw.rect(ECRAN, (255,0,0), (TAILLE_CASE[0]*x, TAILLE_CASE[1]*y, 50, 50))
##            #Cases de connexion temporairement affichées en rouge

class Case:
    def __init__(self, typeCaseF):
        self.typeCase = typeCaseF

    def affiche_case(self, colonneF, ligneF):
        #Pour l'instant on affiche un rectangle d'une certaine couleur pour représenter la case
        hauteur, largeur = TAILLE_CASE[0], TAILLE_CASE[1]
        couleur = (self.typeCase*250, self.typeCase*250, self.typeCase*250)
        #On considère ici que la case vaut 0 ou 1, on affiche noir ou (presque) blanc
        pygame.draw.rect(ECRAN, couleur, (hauteur*colonneF, largeur*ligneF, hauteur, largeur))




def redrawGameWindow():
    #affichage carte
    CarteUnePiece.cartesChargees[piece_actuelle].affiche_carte()
    #affichage perso
    perso.affichage(ECRAN)
    
    pygame.display.update()






####################################################################################
#boucle principale
perso = Joueur(300,410,64,64)
continuer = True

testCarteGlobale = Piece.initTempListePieces()
piece_actuelle = 0
Piece.listePieces[piece_actuelle].revele()

while continuer :
    clock.tick(30)


    #events
    for event in pygame.event.get() :
        #Fermeture de la fenêtre
        if event.type == pygame.QUIT:
            continuer = False

    #appuyer sur les touches pour se déplacer (en haut à gauche fenêtre : (0,0))
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and perso.x >= perso.vitesse:
        perso.x = perso.x - perso.vitesse
        
    elif keys[pygame.K_RIGHT] and perso.x < (TAILLE_ECRAN[0] - perso.width):
        perso.x = perso.x + perso.vitesse
        
    elif keys[pygame.K_UP] and perso.y >= perso.vitesse:
        perso.y = perso.y - perso.vitesse
        
    elif keys[pygame.K_DOWN] and perso.y < (TAILLE_ECRAN[1] - perso.height):
        perso.y = perso.y + perso.vitesse

    redrawGameWindow()
        
            
pygame.quit()
