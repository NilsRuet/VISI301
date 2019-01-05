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
            pygame.draw.rect(fenetre, (0,255,0), (self.x_bouton-10,self.y_bouton-10,self.largeur+20,self.hauteur+20),0)
            #On dessine un contour vert au bouton courant (rreprésentant rectangle de selection)
            
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
        noms_menus = ["Jouer", "Tutoriel", "Options", "Quitter"]
        posX = Affichage.TAILLE_ECRAN[0]/2-100 #centré
        posY = Affichage.TAILLE_ECRAN[1]/2-200 #Position du premier bouton
        largeur = 200
        hauteur = 100

        #création des boutons et stockage dans un tableau
        self.tab_boutons = []
        for nom in noms_menus:
            self.tab_boutons.append(Bouton(couleur_boutons, nom, posX, posY, largeur, hauteur))
            posY += 120
        

    def affiche_menu(self, fenetre):
        for bouton_courant in self.tab_boutons:
            bouton_courant.affiche_bouton(fenetre)

    def lance_menu(self,fenetre):
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
                    action = 3

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
                      # (jouer, options, tuto ou quitter)
            


#############################################################################################
#Programme principal pour tests
##
##pygame.init()
##pygame.font.init()
##
##menu = Menu_principal()
##menu.lance_menu(Affichage.ECRAN)
