*Collatinus 11 -- guide*

[index](index.html) précédent : [Serveur](server.html) suivant : [Pour les programmeurs](programmeurs.html) 

Utilisation avancée
===================

	Pour faire son travail, Collatinus s'appuie sur une
    collection de fichiers qui contiennent toutes les
    connaissances nécessaires. À l'initialisation du
    programme, ils sont tous lus, et les données mises
    en listes et placées en mémoire vive.

Si on remarque une erreur ou une lacune dans les
résultats, et qu'on a des connaissances suffisantes en
gestion et édition de fichiers, on peut commencer à les
modifier. Il faut bien sûr prendre des précautions,
notamment **en prenant soin de faire une copie de
sauvegarde avant toute intervention** : on crée un
répertoire dont on note bien le chemin, et on y copie
les fichiers qu'on a l'intention de modifier. On peut
ainsi, en cas d'échecs, les rétablir dans leur état
initial.

Les fichiers les plus importants sont détaillés ci-dessous.

## Le fichier morphos.la
C'est un simple fichier dans lequel sont toutes les
morphologies possibles que peuvent prendre les formes
latines. Ainsi pour désigner une morphologie, on donne
le numéro de la ligne où elle se trouve. Par exemple,
la morphologie 
_vocatif masculin singulier participe présent actif_ est
désignée par le nombre _190_.

## le fichier modeles.la
C'est de loin le plus important. Y sont placés tous les
modèles de flexion. 

Un modèle est un ensemble de lignes. Chaque modèle est séparé
du précédent par une ligne vide.

Une ligne commençant par un point d'exclamation est un 
commentaire. Lors de sa lecture, Collatinus n'en tient
pas compte.

Chaque ligne est bâtie sur le schéma **clé:valeur**
Tout ce qui précède _le premier caractère **deux
points**_ est la clé, le reste est la valeur.
La première clé doit être le nom du modèle. L'ordre
dans lequel apparaissent les autres clés n'a pas
d'importance, mais mieux vaut rester cohérent et garder
la même disposition.

### Les clés

* modèle:nom-du-modèle Exemple : **modele:uita**
* Liste des radicaux :   
    R:\<n1\>:\<n2\>,\<ch\>
    * n1 : numéro du radical
    * n2 : nombre de caractères à ôter de la forme canonique 
    * ch : chaîne à ajouter à la chaîne obtenue pour avoir le radical. S'il n'y a aucune chaîne à ajouter, la valeur est 0.  exemple pour uita : **R:1:1:0**, ce qui signifie que pour le radical 1, on enlève un caractère à *uita*, ce qui donne *uit*, et on n'ajoute rien.
* désinences :
	des:\<intervalle\>:\<num\>:\<listeDes\>
    * intervale : liste de n° de morphologies séparées
	par des virgules, ou intervalle de numéros
	\<premier\>-\<dernier\>. Les deux méthodes peuvent
	voisiner dans un intervalle.
    * num : numéro du radical utilisé par ces désinences.
	* listeDes : liste des désiences. On peut ne donner qu'une fois une désinence qui se répète en fin de liste.

### Les variables
Comme les mêmes séries de désinences sont souvent utilisées de nombreuses fois par 
des modèles et des radicaux différents, on peut mettre ces séries en variables. Ainsi,
pour le modèle uita. Au lieu d'écrire :

	modele:uita
	R:1:1,0
	des:1-12:1:ă;ă;ăm;āe;āe;ā;āe;āe;ās;ārum;īs;īs

On définit une variable de cette manière :

	$<variable>:<valeurs>

Par exemple, pour définir la variable uita :

	$uita=ă;ă;ăm;āe;āe;ā;āe;āe;ās;ārum;īs;īs

et la définition du modèle deviendra :

	modele:uita
	R:1:1,0
	des:1-12:1:$uita

La variable $uita peut être utilisée pour le participe parfait :

	modele:amo
	(radicaux, autres désinences)
	des:315-326:2:$uita

## Le fichier lemmes.la 
C'est un gros fichier qui donne tous les mots latins, leur modèle,
leurs radicaux, et les indications morphologiques qui
apparaîtront dans l'analyse.

Chaque lemme occupe une seule ligne. Cinq champs sont séparés par
le caractère **|** :
1. la forme canonique du lemme ; si le dictionnaire
n'en donne pas toutes les quantités, on la réécrit
entièrement mesurée après le signe **=**.
2. son modèle, pris dans le fichier modeles.la ;
3. s'il n'est pas défini par modeles.la, son radical de
génitif, ou d'infectum pour les verbes ;
4. s'il n'est pas défini par modeles.la, son radical de
perfectum ;
5. ses indications morphologiques

Exemple :

	ablŭo=ā̆blŭo|lego|ā̆blŭ|ā̆blūt|is, ere, lui, lutum

## les irréguliers
On place dans le fichier irregs.la les formes
irrégulières. On peut hésiter entre l'ajout d'une forme
dans ce fichier ou la définition d'un nouveau modèle.
Si plus de trois lemmes construisent une forme dite
irrégulière de la même manière, mieux vaut créer un
modèle. De même, si un lemme a plus de trois formes
irrégulières, mieux vaut créer un modèle pour ce lemme.

Le format est simple :

	<forme>:<lemme>:<morphos>

1. la forme doit être mesurée. On lui ajoute un
astérisque si c'est une forme irrégulière exclusive,
c'est à dire si la forme régulière correspondante
n'existe pas ;
2. Le lemme, sans ses quantités ;
3. La liste entre virgule des morphologies qui
utilisent cette forme. On peut utiliser la syntaxe des
intervalles de la clé **des** du fichier modeles.la.

Exemples :
	ălĭud*:alius:37-39
	āccēstĭs:accedo:143
	āmbŏbŭs*:ambo:17,18,29,30,47,48

## les fichiers de traduction
Les fichiers de traductions sont tous nommées
lemmes.??, les deux points d'interrogation étant deux
caractères qui servent à désigner la langue cible.
(fr=français, it=italien, etc.) 

Leur format est extrêmement simple :
   <lemme>:<traduction>
1. **lemme** : le lemme sans quantités ;
2. **traduction** : la traduction dans la langue cible.


## les fichiers de contraction et d'assimilation 

bin/data/assimilations.la et bin/data/contractions.la sont deux 
fichiers qui permettent de déclarer 

* Les assimilations : la forme _affert_ n'est pas reconnue, mais
  une règle d'assimilation permet de remplacer _-aff-_
  par _-adf-_, et  d'analyser aussi la forme
  _adfert_, qui est reconnue.
* Les contractions : la forme _amassem_ n'est pas reconnue, mais une
  règle de contraction permet de remplacer _-assem_ par
  _-auissem_, ce qui donne _amauissem_, qui est reconnu.

[index](index.html) précédent : [Serveur](server.html) suivant : [Pour les programmeurs](programmeurs.html) 
