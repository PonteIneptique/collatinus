#include "mot.h"

class Mot(object):
    def __init__(forme, rang, debVers, *parent):
    self._forme = forme
    self._rang = rang
    self._lemmatiseur = qobject_cast<Lemmat *>(parent)
    self._probas.clear()
    self._tagEncl = ""
    if forme.isEmpty():
        self._tags << "snt"
        self._probas["snt"] = 1
    else:
        self._mapLem = self._lemmatiseur.lemmatiseM(forme, (rang == 0) or debVers)
        self.enclitique = ""
        # échecs
        if _mapLem.empty():
            # Je ne sais pas encore quoi faire.
        else:
            foreach (Lemme *l, _mapLem.keys())
                lem = l.humain(True, _lemmatiseur.cible(), True)
                nb = l.nbOcc()
                for m in _mapLem.value(l):
                    lt = _lemmatiseur.tag(l, m.morpho); # Maintenant, c'est une liste de tags.
                    # Pour les analyses, garde la liste de tags.
                    fr = nb * _lemmatiseur.fraction(lt)
                    _lemmes.append(lem)
                    _tags.append(lt)
                    _nbOcc.append(fr)
                    #                    qDebug() << forme << lem << nb << lt << t << fr
                    if m.sufq.isEmpty():
                        if m.morpho == "-") _morphos.append(m.grq:
                        else _morphos.append(m.grq + " " + m.morpho)

                    else:
                        if m.morpho == "-") _morphos.append(m.grq + " + " + m.sufq:
                        else _morphos.append(m.grq + " + " + m.sufq + " " + m.morpho)
                        enclitique = m.sufq

                    while (lt.size() > 2)
                        t = lt.mid(0,3)
                        lt = lt.mid(4)
                        fr = nb * _lemmatiseur.fraction(t)
                        _probas[t] += fr



        if Ch.abrev.contains(forme):
            # C'est un nom à n'importe quel cas !
            _probas.clear()
            pseudo = "n%1"
            for (i = 1; i < 7; i++) _probas[pseudo.arg(i)+"1"] = _lemmatiseur.tagOcc(pseudo.arg(i)+"1")

        # J'ai construit les listes de lemmes, morphos, et nombres d'occurrences.
        # J'ai aussi une QMap qui associe les tags aux probas, je dois normaliser.
        total = 0
        for t in _probas.keys(): total += _probas[t]
        if total == 0:
            total = 1
            #qDebug() << forme << " : toutes les probas sont nulles not "

        _maxProb = ""
        prMax = -1
        for t in _probas.keys():
            _bestOf[t] = 0.; # Je prépare une liste des tags
#            qDebug() << t << _probas[t]
            pr = _probas[t] * 1024 /total
            if prMax < pr:
                prMax = pr
                _maxProb = t

            if (pr == 0) pr++
            _probas[t] = pr


        if ((enclitique == "quĕ") or (enclitique == "vĕ")) _tagEncl = "ce "
        elif (enclitique == "nĕ") _tagEncl = "de "
        elif (enclitique == "st") _tagEncl = "v11"
        if forme.endsWith("cum"):
            encl = (forme == "mecum") or (forme == "tecum") or (forme == "secum")
            encl = encl or (forme == "nobiscum") or (forme == "vobiscum") or (forme == "quibuscum")
            encl = encl or (forme == "quacum") or (forme == "quocum") or (forme == "quicum")
            if encl:
#                qDebug() << forme << " avec enclitique"
                _tagEncl = "re "
                if _tags.isEmpty():
                    _tags.append("p61")
                    _probas.insert("p61",1024)
                    _lemmes.append(forme)
                    _morphos.append("...")
                    _nbOcc.append(1)

                elif _probas.size() == 1:
                    if not _probas.keys().contains("p61"):
                        _tags[0]="p61"
                        _probas.clear()
                        _probas.insert("p61",1024)


                else qDebug() << "Erreur sur " << forme << " : " << _tags



#    qDebug() << forme


def choisir(self, t, tout):
    choix = ""
    valeur = -1
    for (int i=0; i < _tags.size(); i++)
        if (_tags[i].contains(t)) and (valeur < _nbOcc[i]):
            # _tags peut être une liste de tags, que t est un tag.
            choix = _lemmes[i] + " — " + _morphos[i]
            valeur = _nbOcc[i]

    if not choix.isEmpty():
        choix.prepend("<br/>—&gt;&nbsp;<span style='color:black'>")
        choix.append("</span>\n")

    if tout or choix.isEmpty():
        choix.append("<span style='color:#777777'><ul>")
        for (int i=0; i < _tags.size(); i++)
            format = "%1 : %2 ; "
            lg = "<li>" + _lemmes[i] + " — " + _morphos[i] + " ("
            lt = _tags[i]
#            qDebug() << lg << lt
            while (lt.size() > 2)
                t = lt.mid(0,3)
                lt = lt.mid(4)
                lg.append(format.arg(t).arg(_bestOf[t]))

            lg.chop(3)
            lg.append(")</li>\n")
            choix.append(lg)

        choix.append("</ul></span>\n")

    QString ajout
    if (t == _maxProb) ajout = t
    ajout = t + " (" + _maxProb + ")"
    choix.prepend("<li><strong>" + _forme + "</strong> " + ajout)
    choix.append("</li>")
    return choix


def tagEncl(self):
    return _tagEncl


def inconnu(self):
    return _tags.isEmpty()


def tags(self):
    ret = _probas.keys()
    return ret


def proba(self, t):
    if _probas.contains(t):
        return _probas[t]
    return 0


def forme(self):
    return _forme


def setBestOf(self, t, pr):
#    qDebug() << t << pr
    if _bestOf.keys().contains(t):
        if (pr > _bestOf[t]) _bestOf[t] = pr

    else qDebug() << t << pr
        # _bestOf[t] = pr

