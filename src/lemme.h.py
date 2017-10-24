'''               lemme.h
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

#ifndef LEMME_H
#define LEMME_H

#include <QMultiMap>
#include <QObject>
#include <QString>
#include "irregs.h"
#include "lemmatiseur.h"
#include "modele.h"

class Irreg
class Lemmat
class Lemme
class Modele

class Radical : public QObject
   private:
    QString _gr
    QString _grq
    Lemme* _lemme
    int _numero

   public:
    Radical(QString g, n, parent)
    QString gr()
    QString grq()
    Lemme* lemme()
    Modele* modele()
    int numRad()


class Lemme : public QObject
    Q_OBJECT
   private:
    QString                     _cle
    QString                     _gr
    QString                     _grd
    QString                     _grq
    QString                     _grModele
    QString                     _hyphen; # Pour les césures étymologies
    QString                     _indMorph
    QList<Irreg*>               _irregs
    Modele*                     _modele
    int                         _nh
    Lemmat*                     _lemmatiseur
    QList<int>                  _morphosIrrExcl
    int                         _nbOcc; # Nombre d'occurrences du lemme dans les textes du LASLA
    int                         _origin; # lemmes ou lem_ext
    QString                     _pos
    QMap<int, QList<Radical*> > _radicaux
    QString                     _renvoi
    QMap<QString, _traduction

   public:
    Lemme( QString linea, origin, parent)
    void                ajIrreg(Irreg* irr)
    void                ajNombre(int n)
    void                ajRadical(int i, r)
    void                ajTrad(QString t, l)
    QString             ambrogio()
    QString             cle()
    QList<int>          clesR()
    bool                estIrregExcl(int nm)
    QString             genre()
    QString             getHyphen (); # Accesseurs pour les césures étymologiques
    QString             gr()
    QString             grq()
    QString             grModele()
    QString             humain(html = False, l = "fr", nbr = False)
    QString             indMorph()
    QString             irreg(int i, excl)
    Modele*             modele()
    int                 nbOcc() const;    # Retourne le nombre d'occurrences du lemme
    void                clearOcc(); # Efface       "           "            "
    int                 nh()
    int                 origin()
    QString static      oteNh(QString g, nh)
    QString             pos()
    QList<Radical*>     radical(int r)
    bool                renvoi()
    void                setHyphen (QString h)
    QString             traduction(QString l)
    inline bool operator<( Lemme &l)


#endif
