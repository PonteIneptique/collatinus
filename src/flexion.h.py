'''    flexion.h
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

#ifndef FLEXION_H
#define FLEXION_H

#include <QString>
#include <QStringList>
#include <QUrl>

#include "lemmatiseur.h"
#include "lemme.h"

#define OMIS 1
#define PARENTH 3

class Flexion : public QObject
    Q_OBJECT

   private:
    Lemme *_lemme
    Lemmat *_lemmatiseur
    # constantes de table html :
    QString  static entete
    QString  static lina
    QString  static linb
    QString  static linc
    QString  static queue
    # constantes d'affichage désinence
    int  omis = OMIS
    int  parenth = PARENTH
    # menu
    QString menuLem
    # construction des tableaux par pos
    QString tabNom()
    QString tabPron()
    QString tabAdj()
    QString tabAdv()
    QString tabV()

   public:
    Flexion(QObject *parent = 0)
#    QStringList  static cas
    QString           static entreParenth(QString e)
    QStringList  static genres
    QStringList  static nombres
    QStringList  static temps
    QString                  forme(int m, label = False)
    QString           static gras(QString g)
    QStringList              menu()
    void                     setLemme(Lemme *l)
    void                     setMenu(QStringList m)
    QString                  tableau(Lemme *l)
    QString                  tableaux(MapLem *ml)
    QString                  tableaux(MapLem ml)


#endif
