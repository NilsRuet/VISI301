import pygame
import random

from Options import *
from Piece import *
from Persos import *
from Labyrinthe import *
from Affichage import *
pygame.init()

def redrawGameWindow():
    CarteUnePiece.cartesChargees[perso.piece_actuelle].affiche_carte()
    CarteUnePiece.cartesChargees[perso.piece_actuelle].affiche_ennemis()
    perso.affichage()
    laby.affiche_lab((Piece.listePieces[perso.piece_actuelle].i, Piece.listePieces[perso.piece_actuelle].j))
    pygame.display.update()

####################################################################################
#boucle principale
continuer = True

laby = Labyrinthe(OptJeu.TAILLE_LABYRINTHE)
Piece.initListePieces(laby)

perso = Joueur(0,0,Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1],laby.depart)
Piece.listePieces[perso.piece_actuelle].revele(laby)

touche_move = False

while continuer :
    for event in pygame.event.get() :
        #Fermeture de la fenêtre
        if event.type == pygame.QUIT:
            continuer = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                perso.direction = "GAUCHE"
                touche_move = True
            if event.key == pygame.K_RIGHT:
                perso.direction = "DROITE"
                touche_move = True
            if event.key == pygame.K_UP:
                perso.direction = "HAUT"
                touche_move = True
            if event.key == pygame.K_DOWN:
                perso.direction = "BAS"
                touche_move = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and perso.direction == "GAUCHE":           
                touche_move = False
            if event.key == pygame.K_RIGHT and perso.direction == "DROITE":               
                touche_move = False
            if event.key == pygame.K_UP and perso.direction == "HAUT":              
                touche_move = False
            if event.key == pygame.K_DOWN and perso.direction == "BAS":               
                touche_move = False
            
                
    if touche_move:
        perso.move(CarteUnePiece.cartesChargees[perso.piece_actuelle].carte)
                
    Piece.listePieces[perso.piece_actuelle].revele(laby)
    redrawGameWindow()
    
    if perso.sortie_atteinte(laby.arrivee):
        print("Gagné!")
        continuer=False
        
            
pygame.quit()
