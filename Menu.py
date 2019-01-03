##################################################################################################
#Fichier permettant de gérer et d'afficher un menu
import pygame
from Affichage import *


class Menu:
    #Classe permettant de créer et de gérer les différents boutons d'un menu
    def __init__(self, application, *groupes):
        #On définit d'abord tous les paramètres utilisés pour créer un bouton
        self.couleurs = dict(
            normal=(0, 200, 0),
            survol=(0, 200, 200), )
        self.couleur_texte = (0,0,0) #texte en noir par défaut
        #dictionnaire qui contient la couleur des boutons

        font = pygame.font.SysFont('Calibri',24, bold=True)
        #police d'écriture

        #définition du nom des menus et de l'action à appeler pour chaque bouton
        contenu = (
                    ('JOUER', application.affiche_jeu),
                    ('OPTIONS', application.affiche_options),
                    ('TUTORIEL', application.affiche_tutoriel),
                    ('QUITTER', application.affiche_quitter)
                                                    )
        posX = (Affichage.TAILLE_ECRAN[0]/2) #position du premier bouton au centre de la largeur de l'écran
        posY = 200 #valeur arbitraire pour l'instant
        largeur = 200
        hauteur = 50

        self._boutons = [] #tableau qui contiendra tous les boutons et leurs attributs
        for texte, action in contenu :
            bouton_courant = BoutonRectMenu(
                            texte,
                            font,
                            self.couleurs['normal'],
                            self.couleur_texte,
                            posX,
                            posY,
                            largeur,
                            hauteur,
                            action
                                            )
            self._boutons.append(bouton_courant) #Ajout du bouton dans le tableau
            posY += 100 #Définition de la position du bouton suivant
            for groupe in groupes :
                groupe.add(bouton_courant) #on ajoute le sprite du bouton dans la liste des sprites

    def update(self, events):
        #fonction qui met à jour l'affichage du menu
        clic, *_ = pygame.mouse.get_pressed()
        posSouris = pygame.mouse.get_pos()
        for bouton in self._boutons :
            if bouton.rect.collidepoint(*posSouris): #Si le pointeur est sur un bouton
                bouton.afficher(self.couleurs['survol']) #Changement de la couleur du bouton
                if clic: #Si on clique
                    #Appel de l'action que doit effectuer le bouton
                    bouton.executerAction()
                break
            else:
                bouton.afficher(self.couleurs['normal']) #pas sur un bouton

    def init(self):
        #permet d'initialiser le pointeur de la souris
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    
            
        

class BoutonRectMenu(pygame.sprite.Sprite):
    #Classe permettant de gérer un bouton rectangulaire dans un menu
    #Hérite d'une classe pré-existante de pygame qui gère tous les objets visibles
    def __init__(self, texte, font, couleur_bouton, couleur_texte, posX, posY, largeur, hauteur, action):
        super().__init__()
        #appel du constructeur de la classe mère
        
        self._action = action #action que le bouton déclenche quand on clique dessus

        self.image = pygame.Surface((largeur, hauteur))
        #création d'une surface à l'aide de la largeur et de la hauteur entrées en paramètres
        self.rect = self.image.get_rect()
        #Récupère la zone de la surface sous la forme d'un rectangle
        self.centre_rect = (posX, posY)
        #Définition de la position du centre du rectangle

        #Gestion du texte qui se trouve dans le bouton
        self.texte = font.render(texte, True, couleur_texte)
        #écrit le texte sur la surface définie précédemment
        self.texte_rect = self.texte.get_rect()
        self.texte_rect_centre = (largeur/2, hauteur/2)

        self.afficher(couleur_bouton)

    def afficher(self,couleur):
        #fonction qui affiche le bouton sur l'écran
        self.image.fill(couleur)
        self.image.blit(self.texte, self.texte_rect)

    def executerAction(self):
        #Appel l'action à effectuer quand on appuie sur le bouton
        self._action()

class Application:
    #Classe permettant de gérer les différentes parties du jeu (jeu en lui-même, menus...)
    #Peut-être à définir dans un autre fichier
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("test menu")
        self.fond = (0,0,0)
        self.fenetre = Affichage.ECRAN
        self.groupeAffichage = pygame.sprite.Group() #Groupe contenant les sprites à afficher
        self.run = True

    def _reinitialiser(self):
        try:
            self.ecran.init()
            self.groupeAffichage.empty()
            #On vide la liste contenant les sprites à afficher
        except AttributeError:
            pass

    def affiche_menu(self):
        #gère l'affichage du menu
        self._reinitialiser()
        self.ecran = Menu(self, self.groupeAffichage)

    def affiche_jeu(self):
        #gère l'affichage du jeu
        #TODO
        self._reinitialiser()

    def affiche_options(self):
        #gère l'affichage des options
        #TODO
        self._reinitialiser()

    def affiche_tutoriel(self):
        #gère l'affichage du tutoriel
        #TODO
        self._reinitialiser()

    def affiche_quitter(self):
        #gère le cas où on souhaite quitter le jeu
        self.run = False

    def update(self):
        events = pygame.event.get()
        for event in events :
            if event.type == pygame.QUIT:
                self.affiche_quitter()
            
        self.fenetre.fill(self.fond)
        self.ecran.update(events)
        self.groupeAffichage.update()
        self.groupeAffichage.draw(self.fenetre) #dessine tous les sprites à afficher
        pygame.display.update()

########################################################################################
#Programme principal pour tests

appli = Application()
appli.affiche_menu()

clock = pygame.time.Clock()

while appli.run:
    appli.update()
    clock.tick(30)
    
pygame.quit()
    
    

        
