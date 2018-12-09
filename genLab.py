import random

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
            

    def print_lab(self):
        print("-"*(len(self.carte)*2+3))
        for i in range(len(self.carte)):
            ligne="| "
            for j in range(len(self.carte[0])):
                if isinstance(self.carte[i][j], Zone):
                    #ligne+="{:^4}".format(str(self.carte[i][j].get_zone()))
                    ligne+="{:^2}".format(" ")
                elif isinstance(self.carte[i][j], bool):
                    if self.carte[i][j]:
                        ligne+="{:^2}".format("+")
                    else:
                        ligne+="{:^2}".format(" ")
                else:
                    ligne+="{:^2}".format(str(self.carte[i][j]))
            print(ligne+"|")
        print("-"*(len(self.carte)*2+3))
                
Labyrinthe(10).print_lab()
#Ligne de test
