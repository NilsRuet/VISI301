########################
# Fichier contenant la boucle principal du programme
# A executer pour lancer le jeu

import pygame

from Options import *
from Piece import *
from Persos import *
from Labyrinthe import *
from Affichage import *
from Armes import *

pygame.init()

def redrawGameWindow():
    #Procedure gérant l'ordre d'affichage des éléments

    Affichage.ECRAN.fill((0,0,0))
    #On efface ce qui est déjà affiché = tout l'écran de jeu devient noir 
    
    CarteUnePiece.cartesChargees[perso.piece_actuelle].affiche_carte()
    CarteUnePiece.cartesChargees[perso.piece_actuelle].affiche_ennemis()
    perso.affichage()
    #Affichage de la pièce et de ses éléments
    
    perso.affichage_vie()
    #Affichage de la vie du personnage
    
    laby.affiche_lab((Piece.listePieces[perso.piece_actuelle].i, Piece.listePieces[perso.piece_actuelle].j))
    #Affichage de la carte du labyrinthe

    pygame.display.update()

####################################################################################
#boucle principale
    
continuer = True

laby = Labyrinthe(OptJeu.TAILLE_LABYRINTHE)
Piece.initListePieces(laby)
#Génération de la carte

perso = Joueur(0,0,Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1],laby.depart)
perso.set_arme(Melee(perso, 10, 300))
#Test d'une arme avec 10 d'attaque, attaque toutes les 0.3s

Piece.listePieces[perso.piece_actuelle].revele(laby)
#Génération du personnage et de la pièce de départ

touche_move = False
#Booléen permettant de savoir si une touche de déplacement est en train d'être enfoncée

while continuer :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #Fermeture de la fenêtre
            continuer = False
        if event.type == pygame.KEYDOWN:
            #On lit les touches enfoncées, on modifie la direction du personnage en fonction
            #On indique aussi qu'une touche de direction est enfoncée
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
            if event.key == pygame.K_r:
                perso.attaquer()

        if event.type == pygame.KEYUP:
            #On lit les touches relâchées, pour arrêter un mouvement il faut que la direction du personnage
            #corresponde à la touche relâchée
            if event.key == pygame.K_LEFT and perso.direction == "GAUCHE":           
                touche_move = False
            if event.key == pygame.K_RIGHT and perso.direction == "DROITE":               
                touche_move = False
            if event.key == pygame.K_UP and perso.direction == "HAUT":              
                touche_move = False
            if event.key == pygame.K_DOWN and perso.direction == "BAS":               
                touche_move = False

            
    CarteUnePiece.cartesChargees[perso.piece_actuelle].action_ennemis(perso)
    #On bouge les ennemis de la pièce actuelle
    
    if touche_move:
        perso.move(CarteUnePiece.cartesChargees[perso.piece_actuelle])
        #On bouge le personnage si nécessaire
                
    Piece.listePieces[perso.piece_actuelle].revele(laby)
    #On charge la pièce actuelle (cas où le personnage change de pièce)
    
    redrawGameWindow()
    #On affiche tout
    
    if perso.vie==0:
        #Détection défaite, si le joueur n'a plus de vie
        print("Perdu")
        continuer=False
        
    if perso.sortie_atteinte(laby.arrivee):
        #Détection de l'arrivée dans la pièce finale du labyrinthe
        print("Gagné!")
        continuer=False
        
            
pygame.quit()
