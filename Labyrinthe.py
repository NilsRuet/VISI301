###########################################################################
# Fichiers contenant les classes de génération et d'affichage du labyrinthe

import random
from Affichage import *

class Zone:
    #Classe représentant une "case" du labyrinthe, permet de facilement lier des cases entre elles
    def __init__(self, nb):
        self.zone = nb
        #Numero de la case
        self.suiv=None
        #Case à laquelle est rattaché cette case
        
    def devient(self, nv_zone):
        #Méthode permettant de lier deux zones du labyrinthe
        parcours_anc_val=self
        parcours_nv_val=nv_zone
        
        while not parcours_nv_val.suiv is None:
            parcours_nv_val=parcours_nv_val.suiv
        while not parcours_anc_val.suiv is None:
            parcours_anc_val=parcours_anc_val.suiv
        #On trouve les cases "finales" auxquelles sont rattachées les cases à fusionner
            
        parcours_anc_val.suiv=parcours_nv_val
        #la case finale d'une des deux cases est rattachée à la case finale de l'autre case

    def get_zone(self):
        #Méthode permettant de retrouver la valeur de la case finale à laquelle est rattachée une case
        parcours = self
        while not parcours.suiv is None:
            parcours=parcours.suiv
        return parcours.zone


class Labyrinthe:
    #Classe représentant un labyrinthe
    
    def __init__(self, taille):
        self.carte=["+"]*(2*taille-1)
        self.taille = 2*taille-1
        self.nb_zones=0
        
        #Initialisation des zones (= pièces) du labyrinthe
        for colonne in range(len(self.carte)):
            self.carte[colonne]=["+"]*(2*taille-1)
        
        #Initialisation des zones (= pièces) du labyrinthe
        for colonne in range(0,len(self.carte),2):
            for ligne in range(0,len(self.carte[0]),2):
                self.nb_zones+=1
                self.carte[colonne][ligne]=Zone(self.nb_zones)
        
        #Initialisation mur verticaux
        for colonne in range(1,len(self.carte), 2):
            for ligne in range(0,len(self.carte[0]),2):
                self.carte[colonne][ligne]=True
       
        #Initialisation mur horizontaux
        for colonne in range(0,len(self.carte), 2):
            for ligne in range(1,len(self.carte[0]),2):
                self.carte[colonne][ligne]=True          

        #Début de l'algorithme de génération
        #On liste les murs du labyrinthes
        liste_murs=[]
        
        #On liste les murs verticaux
        for colonne in range(1,len(self.carte), 2):
            for ligne in range(0,len(self.carte[0]),2):
                liste_murs.append((colonne,ligne))

        #On liste les murs horizontaux
        for colonne in range(0,len(self.carte), 2):
            for ligne in range(1,len(self.carte[0]),2):
                liste_murs.append((colonne,ligne))

        #On mélange la liste des murs pour générer un labyrinthe aléatoire
        random.shuffle(liste_murs)

        #On va créer le labyrinthe en brisant si possible les murs, dans l'ordre de la liste
        for coord_mur in liste_murs:
            #Pour chaque mur on test si on peut le briser
            x = coord_mur[0]
            y = coord_mur[1]
            #On indique les salles séparées par le mur en fonction de s'il est vertical ou horizontal
            if x%2==0:
                #horizontal
                salles_voisines=((x,y+1),(x,y-1)) 
            else:
                #vertical
                salles_voisines=((x+1,y),(x-1,y))
                
            if self.brisable(salles_voisines[0],salles_voisines[1]):
                #Si le mur est brisable on fusionne les deux "zones" auxquelles appartiennent les salles
                #Et on brise le mur
                salle1 = self.carte[salles_voisines[0][0]][salles_voisines[0][1]]
                salle2 = self.carte[salles_voisines[1][0]][salles_voisines[1][1]]
                salle1.devient(salle2)                
                self.carte[x][y]=False

        self.depart = random.randint(1,self.nb_zones)
        self.arrivee = random.randint(1,self.nb_zones)
        while self.arrivee==self.depart:
            self.arrivee = random.randint(1,self.nb_zones)
        #On choisit au hasard deux cases du labyrinthe différentes qui seront l'arrivée et le départ
            
    def brisable(self, salle1, salle2):
        #Méthode permettant de savoir si deux salles n'appartiennent pas à la même zone
        #donc si le mur entre ces deux salles peut etre briser sans créer de boucle
        num1 = self.carte[salle1[0]][salle1[1]].get_zone()
        num2 = self.carte[salle2[0]][salle2[1]].get_zone()
        return num1!=num2
    
    def print_lab(self, piece_actu=(0,0)):
        #Méthode permettant l'affichage du labyrinthe dans la console
        print("-"*(len(self.carte)*2+3))
        for i in range(len(self.carte)):
            ligne="| "
            for j in range(len(self.carte[0])):
                if i==piece_actu[0] and j==piece_actu[1]:
                    ligne+="{:^2}".format("*")
                elif isinstance(self.carte[i][j], Zone):
                    ligne+="{:^2}".format(" ")
                elif isinstance(self.carte[i][j], bool):
                    if self.carte[i][j]:
                        if i%2 == 0:
                            c="+"
                        else:
                            c="+"
                        ligne+="{:^2}".format(c)
                    else:
                        ligne+="{:^2}".format(" ")
                else:
                    ligne+="{:^2}".format(str(self.carte[i][j]))
            print(ligne+"|")
        print("-"*(len(self.carte)*2+3))

    def affiche_lab(self, piece_actu=(0,0)):
        #Méthode d'affichage du labyrinthe dans une fenêtre
        
        #Affichage des pièces
        for col_lab in range(0,len(self.carte),2):
            for ligne_lab in range(0,len(self.carte[0]),2):
                col = col_lab//2
                ligne = ligne_lab//2
                #Pour chaque pièce, on retrouve ses coordonnées relatives aux autres pièces (en ignorant les murs)
                
                largeur=Affichage.CARTE.taille_piece[0]
                hauteur=Affichage.CARTE.taille_piece[1]
                #On définit les dimensions d'une pièce
                
                x_piece=Affichage.CARTE.coords.xi + (col)*largeur
                y_piece=Affichage.CARTE.coords.yi + (ligne)*hauteur
                #On définit les coordonnée et la taille de la pièces à afficher
                
                if col_lab==piece_actu[0] and ligne_lab==piece_actu[1]:
                    #Affichage de la pièce dans laquelle se trouve le personnage
                    pygame.draw.rect(Affichage.ECRAN, (200,200,200), (x_piece, y_piece, largeur, hauteur))
                    
                elif self.carte[col_lab][ligne_lab].zone == self.depart:
                    #Affichage de la pièce de départ (bleue)
                    pygame.draw.rect(Affichage.ECRAN, (0,0,255), (x_piece, y_piece, largeur, hauteur))
                    
                elif self.carte[col_lab][ligne_lab].zone  == self.arrivee:
                    #Affichage de la pièce d'arrivée (rouge)
                    pygame.draw.rect(Affichage.ECRAN, (255,0,0), (x_piece, y_piece, largeur, hauteur))
                    
                else:
                    #Affichage d'une pièce sans particularité
                    pygame.draw.rect(Affichage.ECRAN, (255,255,255), (x_piece, y_piece, largeur, hauteur))
                    
        #Affichage des murs verticaux
        for col_mur in range(1,len(self.carte), 2):
            for ligne_mur in range(0,len(self.carte[0]),2):
                #On sélectionne chaque mur vertical (x impair, y pair dans le labyrinthe)
                
                x_mur = (((col_mur)//2)+1)*Affichage.CARTE.taille_piece[0] + Affichage.CARTE.coords.xi
                y_mur = (((ligne_mur)//2))*Affichage.CARTE.taille_piece[1] + Affichage.CARTE.coords.yi
                #On définit les coordonnées du mur             
                if self.carte[col_mur][ligne_mur]:
                    Affichage.ECRAN.blit(Sprite.liste["mur_vertical"].image,(x_mur+Sprite.liste["mur_vertical"].xi,y_mur+Sprite.liste["mur_vertical"].yi))
                else:
                    Affichage.ECRAN.blit(Sprite.liste["ouverture_verticale"].image,(x_mur+Sprite.liste["ouverture_verticale"].xi,y_mur+Sprite.liste["ouverture_verticale"].yi))
        #Affichage des murs horizontaux
        for col_mur in range(0,len(self.carte),2):
            for ligne_mur in range(1,len(self.carte[0]),2):
                #On sélectionne chaque mur horizontal (x pair, y impair dans le labyrinthe)
                x_mur = (((col_mur)//2))*Affichage.CARTE.taille_piece[0] + Affichage.CARTE.coords.xi
                y_mur = (((ligne_mur)//2)+1)*Affichage.CARTE.taille_piece[1] + Affichage.CARTE.coords.yi
                #On définit les coordonnées du mur
                
                if self.carte[col_mur][ligne_mur]:
                    Affichage.ECRAN.blit(Sprite.liste["mur_horizontal"].image,(x_mur+Sprite.liste["mur_horizontal"].xi,y_mur+Sprite.liste["mur_horizontal"].yi))
                else:
                    Affichage.ECRAN.blit(Sprite.liste["ouverture_horizontale"].image,(x_mur+Sprite.liste["ouverture_horizontale"].xi,y_mur+Sprite.liste["ouverture_horizontale"].yi))
