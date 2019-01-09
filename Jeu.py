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

class Jeu:
    def load_sprites():
        Sprite("ressources/neige.png","neige",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/sapin.png","sapin",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1],fix_height=False, decalage_pourcent_y=-50)
        Sprite("ressources/feudecamp.png","feudecamp",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        
        Sprite("ressources/ennemiH.png","ennemiH",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/ennemiB.png","ennemiB",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/ennemiD.png","ennemiD",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/ennemiG.png","ennemiG",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])

        Sprite("ressources/joueurH.png","joueurH",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/joueurB.png","joueurB",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/joueurD.png","joueurD",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/joueurG.png","joueurG",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])

        Sprite("ressources/mur_vertical.png","mur_vertical",Affichage.CARTE.taille_piece[0]//10,Affichage.CARTE.taille_piece[1])
        Sprite("ressources/mur_horizontal.png","mur_horizontal",Affichage.CARTE.taille_piece[0],Affichage.CARTE.taille_piece[1]//10)
        Sprite("ressources/ouverture_verticale.png","ouverture_verticale",Affichage.CARTE.taille_piece[0]//10,Affichage.CARTE.taille_piece[1])
        Sprite("ressources/ouverture_horizontale.png","ouverture_horizontale",Affichage.CARTE.taille_piece[0],Affichage.CARTE.taille_piece[1]//10)
        
    def reset():
        Piece.listePieces={}
        CarteUnePiece.cartesChargees={}
         
    
    def __init__(self):
        Jeu.load_sprites()

        self.rejouer = False
        self.continuer=True
        self.gagne=False

        self.laby = Labyrinthe(OptJeu.TAILLE_LABYRINTHE)
        Piece.initListePieces(self.laby)
        #Génération du labyrinthe

        x = OptJeu.NB_CASES//2 +1
        y = OptJeu.NB_CASES//2 +1
        
        self.perso = Joueur(x,y,Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1],self.laby.depart)
        self.perso.set_arme(Melee(self.perso, 10, 300))#Test d'une arme avec 10 d'attaque, attaque toutes les 0.3s        
        Piece.listePieces[self.perso.piece_actuelle].revele(self.laby)
        #Génération du personnage et de la pièce de départ

    def gerer_event_move(self, event):
        touche_move=False
        
        if event.type == pygame.KEYDOWN:
        #On lit les touches enfoncées, on modifie la direction du personnage en fonction
        #On indique aussi qu'une touche de direction est enfoncée
            if event.key == pygame.K_LEFT:
                self.perso.direction = "GAUCHE"
                touche_move = True
            if event.key == pygame.K_RIGHT:
                self.perso.direction = "DROITE"
                touche_move = True
            if event.key == pygame.K_UP:
                self.perso.direction = "HAUT"
                touche_move = True
            if event.key == pygame.K_DOWN:
                self.perso.direction = "BAS"
                touche_move = True
                
        if event.type == pygame.KEYUP:
            #On lit les touches relâchées, pour arrêter un mouvement il faut que la direction du personnage
            #corresponde à la touche relâchée
            if event.key == pygame.K_LEFT and self.perso.direction == "GAUCHE":           
                touche_move = False
            if event.key == pygame.K_RIGHT and self.perso.direction == "DROITE":               
                touche_move = False
            if event.key == pygame.K_UP and self.perso.direction == "HAUT":              
                touche_move = False
            if event.key == pygame.K_DOWN and self.perso.direction == "BAS":               
                touche_move = False
                
        if touche_move:
            self.perso.move(CarteUnePiece.cartesChargees[self.perso.piece_actuelle])

    def gerer_event_attaque(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.perso.attaquer()

    def gerer_event_quit(self, event):
        if event.type == pygame.QUIT:
            #si on appuie sur la croix on quitte la boucle de jeu
            #et on ne rentre pas dans le menu gameover => on revient au menu principal
            self.arreter_jeu()
            self.entrer_gameover = False
            
    def gerer_events(self):
        for event in pygame.event.get():
            self.gerer_event_quit(event)
            self.gerer_event_move(event)
            self.gerer_event_attaque(event)

    def executer_actions_ennemis(self):
        CarteUnePiece.cartesChargees[self.perso.piece_actuelle].action_ennemis(self.perso)

    def gerer_etat_jeu(self):
        if self.perso.vie==0:
            #Détection défaite, si le joueur n'a plus de vie
            self.gagne=False
            self.arreter_jeu()
            
        if self.perso.sortie_atteinte(self.laby.arrivee):
            #Détection de l'arrivée dans la pièce finale du labyrinthe
            self.gagne=True
            self.arreter_jeu()

    def redrawGameWindow(self):
        #Procedure gérant l'ordre d'affichage des éléments

        Affichage.ECRAN.fill((0,0,0))
        #On efface ce qui est déjà affiché = tout l'écran de jeu devient noir

        Affichage.JEU.fond_jeu(Sprite.liste["neige"])
        #Affichage du fond du jeu (= fond de la pièce actuelle)

        CarteUnePiece.cartesChargees[self.perso.piece_actuelle].affiche_ennemis()
        self.perso.affichage()
        #Affichage des personnages

        CarteUnePiece.cartesChargees[self.perso.piece_actuelle].affiche_carte()
        #Affichage des éléments de la pièces
        
        self.perso.affichage_vie()
        #Affichage de la vie du personnage
        
        self.laby.affiche_lab((Piece.listePieces[self.perso.piece_actuelle].i, Piece.listePieces[self.perso.piece_actuelle].j))
        #Affichage de la carte du labyrinthe

        pygame.display.update()

    def arreter_jeu(self):
        self.continuer = False

    def game_over(self):
        if self.gagne:
            titre="Vous avez gagné !"
            taille_titre = int(110*Affichage.TAILLE_ECRAN[1]/600)
        else:
            titre="Game over"
            taille_titre = int(180*Affichage.TAILLE_ECRAN[1]/600)
            
        menu_gameover = Menu((255,0,0), ["Rejouer", "Menu principal"],
                         Affichage.TAILLE_ECRAN[1]/2+(50*Affichage.TAILLE_ECRAN[1]/600), 400, 90, 20,
                         titre, Affichage.TAILLE_ECRAN[1]/2-(200*Affichage.TAILLE_ECRAN[1]/600), taille_titre)

        action =  menu_gameover.lance_menu(Affichage.ECRAN)
        
        if action==0:
            self.rejouer=True
       
    def executer_jeu(self):
        while self.continuer:
            self.gerer_events()
            Piece.listePieces[self.perso.piece_actuelle].revele(self.laby)
            self.executer_actions_ennemis()
            self.gerer_etat_jeu()
            self.redrawGameWindow()
        self.game_over()
        Jeu.reset()
        
        

    

