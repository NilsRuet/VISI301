Principe du jeu:
Le joueur incarne un personnage qui se déplace dans une pièce, dans une pièce on trouve des portes vers d'autres pièces. Quand le joueur atteint une porte, il change de pièce. Son but est d'atteindre une pièce finale, qui représente la fin du labyrinthe.

Pour jouer :
Exécuter le fichier "main.py", une fenêtre s'ouvre. Cette fenêtre est divisée en deux parties : la partie gauche représente la pièce du labyrinthe dans laquelle on se situe, la partie de droite représente le labyrinthe.
Dans la partie de gauche, le personnage joué est représenté par une case rouge, les portes par des cases verts. Le personnage peut être déplacer à l'aide des touches directionnelles.

Dans la partie de droite, des murs sont représentés par des traits noirs et empêchent le déplacement entre deux pièces séparés par un de ces murs. La pièce dans laquelle se trouve le joueur est représentée par une case grise. La case rouge est la pièce finale à atteindre, la case bleue représente la case de départ.

Lorsque le joueur a réussi à se déplacer dans la pièce finale, il gagne et la fenêtre se ferme.

Fichiers du projet :
"Labyrinthe.py", "Persos.py", "Piece.py" contiennent (respectivement) les classes d'objets relatifs au labyrinthe, aux personnages, aux pièces du labyrinthe
"Options.py" contient les paramètres du jeu (par exemple la taille du labyrinthe).
"Affichage.py" contient les paramètres de l'affichage (Taille de la fenêtre, position des éléments sur la fenêtres etc.).
"Main.py" contient la boucle principale du jeu et le gestionnaire d'évènements.


Perspectives :
-Le joueur rencontre des ennemis sur son chemin, qu'il combat à l'aide d'une arme. Les ennemis deviennent de plus en plus forts lorsque le joueur se rapproche de la pièce finale. Au fil de sa progression le joueur récupère de meilleures armes/améliore son arme pour compenser le gain en difficulté des ennemis.

-Le joueur récupère des objets qui lui permettent d'accéder à des pièces inaccessibles sans l'aide de ceux-ci. Certaines pièces peuvent par exemple de rien afficher si le joueur ne dispose pas de l'objet requis.

-Les options d'affichage et de jeu sont modifiables depuis l'interface du jeu.
