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
        
    def __init__(self, coordsF, tailleF):
        self.coords = coordsF
        #Coordonnées "de départ" pour afficher le jeu

        self.taille=tailleF
        
        self.taille_case = (round(tailleF/OptJeu.NB_CASES),round(tailleF/OptJeu.NB_CASES))
        #Taille des cases du jeu

    def fond_jeu(self, sprite_fond):
        #Colle une image par défaut sur chaque case du jeu
        for colonne in range(OptJeu.NB_CASES):
            for ligne in range(OptJeu.NB_CASES):
                Affichage.ECRAN.blit(sprite_fond.image, (colonne*self.taille_case[0], ligne*self.taille_case[1]))
                
class Affichage_carte:
    #Classe regroupant les caractéristiques de la carte
    def fond_carte(self):
        Affichage.ECRAN.blit(Sprite.liste["fond_carte"].image, (self.coords.xi+Sprite.liste["fond_carte"].xi, self.coords.yi+Sprite.liste["fond_carte"].yi))
        
    def __init__(self, coordsF, tailleF):
        self.coords = coordsF
        #Coordonnées "de départ" pour afficher la carte

        self.taille = tailleF
        vraie_taille_piece = round((tailleF/OptJeu.TAILLE_LABYRINTHE))
        self.taille_piece = (vraie_taille_piece,vraie_taille_piece)
        #Taille des cases de la carte

class Affichage_vie:
    def __init__(self, coordsF, largeurF, hauteurF):
        self.coords = coordsF
        self.largeur = largeurF
        self.hauteur = hauteurF

class Affichage_durabilite_arme:
    def __init__(self, coordsF, largeurF, hauteurF):
        self.coords = coordsF
        self.largeur = largeurF
        self.hauteur = hauteurF

class Affichage_puissance_arme:
    def __init__(self, coordsF, largeurF, hauteurF):
        self.coords = coordsF
        self.largeur = largeurF
        self.hauteur = hauteurF

class Affichage_points:
    def __init__(self, coordsF, taille_texteF):
        self.coords = coordsF
        self.taille_texte=taille_texteF
        
class Sprite:
    liste={}
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
                #Adaptation de la largeur par rapport à la hauteur
                coef_largeur_hauteur = self.image.get_width()/self.image.get_height()
                scale_width = round(scale_height*coef_largeur_hauteur)             
                
            if not fix_height:
                #Adaptation de la hauteur par rapport à la largeur
                coef_hauteur_largeur = self.image.get_height()/self.image.get_width()
                scale_height = round(scale_width*coef_hauteur_largeur)

        self.xi = round(width*(decalage_pourcent_x/100))
        self.yi = round(height*(decalage_pourcent_y/100))
        
        self.image = pygame.transform.scale(self.image, (scale_width, scale_height))

        Sprite.liste[nom]=self

        
class Affichage:
    #Initialisation de la fenêtre
    def init(hauteur_ecran=600):
        TAILLE_ECRAN = (hauteur_ecran*2, hauteur_ecran) #largeur / hauteur

        #Taille des éléments
    
        taille_jeu = round(TAILLE_ECRAN[0]/2)
        #Jeu
    
        largeur_vie = round((TAILLE_ECRAN[0]/2)-20)
        hauteur_vie = round(largeur_vie/30)
        #Vie
    
        largeur_durabilite = round((TAILLE_ECRAN[0]/2)-20)
        hauteur_durabilite = round(largeur_durabilite/30)
        #Durabilite de l'arme

        largeur_attaque = round((TAILLE_ECRAN[0]/4)-20)
        hauteur_attaque = round(largeur_durabilite/30)
        #Puissance d'attaque de l'arme
    
        taille_carte = round((TAILLE_ECRAN[1]/1.5))
        #Carte

        taille_points = TAILLE_ECRAN[1]//10

        #Positions des éléments

        X_JEU, Y_JEU = 0, 0
        #Jeu
      
        Y_CARTE = round((TAILLE_ECRAN[1]-taille_carte)/2)
        X_CARTE = round(taille_jeu+1+taille_carte/10)
        #Carte
    
        X_VIE, Y_VIE = (TAILLE_ECRAN[0]/2)+10, 10
        X_DURABILITE, Y_DURABILITE = (TAILLE_ECRAN[0]/2)+10, Y_VIE+hauteur_vie+10
        X_ATTAQUE, Y_ATTAQUE = (TAILLE_ECRAN[0]/2)+10, Y_DURABILITE+hauteur_durabilite+10
        #Vie

        X_POINTS, Y_POINTS = X_CARTE, round(Y_CARTE+taille_carte*1.1+10)
        #Points du joueurs


        Affichage.TAILLE_ECRAN = TAILLE_ECRAN
        Affichage.ECRAN = pygame.display.set_mode(TAILLE_ECRAN)
                       
        Affichage.VIE=Affichage_vie(Coords(X_VIE, Y_VIE), largeur_vie, hauteur_vie)
        Affichage.DURABILITE=Affichage_vie(Coords(X_DURABILITE, Y_DURABILITE), largeur_durabilite, hauteur_durabilite)
        Affichage.ATTAQUE=Affichage_vie(Coords(X_ATTAQUE, Y_ATTAQUE), largeur_attaque, hauteur_attaque)
        Affichage.JEU = Affichage_jeu(Coords(X_JEU, Y_JEU), taille_jeu)
        Affichage.CARTE = Affichage_carte(Coords(X_CARTE, Y_CARTE), taille_carte)
        Affichage.POINTS = Affichage_points(Coords(X_POINTS, Y_POINTS), taille_points)
    #Initialisation des caractéristiques d'affichage de tous les éléments
    

    def rectangle_barre_progressive(x, y, largeur, hauteur, quantite, quantite_max, quantite_min=0):
        rect=(x,y, int(largeur*((quantite-quantite_min)/(quantite_max-quantite_min))), hauteur)
        return rect
    
Affichage.init()
