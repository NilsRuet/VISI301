########################
# Fichier contenant la boucle gérant le jeu et les évènements liés au jeu

import pygame

from Menu import *
from Options import *
from Piece import *
from Persos import *
from Labyrinthe import *
from Affichage import *
from Armes import *

####################################################################################
#Endroit provisoire pour le chargement des sprites
Sprite("ressources/neige.png","neige",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
Sprite("ressources/sapin.png","sapin",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1],fix_height=False, decalage_pourcent_y=-50)

Sprite("ressources/ennemiH.png","ennemiH",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
Sprite("ressources/ennemiB.png","ennemiB",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
Sprite("ressources/ennemiD.png","ennemiD",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
Sprite("ressources/ennemiG.png","ennemiG",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])

####################################################################################
def lance_jeu():
    #boucle principale qui gère le jeu et les évènements liés au jeu

    def redrawGameWindow():
        #Procedure gérant l'ordre d'affichage des éléments

        Affichage.ECRAN.fill((0,0,0))
        #On efface ce qui est déjà affiché = tout l'écran de jeu devient noir

        Affichage.JEU.fond_jeu(Sprite.liste["neige"])
        #Affichage du fond du jeu (= fond de la pièce actuelle)

        CarteUnePiece.cartesChargees[perso.piece_actuelle].affiche_ennemis()
        perso.affichage()
        #Affichage des personnages

        CarteUnePiece.cartesChargees[perso.piece_actuelle].affiche_carte()
        #Affichage des éléments de la pièces
        
        perso.affichage_vie()
        #Affichage de la vie du personnage
        
        laby.affiche_lab((Piece.listePieces[perso.piece_actuelle].i, Piece.listePieces[perso.piece_actuelle].j))
        #Affichage de la carte du labyrinthe

        pygame.display.update()

######################################################################################################################
        
    continuer = True
    entrer_gameover = True #Par défaut, à la fin du jeu, on rentre dans le menu gameover

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
                #si on appuie sur la croix on quitte la boucle de jeu
                #et on ne rentre pas dans le menu gameover => on revient au menu principal
                continuer = False
                entrer_gameover = False
                
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
            continuer = False
            menu_gameover = Menu((255,0,0), ["Rejouer", "Menu principal"],
                                 Affichage.TAILLE_ECRAN[1]/2+50, 400, 90, 20, "Game Over",
                                 Affichage.TAILLE_ECRAN[1]/2-200, 200)
            
        if perso.sortie_atteinte(laby.arrivee):
            #Détection de l'arrivée dans la pièce finale du labyrinthe
            continuer = False
            menu_gameover = Menu((255,0,0), ["Rejouer", "Menu principal"],
                                 Affichage.TAILLE_ECRAN[1]/2+50, 400, 90, 20, "Vous avez gagné !",
                                 Affichage.TAILLE_ECRAN[1]/2-200, 130)

    #Affichage du menu gameover
    if entrer_gameover:
        continuer_gameover = True
        while continuer_gameover: #Tant qu'on a pas fait un choix dans le menu
            action = menu_gameover.lance_menu(Affichage.ECRAN) #on lance le menu game over
            if action == 0: #Rejouer, on relance le jeu
                lance_jeu()
            elif action == 1:
            #dernier bouton donc c'est celui qui fait sortir du menu courant
                continuer_gameover = False
    #une fois sortis de la boucle, on revient au menu principal

