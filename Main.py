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
###########################################################################################
def choix_menu_principal():
    menu = menu_principal()
    
    action = menu.lance_menu(Affichage.ECRAN)
    return action

def traiter_choix_menu_principal(action):
    fin_utilisation=False
    if action==0: #Jouer
        enjeu=True
        while enjeu:
            jeu = Jeu()
            jeu.executer_jeu()
            enjeu=jeu.rejouer

##    elif action == 1 :  #Tutoriel
##        lance_tutoriel()
        
    elif action ==2: #Options
        lance_options()
        
    elif action==3: #Quitter
        fin_utilisation=True

    return not fin_utilisation
##########################################################################################
#Programme principal
continuer = True
while continuer:
    action = choix_menu_principal()
    continuer = traiter_choix_menu_principal(action)


#Quitter l'application
pygame.quit()
        
    
    

