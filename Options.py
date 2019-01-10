class OptJeu:
###Classe qui gère les différentes options du jeu
##    TAILLE_LABYRINTHE = 5
##    NB_CASES = 13
##    DIFFICULTE_LABY = "moyenne"
##    DIFFICULTE_ENNEMI = "moyenne"

    #Classe qui gère les différentes options du jeu
    
    def __init__(hauteur_fenetre=600, taille_laby=5,
                 difficulte_laby="moyenne", difficulte_ennemi="moyenne"):
        
        self.hauteur_fenetre = hauteur_fenetre
        self.taille_laby = taille_laby
        self.difficulte_laby = dificulte_laby
        self.difficulte_ennemi = difficulte_ennemi

    def set_hauteur_fenetre(self, nouvelle_hauteur):
        self.hauteur_fenetre = nouvelle_hauteur

    def set_taille_laby(self, nouvelle_taille):
        self.taille_laby = taille_laby

    def set_difficulte_laby(self, nouvelle_difficulte):
        self.difficulte_laby = difficulte_laby

    def set_dfficulte_ennemi(self, nouvelle_difficulte):
        self.difficulte_ennemi = difficulte_ennemi
