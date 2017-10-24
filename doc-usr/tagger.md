*Collatinus 11 -- guide*

[index](index.html) précédent : [Fléchir](flechir.html) suivant : [Serveur](server.html) 

Tagger
======

         Cette fonctionnalité est expérimentale et
         il convient de l’utiliser avec prudence !

Le but d’un tagueur (ou tagger) probabiliste est de proposer
la _meilleure_ analyse d’une phrase ou d’un texte,
en tenant compte de façon simpliste du contexte.
**Attention !** Comme son nom l’indique, c’est un processus _probabiliste_,
ce qui signifie qu’il peut se tromper.
Ce qu’il considère comme la _meilleure_ analyse
peut être **fausse**.
Un tagueur probabiliste ne remplace pas une analyse syntaxique
et la compréhension d’un texte. Il ne peut qu’aider.

Dès que l’on clique sur un mot dans le texte, le programme
analyse la phrase qui contient ce mot et propose les
deux meilleures séquences de tags associées. Il indique
aussi les probabilités qu’il leur attribue. Si ces 
probabilités sont voisines, la seconde possibilité doit
être examinée également. Toujours est-il que seule la
meilleure séquence est explicitée dans la suite.
Le bouton _tout afficher_ en haut à droite de l’onglet tagger
permet d’afficher toutes les lemmatisations possibles
(comme dans l’onglet _Lexique et morphologie_, mais sous 
une autre forme). Lorsqu’il est inactif, seule la lemmatisation
choisie dans la _meilleure solution_ du tagger est affichée.

Le bouton représentant des _engrenages_ permet de traiter
l’ensemble du texte, phrase par phrase. 
Si le texte est long, ça peut prendre un peu de temps.

Un tagueur probabiliste est un outil utilisé couramment
en Traitement Automatique des Langues (TAL ou NLP, pour
Natural Laguage Processing) pour lever les ambiguïtés.
De telles ambiguïtés sont fréquentes dans toutes les
langues. Le sens de la phrase nous éclaire dans nos choix.
Mais un ordinateur n’a pas accès au sens…

Sans entrer dans les détails du fonctionnement d’un tagueur
probabiliste, il associe des étiquettes (tag en anglais)
aux formes, étiquettes révélatrices de la nature 
ou de la fonction du mot. À partir d’une phrase, vue comme
une succession de formes, on peut construire un grand nombre
de successions d’étiquettes. Reste à associer à chacune de ces
séquences possibles une probabilité pour qu’elle soit la bonne. 
Un tagueur probabiliste repose sur une connaissance statistique
de la langue et sur des hypothèses simplificatrices pour
évaluer la probabilité à associer à une séquence de tags.
La séquence avec la plus forte probabilité a des chances
d’être la bonne.
Avec les langues modernes (anglais, français…), ça marche
plutôt bien avec des taux de réussite entre 90 et 99%.
À notre connaissance, il n’est pas démontré que cela
puisse donner de tels résultats avec le Latin.

La connaissance statistique de la langue est tirée de
l’examen d’un corpus d’apprentissage. En l’occurrence,
nous avons dépouillé le corpus des textes latins lemmatisés
par le LASLA à l’université de Liège. Il compte plus
de 1,5 million de mots lemmatisés et analysés à la main.
Pour l’utilisation dans Collatinus, on en a tiré :
 1.  Le nombre d’occurrences de chaque lemme.
 1.  La fréquence des différents cas (pour les formes 
     déclinées) et modes (pour les verbes).
 1.  Le nombre d’occurrences de chaque séquence de 3 tags.

Ces résultats sont utilisés pour évaluer les probabilités 
dont le tagueur a besoin.

[index](index.html) précédent : [Fléchir](flechir.html) suivant : [Serveur](server.html) 
