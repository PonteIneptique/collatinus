'''   scandeur.cpp
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

#include "ch.h"
#include "lemmatiseur.h"

#include <QDebug>

'''*
 * \fn QStringList Lemmat.cherchePieds (int nbr, ligne, i, bool
 *pentam)
 * \brief cherchePieds est une routine récursive qui construit la liste
 * de toutes les combinaisons possibles de dactyles et de spondées
 * en commençant par le caractère d'indice i.
 * Elle est récursive car chaque fois qu'elle a trouvé un D ou un S,
 * elle va chercher toutes les combinaisons possibles à partir
 * du caractère d'indice i+3 ou i+2.
 * Les longues sont notées + et les brèves -.
 * Les mots sont séparés par un espace et on a gardé une trace
 * des élisions avec un `.
 * Une grande partie de la difficulté vient des voyelles communes
 * ou indéterminées, *. S'il n'y avait que des + et des -,
 * on n'aurait que D=+-- et S=++. Avec l'* en plus, faut considérer
 * toutes les possibilités :
 * s=*+, +* ou **
 * d=*--, +*-, +-*, +**, *-*, **- ou ***.
 *************************'''
def cherchePieds(self, nbr, ligne, i, pentam):
    QStringList res
    longueurs = "+-*"
    ll = ligne.count()
    if (i >= ll)  # trop loin !
        res << ""
        return res

    if (nbr == 1)  # Dernier pied !
        # qDebug () << i << " " << ll << " " << ligne << ligne[i] <<
        # ligne[i+1]
        if pentam:
            # C'est un pentamètre, ne dois avoir
            # qu'une quantité indifférente
            if (ligne[i] == ' ') i += 1
            # J'étais sur un blanc (espace entre deux mots),
            # j'ai avancé d'une syllabe
            if ((i == ll - 1) or (ligne[i + 1] == ' ')) res << "Z"
            # Fin de ligne ou du mot
            else:
                res << ""
            return res

        else:
            # C'est un hexamètre, cherche encore deux syllabes
            while (not longueurs.contains(ligne[i]) and i < ll) i += 1
            # qDebug()<<i<<" "<<ll<<" "<<ligne<< ligne[i] << ligne[i+1]
            if i > ll - 2:
                res << ""
                return res

            if ligne[i] != '-':
                if i == ll - 2 and longueurs.contains(ligne[i + 1]):
                    res << "X"
                elif ligne[i + 2] == ' ':
                    res << "X"
                else:
                    res << ""

            else:
                res << ""
            return res


    # J'ai traité les cas qui terminent la récursion
    while (not longueurs.contains(ligne[i]) and i < ll) i += 1
    if i == ll:
    {  # Encore un cas qui termine
        res << ""
        return res

    car1 = ligne[i]
    j = i + 1
    while (not longueurs.contains(ligne[j]) and j < ll) j += 1
    if (j == ll)  # Je n'ai qu'une syllabe : fin prématurée de pentamètre ?
        res << "z"
        return res

    car2 = ligne[j]
    QChar car3
    k = j + 1
    while (not longueurs.contains(ligne[k]) and k < ll) k += 1
    if k == ll:
        car3 = ' '
    else:
        car3 = ligne[k]
    if car1 == '-':
    {  # Encore un cas qui termine : aucun pied ne commence par une brève
        res << ""
        return res

    if nbr == 4 and car1 == '+':
        res << Ch.ajoute("Y", cherchePieds(3, ligne, i + 1, True))
    if nbr == 4 and car1 == '*':
        res << Ch.ajoute("y", cherchePieds(3, ligne, i + 1, True))
    if car1 == '+' and car2 == '+':
        res << Ch.ajoute("S", cherchePieds(nbr - 1, ligne, j + 1, pentam))
    if ((car1 == '+' and car2 == '*') or (car1 == '*' and car2 == '+') or
        (car1 == '*' and car2 == '*'))
        res << Ch.ajoute("s", cherchePieds(nbr - 1, ligne, j + 1, pentam))
    if car1 == '+' and car2 == '-' and car3 == '-':
        res << Ch.ajoute("D", cherchePieds(nbr - 1, ligne, k + 1, pentam))
    if (car1 == '*' and (car2 == '-' or car2 == '*') and
        (car3 == '-' or car3 == '*'))
        res << Ch.ajoute("d", cherchePieds(nbr - 1, ligne, k + 1, pentam))
    if (car1 == '+' and ((car2 == '*' and (car3 == '-' or car3 == '*')) or
                        (car2 == '-' and car3 == '*')))
        res << Ch.ajoute("d", cherchePieds(nbr - 1, ligne, k + 1, pentam))
    return res


'''*
 * \fn QStringList Lemmat.formeq (QString forme, *nonTrouve, debPhr)
 * \brief Renvoie forme scandée de toutes les manières possibles en appliquant
 *        les quantités données par les dictionnaires et les règles prosodiques.
 '''
QStringList Lemmat.formeq(QString forme, *nonTrouve, debPhr,
                           int accent)
    *nonTrouve = True
    if forme.isEmpty()) return QStringList(:
    mp = lemmatiseM(forme, _majPert or debPhr)
    if mp.empty():
        if accent == 0:
            return QStringList() << parPos(forme)
        else:
            return QStringList() << forme

    *nonTrouve = False
    QStringList lforme
    QMap<QString, mFormes
    maj = forme.at(0).isUpper()
    foreach (Lemme *l, mp.keys())
        for s in mp.value(l):
            # f = Ch.ajoutSuff(s.grq, s.sufq, "", accent)
            # Le 3e paramètre, actuellement "", prévu pour accepter
            # l.getHyphen(). Donc
            f = Ch.ajoutSuff(s.grq,s.sufq,l.getHyphen(),accent)
            #			if s.grq == "-") f = l.grq(:
            #			f = parPos(s.grq)
            if maj) f[0] = f[0].toUpper(:
            mFormes[f] += fraction(tag(l,s.morpho)) * l.nbOcc(); # Je compte le nombre d'occurrences de chaque forme.
#            lforme.append(f)


    #    lforme.removeDuplicates()
    for f in mFormes.keys():
        nb = mFormes[f]
        i = 0
        while (i< lforme.size())
            if (mFormes[lforme[i]] > nb) i += 1
            else:
                # Le nombres d'occurrences de la forme courante est supérieur à la forme actuellement en position i.
                lforme.insert(i,f); # J'insère la forme courante en i.
                i = lforme.size() + 1; # Je sors !


        if (i == lforme.size()) lforme.append(f); # Je suis arrivé à la fin de la liste sans insérer la forme courante.

    return lforme


'''*
 * \fn QString Lemmat.scandeTxt (QString texte, stats)
 * \brief Scande le texte, les statistiques si stats
 *        est à True, renvoie le résultat.
 * \param   texte : le texte à scander ou à accentuer
 *          stats : booléen qui affiche ou non les statistiques
 *          accent : un entier qui détermine si le résultat est
 * scandé ou accentué. Les valeurs permises sont 0 (texte scandé),
 * 1-3 texte accentué, 5-7 texte accentué avec les syllabes marquées.
 * Les valeurs non-nulles règlent le comportement de l'accent si la pénultième
 * est commune : 1 et 5 la considère comme longue, et 6 comme brève,
 * 3 et 7 ne place pas l'accent car la pénultième est ambiguë.
 '''
def scandeTxt(self, texte, accent, stats):
    accent = accent & 15
    QString schemaMetric
    QMap<QString, freqMetric
    bool deb_phr
    int decalage
    QStringList vers
    QStringList formes
    QStringList aff
    lignes = texte.split("\n")
    for ligne in lignes:
        QStringList separ
        if ligne.isEmpty():
            separ.append(ligne)
        else:
            separ = ligne.split(QRegExp("\\b"))
        if (separ.count() > 0 and separ.at(0).count() > 0 and
            separ.at(0).at(0).isLetter())
            separ.prepend("")
        if (separ.count() > 0 and separ.at(separ.count() - 1).count() > 0 and
            separ.at(separ.count() - 1).at(0).isLetter())
            separ.append("")
        # J'ai maintenant une liste de formes et une liste de séparateurs
        # la ligne d'origine est la concaténation de separ[i]
        # Les termes pairs sont les séparateurs.
        # Les termes impairs sont les mots.
        # J'ai toujours un dernier séparateur, vide.
        # La scansion peut commencer !
        decalage = aff.count()
        if separ.size() < 3:
            aff.append(ligne + "<br />\n")
            # C'est une ligne vide ou ne contenant pas de lettre :
            # je la laisse comme elle est !
            continue

        bool nonTr, nonTrSuiv
        QStringList lforme
        lfs = formeq(separ[1], &nonTrSuiv, True, accent)
        schemaMetric = ""
        for (i = 1; i < separ.length(); i += 2)
            aff.append(separ[i - 1])
            lforme = lfs
            nonTr = nonTrSuiv
            if i < separ.length() - 2:
                deb_phr = separ[i + 1].contains(Ch.rePonct)
                lfs = formeq(separ[i + 2], &nonTrSuiv, deb_phr, accent)
                if accent == 0:
                    if Ch.consonnes.contains(lfs[0].at(0).toLower()):
                        for (j = 0; j < lforme.length(); ++j)
                            Ch.allonge(&lforme[j])
                    else:
                        for (j = 0; j < lforme.length(); ++j)
                            Ch.elide(&lforme[j])


            lforme.removeDuplicates()
            # C'est le bon moment pour extraire le schéma métrique
            if stats:
                if nonTr:
                    schemaMetric.append("?" + Ch.versPC(lforme[0]) + " ")
                else:
                    schMet = Ch.versPedeCerto(lforme[0])
                    if lforme.length() > 1:
                        for (ii = 1; ii < lforme.length(); ii++)
                            schMet2 = Ch.versPedeCerto(lforme[ii])
                            if schMet.size() != schMet2.size():
                                schMet = "@" + lforme[0]
                                continue

                            else:
                                for (j = 0; j < schMet.size(); j++)
                                    if schMet[j] != schMet2[j]:
                                        schMet[j] = '*'
                            # En cas de réponse multiple,
                            # je marque comme communes les voyelles qui
                            # diffèrent

                    schemaMetric.append(schMet + " ")


            # ajouter des parenthèses pour les analyses multiples
            if lforme.length() > 1:
                lforme[1].prepend('(')
                lforme[lforme.length() - 1].append(')')

            if nonTr:
                aff.append("<em>" + lforme[0] + "</em>")
            else:
                aff.append(lforme.join(" "))
            # pour les analyses multiples, dois insérer des espaces.

        aff.append(separ[separ.length() - 1] + "<br />\n")
        # Je termine la ligne par le dernier séparateur et un saut de ligne.
        if stats:
            # Je cherche des vers dans la prose
            ii = 0
            numMot = 1
            lsch = schemaMetric.count() - 10
            # Un pentamètre compte au moins 10 syllabes, l'hexamètre 12.
            longueurs = "+-*"
            QStringList result
            while (ii < lsch)
                while (not longueurs.contains(schemaMetric[ii]) and ii < lsch)
                    ii += 1
                # Je suis au début du mot
                result.clear()
                if ii < lsch and schemaMetric[ii] != '-':
                    result = cherchePieds(6, schemaMetric, ii, False)
                # analyse du résultat
                QString numero
                numero.setNum(ii)
                ajout = ""
                for item in result:
                    if item.count() == 6:
                        if ajout == "":
                            ajout = "<span style='color:red' title='" + item
                        else:
                            ajout += "\n" + item
                        syllabes = 0
                        for (a = 0; a < 6; a++)
                            if (item[a] == 'S' or item[a] == 's' or
                                item[a] == 'X')
                                syllabes += 2
                            if (item[a] == 'D' or item[a] == 'd') syllabes += 3
                            if (item[a] == 'Y' or item[a] == 'y' or
                                item[a] == 'Z')
                                syllabes += 1

                        j = ii
                        nbMots = 1
                        while (syllabes > 0)
                            if (schemaMetric[j] == '?' or
                                schemaMetric[j] == '@')
                                j += 1
                            elif longueurs.contains(schemaMetric[j]):
                                j += 1
                                syllabes -= 1

                            else:
                                nbMots += 2
                                while (not longueurs.contains(schemaMetric[j]) and
                                       (j < schemaMetric.size()))
                                    j += 1


                        it = item + " : "
                        for (j = 0; j < nbMots; j++)
                            it += aff[decalage + numMot + j]
                        if item.endsWith("Z"):
                            it = "<span style='color:red'>" + it + "</span>"
                        vers << it + "<br>\n"


                if ajout != "":
                    # decalage+numMot est le numéro du
                    # mot, la liste aff, mon analyse a commencé.
                    aff[decalage + numMot] =
                        ajout + "'>" + aff[decalage + numMot]
                    # 3 premiers mots en rouge
                    # aff[decalage+numMot+5]=aff[decalage+numMot+5]+"</span>"
                    # aff[decalage+numMot+5]+="</span>"
                    if aff.count() > decalage + numMot + 5:
                        aff[decalage + numMot + 5].append("</span>")

                while ((schemaMetric[ii] != ' ') and ii < lsch) ii += 1
                numMot += 2
                # Je suis sur le blanc qui précède un mot

            # Je remplace les +-* par des signes plus conventionnels
            schemaMetric.replace('-', "∪")
            schemaMetric.replace('+', "‑")
            schemaMetric.replace('*', "∪̲")
            # schemaMetric.replace('-', "u")
            # schemaMetric.replace('+', "-")
            # schemaMetric.replace('*', "-\u0306")
            aff.append("&nbsp;<small>" + schemaMetric + "</small>&nbsp;<br>\n")
            schemaMetric.remove(" ")
            schemaMetric.remove("`")
            # Pour ignorer la longueur de la dernière voyelle
            # if not schemaMetric.endsWith("\u0306"):
            #            # schemaMetric[schemaMetric.length()-1]='-'
            # schemaMetric.append("\u0306")
            #
            freqMetric[schemaMetric] += 1


    if stats:
        # Il me reste à trier les freqMetric
        formes.clear()
        for schM in freqMetric.keys():
            if freqMetric[schM] > 1:
                # Je ne garde que les schéma qui apparaissent plus d'une fois.
                n = freqMetric[schM] + 10000
                QString numero
                numero.setNum(n)
                numero = numero.mid(1)
                formes << numero + " : " + schM

        formes.sort()
        aff.prepend(
            "<a href='#statistiques'>Statistiques</a> "
            "<a href='#analyses'>Analyses</a><br>\n")
        aff.prepend("<a name='texte'></a>")
        # aff.prepend("------------<br/>\n")
        # Pour séparer la liste du texte.
        vers.prepend(
            "<hr><a href='#texte'>Texte</a> "
            "<a href='#statistiques'>Statistiques</a><br>\n")
        vers.prepend("<a name='analyses'></a>")
        for (i = 0; i < formes.size(); i++)
            lg = formes[i]
            while (lg[0] == '0') lg = lg.mid(1)
            vers.prepend(lg + "<br/>\n")
            # En faisant un prepend, j'inverse l'ordre :
            # le plus fréquent finira premier

        vers.prepend(
            "<hr><a href='#texte'>Texte</a> "
            "<a href='#analyses'>Analyses</a><br>\n")
        vers.prepend("<a name='statistiques'></a>")
        vers.append(
            "<a href='#texte'>Texte</a> "
            "<a href='#statistiques'>Statistiques</a> "
            "<a href='#analyses'>Analyses</a><br>\n")
        aff << vers
        # aff.prepend("------------<br/>\n")
        # Pour séparer la liste du texte.
        # for ligne in vers: aff.prepend(ligne)

    return aff.join("")

