#Programme principal
#A exécuter pour lancer le menu du jeu

#Importations
import pygame
from Menu import *
from Jeu  import *

#Initialisations pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption("Jeu")

#Initialisation de la fenêtre (fond noir)
Affichage.ECRAN.fill((0,0,0))


#boucle principale
continuer = True
menu_principal = Menu((255,0,0), ["Jouer", "Tutoriel", "Options", "Quitter"],
                Affichage.TAILLE_ECRAN[1]/2-150, 200, 90, 20, "Menu Principal",
                Affichage.TAILLE_ECRAN[1]/2-265, 70)

while continuer:
    action = menu_principal.lance_menu(Affichage.ECRAN)
    if action == 0: #Jouer, on lance le jeu
        lance_jeu()
##  elif action == 1: #Tutoriel, on lance le menu du tuto
##
##  elif action == 2: #Options, on lance le menu des options
    elif action == 3: #Quitter le programme, on ferme la fenêtre
        continuer = False


#Quitter l'application
pygame.quit()
        
    
    

