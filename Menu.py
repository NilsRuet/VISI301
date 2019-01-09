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
        self.estSelectionne = False #Booléen qui indique si le joueur à le sélecteur sur le bouton

    def affiche_bouton(self, fenetre):
        #méthode qui permet d'afficher le bouton sur l'écran
        if self.estSelectionne:
            pygame.draw.rect(fenetre, (0,255,0), (self.x_bouton-8,self.y_bouton-8,self.largeur+16,self.hauteur+16),0)
            #On dessine un contour vert au bouton courant (représentant rectangle de selection)
            
        pygame.draw.rect(fenetre, self.couleur, (self.x_bouton, self.y_bouton, self.largeur, self.hauteur))
        font = pygame.font.SysFont('Calibri',int(60*Affichage.TAILLE_ECRAN[1]/600)) #choix de la police d'écriture et de la taille
        texte = font.render(self.texte, 1, (0,0,0)) #texte en noir
        fenetre.blit(texte, (self.x_bouton + (self.largeur/2 - texte.get_width()/2), self.y_bouton + (self.hauteur/2 - texte.get_height()/2)))
        #centre le texte dans le bouton


class Menu:
    #Classe permettant de gérer un menu contenant plusieurs boutons
    #Les boutons sont situés au centre de l'écran et alignés verticalement.
    #Le titre est centré horizontalement.
    def __init__(self, couleurs_boutons, noms_menus, posY, largeur, hauteur, distance_boutons, titre_menu, posY_titre, taille_titre):
        #définition des attributs des boutons du menu
        self.couleur_boutons = couleurs_boutons
        self.noms_menus = noms_menus #tableau de chaines de caractères
        self.largeur = int(largeur * Affichage.TAILLE_ECRAN[1]/600)
        self.hauteur = int(hauteur * Affichage.TAILLE_ECRAN[0]/1000)
        self.posX = Affichage.TAILLE_ECRAN[0]/2-(self.largeur/2) #centré
        self.posY = posY #Position du premier bouton
        self.distance_boutons = int(self.hauteur + distance_boutons * (Affichage.TAILLE_ECRAN[1]/1000))

        #définition du titre du menu
        font = pygame.font.SysFont('Calibri', taille_titre)
        self.titre_menu = font.render(titre_menu, 1, (255, 0, 0)) #texte en rouge
        self.posX_titre = Affichage.TAILLE_ECRAN[0]/2 - self.titre_menu.get_width()/2 #centré
        self.posY_titre = posY_titre

        #création des boutons et stockage dans un tableau
        self.tab_boutons = []
        for nom in noms_menus:
            self.tab_boutons.append(Bouton(self.couleur_boutons, nom, self.posX, self.posY, self.largeur, self.hauteur))
            self.posY += self.distance_boutons
        

    def affiche_menu(self, fenetre):
        #Affichage du titre du menu
        fenetre.blit(self.titre_menu, (self.posX_titre, self.posY_titre))
        #Affichage des boutons
        for bouton_courant in self.tab_boutons:
            bouton_courant.affiche_bouton(fenetre)

    def lance_menu(self, fenetre):
        continuer = True

        #Placement du rectangle de selection par défaut
        action = 0
        self.tab_boutons[action].estSelectionne = True

        clock = pygame.time.Clock()

        while continuer :
            clock.tick(30)
            
            #Gestion des évènements
            for event in pygame.event.get():
                #Fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    continuer = False
                    action = len(self.tab_boutons)-1 #On considère que le dernier bouton est celui qui fait sortir du menu courant

                #Gestion du déplacement du rectangle de sélection 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP : #si on appuie sur la flèche du haut
                        if action >= 1:
                            #On positionne le rectangle de selection sur la case du dessus
                            self.tab_boutons[action].estSelectionne = False
                            action -= 1
                            self.tab_boutons[action].estSelectionne = True
                            
                    if event.key == pygame.K_DOWN: #si on appuie sur la flèche du bas
                        if action <= len(self.tab_boutons)-2:
                            #On positionne le rectangle de selection sur la case du dessous
                            self.tab_boutons[action].estSelectionne = False
                            action += 1
                            self.tab_boutons[action].estSelectionne = True
                            
                    if event.key == pygame.K_RETURN: #si le joueur appuie sur entrée
                        continuer = False
                            
            #Affichage       
            fenetre.fill((0,0,0))
            self.affiche_menu(fenetre)
            #Rafraichissement de l'affichage
            pygame.display.update()
            

        return action #possibilité de réutiliser le résultat pour savoir quel programme lancer
