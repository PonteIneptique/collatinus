/*                 syntaxe.h
 *
 *  This file is part of COLLATINUS.
 *
 *  COLLATINUS is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  COLLATINVS is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with COLLATINUS; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * © Yves Ouvrard, 2009 - 2016
 */

/**
 * \file syntaxe.h
 * \brief module d'analyse syntaxique
 */

/*
   Module d'analyse syntaxique.

- TODO Une règle a deux membres : père et fils
  Une expression peut avoir trois membres ou plus.
  Exemple :
    nominatif + datif + sum
    On résout en posant une règle supplémentaire
    sumDatif:
    - fils datif
    - sum père d'un sujet au nominatif.

- Trouver le moyen d'exprimer la projectivité dans la hiérarchisation des liens
  . si le mot suivant n'est pas lié à motCour
    . chercher s'il est lié au mot précédent.
      . si oui, continuer
      . si non chercher s'il est lié au mot suivant.
        . si oui, on peut continuer à condition que la morpho
          du mot suivant lui permette d'être lié à motCour.
          . si non, le groupe est terminé.

 . Exemple de structure sur laquelle travailler :
   "incidit de uxoribus mentio."  On en vient à parler des épouses.
      | |   ||    |       |
      | +---++----+       |
      +-------------------+

 . TODO Il faudrait que certains mots+lien soient bloquants.  Une
   préposition bloque les expansions à droite du verbe
   jusqu'à ce que son régime soit lu.
   bloquant = lien prioritaire ? Soit la phrase
   De uxoribus incidit mentio.
   /uxoribus/ pourrait être le sub de /incidit/, mais
   comme il peut être aussi le sub de /de/, on peut
   dire que le lien de -> uxoribus est prioritaire
   sur le lien uxoribus <- incidit.

*/

#ifndef SYNTAXE_H
#define SYNTAXE_H

#include <QString>
#include "flexfr.h"
#include "lemmatiseur.h"

class RegleS;

class ElS : public QObject
{
    Q_OBJECT

   private:
    RegleS     *_regle;
    QStringList _lemmes;
    QStringList _pos;
    QStringList _morphos;

   public:
    ElS(QString lin, RegleS *parent);
    bool okLem(QString l);
    bool okPos(QString p);
    bool okMorpho(QString m);
    QStringList pos();
};

class Syntaxe;
class Mot;

class RegleS : public QObject
{
    Q_OBJECT

   private:
    QString _accord;
    QString _doc;
    QString _f;
    QString _id;
    QString _idPere;
    RegleS *_pere;
    QString _sens;
    ElS    *_super;
    ElS    *_sub;
    QString _synt;
    Syntaxe *syntaxe;
    QString _tr;

   public:
    RegleS(QStringList lignes, QObject *parent=0);
    QString   accord();
    bool      bloquant();
    QString   doc();
    bool      estSub(Lemme *l, QString morpho, bool ante);
    bool      estSuper(Lemme *l, QString morpho);
    QString   f();
    QString   fonction(Mot *super = 0, Mot *sub = 0);
    QString   id();
    QString   idPere();
    bool      multiple();
    QString   sens();
    ElS    *  super();
    ElS    *  sub();
    QString   synt();
    QString   tr();
};

class Super : public QObject
{
    Q_OBJECT

   private:
    RegleS *_regle;
    Lemme  *_lemme;
    Lemme  *_lemmeSub;
    QString _morpho;
    Mot    *_mot;
    Mot    *_motSub;
    SLem    _slemSub;
    QString _traduction;

   public:
    Super(RegleS *r, Lemme *l, QString m, Mot *parent);
    void    addSub(Mot *m, Lemme *l, SLem sl);
    void    annule();
    bool    bloquant();
    bool    complet(); // vrai si super a un sub validé
    Super  *copie();   // clone, avec motsub à NULL
    bool    estSub(Lemme *l, QString morpho, bool ante);
    QString fonction();
    Lemme  *lemme();
    Lemme  *lemmeSub();
    QString morpho();
    Mot    *mot();
    Mot    *motSub();
    RegleS *regle();
    SLem    slemSub();
    void    setTraduction(QString t);
    QString traduction();
};

class Mot : public QObject
{
    // TODO : il manque un vrai champ Mot *_super, ou une liste de Mots.
    //        La liste actuelle ne donne pas les subs.

    Q_OBJECT

   private:
    bool            _clos;
    QString         _gr;
    int             _grPrim;  // rang du premier mot du groupe
    int             _grUlt;   // rang du dernier mot du groupe
    MapLem          _morphos;
    QString         _ponctD;
    QString         _ponctG;
    int             _rang;
    QList<RegleS *> _rSub;
    QList<Super *>  _super;
    Syntaxe         *syntaxe;
    bool            _vu;

   public:
    Mot(QString g, QObject *parent=0);
    void           addRSub(RegleS *r);
    void           addSuper(RegleS *r, Lemme *l, QString m);
    void           addSuper(Super *s);
    bool           clos();
    QString        gr();
    void           grCalc();  // met à jour _grPrim et _grUlt;
    int            grPrim();  // rang du premier mot du groupe du mot
    int            grUlt();   //  "      dernier  "
    QString        humain();
    MapLem         morphos();
    bool           orphelin();
    QString        ponctD();
    QString        ponctG();
    int            rang();
    void           setMorphos(MapLem m);
    void           setPonctD(QString c);
    void           setPonctG(QString c);
    void           setRang(int r);
    void           setRSub(QList<RegleS *>);
    void           setRSuper(QList<RegleS *>);
    void           setClos();
    void           setVu();
    QList<Super *> super();  // liste des règles qui peuvent faire du mot un super
    bool           superDe(Mot *m);
    bool           terminal();  // pas de sub
    bool           vu();
};

class Syntaxe : public QObject
{
    Q_OBJECT

   private:
    bool                    accord(QString ma, QString mb, QString cgn);
    int                     groupe(int r);
    Lemmat                *_lemmatiseur;
    int                    _nbmots;
    QMap<QString, RegleS*> _regles;
    Mot*                    superDe(Mot *m);
    QString                _texte;
    // variables
    Mot                   *_motCour; // mot courant
    QList<Mot *>           _mots;
    QList<Mot *>           _motsP;   // mots précédents
    QList<Mot *>           _motsS;   // mots suivants
    Pronom                *_pronom;
    int                    r; //, x;
    QString                _rapport;

   public:
    Syntaxe(QString t, Lemmat *parent);
    QString analyse(QString t, int p);
    bool    estSuper(Mot *sup, Mot *sub);
    QString liens(Mot *m);
    QString motSous(int p);
    bool    orphelin(Mot *m);
    RegleS* regle(QString id);
    void    selectionne(Mot *m, Super *s); // élimine tous les autres liens que s faisant de m leur sub
    void    setText(QString t);
    bool    super(Mot *sup, Mot *sub);  // construit le lien
    QString tr(RegleS *r, Lemme *sup, QString msup, Lemme *sub, QString msub);
    QString trLemme(Lemme *l, QString m);
    bool    virgule(Mot *ma,
                    Mot *mb);  // vrai si une virgule sépare 2 mots successifs
};

#endif
