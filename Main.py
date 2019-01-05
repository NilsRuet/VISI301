#Programme principal
#A exécuter pour lancer le menu du jeu

#Importations
import pygame
from Menu import *
#from Jeu import *
from Affichage import *

#Initialisations pygame
pygame.init()
pygame.font.init()

#Initialisation de la fenêtre (fond noir)
Affichage.ECRAN.fill((0,0,0))

#Boucle principale
continuer = True
#On détermine la première chose à afficher (menu principal)
menu = Menu_principal()
action = menu.lance_menu(Affichage.ECRAN)

while continuer:
##    if action == 0: #Jouer, on lance le jeu
##
##    elif action == 1: #Tutoriel, on lance le menu du tuto
##
##    elif action == 2: #Options, on lance le menu des options

    if action == 3: #Quitter le programme, on ferme la fenêtre
        continuer = False

pygame.quit()
        
    
    

