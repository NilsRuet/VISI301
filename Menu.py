##################################################################################################
#Fichier permettant de gérer et d'afficher un menu
import pygame
from Affichage import *

Affichage.TAILLE_ECRAN[0] #largeur fenêtre
Affichage.TAILLE_ECRAN[1] #hauteur fenêtre

class Menu:
    #Classe permettant de créer et de gérer les différents boutons d'un menu
    def __init__(self):
        #On définit d'abord tous les paramètres utilisés pour créer un bouton
        couleurs = dict(
            normal=(0, 200, 0),
            survol=(0, 200, 200), )
        couleur_texte = (0,0,0) #texte en noir par défaut
        
        #dictionnaire qui contient la couleur des boutons

        font = pygame.font.SysFont('Calibri',24, bold=True)
        #police d'écriture

        #définition du nom des menus et de l'action à appeler pour chaque bouton
        #TODO Appel des différentes actions
        contenu = (
                    ('JOUER', affiche_jeu),
                    ('OPTIONS', affiche_options),
                    ('TUTORIEL', affiche_tutoriel),
                    ('QUITTER', affiche_quitter)
                                                    )
        posX = (Affichage.TAILLE_ECRAN[0]/2) #position du premier bouton au centre de la largeur de l'écran
        posY = 200 #valeur arbitraire pour l'instant
        largeur = 200
        hauteur = 50

        self.boutons = [] #tableau qui contiendra tous les boutons et leurs attributs
        for texte, action in contenu :
            bouton_courant = BoutonRectMenu(
                            texte,
                            font,
                            couleurs['normal'],
                            couleur_texte,
                            posX,
                            posY,
                            largeur,
                            hauteur,
                            action
                                            )
            self.boutons.append(bouton_courant) #Ajout du bouton dans le tableau
            posY += 100 #Définition de la position du bouton suivant

    def update_menu(self, events):
        #fonction qui met à jour l'affichage du menu
        clic = pygame.mouse.get_pressed()
        posSouris = pygame.mouse.get_pos()
        for bouton in self.boutons :
            if bouton.rect.collidepoint(posSouris): #Si le pointeur est sur un bouton
                bouton.afficher(self.couleurs['survol']) #Changement de la couleur du bouton
                if clic: #Si on clique
                    
            
        
                            
                    
        


class BoutonRectMenu(pygame.sprite.Sprite):
    #Classe permettant de gérer un bouton rectangulaire dans un menu
    #Hérite d'une classe pré-existante de pygame qui gère tous les objets visibles
    def __init__(self, texte, font, couleur_bouton, couleur_texte, posX, posY, largeur, hauteur, action):
        super().__init__()
        #appel du constructeur de la classe mère
        
        self.font = font #police d'écriture du bouton
        self.couleur_bouton = couleur_bouton #couleur du bouton
        self.couleur_texte = couleur_texte #couleur du texte du bouton
        self.posX = posX #abscisse du centre du bouton
        self.posY = posY #ordonnée du centre du bouton
        self.largeur = largeur #largeur du bouton
        self.hauteur = hauteur #hauteur du bouton
        self.action = action #action que le bouton déclenche quand on clique dessus

        self.surface = pygame.Surface((largeur, hauteur))
        #création d'une surface à l'aide de la largeur et de la hauteur entrées en paramètres
        self.rect = surface.get_rect()
        #Récupère la zone de la surface sous la forme d'un rectangle
        self.centre_rect = (posX, posY)
        #Définition de la position du centre du rectangle

        #Gestion du texte qui se trouve dans le bouton
        self.texte = font.render(texte, True, couleur_texte)
        #écrit le texte sur la surface définie précédemment
        self.texte_rect = texte.get_rect()
        self.texte_rect_centre = (largeur/2, hauteur/2)

    def afficher(self,couleur):
        #fonction qui affiche le bouton sur l'écran
        self.surface.fill(couleur)
        self.surface.blit(self.texte, self.texte_rect)

        
