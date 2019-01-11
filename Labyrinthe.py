###########################################################################
# Fichiers contenant les classes de génération et d'affichage du labyrinthe

import random
from Affichage import *
from Options import *
from Piece import *

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
    
    def __init__(self, nb_salles_par_ligne):
        self.nb_zones=0
        self.taille = 2*nb_salles_par_ligne-1
        self.init_struct_carte_lab(self.taille)
        self.creer_lab_parfait()
        if OptJeu.DIFFICULTE_LABY == "moyenne":
            self.enlever_murs(1/4)
        elif OptJeu.DIFFICULTE_LABY == "faible":
            self.enlever_murs(1/2)
        
        self.arrivee = random.randint(1,self.nb_zones)
    
    def init_struct_carte_lab(self, taille):
        self.carte=["+"]*(taille)
        for colonne in range(len(self.carte)):
            self.carte[colonne]=["+"]*(taille)
            
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

    def creer_lab_parfait(self):
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

    def enlever_murs(self, proportion):
        liste_murs=[]
        #On liste les murs verticaux
        for colonne in range(1,len(self.carte), 2):
            for ligne in range(0,len(self.carte[0]),2):
                if self.carte[colonne][ligne]:
                    liste_murs.append((colonne,ligne))

        #On liste les murs horizontaux
        for colonne in range(0,len(self.carte), 2):
            for ligne in range(1,len(self.carte[0]),2):
                if self.carte[colonne][ligne]:
                    liste_murs.append((colonne,ligne))

        random.shuffle(liste_murs)
        for i in range(0,round(proportion*len(liste_murs))):
            self.carte[liste_murs[i][0]][liste_murs[i][1]]=False
          
    def brisable(self, salle1, salle2):
        #Méthode permettant de savoir si deux salles n'appartiennent pas à la même zone
        #donc si le mur entre ces deux salles peut etre briser sans créer de boucle
        num1 = self.carte[salle1[0]][salle1[1]].get_zone()
        num2 = self.carte[salle2[0]][salle2[1]].get_zone()
        return num1!=num2

    def get_piece(self, col, ligne):
        return Piece.listePieces[self.carte[col][ligne].zone]

    def placer_depart(self, num_depart):
        self.depart = num_depart
        
    def affiche_lab(self, piece_actu=(0,0)):
        #Méthode d'affichage du labyrinthe dans une fenêtre 
        def trouve_coords_elem(x_lab, y_lab):
            largeur_piece = Affichage.CARTE.taille_piece[0]
            epaisseur_mur = Affichage.CARTE.taille_mur[0]

            nb_pieces_x = ((x_lab+1)//2)
            nb_murs_x = ((x_lab)//2)

            nb_pieces_y = ((y_lab+1)//2)
            nb_murs_y = ((y_lab)//2)

            x = epaisseur_mur*nb_murs_x + largeur_piece*nb_pieces_x + Affichage.CARTE.coords.xi
            y = epaisseur_mur*nb_murs_y + largeur_piece*nb_pieces_y + Affichage.CARTE.coords.yi

            return x, y

        #Affichage des pièces
        for col_lab in range(0,len(self.carte),2):
            for ligne_lab in range(0,len(self.carte[0]),2):
                x_piece, y_piece = trouve_coords_elem(col_lab, ligne_lab)
                #On définit les coordonnée et la taille de la pièces à afficher
                if self.get_piece(col_lab, ligne_lab).vue:
                    if col_lab==piece_actu[0] and ligne_lab==piece_actu[1]:
                        #Affichage de la pièce dans laquelle se trouve le personnage
                        Affichage.ECRAN.blit(Sprite.liste["piece_joueur"].image,(x_piece+Sprite.liste["piece_joueur"].xi,y_piece+Sprite.liste["piece_joueur"].yi))
                    elif (self.get_piece(col_lab, ligne_lab).typePiece == "repos") or (self.get_piece(col_lab, ligne_lab).typePiece == "depart"):
                        Affichage.ECRAN.blit(Sprite.liste["piece_feu_de_camp"].image,(x_piece+Sprite.liste["piece_feu_de_camp"].xi,y_piece+Sprite.liste["piece_feu_de_camp"].yi))
                    else:
                        Affichage.ECRAN.blit(Sprite.liste["piece_vide"].image,(x_piece+Sprite.liste["piece_vide"].xi,y_piece+Sprite.liste["piece_vide"].yi))
                 

           
        #Affichage des murs verticaux
        for col_mur in range(1,len(self.carte), 2):
            for ligne_mur in range(0,len(self.carte[0]),2):
                #On sélectionne chaque mur vertical (x impair, y pair dans le labyrinthe)
                if self.get_piece(col_mur+1, ligne_mur).vue or self.get_piece(col_mur-1, ligne_mur).vue:
                    #On regarde si une des pièces qu'il sépare a été vue avant de l'afficher.
                    x_mur, y_mur = trouve_coords_elem(col_mur, ligne_mur)
                    #On définit les coordonnées du mur             
                    if self.carte[col_mur][ligne_mur]:
                        Affichage.ECRAN.blit(Sprite.liste["mur_vertical"].image,(x_mur+Sprite.liste["mur_vertical"].xi,y_mur+Sprite.liste["mur_vertical"].yi))
                    else:
                        Affichage.ECRAN.blit(Sprite.liste["ouverture_verticale"].image,(x_mur+Sprite.liste["ouverture_verticale"].xi,y_mur+Sprite.liste["ouverture_verticale"].yi))
                    
        #Affichage des murs horizontaux
        for col_mur in range(0,len(self.carte),2):
            for ligne_mur in range(1,len(self.carte[0]),2):
                #On sélectionne chaque mur horizontal (x pair, y impair dans le labyrinthe)
                if self.get_piece(col_mur, ligne_mur+1).vue or self.get_piece(col_mur, ligne_mur-1).vue:
                    #On regarde si une des pièces qu'il sépare a été vue avant de l'afficher.
                    x_mur, y_mur = trouve_coords_elem(col_mur, ligne_mur)
                    #On définit les coordonnées du mur
                
                    if self.carte[col_mur][ligne_mur]:
                        Affichage.ECRAN.blit(Sprite.liste["mur_horizontal"].image,(x_mur+Sprite.liste["mur_horizontal"].xi,y_mur+Sprite.liste["mur_horizontal"].yi))
                    else:
                        Affichage.ECRAN.blit(Sprite.liste["ouverture_horizontale"].image,(x_mur+Sprite.liste["ouverture_horizontale"].xi,y_mur+Sprite.liste["ouverture_horizontale"].yi))
