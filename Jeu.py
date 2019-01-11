#########################################################################
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
    touche_move_enfoncee = False
    def load_sprites():
        #Méthode permettant de charger toutes les textures utilisées par le jeu

        Sprite("ressources/neige.png","neige",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/sapin.png","sapin",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1],fix_height=False, decalage_pourcent_y=-50)
        Sprite("ressources/feudecamp.png","feudecamp",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/bougies.png","bougies",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/moufles.png","moufles",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/raquettes.png","raquettes",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/charbon.png","charbon",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        #Textures de case d'une pièce

        Sprite("ressources/ennemiH.png","ennemiH",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/ennemiB.png","ennemiB",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/ennemiD.png","ennemiD",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/ennemiG.png","ennemiG",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        #Textures des ennemis

        Sprite("ressources/joueurH.png","joueurH",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/joueurB.png","joueurB",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/joueurD.png","joueurD",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        Sprite("ressources/joueurG.png","joueurG",Affichage.JEU.taille_case[0],Affichage.JEU.taille_case[1])
        #Texture du joueur

        Sprite("ressources/mur_vertical.png","mur_vertical",Affichage.CARTE.taille_mur[0],Affichage.CARTE.taille_mur[1])
        Sprite("ressources/mur_horizontal.png","mur_horizontal",Affichage.CARTE.taille_mur[1],Affichage.CARTE.taille_mur[0])
        Sprite("ressources/ouverture_verticale.png","ouverture_verticale",Affichage.CARTE.taille_mur[0],Affichage.CARTE.taille_mur[1])
        Sprite("ressources/ouverture_horizontale.png","ouverture_horizontale",Affichage.CARTE.taille_mur[1],Affichage.CARTE.taille_mur[0])
        Sprite("ressources/piece_joueur.png","piece_joueur",Affichage.CARTE.taille_piece[0],Affichage.CARTE.taille_piece[1])
        Sprite("ressources/piece_feu_camp.png","piece_feu_de_camp",Affichage.CARTE.taille_piece[0],Affichage.CARTE.taille_piece[1])
        Sprite("ressources/neige.png","piece_vide",Affichage.CARTE.taille_piece[0],Affichage.CARTE.taille_piece[1])
        Sprite("ressources/fond_carte.png","fond_carte",Affichage.CARTE.taille,Affichage.CARTE.taille)
        #Textures utilisées pour afficher la carte du labyrinthe
        
    def reset():
        #Méthode permettant de réinitialiser les attributs de classe utilisés dans une partie
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
        #Méthode qui gère les évènements relatifs aux déplacements
        if event.type == pygame.KEYDOWN:
        #On lit les touches enfoncées, on modifie la direction du personnage en fonction
        #On indique aussi qu'une touche de direction est enfoncée
            if event.key == pygame.K_LEFT:
                self.perso.direction = "GAUCHE"
                self.touche_move_enfoncee=True
            if event.key == pygame.K_RIGHT:
                self.perso.direction = "DROITE"
                self.touche_move_enfoncee=True
            if event.key == pygame.K_UP:
                self.perso.direction = "HAUT"
                self.touche_move_enfoncee=True
            if event.key == pygame.K_DOWN:
                self.perso.direction = "BAS"
                self.touche_move_enfoncee=True
                
        if event.type == pygame.KEYUP:
            #On lit les touches relâchées, pour arrêter un mouvement il faut que la direction du personnage
            #corresponde à la touche relâchée
            if event.key == pygame.K_LEFT and self.perso.direction == "GAUCHE":           
                self.touche_move_enfoncee = False
            if event.key == pygame.K_RIGHT and self.perso.direction == "DROITE":               
                self.touche_move_enfoncee = False
            if event.key == pygame.K_UP and self.perso.direction == "HAUT":              
                self.touche_move_enfoncee = False
            if event.key == pygame.K_DOWN and self.perso.direction == "BAS":               
               self.touche_move_enfoncee = False   
        
    def gerer_event_interaction(self, event):
        #Méthode qui gère les évènements où le joueur veut interagir avec un élément
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.perso.interagir(CarteUnePiece.cartesChargees[self.perso.piece_actuelle])
                
    def gerer_event_attaque(self, event):
        #Méthode qui gère les évènements d'attaque
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.perso.attaquer()

    def gerer_event_quit(self, event):
        #Méthode qui gère les évènements pour quitter le jeu
        if event.type == pygame.QUIT:
            #si on appuie sur la croix on quitte la boucle de jeu
            #et on ne rentre pas dans le menu gameover => on revient au menu principal
            self.arreter_jeu()
            self.entrer_gameover = False
            
    def gerer_event_changement_attaque(self, event):
        #Méthode qui gère les évènements où le joueur veut modifier l'attaque de son arme
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.perso.arme.modifier_attaque(round(-self.perso.arme.max_attaque/10))
            if event.key == pygame.K_f:
                self.perso.arme.modifier_attaque(round(self.perso.arme.max_attaque/10))
    
    def gerer_events(self):
        #Méthode appelant toutes les méthodes de gestion d'évènement
        for event in pygame.event.get():
            self.gerer_event_quit(event)
            self.gerer_event_move(event)
            self.gerer_event_interaction(event)
            self.gerer_event_changement_attaque(event)
            self.gerer_event_attaque(event)
            
    def gerer_actions_event(self):
        #Méthode appliquant les actions à faire lorsque des évènements sont en cours
        if self.touche_move_enfoncee:
            self.perso.move(CarteUnePiece.cartesChargees[self.perso.piece_actuelle])


    def executer_actions_ennemis(self):
        #Méthode faisant agir les ennemis
        CarteUnePiece.cartesChargees[self.perso.piece_actuelle].action_ennemis(self.perso)

    def gerer_transitions(self):
        #Méthode de gestion des changements de pièce
        Piece.listePieces[self.perso.piece_actuelle].revele(self.laby)
        
    def gerer_etat_jeu(self):
        #Méthode qui gère l'état du jeu
        if self.perso.vie<=0:
            #Détection défaite, si le joueur n'a plus de vie
            self.gagne=False
            self.arreter_jeu()
            
        if self.perso.gagne:
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

        self.perso.affichage_points()
        
        Affichage.CARTE.fond_carte()
        self.laby.affiche_lab((Piece.listePieces[self.perso.piece_actuelle].i, Piece.listePieces[self.perso.piece_actuelle].j))
        #Affichage de la carte du labyrinthe

        self.perso.arme.afficher_statistiques()
        #Affichage des statistiques de l'arme
        
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
                       (325*Affichage.TAILLE_ECRAN[1]/600), 400, 90, 25, titre,
                        Affichage.TAILLE_ECRAN[1]/2-(200*Affichage.TAILLE_ECRAN[1]/600), taille_titre)
        
        action =  menu_gameover.lance_menu(Affichage.ECRAN)
        
        if action==0:
            self.rejouer=True
       
    def executer_jeu(self):
        while self.continuer:
            self.gerer_events()
            self.gerer_actions_event()
            self.gerer_transitions()
            self.executer_actions_ennemis()
            self.gerer_etat_jeu()
            self.redrawGameWindow()
        self.game_over()
        Jeu.reset()
        
        

    

