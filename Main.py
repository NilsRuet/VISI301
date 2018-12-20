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
    perso.affichage()
    laby.affiche_lab((Piece.listePieces[perso.piece_actuelle].i, Piece.listePieces[perso.piece_actuelle].j))
    pygame.display.update()

####################################################################################
#boucle principale
continuer = True

laby = Labyrinthe(OptJeu.TAILLE_LABYRINTHE)
Piece.initListePieces(laby)

perso = Joueur(0,0,Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
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
                perso.move(OptJeu.NB_CASES,CarteUnePiece.cartesChargees[perso.piece_actuelle].carte)
    Piece.listePieces[perso.piece_actuelle].revele(laby)
    redrawGameWindow()
        
            
pygame.quit()
