/*                 syntaxe.cpp
 * This file is part of COLLATINUS.  *
 * COLLATINUS is free software; you can redistribute it and/or modify *  it
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

// XXX vérifier que suam a bien les deux morphos pronom
// et adjectif et qu'elles sont soumises à la recherche
// de liens.

// XXX ajouter le genre des noms dans leur analyse morpho
//     Si le nom a deux genres, deux analyses par cas+nombre

#include "syntaxe.h"
#include <QFile>
#include <QMap>
#include <QRegExp>
#include <QStringList>
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
    if (ecl.at(1) == "g")
        _idSub = ecl.at(2);
    else
    {
        _idSub.clear();
        _lemmes = ecl.at(1).split(',', QString::SkipEmptyParts);
        _pos = ecl.at(2).split(',', QString::SkipEmptyParts);
        _morphos = ecl.at(3).split(' ', QString::SkipEmptyParts);
    }
}

QString ElS::idSub()
{
    return _idSub;
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

bool ElS::okPos(QString p)
{
    if (_pos.empty()) return true;
    bool ret = false;
    foreach (QString ep, _pos)
        ret = ret || p.contains(ep);
    return ret;
}

QStringList ElS::pos()
{
    return _pos;
}


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
            case 0: // id
                _id = ecl.at(1);
                break;
            case 1: // doc
                _doc = ecl.at(1);
                break;
            case 2: // pere
                {
                    _idPere = ecl.at(1);
                    RegleS *rp = syntaxe->regle(_idPere);
                    if (rp != NULL)
                    {
                        _sens   = rp->sens();
                        _accord = rp->accord();
                        _f      = rp->f();
                        _synt   = rp->synt();
                        _tr     = rp->tr();
                        // sub et super non clonés !
                    }
                }
                break;
            case 3:  // super
                _super = new ElS(lin, this);
                break;
            case 4:  // sub
                _sub = new ElS(lin, this);
                break;
            case 5:  // sens
                _sens = ecl.at(1);
                break;
            case 6:  // accord
                _accord = ecl.at(1);
                break;
            case 7:  // traduction
                _tr = ecl.at(1);
                break;
            case 8:  // fonction
                _f = ecl.at(1);
                break;
            case 9:  // divers élément syntaxiques
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

QString RegleS::idSub()
{
    return _sub->idSub();
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

/**
 * \fn bool RegleS::multiple()
 * \brief vrai si le superordonné accepte plusieurs
 *     subordonnés via la même règle.
 */
bool RegleS::multiple()
{
    return !_synt.contains('u');
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
    if (_motSub != NULL) return;
    _motSub = m;
    _lemmeSub = l;
    _slemSub = sl;
}

void Super::annule()
{
    // libérer l'attribut clos() ?
    _motSub = NULL;
}

bool Super::bloquant()
{
    return _regle->bloquant();
}

bool Super::complet()
{
    return _motSub != NULL;
}

Super* Super::copie()
{
    return new Super(_regle, _lemme, _morpho, _mot);
}

/**
 * \fn bool Super::estSub(Lemme *l, QString morpho, bool ante)
 * \brief renvoie vrai si le lemme l de morphno morpho et ante = true si
 *        le mot sub est placé avant _mot, peut être subordonné à _mot
 *        via la règle _regle.
 */
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

QString Super::fonction()
{
    return _regle->fonction(_mot, _motSub);
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

QString Super::traduction()
{
    return _traduction;
}

/**
 * \fn Mot::Mot(QString g)
 * \brief Créateur de la classe Mot.
 */
Mot::Mot(QString g, QObject *parent)
{
    if (parent != 0)
        syntaxe = qobject_cast<Syntaxe*>(parent);
    _gr = g;
    _ponctD = '\0';
    _ponctG = '\0';
    _clos = false;
    _vu = false;
}

void Mot::addRSub(RegleS *r)
{
    _rSub.append(r);
}

void Mot::addSuper(RegleS *r, Lemme *l, QString m)
{
    _super.append(new Super(r, l, m, this));
}

void Mot::addSuper(Super *s)
{
    _super.append(s);
}

bool Mot::clos()
{
    return _clos;
}

QString Mot::gr()
{
    return _gr;
}

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

MapLem Mot::morphos()
{
    return _morphos;
}

bool Mot::orphelin()
{
    return syntaxe->orphelin(this);
}

/**
 * \fn bool Mot::perePar(QString idsub)
 * \brief renvoie vrai si le mot possède un sub via la règle d'id idsub.
 */
bool Mot::perePar(QString idsub)
{
    foreach (Super *s, _super)
        if (s->complet() && s->regle()->id() == idsub)
            return true;
    return false;
}

QString Mot::ponctD()
{
    return _ponctD;
}

QString Mot::ponctG()
{
    return _ponctG;
}

int Mot::rang()
{
    return _rang;
}

void Mot::setClos()
{
    _clos = true;
}

void Mot::setMorphos(MapLem m)
{
    _morphos = m;
}

void Mot::setPonctD(QString p)
{
    _ponctD = p;
}

void Mot::setRang(int r)
{
    _rang = r;
    _grPrim = r;
    _grUlt = r;
}

void Mot::setPonctG(QString p)
{
    _ponctG = p;
}

QList<Super *> Mot::super()
{
    return _super;
}

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
        nm->setRang(_mots.count()-1);
    }
    _nbmots = _mots.count();
    r = 0;
    while (r < _nbmots)
        r = groupe(r);
    if (_mots.count() > pmc)
        return liens(_mots.at(pmc)); 
    else return "";
}

QString Syntaxe::liens(Mot *m)
{
    QMap<QString,QString> mmf;
    // superordonné
    for (int i=0;i<_mots.count();++i)
    {
        if (i==m->rang()) continue;
        Mot *sup = _mots.at(i);
        foreach(Super *s, sup->super())
        {
            if (!s->complet()) continue;
            QString ligne;
            QTextStream ts(&ligne);
            if (s->motSub() == m)
            {
                 ts << " <li style=\"color:blue;font-style:italic;\">" 
                    << tr(s->regle(), s->lemme(),
                          s->morpho(), s->lemmeSub(),
                          s->slemSub().morpho)
                    << "</li>";
                mmf.insert(s->fonction(), ligne);
            }
        }
    }
    // subordonnés
    foreach(Super *s, m->super())
    {
        if (!s->complet()) continue;
        QString ligne;
        QTextStream ts(&ligne);
        ts << " <li style=\"color:blue;font-style:italic;\">" 
            << tr(s->regle(), s->lemme(),
                  s->morpho(), s->lemmeSub(),
                  s->slemSub().morpho)
            << "</li>";
        mmf.insert(s->fonction(), ligne);
    }
    QStringList ret;
    foreach(QString f, mmf.keys())
    {
        ret.append(f);
        ret.append("<ul>");
        QStringList lt = mmf.values(f);
        lt.removeDuplicates();
        ret.append (lt.join(""));
        ret.append("</ul>");
    }
    return ret.join("");
}

QStringList Syntaxe::liensPF(int p, int f)
{
    /*
    QStringList ret;
    QString l;
    QTextStream(&l) << "liens pour "<<f<<" subordonné à "<<p;
    ret.append (l);
    return ret;
    */
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
}

bool Syntaxe::estSuper(Mot *sup, Mot *sub)
{
    foreach (Super *s, sup->super())
        if (s->motSub() == sub) return true;
    return false;
}

/**
 * \fn int Syntaxe::groupe()
 * \brief renvoie le rang du père de mot[r],
 */
int Syntaxe::groupe(int r)
{
    // Forte potantibus his apud Sextum ...
    // incidit de uxoribus mentio
    Mot *cour = _mots.at(r);
    // éviter les passages inutiles
    if (cour->vu()) 
    {
        return cour->grUlt()+1;
    }
    int x = 1;
    while (r + x < _nbmots)
    {
        Mot *mTest = _mots.at(r + x);
        if (orphelin(cour) && (super(mTest, cour)))
        {
            return r + x;
        }
        if (super(cour, mTest))
        {
            x = groupe(r+x)-r;
            if ((r+x < _nbmots-1) && _mots.at(r+x)->clos()) ++x;
        }
        else
        {
            x = groupe(r+x);
        }
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

void Syntaxe::selectionne(Mot *m, Super *s)
{
    for (int i=0;i<m->rang();++i)
    {
        Mot *mprec = _mots.at(i);
        foreach(Super *sprec, mprec->super())
            if (sprec->motSub()==m && sprec != s)
            {
                sprec->annule();
            }
    }
}

void Syntaxe::setText(QString t)
{
    _texte = t;
}

bool Syntaxe::super(Mot *sup, Mot *sub)
{
    if (sub->clos()) return false;
    bool retour = false;
    foreach (Super *s, sup->super())
    {
        // s'il y a une contrainte de liens, vérifier l'existence de ce lien
        QString idsub = s->regle()->idSub();
        if (!idsub.isEmpty() && !sub->perePar(idsub))
            continue;
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
                    if (!s->complet())
                    {
                        s->addSub(sub, l, sl);
                        if (s->bloquant())
                        {
                            sub->setClos();
                            selectionne(sub, s);
                        }
                    }
                    else if (s->regle()->multiple())
                    {
                        // cloner s, le compléter
                        Super *nSuper = s->copie();
                        nSuper->addSub(sub, l, sl);
                        sup->addSuper(nSuper);
                    }
                }
            }
        }
        retour = retour || (s->motSub() == sub);
    }
    // supprimer les règles parentes si une règle dérivée est validée
    foreach (Super *s, sup->super())
    {
        QString rp = s->regle()->idPere();
        if (s->complet() && (!rp.isEmpty()))
        {
            foreach (Super *sp, sup->super())
                if (sp->complet() && sp->regle()->id() == rp)
                {
                    sp->annule();
                }
        }
    }

    return retour;
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
