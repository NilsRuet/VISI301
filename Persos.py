##############################################################################################
# Fichiers contenant les classes relatives aux personnages du jeu comme le joueur, les ennemis

import pygame
import random
from math import sqrt
from Options import *
from Affichage import *

class Perso():
    #Classe de base pour tous les personnages mobiles
    directions={"BAS":[0,1],"DROITE":[1,0],"HAUT":[0,-1],"GAUCHE":[-1,0]}
    
    def __init__(self,x,y,width,height,vitesse):
        self.x = x
        self.y = y
        self.direction = "BAS"
        self.width = width
        self.height = height
        self.last_mvt = 0
        #stockage du temps du dernier mouvement pour gestion de la vitesse de dépacement
        self.vitesse = vitesse #nombre de millisecondes entre chaque déplacement

        #Chaque personnage mobile possède des coordonnées dans une pièce, une direction, une largeur et une hauteur (affichage) (à déplacer)
        #On connaît moment où son dernier mouvement a été effectué ainsi que sa vitesse

    def case_ennemi(x, y, piece):
        #Méthode vérifiant que la case ne contient pas un ennemi
        ennemi_trouve = False
        return piece.ennemis.get((x,y)) != None
        
    def case_valide(x, y, piece):
        #Méthode permettant de savoir si une case dans une pièce autorise des personnages à se déplacer dessus
        autoriser_mouvement=True
        if not 0 <= x < OptJeu.NB_CASES:
            autoriser_mouvement = False         
        elif not 0 <= y < OptJeu.NB_CASES:
            autoriser_mouvement = False
        #On vérifie que la case est dans la pièce

        else:
            if piece.carte[x][y].collision:
                #On vérifie que la case autorise les personnages à etre dessus
                autoriser_mouvement = False
                
        autoriser_mouvement = autoriser_mouvement and not Perso.case_ennemi(x, y, piece)
        #On vérifie en plus que la case ne contient pas d'ennemi
        return autoriser_mouvement

class Joueur(Perso):
    #Classe représentant le personnage joué
    sprite_direction={"HAUT":"joueurH","BAS":"joueurB","GAUCHE":"joueurG","DROITE":"joueurD"}
    
    VIE_DEPART=100
    #Vie de depart du joueur
    #Pour les tests
    VITESSE=250
    #Vitesse de départ du joueur

    def __init__(self,x,y,width,height,pieceF=1):
        Perso.__init__(self,x,y,width,height,Joueur.VITESSE)
        #Un joueur a les mêmes types de caractéristiques que tous les personages mobiles
        self.max_vie = Joueur.VIE_DEPART
        self.vie = Joueur.VIE_DEPART
        #En plus d'un nombre de points de vie
        self.piece_actuelle = pieceF
        #Et du numéro de la pièce dans laquelle il se trouve
        self.arme=None
        self.points=0
        self.gagne = False
        
    def set_arme(self, armeF):
        #Permet de modifier l'arme du joueur
        self.arme = armeF
    
    def move(self,piece):
        #Méthode permettant de bouger le personnage
        autoriser_mouvement = True
        #Booléen mis à faux si le déplacement est impossible
        
        dx=Perso.directions[self.direction][0]
        dy=Perso.directions[self.direction][1]
        #dx et dy représentent la position relative au joueur de la case vers laquelle il veut se déplacer
        
        #Gestion de la vitesse de déplacement
        if (pygame.time.get_ticks() - self.last_mvt) < self.vitesse:
            autoriser_mouvement = False       
        
        else:
            #Gestion des collisions
            autoriser_mouvement = Joueur.case_valide(self.x+dx, self.y+dy,piece)
            
        #Deplacement du personnage
        if autoriser_mouvement:
            self.x = self.x + dx
            self.y = self.y + dy             
            self.last_mvt = pygame.time.get_ticks()

            #Gestion des changements de pièce
            if isinstance(piece.carte[self.x][self.y].typeCase, int):
                self.piece_actuelle = -piece.carte[self.x][self.y].typeCase
                self.x = (OptJeu.NB_CASES-1)-self.x
                self.y = (OptJeu.NB_CASES-1)-self.y

    def sortie_atteinte(self, num_sortie):
        #Méthode qui détecte si le joueur a atteint la sortie du labyrinthe
        return self.piece_actuelle==num_sortie

    def affichage_vie(self):
        #Méthode affichant la barre de vie du joueur
        rect_vie = Affichage.rectangle_barre_progressive(Affichage.VIE.coords.xi, Affichage.VIE.coords.yi, Affichage.VIE.largeur, Affichage.VIE.hauteur, self.vie, self.max_vie)
        pygame.draw.rect(Affichage.ECRAN, (0, 127, 0), rect_vie)

    def affichage_points(self):
        #Méthode affichant les points du joueur
        texte="Points : {}".format(self.points)
        font = pygame.font.SysFont('Calibri',Affichage.POINTS.taille_texte) #choix de la police d'écriture et de la taille
        texte = font.render(texte, 1, (255,255,255))
        Affichage.ECRAN.blit(texte, (Affichage.POINTS.coords.xi, Affichage.POINTS.coords.yi))
        

    def attaquer(self):
        #Méthode définissant les actions exécutées lorsque le joueur attaque
        self.arme.attaquer()

    def se_repose(self):
        #Méthode définissant les actions exécutées lorsque le joueur se repose
        self.vie = self.max_vie

    def interagir(self, piece):
        #Méthode permettant de savoir quelle action effectuer sur le personnage
        #en fonction de la case avec laquelle le personnage essaye d'interagir
        
        x_case = self.x + Perso.directions[self.direction][0]
        y_case = self.y + Perso.directions[self.direction][1]
        if 0<=x_case<OptJeu.NB_CASES and 0<=y_case<OptJeu.NB_CASES:
            if piece.carte[x_case][y_case].typeCase == "f":
                self.se_repose()
                self.arme.restaurer_durabilite()

            if self.points>0:
                if piece.carte[x_case][y_case].typeCase == "h":
                    self.max_vie+=10
                    self.points-=1
                if piece.carte[x_case][y_case].typeCase == "v":
                    self.vitesse*=0.95
                    self.points-=1
                if piece.carte[x_case][y_case].typeCase == "d":
                    self.arme.max_durabilite*=1.1
                    self.arme.max_attaque = round(sqrt(self.arme.durabilite))
                    self.points-=1
            if piece.carte[x_case][y_case].typeCase == "c":
                self.gagne=True
            
    def affichage(self):
        #Méthode d'affichage du joueur

        sprite = Sprite.liste[Joueur.sprite_direction[self.direction]]
        
        x = self.x*Affichage.JEU.taille_case[0] + Affichage.JEU.coords.xi +sprite.xi
        #Coordonnée en x de la case à laquelle se trouve l'ennemi, + coordonnée de départ en x du jeu + décalage du sprite en x
        y = self.y*Affichage.JEU.taille_case[1] + Affichage.JEU.coords.yi +sprite.yi
        #Coordonnée en y de la case à laquelle se trouve l'ennemi, + coordonnée de départ en y du jeu + décalage du sprite en y
        
        Affichage.ECRAN.blit(sprite.image,(x,y))
    

class Ennemi(Perso):
    #Classe représentant un ennemi, qui attaque le joueur
    sprite_direction={"HAUT":"ennemiH","BAS":"ennemiB","GAUCHE":"ennemiG","DROITE":"ennemiD"}
    
    VIE_DEPART=20
    ATTAQUE=10
    VITESSE_ATTAQUE=1000
    VITESSE=400
    def case_valide(x,y,piece,joueur):
        #Gestion du déplacement d'un ennemi
        return Perso.case_valide(x,y,piece) and not (joueur.x == x and joueur.y == y)
        #Même conditions que tous les personnages mobiles, mais ne peut pas aller sur la même case qu'un joueur

    
    def __init__(self,x,y,pieceF,distance, distance_max,width=Affichage.JEU.taille_case[0],height=Affichage.JEU.taille_case[1]):
        #Création d'un ennemi, avec des valeurs par défaut pour la largeur et la hauteur
        proximite_fin = ((distance_max-distance)/distance_max)
        if OptJeu.DIFFICULTE_ENNEMI == "facile":
            difficulte = 0.75
        elif OptJeu.DIFFICULTE_ENNEMI == "moyenne":
            difficulte = 1
        else:
            difficulte = 1.25
            
        Perso.__init__(self,x,y,width,height,Ennemi.VITESSE)
        
        self.vie = (Ennemi.VIE_DEPART*difficulte)+(0.5*proximite_fin)*Ennemi.VIE_DEPART*difficulte
        #La vie augmente linéairement jusqu'au double de celle de base (en difficulté moyenne)
        
        self.attaque = (Ennemi.ATTAQUE*difficulte)+(0.5*proximite_fin)*Ennemi.ATTAQUE*difficulte
        #L'attaque augmente linéairement jusqu'au double de celle de base (en difficulté moyenne)
        
        self.vitesse*=(1/difficulte)*(0.80+0.20*(1-proximite_fin))
        
        self.vitesse_attaque = Ennemi.VITESSE_ATTAQUE
        self.last_attaque = 0
        self.piece = pieceF


    def action(self, joueur):
        #Gestionnaire des actions réalisées par un ennemi
        self.attaquer(joueur)
        self.move(joueur)
        

    def move(self, joueur):
        #Méthode bougeant si possible l'ennemi vers le joueur
        autoriser_mouvement = True

        #Calcul de la direction à prendre pour aller vers le joueur
        distance_x = joueur.x - self.x
        distance_y = joueur.y - self.y

        #On réduit la distance en x si elle est plus élevée que celle en y, et inversement
        if abs(distance_x)>abs(distance_y):
            if distance_x == 0:
                #TODO ce test existe car la génération actuelle des ennemis a une probabilité d'en créer un sous le joueur
                dx=0
            else:                   
                dx = round(distance_x/abs(distance_x))
            dy = 0
        else:
            dx = 0
            if distance_y==0:
                dy=0
            else:
                dy = round(distance_y/abs(distance_y))

        #Gestion de la vitesse de déplacement
        if (pygame.time.get_ticks() - self.last_mvt) < self.vitesse:
            autoriser_mouvement = False       
        
        else:
            #Si l'ennemi a le droit de se déplacer
            
            #Gestion des collisions
            autoriser_mouvement = Ennemi.case_valide(self.x+dx,self.y+dy,self.piece,joueur)

            #Gestion de la direction
            if abs(dy)>abs(dx):
                #si on se déplace plus verticalement qu'horizontalement
                #On choisit la direction en fonction du signe du déplacement vertical
                if dy<0:
                    self.direction="HAUT"
                else:
                    self.direction="BAS"
            else:
                #Sinon on choisit la direction en fonction du signe du déplacement horizontal
                if dx<0:
                    self.direction="GAUCHE"
                else:
                    self.direction="DROITE"
            
        #Deplacement du personnage
        if autoriser_mouvement:
            del self.piece.ennemis[self.x, self.y]
            
            self.x = self.x + dx
            self.y = self.y + dy
            
            self.piece.ennemis[self.x, self.y] = self
                
            self.last_mvt = pygame.time.get_ticks()
    
    def attaquer(self, joueur):
        #Méthode gérant les actions exécutées quand l'ennemi veut attaquer le joueur
        if [joueur.x-self.x,joueur.y-self.y] == Perso.directions[self.direction]:
            #Si le joueur est sur la case où l'ennemi veut se déplacer
            if not ((pygame.time.get_ticks() - self.last_attaque) < self.vitesse_attaque):
                joueur.vie-=self.attaque
                self.last_attaque = pygame.time.get_ticks()

    def meurt(self):
        #Méthode permettant de supprimer un ennemi
        del self.piece.ennemis[self.x, self.y]

    def affiche(self):
        #Méthode d'affichage d'un ennemi

        sprite = Sprite.liste[Ennemi.sprite_direction[self.direction]]
        
        x = self.x*Affichage.JEU.taille_case[0] + Affichage.JEU.coords.xi +sprite.xi
        #Coordonnée en x de la case à laquelle se trouve l'ennemi, + coordonnée de départ en x du jeu + décalage du sprite en x
        y = self.y*Affichage.JEU.taille_case[1] + Affichage.JEU.coords.yi +sprite.yi
        #Coordonnée en y de la case à laquelle se trouve l'ennemi, + coordonnée de départ en y du jeu + décalage du sprite en y
        
        Affichage.ECRAN.blit(sprite.image,(x,y))
        
        
