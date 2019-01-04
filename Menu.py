import pygame
from Affichage import *

class Bouton:
    #Classe permettant de gérer un bouton rectangulaire dans un menu
    def __init__(self, couleur, texte, x_bouton, y_bouton, largeur, hauteur):
        #définition des attributs d'un bouton
        self.fenetre = Affichage.ECRAN
        self.couleur = couleur
        self.texte = texte
        self.x_bouton = x_bouton
        self.y_bouton = y_bouton
        self.largeur = largeur
        self.hauteur = hauteur

    def affiche_bouton(self, fenetre):
        #méthode qui permet d'afficher le bouton sur l'écran
        pygame.draw.rect(fenetre, self.couleur, (self.x_bouton, self.y_bouton, self.largeur, self.hauteur))
        font = pygame.font.SysFont('Calibri',60) #choix de la police d'écriture et de la taille
        texte = font.render(self.texte, 1, (0,0,0)) #texte en noir
        fenetre.blit(texte, (self.x_bouton + (self.largeur/2 - texte.get_width()/2), self.y_bouton + (self.hauteur/2 - texte.get_height()/2)))
        #centre le texte dans le bouton

class Menu_principal:
    #Classe permettant de gérer un menu contenant plusieurs boutons
    def __init__(self):
        #définition des attributs des boutons du menu
        couleur_boutons = (255,0,0)
        noms_menus = ["Jouer", "Options", "Tutoriel", "Quitter"]
        posX = Affichage.TAILLE_ECRAN[0]/2-100 #centré
        posY = Affichage.TAILLE_ECRAN[1]/2-200 #Position du premier bouton
        largeur = 200
        hauteur = 100

        #création des boutons et stockage dans un tableau
        self.tab_boutons = []
        for nom in noms_menus:
            self.tab_boutons.append(Bouton(couleur_boutons, nom, posX, posY, largeur, hauteur))
            posY += 110
        

    def affiche_menu(self, fenetre):
        for bouton_courant in self.tab_boutons:
            bouton_courant.affiche_bouton(fenetre)
            


#############################################################################################
#Programme principal pour tests

pygame.init()
pygame.font.init()
continuer = True

menu = Menu_principal()

clock = pygame.time.Clock()

while continuer :
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #Fermeture de la fenêtre
            continuer = False
            
    Affichage.ECRAN.fill((255,255,255))
    menu.affiche_menu(Affichage.ECRAN)

    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
