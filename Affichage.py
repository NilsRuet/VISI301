###############################
# Contient l'ensemble des classes uniquement utilisées
# pour l'affichage des éléments du jeu

import pygame
from Options import *

class Coords:
    #Classe permettant de créer un objet contenant des coordonnées
    #En plus d'isoler cette caractéristique, permet d'accéder plus instinctivement
    #aux coordonnées selon les axes horizontaux et verticaux, en nommant les valeurs xi et yi
    def __init__(self, xF, yF):
        self.xi = xF
        self.yi = yF

class Affichage_jeu:
    #Classe regroupant les caractéristiques de l'affichage du jeu 
    #et les méthodes pour afficher les éléments qui ne dépendent pas de données de la partie
        
    def __init__(self, coordsF, tailleF):
        self.coords = coordsF
        #Coordonnées "de départ" pour afficher le jeu

        self.taille=tailleF
        #Taille du jeu dans la fenêtre
        
        self.taille_case = (round(tailleF/OptJeu.NB_CASES),round(tailleF/OptJeu.NB_CASES))
        #Taille des cases du jeu

    def fond_jeu(self, sprite_fond):
        #Colle une image par défaut sur chaque case du jeu
        for colonne in range(OptJeu.NB_CASES):
            for ligne in range(OptJeu.NB_CASES):
                Affichage.ECRAN.blit(sprite_fond.image, (colonne*self.taille_case[0], ligne*self.taille_case[1]))
                
class Affichage_carte:
    #Classe regroupant les caractéristiques d'affichage de la carte
    #et les méthodes pour afficher les éléments qui ne dépendent pas de données de la partie
    
    def fond_carte(self):
        #Affiche un fond à l'endroit où s'affiche la carte
        Affichage.ECRAN.blit(Sprite.liste["fond_carte"].image, (self.coords.xi+Sprite.liste["fond_carte"].xi, self.coords.yi+Sprite.liste["fond_carte"].yi))
        
    def __init__(self, coordsF, tailleF):
        self.coords = coordsF
        #Coordonnées de la zone où afficher la carte

        self.taille = tailleF
        #Taille de la zone où est affichée la carte
        
        largeur_piece = round(tailleF/(1.1*OptJeu.TAILLE_LABYRINTHE-0.1))
        largeur_mur = round(0.1*largeur_piece)
        #La largeur de la pièce est la solution du système où 
            #taille_carte = taille_labyrinthe*taille_piece + (taille_labyrinthe-1)*epaisseur_mur
            #epaisseur_mur = 0.1*taille_piece
        
        self.taille_mur = (largeur_mur,largeur_piece)
        #Dimension des murs
        self.taille_piece = (largeur_piece,largeur_piece)
        #Taille des cases de la carte

class Affichage_vie:
    #Classe regroupant les caractéristiques d'affichage de la vie du personnage
    def __init__(self, coordsF, largeurF, hauteurF):
        self.coords = coordsF
        #Coordonnées de la zone d'affichage de la vie
        
        self.largeur = largeurF
        self.hauteur = hauteurF
        #Dimensions de la zone d'affichage de la vie

class Affichage_durabilite_arme:
    #Classe regroupant les caractéristiques d'affichage de la durabilité de l'arme du personnage
    def __init__(self, coordsF, largeurF, hauteurF):
        self.coords = coordsF
        #Coordonnées de la zone d'affichage
        
        self.largeur = largeurF
        self.hauteur = hauteurF
        #Dimensions de la zone d'affichage
        
class Affichage_puissance_arme:
    #Classe regroupant les caractéristiques d'affichage de la puissance de l'arme du personnage
    def __init__(self, coordsF, largeurF, hauteurF):
        self.coords = coordsF
        #Coordonnées de la zone d'affichage
        
        self.largeur = largeurF
        self.hauteur = hauteurF
        #Dimensions de la zone d'affichage

class Affichage_points:
    #Classe regroupant les caractéristiques d'affichage des points obtenus par le personnage
    def __init__(self, coordsF, taille_texteF):
        self.coords = coordsF
        #Coordonnées d'affichage
        
        self.taille_texte=taille_texteF
        #Taille du texte
        
class Sprite:
    #Classe permettant de charger une image et de lui attribuer des caractéristiques
    #Ainsi que d'accéder à la liste des images déjà chargées
    
    liste={}
    #Dictionnaire contenant les images déjà chargées
    
    def __init__(self, file, nom, width, height, fix_width=True, fix_height=True, decalage_pourcent_x=0, decalage_pourcent_y=0):
        #Sert à initialiser une image
        #width, height : dimension de l'emplacement où l'image est affichée
        #
        #nom : nom sous lequel enregistrer l'image dans la liste des images
        #
        #fix_width, fix_height : si fix_width est faux, on ignore la largeur imposée et on la définit par rapport à la hauteur imposée en gardant les proportions de l'image de base
        #Inversement si fix_heught est faux. Ces deux paramètres permettent de choisir si on veut adapter la taille de l'image à son emplacement
        #
        #decalage_pourcent_x, decalage_pourcent_y : permet de spécifier un décalage en donnant sa valeur en % par rapport à la taille de l'image finale
        #Exemple : si decalage_pourcent_x vaut 0.2 et que la largeur finale de l'image est 100, l'image a un décalage de 20 pixels en x.

        self.image = pygame.image.load(file).convert_alpha()

        scale_width = width
        scale_height = height

        if not(fix_width and fix_height):
            if not fix_width:
                #Adaptation de la largeur par rapport à la hauteur en gardant les proportions de l'image d'origine
                coef_largeur_hauteur = self.image.get_width()/self.image.get_height()
                scale_width = round(scale_height*coef_largeur_hauteur)             
                
            if not fix_height:
                #Adaptation de la hauteur par rapport à la largeur en gardant les proportions de l'image d'origine
                coef_hauteur_largeur = self.image.get_height()/self.image.get_width()
                scale_height = round(scale_width*coef_hauteur_largeur)

        self.xi = round(width*(decalage_pourcent_x/100))
        self.yi = round(height*(decalage_pourcent_y/100))
        #Nombre de pixels selon les axes x et y dont l'image va être décalée par défaut
        
        self.image = pygame.transform.scale(self.image, (scale_width, scale_height))
        #Adaptation de la taille de l'image axu caractéristiques voulues

        Sprite.liste[nom]=self

        
class Affichage:
    #Classe contenant des attributs qui spécifient l'affichage des éléments du jeu
    
    def init(hauteur_ecran=600):
        TAILLE_ECRAN = (hauteur_ecran*2, hauteur_ecran)
        #On fixe le rapport largeur fenetre/hauteur fenetre

        #Taille des éléments
    
        taille_jeu = round(TAILLE_ECRAN[0]/2)
        #Le jeu s'affiche sur la moitié de la largeur fenêtre
    
        largeur_vie = round((TAILLE_ECRAN[0]/2)-20)
        hauteur_vie = round(largeur_vie/30)
        #La barre de vie est longue comme une moitié de largeur de fenêtre
    
        largeur_durabilite = round((TAILLE_ECRAN[0]/2)-20)
        hauteur_durabilite = round(largeur_durabilite/30)
        #La durabilite de l'arme est longue comme une moitié de largeur de fenêtre

        largeur_attaque = round((TAILLE_ECRAN[0]/4)-20)
        hauteur_attaque = round(largeur_durabilite/30)
        #La puissance d'attaque de l'arme est longue comme un quart de la largeur de la fenêtre.
    
        taille_carte = round((TAILLE_ECRAN[1]/1.5))
        #La carte fait deux tiers de la hauteut de la fenêtre

        taille_points = TAILLE_ECRAN[1]//10
        #La police du texte spécifiant le nombre de points fait un 10eme de la hauteur

        #Positions des éléments

        X_JEU, Y_JEU = 0, 0
        #Jeu, affiché en haut à gauche de la fenêtre
      
        Y_CARTE = round((TAILLE_ECRAN[1]-taille_carte)/2)
        X_CARTE = round(taille_jeu+1+taille_carte/10)
        #Carte, affichée à droite du jeu
    
        X_VIE, Y_VIE = (TAILLE_ECRAN[0]/2)+10, 10
        X_DURABILITE, Y_DURABILITE = (TAILLE_ECRAN[0]/2)+10, Y_VIE+hauteur_vie+10
        X_ATTAQUE, Y_ATTAQUE = (TAILLE_ECRAN[0]/2)+10, Y_DURABILITE+hauteur_durabilite+10
        #Vie, durabilité, attaque affichées en haut de la fenêtre, dans la moitié droite

        X_POINTS, Y_POINTS = X_CARTE, round(Y_CARTE+taille_carte*1.1+10)
        #Points du joueurs, affichés sous la carte du labyrinthe


        Affichage.TAILLE_ECRAN = TAILLE_ECRAN
        Affichage.ECRAN = pygame.display.set_mode(TAILLE_ECRAN)
        #Mise à jour de la taille de l'écran
                       
        Affichage.VIE=Affichage_vie(Coords(X_VIE, Y_VIE), largeur_vie, hauteur_vie)
        Affichage.DURABILITE=Affichage_vie(Coords(X_DURABILITE, Y_DURABILITE), largeur_durabilite, hauteur_durabilite)
        Affichage.ATTAQUE=Affichage_vie(Coords(X_ATTAQUE, Y_ATTAQUE), largeur_attaque, hauteur_attaque)
        Affichage.JEU = Affichage_jeu(Coords(X_JEU, Y_JEU), taille_jeu)
        Affichage.CARTE = Affichage_carte(Coords(X_CARTE, Y_CARTE), taille_carte)
        Affichage.POINTS = Affichage_points(Coords(X_POINTS, Y_POINTS), taille_points)
        #Initialisation des caractéristiques d'affichage de tous les éléments
    

    def rectangle_barre_progressive(x, y, largeur, hauteur, quantite, quantite_max, quantite_min=0):
        #Fonction permettant de créer un rectangle dont la longueur est proportionelle
        #à la quantité passée en paramètre
        rect=(x,y, int(largeur*((quantite-quantite_min)/(quantite_max-quantite_min))), hauteur)
        return rect
    
Affichage.init()
#Permet d'initialiser l'affichage de la fenêtre lorsque ce fichier est importé
