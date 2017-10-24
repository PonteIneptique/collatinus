'''          modele.cpp
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

#include <QDebug>

#include "ch.h"
#include "lemmatiseur.h"
#include "modele.h"

#######/
# DESINENCE #
#######/

'''*
 * \fn Desinence.Desinence (QString d, morph, nr, *parent)
 * \brief Constructeur de la classe Desinence. d est la graphie avec quantités,
 *        morph est le numéro de morphologie (dans la liste de la classe
 * Lemmat),
 *        nr est le numéro de radical accepté par la désinence, parent est
 *        un pointeur sur le modèle du lemme et du radical qui utilisent cette
 *        désinence.
 '''
Desinence.Desinence(QString d, morph, nr, *parent)
    # der, dernier caractère de d, s'il est un nombre, le degré de
    # rareté de la désinence, est 10 par défaut.
    der = -1
    if not d.isEmpty():
        der = d.at(d.length()-1).digitValue()
    if der > 0:
        _rarete = der
        d.chop(1)

    _rarete = 10
    # '-' est la désinence zéro
    if (d == "-") d = ""
    _grq = d
    _gr = Ch.atone(_grq)
    _morpho = morph
    _numR = nr
    _modele = qobject_cast<Modele *>(parent)


'''*
 * \fn QString Desinence.gr ()
 * \brief Graphie de la désinence, et sans quantités.
 '''
QString Desinence.gr() { return _gr;

'''*
 * \fn QString Desinence.grq ()
 * \brief Graphie ramiste avec quantités.
 '''
QString Desinence.grq() { return _grq;


'''*
 * \fn Modele* Desinence.modele ()
 * \brief Modèle de la désinence.
 '''
Modele *Desinence.modele() { return _modele;

'''*
 * \fn int Desinence.morphoNum ()
 * \brief Numéro de morpho de la désinence.
 '''
def morphoNum(self):
    return _morpho


'''*
 * \fn int Desinence.numRad ()
 * \brief Numéro de radical de la désinence.
 '''

def numRad(self):
    return _numR


def rarete(self):
    return _rarete


'''*
 * \fn void Desinence.setModele (Modele *m)
 * \brief Attribue un modèle à la désinence.
 '''
def setModele(self, *m):
    _modele = m


######
# MODELE #
######

'''*
 * \fn Modele.Modele (QStringList ll, *parent)
 * \brief Constructeur de la classe modèle. Chaque item
 *        de la liste ll est constitué de champs séparé par
 *        le caractère ':'. Le premier champ est un mot clé.
 *        Le parent est le lemmatiseur. Pour le format du
 *        fichier data/modeles.la, la documentation
 *        utilisateur.
 '''
Modele.Modele(QStringList ll, *parent)
    _lemmatiseur = qobject_cast<Lemmat *>(parent)
    _pere = 0
    QMultiMap<QString, msuff
    QRegExp re("[:;]([\\w]*)\\+{0,1}(\\$\\w+)")
    for l in ll:
        # remplacement des variables par leur valeur
        while (re.indexIn(l) > -1)
            v = re.cap(2)
            var = _lemmatiseur.variable(v)
            pre = re.cap(1)
            if not pre.isEmpty()) var.replace(";", ";" + pre:
            l.replace(v, var)

        eclats = l.simplified().split(":")
        # modele pere des desْ+ R   abs
        #  0      1    2   3   4   5
        p = cles.indexOf(eclats.first())
        switch (p)
            case 0:  # modèle
                _gr = eclats.at(1)
                break
            case 1:  # père
                _pere = parent.modele(eclats.at(1))
                break
            case 2:  # des+: désinences s'ajoutant à celles du père
            case 3:  # des: désinences écrasant celles du père
                QList<int> li = listeI(eclats.at(1))
                r = eclats.at(2).toInt()
                ld = eclats.at(3).split(';')
                for (i = 0; i < li.count(); ++i)
                    QStringList ldd
                    if i < ld.count():
                        ldd = ld.at(i).split(',')
                    else:
                        ldd = ld.last().split(',')
                    for g in ldd:
                        Desinence *nd = Desinence(g, li.at(i), r, self)
                        _desinences.insert(nd.morphoNum(), nd)
                        _lemmatiseur.ajDesinence(nd)


                # si des+, chercher les autres désinences chez le père :
                if p == 3:
                    for i in li:
                        QList<Desinence *> ldp = _pere.desinences(i)
                        foreach (Desinence *dp, ldp)
                            # cloner la désinece
                            Desinence *dh = clone(dp)
                            _desinences.insert(i, dh)
                            _lemmatiseur.ajDesinence(dh)



                break

            case 4:  # R:n: radical n
                nr = eclats.at(1).toInt()
                _genRadicaux[nr] = eclats.at(2)
                break

            case 8: # abs+
                _absents.append(listeI(eclats.at(1)))
                break
            case 5: # abs
                _absents = listeI(eclats.at(1))
                break
            case 6:  # suffixes suf:<intervalle>:valeur
                QList<int> lsuf = listeI(eclats.at(1))
                gr = eclats.at(2);  # TODO verif : bien formée ?
                for m in lsuf:
                    msuff.insert(gr, m)
                break

            case 7:  # sufd: les désinences du père, suffixées
                if _pere != 0:
                    suf = eclats.at(1)
                    QList<Desinence *> ld = _pere.desinences()
                    foreach (Desinence *d, ld)
                        if _absents.contains(d.morphoNum()):
                            # morpho absente chez le descendant
                            continue
                        nd = d.grq()
                        Ch.allonge (&nd)
                        Desinence *dsuf = Desinence
                            (nd+suf, d.morphoNum(), d.numRad(), self)
                        _desinences.insert(dsuf.morphoNum(), dsuf)
                        _lemmatiseur.ajDesinence(dsuf)


                break

            default:
                qDebug() << "Modèle, erreur" << l


    }  # fin de l'interprétation des lignes

    # père
    if _pere != 0:
        for m in _pere.morphos():
            # héritage des désinence
            if (deja(m)) continue
            QList<Desinence *> ld = _pere.desinences(m)
            foreach (Desinence *d, ld)
                if (_absents.contains(
                        d.morphoNum()))  # morpho absente chez le descendant
                    continue
                Desinence *dh = clone(d)
                _desinences.insert(dh.morphoNum(), dh)
                _lemmatiseur.ajDesinence(dh)


        # héritage des radicaux
        foreach (Desinence *d, _desinences)
            if not _genRadicaux.contains(d.numRad()):
                nr = _pere.genRadical(d.numRad())
                _genRadicaux.insert(d.numRad(), nr)


        # héritage des absents
        _absents = _pere.absents()

    # génération des désinences suffixées
    QList<Desinence *> ldsuf
    clefsSuff = msuff.keys()
    clefsSuff.removeDuplicates()
    for suff in clefsSuff:
        foreach (Desinence *d, _desinences)
            if msuff.values(suff).contains(d.morphoNum()):
                gq = d.grq()
                if gq == "-") gq.clear(:
                gq.append(suff)
                Desinence *dsuf =
                    Desinence(gq, d.morphoNum(), d.numRad(), self)
                ldsuf.insert(dsuf.morphoNum(), dsuf)



    foreach (Desinence *dsuf, ldsuf)
        _desinences.insert(dsuf.morphoNum(), dsuf)
        _lemmatiseur.ajDesinence(dsuf)



'''*
 * \fn bool Modele.absent (int a)
 * \brief Renvoie True si la morpho de rang a
 *        n'existe pas dans le modèle. Certains
 *        modèles, exemple, n'ont pas de singulier,
 *        certains verbes n'ont pas de passif.
 '''
bool Modele.absent(int a) { return _absents.contains(a);

'''*
 * \fn QList<int> Modele.absents ()
 * \brief Retourne la liste des numéros des morphos absentes.
 '''
QList<int> Modele.absents() { return _absents;

'''*
 * \fn QList<int> Modele.clesR ()
 * \brief Liste des numéros de radicaux utilisés, et
 *        rangés dans la map _genRadicaux.
 '''
QList<int> Modele.clesR() { return _genRadicaux.keys();

'''*
 * \fn Desinence* Modele.clone (Desinence *d)
 * \brief Crée une Désinence copiée sur la désinence d.
 '''
Desinence *Modele.clone(Desinence *d)
    return Desinence(d.grq(), d.morphoNum(), d.numRad(), self)


'''*
 * \fn bool Modele.deja (int m)
 * \brief Renvoie True si la désinence a une morpho de rang m.
 *        Permet de savoir s'il faut aller chercher la désinence
 *        de morpho m chez le modèle père.
 '''
bool Modele.deja(int m) { return _desinences.contains(m);

'''*
 * \fn QList<Desinence*> Modele.desinences (int d)
 * \brief Renvoie la liste des désinence de morpho d du modèle.
 '''
QList<Desinence *> Modele.desinences(int d) { return _desinences.values(d);

'''*
 * \fn QList<Desinence*> Modele.desinences ()
 * \brief Renvoie toutes les désinences du modèle.
 '''
QList<Desinence *> Modele.desinences() { return _desinences.values();

'''*
 * \fn bool Modele.estUn (QString m)
 * \brief Renvoie True si le modèle se nomme m, si
 *        l'un de ses ancêtre se nomme m
 '''
def estUn(self, m):
    if (_gr == m) return True
    if (_pere == 0) return False
    return _pere.estUn(m)


'''*
 * \fn QString Modele.gr ()
 * \brief Nom du modèle.
 '''
QString Modele.gr() { return _gr;

QStringList  Modele.cles = QStringList() << "modele"  # 0
                                               << "pere"    # 1
                                               << "des"     # 2
                                               << "des+"    # 3
                                               << "R"       # 4
                                               << "abs"     # 5
                                               << "suf"     # 6
                                               << "sufd"    # 7
                                               << "abs+";   # 8

'''*
 * \fn QString Modele.genRadical (int r)
 * \brief Chaîne permettant de calculer un radical à partir
 *        de la forme canonique d'un lemme. r est le numéro
 *        du radical.
 '''
QString Modele.genRadical(int r) { return _genRadicaux[r];

'''*
 * \fn QList<int> Modele.listeI (QString l)
 * \brief Fonction importante permettant de renvoyer
 *        une liste d'entiers à partir d'une chaîne.
 *        La chaîne est une liste de sections séparées
 *        par des virgules. Une section peut être soit
 *        un entier, un intervalle d'entiers. On
 *        donne alors les limites inférieure et supérieure
 *        de l'intervale, par le caractère '-'.
 *        Nombreux exemples d'intervalles dans le fichier
 *        data/modeles.la.
 '''
def listeI(self, l):
    QList<int> result
    lvirg = l.split(',')
    for virg in lvirg:
        if virg.contains('-'):
            deb = virg.section('-', 0, 0).toInt()
            fin = virg.section('-', 1, 1).toInt()
            for (i = deb; i <= fin; ++i) result.append(i)

        else:
            result.append(virg.toInt())


    return result


'''*
 * \fn QList<int> Modele.morphos ()
 * \brief Liste des numéros des désinences définies par le modèle.
 '''
QList<int> Modele.morphos() { return _desinences.keys();

'''*
 * \fn QChar Modele.pos()
 * \brief Retourne la catégorie du modèle, utilisant
 *        les ancêtres du modèle.
 '''
def pos(self):
    if (estUn("uita") or estUn("lupus") or estUn("miles") or estUn("manus") or
        estUn("res") or estUn("perseus"))
        return 'n'
    if (estUn("doctus") or estUn("fortis")) return 'a'
    if (estUn("amo") or estUn("imitor")) return 'v'
    return 'd'

