# Collatinus-11, notes

lundi 4 janvier 2016 

<!-- voir syntaxe Algo -->

## COMPILATION
Requis :
- Un compilateur C++ ;
- Les bibliothèques Qt 5.
- Ajuster le PATH de la machine pour que
  compilateur et bibliothèques soient accessibles
  depuis le répertoire de développement ;
- En ligne de commande :
  * $ qmake
  * $ make
- Créer les répertoires bin/, bin/data et bin/data/dicos
- Placer dans bin/data/ les lexiques téléchargeables 
  à l'adresse [http://outils.biblissima.fr/collatinus/](http://outils.biblissima.fr/collatinus/)
- Générer le fichier de traductions anglaises :    
  $ lrelease collatinus.pro    
    … et le déplacer dans bin/ :    
  $ mv collatinus\_en.qm bin/
- Placer dans bin/data/dicos les dictionnaires xml et
  djvu les dictionnaires téléchargeables à la même adresse ;
- Générer le fichier de traductions anglaises :    
  $ lrelease collatinus.pro   
  … et le déplacer dans bin/ :    
  $ mv collatinus\_en.qm bin/
- Lancer Collatinus en ligne de commande :    
  * $ cd bin
  * $ ./collatinus    
  ou après avoir installé un raccourci.

## BOGUES ET PROBLÈMES
- Syntaxe : sujet, verbe : la virgule ne bloque pas le lien.
- Flexion de multus et ses degrés allogènes (plus, plurimus)

## À FAIRE :
- Créer une branche exponct (u exponctué de volvo, sanguinis, unicode 1EE5 ụ )
- Lemme::pos étant un char, le transformer en string, pour tenir compte des pos multiples.
- éventuellement : possibilité de déclarer un lien comme sûr,   
    ce qui permet d'éliminer par le suite des concurrents.
- téléchargement : éliminer les fichiers homonymes d'une 
  version antérieure.
- Fichier en paramètre
- Flexion : revenir en début de page
- Compiler pour Win
- Version web (emscripten ?)
- écrire un man
- Dans le presse-papier, insérer une signature "édité avec C11+url";
  idem pour l'impression ?
- Nettoyage des -pte -met -quoi dans les traductions ;
- chargement des lexiques et dictionnaires, compressés,
  prêts à être décompressés et installés par Collatinus.
- Modèles :
  *	Vérifier les modèles ;
  *	Traiter les noms 3ème decl pl. majores, orum, donné sing. ;
  * modèles nolo et malo ;
  * Vérifier facio et fio ;
  *	Construire des modèles passifs/intransitifs.
- Système d'hyperliens dans les résultats, qui permet d'afficher
  des entrées. Par exemple, le lemme multus donne ses degrés par
  un hyperlien vers plus, pluris, et vers plurimus, a, um.

## Branche syntaxe
   * mardi 17 mai 2016 -
     vérifier Super::addSub : un return si le sub est occupé
   * 10 mai 2016 - Certains liens, surtout dans les
     expressions reprises de C10, ont plus de deux éléments :
     . incidit mentio de : 3
     . non solum ... sed etiam : 4.
     il faudrait donc que le principe de lien
     syntaxique soit récursif, càd que l'élément d'un
     lien puisse être lui même un lien.
     . super:inciditMentio
     . sub:de
     ... ou
     . super:incidit+de
     . ѕub:mentio
     L'ablatif absolu en est un autre exemple :
     . super:verbe
     . sub:ablAbs

   * 9 mai - Dans le texte d'exemple l'analyse
     syntaxique de /inde/ provoque une erreur de
     segmentation.
     expressions de C10 dans la base syntaxique de C11.
   * But : ne donner que le(s) père(s) du mot cliqué, avec traduction.
   * Arbre en arcs :
     Forte potantibus his apud Sextum Tarquinium, ubi et Collatinus cenabat Tarquinius, Egeri filius, incidit de uxoribus mentio.  
     ^     |  ^ | |   ^   ^ ||  ^ |        ^      ^ | ^   | | ^      | ^      ^  |         ^   | ^     | | |  ^|    ^       ^  
     |     |  | | |   |   | ||  | |        |      | | |   | | |      | |      |  |         |   | |     | | |  ||    |       |  
     +-cc-/   | | +---+   | ||  | |        |      | | +---+ | +--S---+ |      |  |         +cdn+ |     | | +pr/ \reg+       |  
              | +--prep---+ | \-+ +--app---+      | |       +-----app--|------+  +------app------+     | +-------S----------+  
              |             +--------reg----------/ \-------cc---------+                               |  
              +-------------------------------------cc-------------------------------------------------+  
   * **Contrainte** : Tout mot doit trouver son sub, sauf un, qui est
      un verbe conjugué à l'indicatif ou à l'impératif, Quelquefois un
	  nom.
   * **Hypothèse** : En allant de G à D, lorsque un mot a trouvé son super, les
     mots suivants ne peuvent être sub de ce mot.
   * **Hypothèse** : les prépositions et conj. de subordination sont bloquantes
      - elles ne permettent aux mots précédent de chercher des sub après elles
	    que si elles-mêmes ont trouvé un sub.
      - Elles n'ont pas d'homonyme, et si elles en ont,
	    ils sont eux aussi bloquants (ex. *cum*)
	    (vraiment pas sûr). Le pr. relatif peut
	    être considéré comme bloquant, mais il a des formes ambiguës.
   * Attention aux hyperbates : _Collatinus cenabat Tarquinius_
    Collatinus cenabat Tarquinius.
       ^   |     |        ^
       |   +-----|--------+
       +---------+    

## Branche maj
Branche de mise à jour des lexiques.
- Créer un dépôt distant,
- Dans le dépôt, des fichiers compressés, et une page d'accueil et des liens ;
- Dans Collatinus, menu Lexique ou Aide, ou les deux, une option màj ;
- Créer le dialogue maj 
  * lien vers le dépôt, mode d'emploi ;
  * Un bouton qui lance un QFileDialog de sélection des fichiers téléchargés ;
  * Un bouton OK pour lancer la décompression et copie des fichiers ;
  * Un bouton Annuler.
- Moyens d'identifier la version des dictionnaires et lexiques installés :
  1. Version dans l'en-tête de chaque fichier ;
  2. Faire marcher C11 avec des fichiers versionnés, et indication de remplacement ;
  3. Paquet versionné, prise de version et enregistrement dans les préférences, 
     et dépaquetage sans version.


## DOC
- Un modèle d'utilisation des docks est dans les exemples Qt5 : 
  ${Doc-qt5}/examples/widgets/mainwindows/dockwidgets
