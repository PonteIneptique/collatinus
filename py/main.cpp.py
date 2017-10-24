'''            main.cpp
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

'''*
 * \file main.cpp
 * \brief main
 * \author Yves Ouvrard
 * \version 11
 * \date 2016
 *
 * main
 '''

#include <QApplication>

#include "mainwindow.h"

'''*
 * \fn main (int argc, *argv[])
 * \brief fonction principale de l'application.
 '''
def main(self, argc, *argv[]):
    QApplication app(argc, argv)
    MainWindow mainWin
    mainWin.show()
    return app.exec()

