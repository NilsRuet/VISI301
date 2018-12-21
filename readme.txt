Principe du jeu:
Le joueur incarne un personnage qui se d�place dans une pi�ce, dans une pi�ce on trouve des portes vers d'autres pi�ces. Quand le joueur atteint une porte, il change de pi�ce. Son but est d'atteindre une pi�ce finale, qui repr�sente la fin du labyrinthe.

Pour jouer :
Ex�cuter le fichier "main.py", une fen�tre s'ouvre. Cette fen�tre est divis�e en deux parties : la partie gauche repr�sente la pi�ce du labyrinthe dans laquelle on se situe, la partie de droite repr�sente le labyrinthe.
Dans la partie de gauche, le personnage jou� est repr�sent� par une case rouge, les portes par des cases verts. Le personnage peut �tre d�placer � l'aide des touches directionnelles.

Dans la partie de droite, des murs sont repr�sent�s par des traits noirs et emp�chent le d�placement entre deux pi�ces s�par�s par un de ces murs. La pi�ce dans laquelle se trouve le joueur est repr�sent�e par une case grise. La case rouge est la pi�ce finale � atteindre, la case bleue repr�sente la case de d�part.

Lorsque le joueur a r�ussi � se d�placer dans la pi�ce finale, il gagne et la fen�tre se ferme.

Fichiers du projet :
"Labyrinthe.py", "Persos.py", "Piece.py" contiennent (respectivement) les classes d'objets relatifs au labyrinthe, aux personnages, aux pi�ces du labyrinthe
"Options.py" contient les param�tres du jeu (par exemple la taille du labyrinthe).
"Affichage.py" contient les param�tres de l'affichage (Taille de la fen�tre, position des �l�ments sur la fen�tres etc.).
"Main.py" contient la boucle principale du jeu et le gestionnaire d'�v�nements.


Perspectives :
-Le joueur rencontre des ennemis sur son chemin, qu'il combat � l'aide d'une arme. Les ennemis deviennent de plus en plus forts lorsque le joueur se rapproche de la pi�ce finale. Au fil de sa progression le joueur r�cup�re de meilleures armes/am�liore son arme pour compenser le gain en difficult� des ennemis.

-Le joueur r�cup�re des objets qui lui permettent d'acc�der � des pi�ces inaccessibles sans l'aide de ceux-ci. Certaines pi�ces peuvent par exemple de rien afficher si le joueur ne dispose pas de l'objet requis.

-Les options d'affichage et de jeu sont modifiables depuis l'interface du jeu.
