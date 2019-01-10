#Programme principal
#A exécuter pour lancer le menu du jeu

#Importations
import pygame
from Menu    import *
from Jeu     import *
from Options import *
from Affichage import *

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
    options = OptJeu() #On définit des options par défaut
    return action, options

def traiter_choix_menu_principal(action, options):
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
        lance_options(options)
        options.applique_changements()
        Affichage.init(options.hauteur_fenetre)
        
        
    elif action==3: #Quitter
        fin_utilisation=True

    return not fin_utilisation
##########################################################################################
#Programme principal
continuer = True
while continuer:
    action, options = choix_menu_principal()
    continuer = traiter_choix_menu_principal(action, options)


#Quitter l'application
pygame.quit()
        
    
    

