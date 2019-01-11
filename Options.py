class OptJeu:
#Classe qui gère les différentes options du jeu
    TAILLE_LABYRINTHE = 5
    NB_CASES = 13
    DIFFICULTE_LABY = "moyenne"
    DIFFICULTE_ENNEMI = "moyenne"
    
    def __init__(self, hauteur_fenetre=600, taille_laby=5,
                 difficulte_laby="moyenne", difficulte_ennemi="moyenne"):
        
        self.hauteur_fenetre = hauteur_fenetre
        self.taille_laby = taille_laby
        self.difficulte_laby = difficulte_laby
        self.difficulte_ennemi = difficulte_ennemi

    def set_hauteur_fenetre(self, nouvelle_hauteur):
        #changement de la hauteur de la fenêtre
        self.hauteur_fenetre = nouvelle_hauteur

    def set_taille_laby(self, nouvelle_taille):
        #changement de la taille du labyrinthe
        self.taille_laby = nouvelle_taille

    def set_difficulte_laby(self, nouvelle_difficulte):
        #changement de la difficulté du labyrinthe
        self.difficulte_laby = nouvelle_difficulte

    def set_difficulte_ennemi(self, nouvelle_difficulte):
        #changement de la difficulté des ennemis
        self.difficulte_ennemi = nouvelle_difficulte

    def applique_changements(self):
        #application de tous les changements effectués
        OptJeu.TAILLE_LABYRINTHE = self.taille_laby
        OptJeu.DIFFICULTE_LABY = self.difficulte_laby
        OptJeu.DIFFICULTE_ENNEMI = self.difficulte_ennemi
