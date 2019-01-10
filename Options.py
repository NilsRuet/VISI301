class OptJeu:
#Classe qui gère les différentes options du jeu
    TAILLE_LABYRINTHE = 5
    NB_CASES = 13
    DIFFICULTE_LABY = "moyenne"
    DIFFICULTE_ENNEMI = "moyenne"

    #Classe qui gère les différentes options du jeu
    
    def __init__(self, hauteur_fenetre=600, taille_laby=5,
                 difficulte_laby="moyenne", difficulte_ennemi="moyenne"):
        
        self.hauteur_fenetre = hauteur_fenetre
        self.taille_laby = taille_laby
        self.difficulte_laby = difficulte_laby
        self.difficulte_ennemi = difficulte_ennemi

    def set_hauteur_fenetre(self, nouvelle_hauteur):
        self.hauteur_fenetre = nouvelle_hauteur

    def set_taille_laby(self, nouvelle_taille):
        self.taille_laby = nouvelle_taille

    def set_difficulte_laby(self, nouvelle_difficulte):
        self.difficulte_laby = nouvelle_difficulte

    def set_difficulte_ennemi(self, nouvelle_difficulte):
        self.difficulte_ennemi = nouvelle_difficulte

    def applique_changements(self):
        OptJeu.TAILLE_LABYRINTHE = self.taille_laby
        OptJeu.DIFFICULTE_LABY = self.difficulte_laby
        OptJeu.DIFFICULTE_ENNEMI = self.difficulte_ennemi
