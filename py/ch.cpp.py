'''      ch.cpp
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
 * \file ch.cpp
 * \brief constantes et utilitaires de traitement
 *        des chaînes de caractères
 *
 '''

#include "ch.h"
#include <QRegExp>

#include <QDebug>

'''*
 * \fn Ch.ajoute (QString mot, liste)
 * \brief Ajoute mot au début de chaque item de liste.
 '''
def ajoute(self, mot, liste):
    QStringList res
    for s in liste:
        res.append(s.prepend(mot))
    return res


'''*
 * \fn Ch.allonge(QString *f)
 * \brief modifie f pour que sa dernière voyelle
 *        devienne longue.
 '''
def allonge(self, *f):
    if (f.isEmpty()) return
    taille = f.size()
    # Je sais que le morceau à attacher commence par une consonne.
    if (consonnes.contains(f.at(taille - 1)) and
        not QString("\u0101e \u0101u \u0113u \u014de")
             .contains(f.mid(taille - 3, 2).toLower()))
        f.replace(QRegExp("[a\u0103]([" + consonnes + "])$"), "\u0101\\1")
        f.replace(QRegExp("[e\u0115]([" + consonnes + "])$"), "\u0113\\1")
        f.replace(QRegExp("[i\u012d]([" + consonnes + "])$"), "\u012b\\1")
        f.replace(QRegExp("[o\u014F]([" + consonnes + "])$"), "\u014d\\1")
        f.replace(QRegExp("[u\u016d]([" + consonnes + "])$"), "\u016b\\1")
        f.replace(QRegExp("[y\u0233]([" + consonnes + "])$"), "\u045e\\1")
        f.replace(QRegExp("[A\u0102]([" + consonnes + "])$"), "\u0100\\1")
        f.replace(QRegExp("[E\u0114]([" + consonnes + "])$"), "\u0112\\1")
        f.replace(QRegExp("[I\u012c]([" + consonnes + "])$"), "\u012a\\1")
        f.replace(QRegExp("[O\u014e]([" + consonnes + "])$"), "\u014c\\1")
        f.replace(QRegExp("[U\u016c]([" + consonnes + "])$"), "\u016a\\1")
        f.replace(QRegExp("[Y\u0232]([" + consonnes + "])$"), "\u040e\\1")



'''*
 * \fn Ch:atone(QString a, bdc)
 * \brief supprime tous les diacritiques de la chaîne a
 *        si bdc est à True, diacritiques des majuscules
 *        sont également supprimés.
 '''
def atone(self, a, bdc):
    # Supprimer le combining breve à la fin du mot
    # if a.endsWith(0x0306)) a.chop(1:
    # minuscules
    a.replace(0x0101, 'a')
    a.replace(0x0103, 'a');  # ā ă
    a.replace(0x0113, 'e')
    a.replace(0x0115, 'e');  # ē ĕ
    a.replace(0x012b, 'i')
    a.replace(0x012d, 'i');  # ī ĭ
    a.replace(0x014d, 'o')
    a.replace(0x014f, 'o');  # ō ŏ
    a.replace(0x016b, 'u')
    a.replace(0x016d, 'u');  # ū ŭ
    a.replace(0x0233, 'y')
    a.replace(0x045e, 'y');  # ȳ ў
    if not bdc:
        # majuscule
        a.replace(0x0100, 'A')
        a.replace(0x0102, 'A');  # Ā Ă
        a.replace(0x0112, 'E')
        a.replace(0x0114, 'E');  # Ē Ĕ
        a.replace(0x012a, 'I')
        a.replace(0x012c, 'I');  # Ī Ĭ
        a.replace(0x014c, 'O')
        a.replace(0x014e, 'O');  # Ō Ŏ
        a.replace(0x016a, 'U')
        a.replace(0x016c, 'U');  # Ū Ŭ
        a.replace(0x0232, 'Y')
        a.replace(0x040e, 'Y');  # Ȳ Ў

    a.replace(0x0131, 'i')
    a.replace(0x1ee5, 'u')
    # combining breve
    a.remove(0x0306);  #ō̆ etc.
    return a


'''*
 * \fn Ch:communes(QString g)
 * \brief note comme communes toutes les voyelles qui ne portent pas de quantité.
 '''
def communes(self, g):
    maj = g[0].isUpper()
    g = g.toLower()
    if g.contains("a") or g.contains("e") or g.contains("i") or g.contains("o") or g.contains("u") or g.contains("y"):
        g.replace("a","ā̆")
        g.replace(QRegExp("([^āăō])e"),"\\1ē̆")
        g.replace(QRegExp("^e"),"ē̆")
        g.replace("i","ī̆")
        g.replace("o","ō̆")
        g.replace(QRegExp("([^āēq])u"),"\\1ū̆")
        g.replace(QRegExp("^u"),"ū̆")
        g.replace(QRegExp("^y"),"ȳ̆")
        g.replace(QRegExp("([^ā])y"),"\\1ȳ̆")

    if maj) g[0] = g[0].toUpper(:
    return g


'''*
 * \fn Ch.deQuant(QString *c)
 * \brief utilisée en cas d'élision.
 * supprime la quantité de la voyelle finale de la chaine c
 * lorsque cette voyelle est en fin de mot ou suivie d'un "m".
 '''
def deQuant(self, *c):
    if c.endsWith("\u0306"):
        c.chop(1);  # Supprimer le combining breve à la fin du mot
    c.replace(QRegExp("[\u0101\u0103](m?)$"), "a\\1");  # ā ă
    c.replace(QRegExp("[\u0113\u0115](m?)$"), "e\\1")
    c.replace(QRegExp("[\u012b\u012d](m?)$"), "i\\1")
    c.replace(QRegExp("[\u014d\u014f](m?)$"), "o\\1")
    c.replace(QRegExp("[\u016b\u016d](m?)$"), "u\\1")
    c.replace(QRegExp("[\u0232\u0233](m?)$"), "y\\1")


'''*
 * \fn Ch.deAccent(QString *c)
 * \brief Supprime tous les accents d'un texte (acute, macron, breve)
 '''
def deAccent(self, c):
    c = c.normalized(QString.NormalizationForm_D, QChar.currentUnicodeVersion())
    c.remove("\u0301")
    c.remove("\u0306")
    c.remove("\u0304")
    return c


'''*
 * \fn QString Ch.deramise(QString r)
 * \brief retourne une graphie non-ramiste
 *        de r, dont tous les j deviennent i,
 *        et tous les v deviennent u. Les V majuscules
 *        sont ignorés.
 '''
def deramise(self, r):
    r.replace('J', 'I')
    r.replace('j', 'i')
    r.replace('v', 'u')
    r.replace("æ", "ae")
    r.replace("Æ", "Ae")
    r.replace("œ", "oe")
    r.replace("Œ", "Oe")
    r.replace(0x1ee5, 'u');  # ụ le u muet de suavis, suadeo, etc...
    r.replace ('V', 'U')
    return r


'''*
 * \fn Ch.elide(QString *mp)
 * \brief met entre crochets la dernière syllabe de mp.
 '''
def elide(self, *mp):
    #"Tāntāene"
    #debog = (*mp == "Tāntāene")
    #if (debog) qDebug() << "tantaene" << *mp
    taille = mp.size()
    if ((taille > 1) and ((mp.endsWith('m') or mp.endsWith("\u0101e")) or
                         mp.endsWith("\u0306")) and
        voyelles.contains(mp.at(taille - 2)))
        #if (debog) qDebug() << "cond1"
        deQuant(mp)
        mp.insert(taille - 2, '[')
        mp.append(']')

    elif voyelles.contains(mp.at(taille - 1)) and *mp != "\u014d":
        #if (debog) qDebug() << "cond2"
        deQuant(mp)
        mp.insert(taille - 1, '[')
        mp.append(']')

    #if (debog) qDebug() << *mp


def genStrNum(self, s, *ch, *n):
    ch.clear()
    *n = 0
    for (i = 0; i < s.length(); ++i)
        if not s.at(i).isNumber():
            ch.append(s.at(i))
        else:
            *n = s.mid(i).toInt()
            break



'''*
 * \fn Ch.sort_i( QString &a, &b)
 * \brief compare a et b sans tenir compte des diacritiques ni de la casse.
 * \return True si a < b.
 '''
def sort_i(self, &a, &b):
    return QString.compare(atone(a), atone(b), Qt.CaseInsensitive) < 0


'''*
 * \fn Ch.inv_sort_i( QString &a, &b)
 * \brief compare a et b sans tenir compte des diacritiques ni de la casse.
 * \return True si a > b.
 * Utilisée pour ranger les mots en fontions des fréquences descendantes
 '''
def inv_sort_i(self, &a, &b):
    return QString.compare(atone(a), atone(b), Qt.CaseInsensitive) > 0


'''*
 * \fn Ch.versPC(QString k)
 * \brief Comme versPedeCerto, ici le mot n'a pas été trouvé.
 *        Les voyelles ne sont pas marquées sauf par position...
 '''
def versPC(self, k):
    k = k.toLower()
    if (k.contains("[")) k = k.section("[", 0, 0) + "`"
    k.replace("qu", "")
    k.replace("gu", "")
    k.replace("āe", "+")
    k.replace("ōe", "+")
    k.replace("āu", "+")
    k.replace("ēu", "+")
    # Incomplet : manque la recherche de doubles consonnes ou voyelles
    k.replace("a", "*")
    k.replace("e", "*")
    k.replace("i", "*")
    k.replace("o", "*")
    k.replace("u", "*")
    k.replace("y", "*")
    return versPedeCerto(k)


'''*
 * \fn Ch.versPedeCerto(QString k)
 * \brief remplace les longues de k par +, brèves par - et les communes par
 * *
 '''
def versPedeCerto(self, k):
    # Je remplace les longues par +, brèves par - et les communes par *
    # minuscules
    k.replace(0x0101, '+')
    k.replace(0x0103, '-');  # ā ă
    k.replace(0x0113, '+')
    k.replace(0x0115, '-');  # ē ĕ
    k.replace(0x012b, '+')
    k.replace(0x012d, '-');  # ī ĭ
    k.replace(0x014d, '+')
    k.replace(0x014f, '-');  # ō ŏ
    k.replace(0x016b, '+')
    k.replace(0x016d, '-');  # ū ŭ
    k.replace(0x0233, '+')
    k.replace(0x045e, '-');  # ȳ ў
    # majuscule
    k.replace(0x0100, '+')
    k.replace(0x0102, '-');  # Ā Ă
    k.replace(0x0112, '+')
    k.replace(0x0114, '-');  # Ē Ĕ
    k.replace(0x012a, '+')
    k.replace(0x012c, '-');  # Ī Ĭ
    k.replace(0x014c, '+')
    k.replace(0x014e, '-');  # Ō Ŏ
    k.replace(0x016a, '+')
    k.replace(0x016c, '-');  # Ū Ŭ
    k.replace(0x0232, '+')
    k.replace(0x040e, '-');  # Ȳ Ў
    # "+" + breve = voyelle commune
    k.replace("+\u0306", "*")
    if (k.contains("[")) k = k.section("[", 0, 0) + "`"
    # Je garde une trace de l'élision (pour le rythme)
    k.remove(0x1ee5);  # suppression du u-exponctué.
    k.remove(reLettres)
    return k


def transforme(self, k):
    k.replace("āe", "æ+")
    k.replace("ōe", "œ+")
    k.replace("ăe", "æ-")
    k.replace("Āe", "Æ+")
    k.replace("Ōe", "Œ+")
    # Je remplace les longues par +, brèves par - et les communes par *
    # minuscules
    k.replace(0x0101, "a+")
    k.replace(0x0103, "a-");  # ā ă
    k.replace(0x0113, "e+")
    k.replace(0x0115, "e-");  # ē ĕ
    k.replace(0x012b, "i+")
    k.replace(0x012d, "i-");  # ī ĭ
    k.replace(0x014d, "o+")
    k.replace(0x014f, "o-");  # ō ŏ
    k.replace(0x016b, "u+")
    k.replace(0x016d, "u-");  # ū ŭ
    k.replace(0x0233, "y+")
    k.replace(0x045e, "y-");  # ȳ ў
    # majuscule
    k.replace(0x0100, "A+")
    k.replace(0x0102, "A-");  # Ā Ă
    k.replace(0x0112, "E+")
    k.replace(0x0114, "E-");  # Ē Ĕ
    k.replace(0x012a, "I+")
    k.replace(0x012c, "I-");  # Ī Ĭ
    k.replace(0x014c, "O+")
    k.replace(0x014e, "O-");  # Ō Ŏ
    k.replace(0x016a, "U+")
    k.replace(0x016c, "U-");  # Ū Ŭ
    k.replace(0x0232, "Y+")
    k.replace(0x040e, "Y-");  # Ȳ Ў
    # "+" + breve = voyelle commune
    k.replace("+\u0306", "*")
    k.replace(0x1ee5, "u");  # suppression du u-exponctué.
    return k


def accentue(self, l):
    if ((l == "œ") or (l == "Œ")) return l + "\u0301"
    if (l == "æ") return "ǽ"
    if (l == "Æ") return "Ǽ"
    a = l[0].unicode()
    switch (a)
        case 97:
            return "á"
        case 101:
            return "é"
        case 105:
            return "í"
        case 111:
            return "ó"
        case 117:
            return "ú"
        case 121:
            return "ý"
        case 65:
            return "Á"
        case 69:
            return "É"
        case 73:
            return "Í"
        case 79:
            return "Ó"
        case 85:
            return "Ú"
        case 89:
            return "Ý"
            break
        default:
            return l
            break



def ajoutSuff(self, fq, suffixe, l_etym, accent):
    illius = False
    cesure = False
    sansAccent = False
    if accent > 7:
        illius = True
        accent -= 8

    if accent > 3:
        cesure = True
        accent -= 4

    if accent > 0:
        signes = "+-*"
        fq = transforme(fq)
        l = fq.count('+') + fq.count('-') +
                fq.count('*');  # nombre de syllabes.
        i = fq.size() - 1
        if suffixe.isEmpty() or (suffixe == "st"):
            # Sans suffixe, l'accent est sur l'avant-dernière voyelle si elle
            # n'est pas brève
            if l > 2:
                if illius and fq.endsWith("i*u-s"):
                    fq.chop(5)
                    fq.append("í*u-s")

                else:
                    while (not signes.contains(fq[i])) i -= 1
                    i -= 1
                    while (not signes.contains(fq[i])) i -= 1
                    sansAccent = (fq[i] == '*') and (accent == 3)
                    # La pénultième est commune et je la considère comme ambiguë =
                    # pas d'accent.
                    if (fq[i] == '-') or ((fq[i] == '*') and (accent == 2)):
                        # Remonter à l'antépénultième
                        i -= 1
                        while (not signes.contains(fq[i])) i -= 1

                    if not sansAccent:
                        if i > 1:
                            fq = fq.mid(0, i - 1) + accentue(fq.mid(i - 1, 1)) +
                                    fq.mid(i)
                        else:
                            fq = accentue(fq.mid(i - 1, 1)) + fq.mid(i)



            fq += suffixe

        else:
            # Avec suffixe, l'accent est sur la dernière (avant collage)
            if l > 1:
                while (not signes.contains(fq[i])) i -= 1
                if i > 1:
                    fq = fq.mid(0, i - 1) + accentue(fq.mid(i - 1, 1)) +
                         fq.mid(i)
                else:
                    fq = accentue(fq.mid(i - 1, 1)) + fq.mid(i)

            fq = fq + suffixe
            fq.replace("ĕ","e-"); # pour modoquest
#            fq[fq.size() - 2] = 'e';  # ôte le e-bref.
            l += 1

        # L'entier i pointe sur la longueur de la voyelle accentuée, si
        # j'ai ajouté un \u0301.
        # Si je veux marquer la syllabe accentuée en gras, c'est ici !
        if (l > 1) and cesure:
            # Il y a au moins deux syllabes que je veux séparer
            j = fq.size() - 1
            while (not signes.contains((fq[j])) and (j > 0)) j -= 1
            k = j
            j -= 2
            while (not signes.contains((fq[j])) and (j > 0)) j -= 1
            while (j > 0)
                # la césure doit tomber quelque part entre j et k
                if k == j + 2:
                    fq.insert(j, separSyll);  # Il n'y a que la voyelle (et une
                                              # quantité)
                else:
                    nbCons = 0
                    for (n = j + 1; n < k - 1; n++)
                        if consonnes.contains(fq[n]) or (fq[n] == 'h'):
                            nbCons += 1
                    # J'ai le nombre de consonnes
                    if nbCons == 0:
                        fq.insert(k - 1, separSyll)
                    else:
                        while (not consonnes.contains(fq[k]) and (fq[k] != 'h'))
                            k -= 1
                        if nbCons == 1:
                            fq.insert(k, separSyll)
                        else:
                            # c'est plus compliqué car j'ai au moins deux
                            # consonnes...
                            bool remonte =
                                ((fq[k] == 'l') and (fq[k - 1] != 'l') and (fq[k - 1] != 'r'))
                            remonte = remonte or
                                      ((fq[k] == 'r') and (fq[k - 1] != 'r') and (fq[k - 1] != 'l'))
                            remonte = remonte or (fq[k] == 'h')
                            if (remonte) k -= 1
                            remonte =
                                ((fq[k] == 'c') and (fq[k - 1] == 's') and
                                 (fq[k + 1] != 'a') and (fq[k + 1] != 'o') and
                                 (fq[k + 1] != 'u') and (fq[k + 1] != 'h'))
                            remonte = remonte or
                                      ((fq[k] == 'p') and (fq[k - 1] == 's'))
                            # remonte = remonte or ((fq[k]=='t') and
                            # (fq[k-1]=='s'))
                            remonte = remonte or
                                      ((fq[k] == 'n') and (fq[k - 1] == 'g'))
                            if (remonte) k -= 1
                            fq.insert(k, separSyll)



                k = j
                j -= 2
                while ((j > 0) and not signes.contains((fq[j]))) j -= 1

            # J'ai placé les césures en suivant les règles établies.
            # Mais je peux avoir des césures étymologiques qui vont à
            # l'encontre des règles "normales".
            #            l_etym = e.getHyphen()
            if not l_etym.isEmpty()) foreach (QString etym, l_etym.split(','):
                    fq1 = fq
                    # Je vais parcourir le mot pour vérifier que ça colle
                    i = 0
                    j = 0
                    changement = 0
                    OK = True
                    while ((i < etym.size()) and (j < fq.size()) and OK)
                        if ((etym[i] == fq[j]) or
                            (fq.mid(j, 1) == accentue(etym.mid(i, 1))))
#                            ((etym[i] == '-') and (fq[j] == separSyll)))
                            # Les lettres ou les césures correspondent
                            i += 1
                            j += 1

                        elif signes.contains(fq[j]) or (fq[j] == 0x0301):
                            j += 1;  # C'est une quantité
                        elif (etym[i] != separSyll) and (fq[j] != separSyll):
                            OK = False;  # Les lettres ne correspondent pas.
                        else:
                            # la césure est mal placée.
                            if etym[i] == separSyll:
                                fq.insert(j, separSyll)
                                changement += 1
                                j += 1
                                i += 1

                            else:
                                fq.remove(j, 1)
                                changement -= 1



                    if changement == 1:
                        # La césure étymologique est tombé avant la césure
                        # normale...
                        while (fq[j] != separSyll) j += 1
                        fq.remove(j, 1)

                    if not OK:
                        fq = fq1;  # etym ne correspondait pas aux premières
                                   # lettres de fq.


        fq.remove("+")
        fq.remove("-")
        fq.remove("*")
        return fq

    if (suffixe.isEmpty()) return fq
    # les suffixes possibles sont que, et ve :
    # tous commencent par une consonne
    allonge(&fq)
    if suffixe == "st":
        # Si fq se termine par une voyelle, ne fait rien.
        fq += "s"; # J'ajoute donc le s et je recommence.
        allonge(&fq)
        return fq + "t"

    suffixe.replace("ĕst","ēst"); # Pour des formes comme modoquest
    return fq + suffixe

