# Collatinus-11, notes sur le Tagger.

Samedi 19 novembre 2016

## Introduction
Le problème de la désambiguïsation est un problème récurrent.
Pour essayer de retrouver à quel lemme associer une forme,
on va utiliser des étiquettes (tags) et tenir compte du contexte
par ces seules étiquettes. Plus précisément, dans une phase d'apprentissage,
on a relevé le nombre de séquences de trois tags. Par la suite,
on s'appuie sur ces statistiques pour estimer la séquence la plus probable.

En l'occurrence, l'apprentissage s'est fait sur les textes lemmatisés
au LASLA. Je remercie Dominique Longrée et toute l'équipe du LASLA 
de m'avoir confié leurs textes et permis de les dépouiller à cette fin.
[Les textes traités](http://web.philo.ulg.ac.be/lasla/textes-latins-traites/)
couvrent l'ensemble du Latin classique.

## Travaux préliminaires

Les textes du LASLA associent une forme à un lemme et à un *code en 9*.
Malheureusement, ces *codes en 9* sont trop nombreux et ne peuvent pas
être utilisés comme tags. En effet, le choix de l'ensemble des étiquettes
(tagset) est un problème délicat. Trop simplifié, il ne permet pas de 
résoudre les ambiguïtés. Trop compliqué, il nécessiterait un corpus 
d'apprentissage gigantesque pour que les statistiques soient représentatives.
Dans un premier temps, j'avais gardé la catégorie donnée par le *code en 9*
ainsi que les cas et nombre pour les formes déclinées ou 
le mode pour les formes conjuguées. Pour ces dernières, il m'a
semblé astucieux de distinguer le présent des autres temps. 
Il aurait pu être utile d'avoir aussi les genres, 
mais le LASLA ne les donne pas. Cela conduit à 178 tags.

Pour passer dans Collatinus, il m'a semblé plus simple de
remplacer la catégorie du *code en 9* par le POS tel que
Collatinus le connaît. On perd ainsi les sous-catégories
définies pour les pronoms (E-L) et les adverbes (M-Q).
J'ai alors 91 tags toujours codés sur trois caractères.
Un tag spécial, snt, est associé à la fin de phrase.

Le premier caractère est le POS.
* a : adjectif
* c : conjonction
* d : adverbe
* i : interjection
* m : nombres
* n : nom
* p : pronom
* r : préposition
* v : verbe (forme conjuguée)
* w : forme verbale déclinée

Pour les formes déclinées (a, n, p et w), le deuxième
caractère est le cas (de 1 à 6 du nominatif à l'ablatif, 
dans l'ordre en usage en France, et 7 pour le locatif)
et le troisième est le nombre (1 ou 2).

Pour les formes verbales conjuguées, le deuxième caractère
est le mode.
* 1 : indicatif
* 2 : subjonctif
* 3 : impératif
* 4 : infinitif

Le troisième caractère sert à distinguer le présent des autres temps.
Il vaut 1 si c'est un présent. Sinon, c'est un espace.

Les supins, trop peu nombreux, ont été mélangés avec les impératifs
non-présents (v3 ). Il traine aussi des tags hérités du LASLA, qui ne sont
pas utilisés par Collatinus. En particulier, le # pour l'auxiliaire être.

Avec ces 91 tags, j'ai aussi relevé les trigrammes (séquences de 3 tags
séparés par un espace, donc sur 11 caractères). 
Il y en a 114 981.
Sont aussi dénombrés les bigrammes de début ou de fin de phrase 
(chaines de 7 caractères qui commencent ou finissent par "snt").

Le dépouillement des fichiers du LASLA m'a également permis
d'établir des liens entre les lemmes utilisés au LASLA et ceux
de Collatinus. Je peux donc attribuer aux entrées du lexique
de Collatinus le nombre d'occurrences trouvées dans les textes.
Le gros du travail a été fait par un petit programme.
Il reste encore des cas difficiles à résoudre. Les cas simples
(pouvant être réglés par un non-latiniste) ont été passés en revue.

Les résultats de ces dépouillements sont dans les fichiers
tags.la et nombres.la. Le format de ces fichiers est décrit
au début de chacun d'eux. Il s'agit toujours de texte simple,
donc facile à lire et à réutiliser. Ici, les champs sont séparés
par une virgule (format CSV).

## Ordonner les lemmatisations

Jusqu'à présent, l'ordre dans lequel Collatinus présentait
ses résultats de lemmatisation n'était lié qu'à l'ordre dans
lequel il les avait trouvés. Ainsi, la forme *suis* était
lemmatisée en premier lieu comme le génitif de *sus, suis*
alors que le possessif est plus fréquent.
Maintenant que je connais le
nombre d'occurrences de chaque lemme dans les textes du LASLA,
je peux trier ces solutions pour que la plus fréquente soit
proposée en premier. Toutefois, Collatinus n'est pas un
lemmatiseur de formes (c'est à dire qu'il ne travaille pas
avec la liste des formes possibles associées à un nombre
d'occurrences). Il doit donc *estimer* le nombre d'occurrences
d'une forme à partir de l'analyse morphologique et du nombre
d'occurrences du lemme associé.

J'utilise donc une partie des résultats extraits du dépouillement
des textes du LASLA :
* le nombre d'occurrences des lemmes
* le nombre d'occurrences des tags

Ici, je n'ai pas besoin des séquences de tags puisque je
considère un mot hors de tout contexte.
Je fais implicitement une hypothèse assez forte qui consiste
à supposer que tous les lemmes sont employés à tous les cas et nombres
de la même façon (en tenant compte de la catégorie du mot, évidemment).
Quand je veux associer une forme à un lemme avec un tag spécifique,
je suppose que le nombre d'occurrences à considérer est
simplement le produit du nombre d'occurrences du lemmes et de la
proportion du tag dans la famille. Il faut bien voir que ce n'est là
qu'une approximation et que je ne prétends pas donner une estimation fiable.
Un lemmatiseur de forme donnerait lui le nombre d'occurrences observées.
Exactement.

## Principe du tagger

Un tagger probabiliste va construire, avec les formes qui sont dans
la phrase, toutes les séquences de tags possibles et
leur associer une probabilité. La séquence retenue sera
celle qui a la plus forte probabilité.
La phrase est traitée mot après mot dans l'ordre naturel.
J'ai pris soin de conserver une probabilité, c'est à dire
que si on faisait la somme de toutes les probabilités associées
à chacune des séquences, on trouverait 1.

En pratique, il n'est pas possible de conserver toutes les séquences
car leur nombre croît exponentiellement avec la longueur de la phrase.
Heureusement, le fait de ne considérer que des trigrammes permet
d'introduire un mécanisme d'élagage très efficace. On va donc
progresser en deux temps :
* pousse de toutes les nouvelles branches
* élagage des branches stériles.

La représentation en arbre de l'ensemble des séquences possibles
est assez tentante et naturelle. Toutefois, le mécanisme d'élagage
décrit plus bas s'apparente à du repiquage dans le sens où les
nouvelles branches poussent sur des "troncs" différents.
J'ai donc préféré utiliser une liste de toutes les séquences utiles.

### Nouvelles pousses

Lorsque l'on a déjà traité n-1 mots de la phrase, on a associé à 
chacune des séquences obtenues avec les tags de ces n-1 mots
une probabilité. À chacune de ces séquences, on va ajouter tous 
les tags possibles pour le énième mot et calculer les nouvelles
probabilités. Comme pour la lemmatisation, on a une estimation
du nombre d'occurrences de la forme associée à chacun des tags.
On connaît aussi le nombre observé des trigrammes obtenus en
complétant le bigramme terminal d'une séquence pour n-1 mots
par le tag choisi pour le énième mot. Pour chaque bigramme
terminal, on va construire une probabilité conditionnelle
à partir de ces produits de nombres d'occurrences. Il s'agit 
donc de ces produits divisés par leur somme.
C'est une probabilité associée au tag du énième mot :
* conditionnelle, puisqu'elle dépend du bigramme terminal
des séquences sur les n-1 premiers mots
* normalisée, puisque pour chaque bigramme terminal la somme
sur tous les tags possibles du énième mot donne 1.

La probabilité d'une séquence obtenue en complétant une de 
celles de n-1 mots par un tag du énième mot est simplement
le produit de la probabilité associée à la séquence de départ
et de la probabilité conditionnelle évaluée plus haut.
On vérifie aisément que c'est une probabilité : la somme
de tous les possibles est toujours 1.

### Élagage

Le fait que l'on considère le contexte uniquement à travers
les trigrammes et le calcul des probabilités présenté plus haut
montrent qu'il est inutile de conserver deux séquences qui se 
terminent par le même bigramme. En effet, supposons que nous 
ayons deux telles séquences associées à des probabilités P1 et P2.
On supposera que P1 > P2. Puisque j'ai le même bigramme terminal,
les probabilités conditionnelles associées à l'ajout du énième mot
sont les mêmes. Toutes les séquences issues de la deuxième séquence
considérée auront des probabilités plus petites que le séquence
correspondante issue de la première. Les ajouts successifs de mots
ne permettront jamais à une séquence issue de la deuxième de 
surpasser la meilleure de celle issue de la première.

Pour *chaque bigramme terminal*, il faut conserver la séquence
qui est associée à la plus grande probabilité. C'est la seule
qui puisse conduire à la séquence finale 
(avec tous les mots de la phrase) la plus probable.
Comme je suis *prudent*, je n'aime pas n'avoir aucun choix.
Je souhaite avoir donc un second choix qui serait la
séquence finale avec la deuxième plus grande probabilité.
Pour être sûr de ne pas la perdre en route, je dois donc,
à chaque étape d'élagage, garder deux fois plus de séquences.
Pour *chaque bigramme terminal*, je garde les deux séquences
avec les plus fortes probabilités. Le temps de calcul est alors
doublé, mais reste très raisonnable.

### Information sur les autres tags

On a vu qu'après la phase de pousse, on ne conserve qu'une
séquence pour chacun des bigrammes terminaux possibles.
On risque alors de faire disparaître certains des tags
(les moins favorables) pour le mot en position n-2.
En particulier, on ne saura jamais avec le seul résultat
final (la séquence la plus probable) si on n'a pas laissé
en route une autre possibilité à peine moins probable.
J'ai donc décidé de conserver, avant de procéder à l'élagage,
la meilleure probabilité associée à chacun des tags du 
mot n-2 lorsque j'ai ajouté le énième mot.

Je dois faire cette sélection avant l'élagage, car c'est
le dernier moment où je suis sûr que tous les tags possibles
du mot n-2 sont encore présents dans la liste des séquences.
Attention, ces probabilités sont à manipuler avec précaution.
Il ne faut pas comparer les probabilités de mots différents.
En effet, toutes ces probabilités ne peuvent que décroître 
quand on avance dans la phrase. Il faut se contenter de
regarder ce qui se passe pour un mot donné. En général,
un des tags possibles est associé à une probabilité
nettement plus grande que toutes les autres. Toutefois,
il peut arriver qu'un deuxième choix se dessine avec une
probabilité proche. Je laisse à chacun le soin de se choisir
le sens à donner à *proche*.

### Détails mathématiques

Attention, il faudra bien distinguer :
* les probabilités conjointes de deux (ou plus) variables,
notées P(x,y)
* les probabilités conditionnelles de deux (ou plus) variables,
notées P(x|y)

Dans le premier cas, il s'agit d'une seule distribution de probabilités.
Elle est normalisée à 1 lorsque l'on fait la somme double
sur toutes les valeurs de x et de y. En introduisant
l'événement E=(x,y), on pourrait écrire une probabilité P(E).

Dans le second cas, il s'agit d'une collection de distributions
de probabilités. Chacune d'elles donne la distribution de probabilités
de la variable x. La distribution étant modifiée en fonction de y.
Pour chaque valeur possible de la condition y, la distribution
est normalisée. C'est à dire que la somme (simple) sur x de
P(x|y) donne 1 quelle que soit la valeur choisie pour y.

On va considérer ce qui se passe quand on ajoute le énième
mot aux séquences obtenues avec les n-1 premiers. Les mots
de rang n-1 et n-2 jouent un rôle particulier puisque leurs
tags interviennent dans les trigrammes. On va nommer I, J et
K le nombre de tags possibles pour les mots n-2, n-1 et n.
Et H, le nombre de séquences des n-3 premiers mots.
Le choix d'un tag pour les divers mots sera repéré par un
indice i, j ou k. Le travail déjà effectué avec les n-1
premiers mots a consisté à associer à toutes les séquences
(h, i, j) une probabilité P(h, i, j). L'ajout du énième mot
avec le tag k introduit une probabilité conditionnelle Q(k|i,j).
On a d'une part le nombre d'occurrences estimé du énième mot
avec le tag k que l'on note E(k). D'autre part, on a le
nombre d'occurrences du trigramme (i, j, k) dans cet ordre
que l'on note O(i, j, k). La probabilité conditionnelle est
simplement proportionnelle au produit E(k).O(i, j, k).
On peut donc écrire 

Q(k|i,j) = E(k).O(i, j, k)/S(i,j)

où S(i,j) est la somme sur k des produits E(k).O(i, j, k).
Somme qui dépend des valeurs choisies i et j. Sa présence
au dénominateur assure que Q(k|i,j) est une distribution
de probabilités normalisée à 1.

L'ajout du énième mot conduit à des séquences plus longues 
et plus nombreuses. La séquence construite sur (h, i, j) 
avec le tag k pour le énième mot sera notée (h, i, j, k).
Elle est associée à la probabilité 

P'(h, i, j, k) = P(h, i, j).Q(k|i,j)

En renommant les indices h'=(h,i), i'=j et j'=k, on a donc,
comme à l'ordre n-1, associé une probabilité P'(h', i', j')
à chaque séquence de n mots repérée par les indices h', i', j'.
On peut "oublier" les ' et recommencer avec le mot suivant.

On voit bien sur l'expression de P'(h, i, j, k) que deux séquences
différentes des n-3 premiers mots (des h différents, mais mêmes
i et j) vont garder des probabilités dans le même ordre. Pour
chaque i et j, seule la séquence h(i,j) qui maximise la 
probabilité P(h, i, j) a une chance de mener à la séquence
la plus probable. D'où la recette de l'élagage.

On voit également que i, c'est à dire le tag du mot de rang n-2 
apparaît encore explicitement dans l'expression de P'(h, i, j, k).
Pour chaque valeur de i, je retiens la probabilité p(i) qui est
la plus grande parmi toutes les valeurs P'(h, i, j, k).

## Le futur

Il serait maintenant intéressant de coupler le tagger à
l'analyse syntaxique de la phrase. J'avais renoncé à une
analyse automatique avec construction de l'arbre syntaxique
car, sur une phrase longue et complexe, le nombre de liens
possibles et de combinaisons à examiner explosait. Les temps
de calcul aussi. Avec un tagger probabiliste qui m'indique
quels sont les tags les plus probables, cette complexité
peut se trouver réduite. J'ai un ordre pour établir des liens
et pour essayer de les combiner. Ça peut aider… 
