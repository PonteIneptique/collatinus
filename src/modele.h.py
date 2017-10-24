'''           modele.h
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

#ifndef MODELE_H
#define MODELE_H

#include <QList>
#include <QMultiMap>
#include <QString>
#include <QStringList>
#include <QtCore>

class Lemmat
class Modele

class Desinence : public QObject
    Q_OBJECT
   private:
    QString _gr
    QString _grq
    int     _morpho
    Modele *_modele
    int     _numR
    int     _rarete

   public:
    Desinence(QString d, morph, nr, *parent = 0)
    QString gr()
    QString grq()
    int     rarete()
    Modele *modele()
    int     morphoNum()
    int     numRad()
    void    setModele(Modele *m)


class Modele : public QObject
    Q_OBJECT
   private:
    QList<int> _absents
    QStringList static  cles
    QMultiMap<int, *> _desinences
    QMap<int, _genRadicaux
    QString _gr
    QString _grq
    Lemmat *_lemmatiseur
    Modele *_pere

   public:
    Modele(QStringList ll, *parent = 0)
    bool               absent(int a)
    QList<int>         absents()
    QList<int>         clesR()
    Desinence         *clone(Desinence *d)
    bool               deja(int m)
    QList<Desinence *> desinences(int d)
    QList<Desinence *> desinences()
    bool               estUn(QString m)
    QString            genRadical(int r)
    QString            gr()
    QString            grq()
    static QList<int>  listeI(QString l)
    QList<int>         morphos()
    QChar              pos()


#endif
