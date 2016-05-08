/*                 syntaxe.cpp * *  This file is part of COLLATINUS.  *
 * *  COLLATINUS is free software; you can redistribute it and/or modify *  it
 * under the terms of the GNU General Public License as published by *  the Free
 * Software Foundation; either version 2 of the License, or *  (at your option)
 * any later version.
 *
 *  COLLATINVS is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
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
 * \file syntaxe.cpp
 * \brief module d'analyse syntaxique
 */


#include "syntaxe.h"
#include <QFile>
#include <QRegExp>
#include "flexion.h"

//////////////////////////////
//   Classe ElS             //
//   (Element de Syntaxe    //
//////////////////////////////

/**
 * \fn ElS::ElS(QString lin, RegleS *parent)
 * \brief La classe ElS enregistre les éléments requis
 * des deux mots (super et sub) d'un lien syntaxique
 * Il est donc utilisé deux fois par la classe RegleS.
 * Son créateur s'appuie sur une ligne du fichier
 * bin/data/syntaxe.la.
 */
ElS::ElS(QString lin, RegleS *parent)
{
    _regle = parent;
    QStringList ecl = lin.split(':', QString::KeepEmptyParts);
    _lemmes = ecl.at(1).split(',', QString::SkipEmptyParts);
    _pos = ecl.at(2).split(',', QString::SkipEmptyParts);
    _morphos = ecl.at(3).split(' ', QString::SkipEmptyParts);
}

bool ElS::okLem(QString lem)
{
    return _lemmes.isEmpty() || _lemmes.contains(lem);
}

bool ElS::okMorpho(QString m)
{
    if (_morphos.isEmpty()) return true;
    QStringList lm = m.split(' ');
    foreach (QString em, _morphos)
    {
        bool ok = false;
        foreach (QString elm, lm)
        {
            if (elm.startsWith(em)) ok = true;
        }
        if (!ok) return false;
    }
    return true;
}

bool ElS::okPos(QString p) { return _pos.isEmpty() || _pos.contains(p); }

QStringList ElS::pos() { return _pos; }


//////////////////////////////
//   Classe RegleS          //
//   (Règle Syntaxique)     //
//////////////////////////////

RegleS::RegleS(QStringList lignes, QObject *parent)
{
    syntaxe = qobject_cast<Syntaxe*>(parent);
    QStringList cles = QStringList() << "id"      // 0
                                     << "doc"     // 1  
                                     << "pere"    // 2
                                     << "super"   // 3
                                     << "sub"     // 4
                                     << "sens"    // 5
                                     << "accord"  // 6
                                     << "tr"      // 7
                                     << "f"       // 8
                                     << "synt";   // 9
    foreach (QString lin, lignes)
    {
        QStringList ecl = lin.split(':');
        int i = cles.indexOf(ecl.at(0));
        switch (i)
        {
            case 0:
                _id = ecl.at(1);
                break;
            case 1:
                _doc = ecl.at(1);
                break;
            case 2:
                {
                    _idPere = ecl.at(1);
                    RegleS *rp = syntaxe->regle(_idPere);
                    if (rp != NULL)
                    {
                        _sens   = rp->sens();
                        _accord = rp->accord();
                        _f      = rp->f();
                        _synt   = rp->synt();
                    }
                }
                break;
            case 3:
                _super = new ElS(lin, this);
                break;
            case 4:
                _sub = new ElS(lin, this);
                break;
            case 5:
                _sens = ecl.at(1);
                break;
            case 6:
                _accord = ecl.at(1);
                break;
            case 7:
                _tr = ecl.at(1);
                break;
            case 8:
                _f = ecl.at(1);
                break;
            case 9:
                _synt = ecl.at(1);
                break;
            default:
                break;
        }
    }
}

QString RegleS::accord()
{
    return _accord;
}

bool RegleS::bloquant()
{
    return _synt.contains('b');
}

QString RegleS::doc()
{
    return _doc;
}

QString RegleS::id()
{
    return _id;
}

bool RegleS::estSub(Lemme *l, QString morpho, bool ante)
{
    // sens
    if (ante && _sens == ">") return false;
    // lemme
    if (!_sub->okLem(l->gr())) return false;
    // pos
    if (!_sub->okPos(l->pos())) return false;
    // morpho
    if (!_sub->okMorpho(morpho)) return false;
    return true;
}

bool RegleS::estSuper(Lemme *l, QString morpho)
{
    // lemme
    if (!_super->okLem(l->gr())) return false;
    // pos
    if (!_super->okPos(l->pos())) return false;
    // morpho
    if (!_super->okMorpho(morpho)) return false;
    return true;
}

QString RegleS::f()
{
    return _f;
}

QString RegleS::fonction(Mot *super, Mot *sub)
{
    QString ret = _f;
    if (super != NULL) ret.replace("<super>", "<em>" + super->gr() + "</em>");
    if (sub != NULL) ret.replace("<sub>", "<em>" + sub->gr() + "</em>");
    return ret;
}

QString RegleS::idPere()
{
    return _idPere;
}

QString RegleS::sens()
{
    return _sens;
}

ElS* RegleS::sub()
{
    return _sub;
}

ElS* RegleS::super()
{
    return _super;
}

QString RegleS::synt()
{
    return _synt;
}

QString RegleS::tr()
{
    return _tr;
}

//////////////////////////////////
//   Classe Super               //
//  (superordonné d'une règle)  //
//////////////////////////////////

Super::Super(RegleS *r, Lemme *l, QString m, Mot *parent)
{
    _regle = r;
    _lemme = l;
    _morpho = m;
    _mot = parent;
    _motSub = NULL;
    _traduction = "<em>non traduit</em>";
}

void Super::addSub(Mot *m, Lemme *l, SLem sl)
{
    _motSub = m;
    _lemmeSub = l;
    _slemSub = sl;
}

bool Super::estSub(Lemme *l, QString morpho, bool ante)
{
    if (!_regle->estSub(l, morpho, ante))
    {
        return false;
    }
    if (_motSub != NULL && _regle->synt().contains('u'))
    {
        return false;
    }
    return true;
}

Lemme *Super::lemme()
{
    return _lemme;
}

Lemme *Super::lemmeSub()
{
    return _lemmeSub;
}

QString Super::morpho()
{
    return _morpho;
}

Mot *Super::mot()
{
    return _mot;
}

Mot *Super::motSub()
{
    return _motSub;
}

RegleS *Super::regle()
{
    return _regle;
}

void Super::setTraduction(QString t)
{
    _traduction = t;
}

SLem Super::slemSub()
{
    return _slemSub;
}

QString Super::traduction() { return _traduction; }

/**
 * \fn Mot::Mot(QString g)
 * \brief Créateur de la classe Mot.
 */
Mot::Mot(QString g)
{
    _gr = g;
    _affLiens.clear();
    _ponctD = '\0';
    _ponctG = '\0';
    _vu = false;
}

void Mot::addLien(QString l)
{
    if (!_affLiens.contains(l)) _affLiens.append(l);
}

void Mot::addRSub(RegleS *r) { _rSub.append(r); }

void Mot::addSuper(RegleS *r, Lemme *l, QString m)
{
    _super.append(new Super(r, l, m, this));
}

void Mot::delSuper(Super *s)
{
    _super.removeOne(s);
    delete s;
}

QString Mot::gr() { return _gr; }

void Mot::grCalc()
{
    foreach (Super *s, _super)
    {
        if (s->motSub() == NULL) continue;
        if (s->motSub()->terminal())
        {
            if (s->motSub()->rang() < _grPrim) _grPrim = s->motSub()->rang();
            if (s->motSub()->rang() > _grUlt) _grUlt = s->motSub()->rang();
        }
        else
        {
            s->motSub()->grCalc();
            int grp = s->motSub()->grPrim();
            if (grp < _grPrim) _grPrim = grp;
            int gru = s->motSub()->grUlt();
            if (gru > _grUlt) _grUlt = gru;
        }
    }
}

int Mot::grPrim() { return _grPrim; }

int Mot::grUlt() { return _grUlt; }

QString Mot::humain()
{
    QString ret;
    QTextStream fl(&ret);
    fl << _gr << "\n";
    foreach (Lemme *lem, _morphos.keys())
        fl << lem->grq() << "    - " << lem->traduction("fr") << "\n";
    return ret;
}

QString Mot::liens() { return _affLiens.join("<br/>"); }

MapLem Mot::morphos() { return _morphos; }

bool Mot::orphelin()
{
    foreach (Super *s, _super)
        if (s->motSub() != NULL) return false;
    return true;
}

QString Mot::ponctD()
{
    return _ponctD;
}

int Mot::rang()
{
    return _rang;
}

QString Mot::ponctG() { return _ponctG; }

void Mot::setMorphos(MapLem m) { _morphos = m; }

void Mot::setPonctD(QString p) { _ponctD = p; }

void Mot::setRang(int r)
{
    _rang = r;
    _grPrim = r;
    _grUlt = r;
}

void Mot::setPonctG(QString p) { _ponctG = p; }
QList<Super *> Mot::super() { return _super; }
bool Mot::superDe(Mot *m)
{
    foreach (Super *s, _super)
        if (s->motSub() == m) return true;
    return false;
}

void Mot::setVu()
{
    _vu = true;
}

bool Mot::terminal()
{
    foreach (Super *s, _super)
        if (s->motSub() != NULL) return false;
    return true;
}

bool Mot::vu()
{
    return _vu;
}

Syntaxe::Syntaxe(QString t, Lemmat *parent)
{
    _lemmatiseur = parent;
    setText(t);
    // lecture des données
    QFile fs(qApp->applicationDirPath() + "/data/syntaxe.la");
    fs.open(QFile::ReadOnly);
    QTextStream fls(&fs);
    QStringList slr;  // liste des lignes de la dernière règle lue
    while (!fls.atEnd())
    {
        QString l = fls.readLine().simplified();
        if ((l.isEmpty() && !fls.atEnd()) || l.startsWith("!")) continue;
        QStringList eclats = l.split(":");
        if ((eclats.at(0) == "id" || fls.atEnd()) && !slr.empty())
        {
            RegleS *nrs = new RegleS(slr, this);
            //if (!nrs->idPere().isEmpty())
             //   RegleS *reglePere = regle(nrs->idPere());
            _regles.insert(nrs->id(), nrs);
            slr.clear();
        }
        slr.append(l);
    }
    fs.close();
    _pronom = new Pronom();
}

bool Syntaxe::accord(QString ma, QString mb, QString cgn)
{
    if (cgn.isEmpty()) return true;
    if (cgn.contains('c'))
    {
        foreach (QString k, Flexion::cas)
            if (ma.contains(k) && !mb.contains(k)) return false;
    }
    if (cgn.contains('g'))
    {
        // si ma ou mb n'a pas de genre, renvoyer true
        bool nonG = true;
        foreach (QString g, Flexion::genres)
            nonG = nonG || ma.contains(g);
        if (nonG) return true;
        nonG = true;
        foreach (QString g, Flexion::genres)
            nonG = nonG || mb.contains(g);
        if (nonG) return true;
        // sinon, vérifier l'accord
        foreach (QString g, Flexion::genres)
            if (ma.contains(g) && !mb.contains(g)) return false;
    }
    if (cgn.contains('n'))
    {
        foreach (QString n, Flexion::nombres)
            if (ma.contains(n) && !mb.contains(n)) return false;
    }
    return true;
}

/**
 * \fn QString Syntaxe::analyse (QString t, int p)
 * \brief Analyse de la phrase courante à la position p
 *        du texte t.
 */
QString Syntaxe::analyse(QString t, int p)
{
    // effacer l'analyse précédentre
    _mots.clear();
    if (t.length() == 0) return "";
    // initialisations
    const QList<QChar> chl;
    const int tl = t.length() - 1;
    const QString pp = ".;!?";
    // supprimer les non-alpha de tête
    // régression au début de la phrase
    int dph = p;
    while (dph > 0 && t.count() > dph && !pp.contains(t.at(dph))) --dph;
    // calcul de la position du mot courant
    QString ante = t.mid(dph, p - dph);
    while (ante.count() > 0 && !ante.at(0).isLetter()) ante.remove(0, 1);
    QStringList lante = ante.split(QRegExp("\\W+"));
    int pmc = lante.count() - 1;  // pmc = position du mot courant.
    // progression jusqu'en fin de phrase
    int fph = p;
    while (fph < tl && !pp.contains(t.at(fph))) ++fph;
    // construction des mots
    QString phr = t.mid(dph, fph - dph);
    QStringList lm = phr.split(QRegExp("\\b"));
    for (int i = 1; i < lm.count() - 1; i += 2)
    {
        QString m = lm.at(i);
        Mot *nm = new Mot(m);
        nm->setMorphos(_lemmatiseur->lemmatiseM(m, true));
        QString pprec = lm.at(i - 1);
        pprec.remove(QRegExp("\\s"));
        nm->setPonctG(pprec);
        QString psuiv = lm.at(i + 1);
        psuiv.remove(QRegExp("\\s"));
        nm->setPonctD(psuiv);
        // Peuplement de la liste _super
        // pour chaque règle syntaxique
        foreach (RegleS *r, _regles)
        {
            // pour chaque lemme de motCour
            foreach (Lemme *l, nm->morphos().keys())
            {
                // pour chaque morpho du lemme
                QList<SLem> lsl = nm->morphos().value(l);
                foreach (SLem sl, lsl)
                {
                    QString msup = sl.morpho;
                    if (r->estSuper(l, msup))
                    {
                        nm->addSuper(r, l, msup);
                    }
                }
            }
        }
        _mots.append(nm);
        nm->setRang(_mots.count());
    }
    int nbmots = _mots.count();
    r = 0;
    while (r < nbmots && r > -1)
        r = groupe(r);
    if (_mots.count() > pmc)
        return _mots.at(pmc)->liens();
    else return "";
}

/*
QString Syntaxe::analyseM(QString t, int p)
{
    const QList<QChar> chl;
    const int tl = t.length() - 1;
    const QString pp = ".;!?";
    // Les listes _motsP et _motsS sont ordonnées suivant leur
    // proximité de motCourant. La liste _motsP est donc ordonné
    // de manière régressive par rapport au sens de lecture G->D.

    // avancer jusqu'à la fin du mot sous le curseur
    while (p < tl - 1 && t.at(p + 1).isLetter()) ++p;
    QString m;
    QChar ponctD = '\0';
    QChar ponctG = '\0';
    // mots à gauche de motCour
    int i = p;
    bool limite = false;
    while (i > -1 && !limite)
    {
        QChar c = t.at(i);
        if (c.isLetter()) m.prepend(c);
        if ((!c.isLetter() || i == 0) && !m.isEmpty())
        {
            Mot *nm = new Mot(m);
            nm->setMorphos(_lemmatiseur->lemmatiseM(m, true));
            _motsP << nm;
            m.clear();
            nm->setPonctG(ponctG);
            nm->setPonctD(ponctD);
            ponctG = ponctD;
            ponctD = '\0';
        }
        limite =
            (pp.contains(c) || (i > 0 && c == '\n' && t.at(i - 1) == '\n'));
        if (!limite && c.isPunct()) ponctD = c;
        --i;
    }

    // le premier mot de la liste est le mot Courant.
    _motCour = _motsP.takeFirst();

    // Peuplement de la liste _super
    // pour chaque règle syntaxique
    foreach (RegleS *r, _regles)
    {
        // pour chaque lemme de motCour
        foreach (Lemme *l, _motCour->morphos().keys())
        {
            // pour chaque morpho du lemme
            QList<SLem> lsl = _motCour->morphos().value(l);
            foreach (SLem sl, lsl)
            {
                QString msup = sl.morpho;
                if (r->estSuper(l, msup)) _motCour->addSuper(r, l, msup);
            }
        }
    }
    limite = false;
    i = p + 1;
    while (i < tl && !limite)
    {
        QChar c = t.at(i);
        if (c.isLetter())
            m.append(c);
        else if (!m.isEmpty())
        {
            Mot *nm = new Mot(m);
            nm->setMorphos(_lemmatiseur->lemmatiseM(m));
            _motsS << nm;
            m.clear();
            nm->setPonctD(ponctG);
            nm->setPonctG(ponctD);
            ponctD = ponctG;
            ponctG = '\0';
        }
        limite = (pp.contains(c) ||
                  (i < tl - 1 && c == '\n' && t.at(i + 1) == '\n'));
        if (!limite && c.isPunct()) ponctG = c;
        ++i;
    }
    // RECHERCHE DES LIENS
    QStringList ret;
    // divs à griser après la sortie du groupe ou l'entrée dans un sous-groupe
    QString divP = "<div>";
    QString divS = "<div>";
    bool courSubP = false;  // _motCour n'est pas encore sub à gauche
    bool courSubS = false;  // _motCour n'est pas encore sub à droite
    // pour chaque mot précédent
    for (int i = 0; (i < _motsP.count() || i < _motsS.count()); ++i)
    {
        if (i < _motsP.count())
        {
            bool estLie = false;
            Mot *mp = _motsP.at(i);
            // provisoire : une ponctuation rend le
            // lien improbable.
            if (mp->ponctD() != '\0') divP = "<div style=\"color:grey\">";
            // si _motCour a un père, il ne peux pas avoir de sub plus loin.
            // On brise donc la boucle.
            if (courSubP) break;
            // mp est-іl subordonné à _motCour ?
            // pour chaque Super de _motCour
            foreach (Super *sup, _motCour->super())
            {
                // pour chaque lemme de mp
                foreach (Lemme *l, mp->morphos().keys())
                {
                    // pour chaque morpho du lemme
                    QList<SLem> lsl = mp->morphos().value(l);
                    foreach (SLem sl, lsl)
                    {
                        if (sup->estSub(l, sl.morpho, true) &&
                            (accord(sup->morpho(), sl.morpho,
                                    sup->regle()->accord()))
                            // contiguïté sans virgule
                            && (!(sup->regle()->synt().contains('c') &&
                                  virgule(_motCour, mp))))
                        {
                            QString lin;
                            QTextStream(&lin)
                                << divP << sup->regle()->fonction(_motCour, mp)
                                << "<br/>    " << sup->regle()->doc()
                                << "<br/>    <em>"
                                << tr(sup->regle(), sup->lemme(), sup->morpho(),
                                      l, sl.morpho)
                                << "</em></div>";
                            ret << lin;
                            estLie = true;
                        }
                    }
                }
            }
            // _motCour est-il subordonné à mp ?
            // pour chaque Super de _mp
            foreach (Super *sup, mp->super())
            {
                // pour chaque lemme de _motCour
                foreach (Lemme *l, _motCour->morphos().keys())
                {
                    // pour chaque morpho du lemme
                    QList<SLem> lsl = _motCour->morphos().value(l);
                    foreach (SLem sl, lsl)
                    {
                        if (sup->estSub(l, sl.morpho, true) &&
                            (accord(sup->morpho(), sl.morpho,
                                    sup->regle()->accord())))
                        {
                            QString lin;
                            QTextStream(&lin)
                                << divP << sup->regle()->fonction(_motCour, mp)
                                << "<br/>    " << sup->regle()->doc()
                                << "<br/>    <em>"
                                << tr(sup->regle(), sup->lemme(), sup->morpho(),
                                      l, sl.morpho)
                                << "</em></div>";
                            ret << lin;
                            courSubP = true;
                        }
                    }
                }
            }
            if (!estLie) divP = "<div style=\"color:grey\">";
        }
        // motCour est-il subordonné à mp ?
        // pour chaque mot suivant
        if (i < _motsS.count())
        {
            bool estLie = false;
            Mot *ms = _motsS.at(i);
            // si _motCour a un père, il ne peux pas avoir de sub plus loin.
            // On brise donc la boucle.
            if (courSubS) break;
            // mp est-іl subordonné à _motCour ?
            // pour chaque Super de _motCour
            foreach (Super *sup, _motCour->super())
            {
                // pour chaque lemme de mp
                foreach (Lemme *l, ms->morphos().keys())
                {
                    // pour chaque morpho du lemme
                    QList<SLem> lsl = ms->morphos().value(l);
                    foreach (SLem sl, lsl)
                    {
                        if (sup->estSub(l, sl.morpho, false) &&
                            (accord(sup->morpho(), sl.morpho,
                                    sup->regle()->accord())))
                        {
                            QString lin;
                            QTextStream(&lin)
                                << divS << sup->regle()->fonction(_motCour, ms)
                                << "<br/>    " << sup->regle()->doc()
                                << "<br/>    <em>"
                                << tr(sup->regle(), sup->lemme(), sup->morpho(),
                                      l, sl.morpho)
                                << "</em>";
                            ret << lin;
                            estLie = true;
                        }
                    }
                }
            }
            if (!estLie) divS = "<div style=\"color:grey\">";
            // _motCour est-іl subordonné à mp
            // pour chaque Super de _ms
            foreach (Super *sup, ms->super())
            {
                // pour chaque lemme de _motCour
                foreach (Lemme *l, _motCour->morphos().keys())
                {
                    // pour chaque morpho du lemme
                    QList<SLem> lsl = _motCour->morphos().value(l);
                    foreach (SLem sl, lsl)
                    {
                        if (sup->estSub(l, sl.morpho, false) &&
                            (accord(sup->morpho(), sl.morpho,
                                    sup->regle()->accord())))
                        {
                            QString lin;
                            QTextStream(&lin)
                                << divS << sup->regle()->fonction(_motCour, ms)
                                << "<br/>    " << sup->regle()->doc()
                                << "<br/>    <em>"
                                << tr(sup->regle(), sup->lemme(), sup->morpho(),
                                      l, sl.morpho)
                                << "</em>";
                            ret << lin;
                            courSubS = true;
                        }
                    }
                }
            }
        }
    }
    ret.removeDuplicates();
    return ret.join("<hr/>");
}
*/

bool Syntaxe::estSuper(Mot *sup, Mot *sub)
{
    foreach (Super *s, sup->super())
        if (s->motSub() == sub) return true;
    return false;
}

/**
 * \fn int Syntaxe::groupe()
 * \brief renvoie le rang du père de mot[r]
 */
int Syntaxe::groupe(int r)
{
    Mot *cour = _mots.at(r);
    // éviter les passages inutiles
    if (cour->vu()) return ++r;
    int x = 1;
    while (r + x < _mots.count())
    {
        Mot *mTest = _mots.at(r + x);
        // si cour orphelin, tester mTest comme super de cour
        if (cour->orphelin() && (super(mTest, cour)))
            return r + x;
        if (super(cour, mTest))
            x = groupe(r+x)-r+1;
        else break;
    }
    cour->setVu();
    return ++r;
}

QString Syntaxe::motSous(int p)
{
    QString mot;
    // chercher la limite de mot vers la droite
    while (p < _texte.length() && _texte.at(p).isLetter()) ++p;
    // remonter d'un caractère
    --p;
    while (p > 0 && _texte.at(p).isLetter())
    {
        mot.prepend(_texte.at(p));
        --p;
    }
    return mot;
}

bool Syntaxe::orphelin(Mot *m)
{
    for (int i = 0; i < m->rang(); ++i)
        if (estSuper(_mots.at(i), m)) return false;
    return true;
}

RegleS* Syntaxe::regle(QString id)
{
    return _regles.value(id);
}

void Syntaxe::setText(QString t) { _texte = t; }

bool Syntaxe::super(Mot *sup, Mot *sub)
{
    bool retour = false;
    foreach (Super *s, sup->super())
    {
        // tester toutes les possibilités du mot sub :
        // pour chaque lemme du mot sub
        foreach (Lemme *l, sub->morphos().keys())
        {
            // pour chaque morpho du lemme
            QList<SLem> lsl = sub->morphos().value(l);
            foreach (SLem sl, lsl)
            {
                if (s->estSub(l, sl.morpho, false) &&
                    (accord(s->morpho(), sl.morpho, s->regle()->accord())) &&
                    (!(s->regle()->synt().contains('c') && virgule(sup, sub))))
                {
                    /*
                    // si une règle fille est validée, supprimer la règle mère.
                    foreach (Super *sm, sup->super())
                    {
                        if (sm->motSub() != NULL && s->regle()->idPere() == sm->regle()->id())
                        {
                            sup->delSuper(sm);
                        }
                    }
                    */
                    s->addSub(sub, l, sl);
                }
            }
        }
        retour = retour || (s->motSub() == sub);
        //if (s->motSub() == sub) return true;
    }
    // ajouter les chaînes d'affichage (règle, lien, traduction)
    foreach (Super *s, sup->super())
    {
        if (s->motSub() == NULL) continue;
        QString lien = s->regle()->fonction(sup, sub);
        QString trad =
            tr(s->regle(), s->lemme(), s->morpho(), s->lemmeSub(), s->slemSub().morpho);
        QTextStream ts(&lien);
        ts << " tr. <em>" << trad << "</em>";
        sup->addLien(lien);
        sub->addLien(lien);
    }
    return retour;
    //return false;
}

QString Syntaxe::tr(RegleS *r, Lemme *sup, QString msup, Lemme *sub,
                    QString msub)
{
    QString t = r->tr();
    QString trsup = trLemme(sup, msup);
    QString trsub = trLemme(sub, msub);
    t.replace("<super>", trsup);
    t.replace("<sub>", trsub);
    return t;
}

QString Syntaxe::trLemme(Lemme *l, QString m)
{
    QStringList ret;
    QStringList ltr = l->traduction("fr").split(QRegExp("[;,]"));
    foreach (QString tr, ltr)
    {
        // supprimer les parenthèses dans la ligne de bin/data/lemmes.fr
        tr.remove(QRegExp("[(\\[][^)^\\]]*[)\\]]"));
        QString pos = l->pos();
        if (pos.contains('a')) ret << accorde(tr, m);
        if (pos.contains('n'))
        {
            if (m.contains("plur"))
                ret << pluriel(tr, m);
            else
                ret << tr;
        }
        if (pos.contains('p')) ret << _pronom->accorde(tr, m);
        if (pos.contains('v')) ret << conjnat(tr, m);
        if (ret.empty()) ret << tr;
        /*
        switch (l->pos().unicode())
        {
            // TODO : l'adjectif français doit avoir la
            // morpho de son super !
            case 'a': ret << accorde(tr, m); break;
            case 'n':
                      {
                          if (m.contains("plur"))
                              ret << pluriel(tr, m);
                          else ret << tr;
                          break;
                      }
            case 'p': ret << _pronom->accorde(tr,m);break;
            case 'v': ret << conjnat(tr, m); break;
            default: ret << tr;
        }
        */
    }
    ret.removeDuplicates();
    return ret.join(", ");
}

bool Syntaxe::virgule(Mot *ma, Mot *mb)
{
    int ecart = ma->rang() - mb->rang();
    if (abs(ecart) > 1) return false;
    if ((ecart < 0) && !ma->ponctD().isEmpty()) return true;
    if ((ecart > 0) && !ma->ponctG().isEmpty()) return true;
    return false;
}
