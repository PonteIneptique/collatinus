# Pour une installation sur Mac

Pour que Collatinus fonctionne sur Mac et que soient installés 
tous les fichiers nécessaires au bon endroit, 
il faut définir une "étape de déploiement". 

Dans QtCreator, il faut cliquer sur l'icône **Projets** (un livret dans la colonne 
de gauche). Dans le haut de la page qui s'ouvre apparaît un cadre sombre 
avec Qt 5.... (qui est la version de Qt que vous avez) et en dessous 
deux boutons "Compiler" et "Exécuter" : vous cliquez sur **Exécuter**. 

Dans la rubrique "Déploiement" (la première), vous faites **Ajouter l'étape Déploiement** 
et dans le cadre qui apparaît vous spécifiez **deploy** dans la ligne "Arguments de Make". 
Il vous reste à recompiler et relancer Collatinus. 
Vous obtiendrez ainsi une vraie appli qui peut être copiée et installée 
sur un autre Mac, même s'il ne dispose pas de Qt. 
Et avec tous les fichiers installés au bon endroit.