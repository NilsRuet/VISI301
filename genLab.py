import random
from Affichage import *

class Zone:
    nb=0
    def __init__(self):
        Zone.nb+=1
        self.zone = Zone.nb
        self.suiv=None

    def devient(self, nv_zone):
        parcours_anc_val=self
        parcours_nv_val=nv_zone
        while not parcours_nv_val.suiv is None:
            parcours_nv_val=parcours_nv_val.suiv

        while not parcours_anc_val.suiv is None:
            parcours_anc_val=parcours_anc_val.suiv

        parcours_anc_val.suiv=parcours_nv_val
        Zone.nb-=1

    def get_zone(self):
        parcours = self
        while not parcours.suiv is None:
            parcours=parcours.suiv
        return parcours.zone


class Labyrinthe:
    def brisable(self, salle1, salle2):
        num1 = self.carte[salle1[0]][salle1[1]].get_zone()
        num2 = self.carte[salle2[0]][salle2[1]].get_zone()
        return num1!=num2
    
    def __init__(self, taille):
        self.carte=["+"]*(2*taille-1)
        self.taille = 2*taille-1
        
        for i in range(len(self.carte)):
            #Initialisation largeur carte
            self.carte[i]=["+"]*(2*taille-1)

        for i in range(0,len(self.carte),2):
            #Initialisation hauteur carte
            for j in range(0,len(self.carte[0]),2):
                self.carte[i][j]=Zone()

        for i in range(1,len(self.carte), 2):
            #Initialisation mur verticaux
            for j in range(0,len(self.carte[0]),2):
                self.carte[i][j]=True

        for i in range(0,len(self.carte), 2):
            #Initialisation mur horizontaux
            for j in range(1,len(self.carte[0]),2):
                self.carte[i][j]=True

        #Début de l'algorithme de génération
        #On liste les murs du labyrinthes
        liste_murs=[]
        #Murs verticaux
        for i in range(1,len(self.carte), 2):
            for j in range(0,len(self.carte[0]),2):
                liste_murs.append((i,j))

        #Murs horizontaux
        for i in range(0,len(self.carte), 2):
            for j in range(1,len(self.carte[0]),2):
                liste_murs.append((i,j))

        #On mélange la liste des murs pour générer un labyrinthe aléatoire
        random.shuffle(liste_murs)

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
            

    def print_lab(self, piece_actu=(0,0)):
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
        #Pièces
        for i_lab in range(0,len(self.carte),2):
            for j_lab in range(0,len(self.carte[0]),2):
                i = i_lab//2
                j = j_lab//2
                
                largeur=Affichage.CARTE.taille_piece[0]
                hauteur=Affichage.CARTE.taille_piece[1]
                
                x_piece=Affichage.CARTE.coords.xi + (i)*largeur
                y_piece=Affichage.CARTE.coords.yi + (j)*hauteur
                
                
                if i_lab==piece_actu[1] and j_lab==piece_actu[0]:
                    #piece_actuelle
                    pygame.draw.rect(Affichage.ECRAN, (200,200,200), (x_piece, y_piece, largeur, hauteur))
                else:
                    pygame.draw.rect(Affichage.ECRAN, (255,255,255), (x_piece, y_piece, largeur, hauteur))
        #vertical
        for j_mur in range(0,len(self.carte), 2):
            for i_mur in range(1,len(self.carte[0]),2):
                if self.carte[j_mur][i_mur]:
                    largeur=Affichage.CARTE.taille_piece[0]//10
                    hauteur=Affichage.CARTE.taille_piece[1]

                    x_mur = (((i_mur)//2)+1)*Affichage.CARTE.taille_piece[0] + Affichage.CARTE.coords.xi
                    y_mur = (((j_mur)//2))*Affichage.CARTE.taille_piece[1] + Affichage.CARTE.coords.yi

                    pygame.draw.rect(Affichage.ECRAN, (0,255,0), (x_mur, y_mur, largeur, hauteur))
        #horizontal
        for j_mur in range(1,len(self.carte), 2):
            for i_mur in range(0,len(self.carte[0]),2):
                if self.carte[j_mur][i_mur]:
                    largeur=Affichage.CARTE.taille_piece[0]
                    hauteur=Affichage.CARTE.taille_piece[1]//10

                    x_mur = (((i_mur)//2))*Affichage.CARTE.taille_piece[0] + Affichage.CARTE.coords.xi
                    y_mur = (((j_mur)//2)+1)*Affichage.CARTE.taille_piece[1] + Affichage.CARTE.coords.yi

                    pygame.draw.rect(Affichage.ECRAN, (0,255,0), (x_mur, y_mur, largeur, hauteur))
