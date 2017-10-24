'''      lemmatiseur.h
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
 *  along with COLLATINUS; if not, to the Free Software
 *  Foundation, Inc., Temple Place, 330, Boston, 02111-1307  USA
 *
 * © Yves Ouvrard, 2009 - 2016
 '''

#ifndef LEMMATISEUR_H
#define LEMMATISEUR_H

#include <QMap>
#include <QString>
#include <QStringList>
#include <QtCore/QCoreApplication>

#include "irregs.h"
#include "lemme.h"
#include "modele.h"

class Irreg
class Lemme
class Radical

typedef struct
    QString grq
    QString morpho
    QString sufq
} SLem

typedef QMap<Lemme*, QList<SLem> > MapLem
#include "mot.h"

typedef QPair<QRegExp, Reglep

class Lemmat : public QObject
    Q_OBJECT

   private:
    QHash<QString, _hLem
    QStringList _couleurs
    # fonction d'initialisation
    void ajAssims()
    void ajContractions()
    int  aRomano(QString f)
    void lisIrreguliers()
    void lisFichierLexique(QString filepath)
    void lisLexique()
    void lisExtension()
    void lisModeles()
    void lisMorphos(QString lang)
    void lisNombres()
    void lisParPos()
    void lisTraductions(bool base, extension)
    # variables et utils
    QMap<QString, assims
    QMap<QString, assimsq
    QStringList cherchePieds(int nbr, ligne, i, pentam)
    QMap<QString, _contractions
    QMultiMap<QString, *> _desinences
    QString decontracte(QString d)
    QStringList formeq(QString forme, *nonTrouve, debPhr,
                       accent = 0)
    bool inv(Lemme *l, ml)
    QMultiMap<QString, *> _irregs
    QString _cible;  # langue courante, caractères
    QMap<QString, _cibles
    QMap<QString, *> _lemmes
    QStringList             lignesFichier(QString nf)
    QMap<QString, *> _modeles
    QMap<QString, _morphos
    QMap<QString, _cas
    QMap<QString, _genres
    QMap<QString, _nombres
    QMap<QString, _temps
    QMap<QString, _modes
    QMap<QString, _voix
    QMap<QString, _motsClefs
    # Les morphos doivent pouvoir être données en anglais !
    QMultiMap<QString, *> _radicaux
    QList<Reglep> _reglesp
    QMap<QString, _variables
    # options
    bool _alpha
    bool _extension; # = False
    bool _formeT
    bool _html
    bool _majPert
    bool _morpho
    bool _nonRec
    QMap<QString, _catLasla
    void lisCat()

    QMap<QString, _tagOcc; # Nombre d'occurrences du tag.
    QMap<QString, _tagTot; # Nombre total en fonction du premier caractère du tag.
    QMap<QString, _trigram; # Nombre d'occurrences des séquences de 3 tags.
    void lisTags(tout = False)

    QString _resDir; # Le chemin du répertoire de ressources
    bool _extLoaded; # = True après chargement de l'extension
    # Lorsque j'ai chargé l'extension, dois pouvoir ignorer les analyses qui en viennent.
    bool _nbrLoaded; # Si les nombres ont été chargés, dois les effacer avant de les charger à nouveau.

   public:
    Lemmat(QObject *parent = 0, resDir="")
    void ajDesinence(Desinence *d)
    void ajModele(Modele *m)
    void ajRadicaux(Lemme *l)
    QString assim(QString a)
    QString assimq(QString a)
    QString cible()
    QMap<QString, cibles()
    QString desassim(QString a)
    QString desassimq(QString a)
    static QString deramise(QString r)
    static bool estRomain(QString f)
    QStringList frequences(QString txt)
    MapLem lemmatise(QString f);  # lemmatise une forme
    QString lemmatiseFichier(QString f, alpha = False,
                             cumVocibus = False, cumMorpho = False,
                             nreconnu = True)
    QStringList lemmatiseF(QString f, deb)
    # lemmatiseM lemmatise une forme en contexte
    #MapLem lemmatiseM(QString f, debPhr = True)
    MapLem lemmatiseM(QString f, debPhr = True, desas  =False)
    # lemmatiseT lemmatise un texte
    QString lemmatiseT(QString &t)
    QString lemmatiseT(QString &t, alpha, cumVocibus = False,
                       cumMorpho = False, nreconnu = False)
    Lemme *lemme(QString l)
    # lemmes(ml) renvoie la liste des graphies des lemmes
    QStringList lemmes(MapLem ml)
    Modele *modele(QString m)
    QString morpho(int i)
    QString parPos(QString f)
    QString scandeTxt(QString texte, accent = 0, stats = False)
    # QStringList           suffixes
    QMap<QString, suffixes
    QString variable(QString v)
    # Lire un fichier de césures étymologiques (non-phonétiques)
    void lireHyphen (QString fichierHyphen)

    # accesseurs d'options
    bool optAlpha()
    bool optHtml()
    bool optFormeT()
    bool optMajPert()
    bool optMorpho()
    bool optExtension()

    # Pour l'internationalisation
    QString cas(int i)
    QString genre(int i)
    QString nombre(int i)
    QString temps(int i)
    QString modes(int i)
    QString voix(int i)
    QString motsClefs(int i)

    # Pour le tagger
    QString tagTexte(QString t, p, affTout = True)
#    QString tagPhrase(QString phr)
    QString tag(Lemme *l, morph)
    int fraction(QString listTags)
    int tagOcc(QString t)

    # Code en 9 pour le LASLA
    QString k9(QString m)

    void verbaOut(QString fichier); # Connaître l'usage des mots connus
    void verbaCognita(QString fichier, vb=False); # Coloriser le texte avec les mots connus

   public slots:
    # modificateurs d'options
    void setAlpha(bool a)
    void setCible(QString c)
    void setHtml(bool h)
    void setFormeT(bool f)
    void setMajPert(bool mp)
    void setMorpho(bool m)
    void setNonRec(bool n)
    void setExtension(bool e)


#endif
