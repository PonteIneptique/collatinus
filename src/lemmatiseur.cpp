/*                 lemmatiseur.cpp
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
 * \file lemmatiseur.cpp
 * \brief module de lemmatisation des formes latines
 */

#include <QDir>
#include <QFile>
#include <QRegExp>
#include <QTextStream>
#include <iostream>

#include "ch.h"
#include "lemmatiseur.h"

#include <QDebug>
// #include <QElapsedTimer>
// #define DEBOG
// #define VERIF_TRAD

/**
 * \fn Lemmat::Lemmat (QObject *parent)
 * \brief Constructeur de la classe Lemmat.
 *
 * Il définit quelques constantes, initialise
 * les options à false, et appelle les fonctions
 * de lecture des données : modèles, lexique,
 * traductions et irréguliers.
 */
Lemmat::Lemmat(QObject *parent, QString resDir) : QObject(parent)
{
    if (resDir == "")
        _resDir = qApp->applicationDirPath() + "/data/";
    else if (resDir.endsWith("/")) _resDir = resDir;
    else _resDir = resDir + "/";
    // options
    _alpha = false;
    _formeT = false;
    _html = false;
    _majPert = false;
    _morpho = false;
    _extension = false;
    _extLoaded = false;
    _nbrLoaded = false;
    // suffixes
    suffixes.insert("ne", "nĕ");
    suffixes.insert("que", "quĕ");
    suffixes.insert("ue", "vĕ");
    suffixes.insert("ve", "vĕ");
    suffixes.insert("st", "st");
    // assimilations
    ajAssims();
    // contractions
    ajContractions();
    // lecture des morphos
    QDir rep;
    rep = QDir(_resDir, "morphos.*");
    QStringList ltr = rep.entryList();
    ltr.removeOne("morphos.la");  // S'il traine encore...
    foreach (QString nfl, ltr)
        lisMorphos(QFileInfo(nfl).suffix());
    lisModeles();
    lisLexique();
    lisTags(false);
    lisTraductions(true, false);
    lisIrreguliers();
    lisParPos();
    lisCat();
#ifdef VERIF_TRAD
    foreach (Lemme *l, _lemmes.values()) {
        QString t = l->traduction("fr");
        if (t == "") qDebug() << l->cle() << "non traduit.";
    }
#endif
}

void Lemmat::lisCat()
{
    QStringList lignes = lignesFichier(_resDir + "CatLASLA.txt");
    foreach (QString lin, lignes)
    {
        if (lin.contains(",")) _catLasla.insert(lin.section(",",0,0),lin.section(",",1,1));
    }
}

/**
 * \fn Lemmat::lisNombres
 * \brief Lecture du fichier nombres.la
 * et peuplement de la variable _nbOcc de chaque lemme.
 *
 * Cette routine lit le fichier nombres.la.
 * Ce fichier a été tiré de la lemmatisation de la liste
 * des formes tirées des textes du LASLA.
 * C'est un csv, avec la virgule comme séparateur.
 *
 * Un programme a essayé d'établir la correspondance
 * entre les lemmes de Collatinus (1er champ)
 * avec ceux du LASLA (2e champ) et
 * le nombre d'occurrences associé.
 *
 */
void Lemmat::lisNombres()
{
    QStringList lignes = lignesFichier(_resDir + "nombres.la");
    foreach (QString lin, lignes)
    {
        QStringList liste = lin.split(',');
        QString clef = liste[0];
        clef.remove('-');
        if (_lemmes.contains(clef))
            _lemmes[clef]->ajNombre(liste[2].toInt());
    }
    _nbrLoaded = true;
    // Je lis aussi le début du fichier tags.la
    lisTags(false);
    // Lorsque j'aurai besoin des trigammes pour le tagger, je rappellerai lisTags(true).
    // Je commencerai avec un if (_trigram.isEmpty()) lisTags(true);
}

/**
 * @brief Lemmat::lisTags
 * @param tout : bool
 *
 * Lorsque le booléen tout est false, on ne lit que les nombres d'occurrences des tags.
 *
 * Lorsque le booléen tout est true, on lit tout le fichier,
 * donc aussi les dénombrements des séquences de trois tags.
 *
 * Cette routine lit le fichier tags.la.
 * Ce fichier a été tiré du traitement
 * des textes lemmatisés du LASLA.
 * C'est un csv, avec la virgule comme séparateur.
 *
 * La première partie du fichier donne le nombre d'occurrences de chaque tag
 * que j'ai introduit pour traiter les textes du LASLA.
 * Elle établit aussi la correspondance avec les tags de Collatinus.
 *
 * La deuxième partie donne les séquences de trois tags (LASLA) et
 * le nombre d'occurrences mesuré.
 *
 */
void Lemmat::lisTags(bool tout)
{
    // Nouveau format des données. Le 8 novembre 2016.
    _tagOcc.clear();
    _tagTot.clear();
    _trigram.clear();
    QStringList lignes = lignesFichier(_resDir + "tags.la");
    int max = lignes.count() - 1;
    int i = 0;
    QString l = "";
    QStringList eclats;
    while (i <= max) // && !l.startsWith("! --- "))
    {
        l = lignes.at(i);
        if (l.startsWith("! --- ")) break;
        eclats = l.split(',');
        _tagOcc[eclats[0]] += eclats[1].toInt();
        _tagTot[eclats[0].mid(0,1)] += eclats[1].toInt();
        ++i;
    }
    //  qDebug() << _tagOcc.size() << _tagTot.size();
    if (tout)
    {
        l.clear();
        ++i;
        while (i <= max && !l.startsWith("! --- "))
        {
            l = lignes.at(i);
            eclats = l.split(",");
            _trigram.insert(eclats[0],eclats[1].toInt());
            ++i;
        }
        //  qDebug() << _trigram.size();
    }
}

/**
 * @brief Lemmat::tag
 * @param l : le pointeur vers le lemme
 * @param morph : l'analyse morphologique
 * @return : le tag pour Collatinus
 *
 * Cette routine calcule le tag correspondant
 * à l'analyse morphologique donnée, morph,
 * pour le lemme, l.
 * Ce tag est toujours sur trois caractères.
 *
 * Ce tag est obtenu avec le POS du lemme,
 * suivi des cas (1-6 ou 7) et nombre (1, 2) pour les formes déclinées.
 * Pour les verbes conjugués, on donne le mode (1-4)
 * et un 1 si c'est un présent ou un espace sinon.
 * Les supins ont été joints aux impératifs autres que le présent (groupes trop peu nombreux).
 * Les formes verbales déclinées ont un "w" en tête (à la place du "v" pour verbe).
 * Pour les invariables, le POS est complété avec deux espaces.
 *
 */
QString Lemmat::tag(Lemme *l, QString morph)
{
    // Il faut encore traiter le cas des pos multiples
    QString lp = l->pos();
    QString lTags = "";
    while (lp.size() > 0)
    {
        QString p = lp.mid(0,1);
        lp = lp.mid(1);
        if ((p == "n") && (morph == morpho(413))) // Locatif !
            lTags.append("n71,");
        else if ((p == "v") && (morph.contains(" -u"))) // C'est un supin
            lTags.append("v3 ,");
        else
        {
            p.append("%1%2,");
            if (p.startsWith("v"))
            {
                for (int i=0; i<4; i++) if (morph.contains(modes(i).toLower()))
                {
                    if (morph.contains(temps(0))) p = p.arg(i+1).arg(1); // présent
                    else  p = p.arg(i+1).arg(" ");
                    lTags.append(p);
                    break;
                }
            }
            if (p.size() > 4) // Si p == 4, c'est que c'était un verbe conjugué.
            {
                for (int i=0; i<6; i++) if (morph.contains(cas(i)))
                {
                    if (morph.contains(nombre(1))) p = p.arg(i+1).arg(2);
                    else  p = p.arg(i+1).arg(1);
                    if (p.startsWith("v")) p[0] = 'w'; // Forme verbale déclinée.
                    lTags.append(p);
                    break;
                }
            }
            if (p.size() > 4)
            {
                p = p.arg(" ").arg(" ");
                lTags.append(p);
            }
            //if (!_tagOcc.contains(p.mid(0,3)))
            //   qDebug() << l->cle() << morph << p << " : Tag non trouvé !";
        }
    }
    return lTags;
}

/**
 * @brief Lemmat::fraction
 * @param t : le tag
 * @return : la fraction moyenne du tag.
 *
 * Ce résultat est un entier, exprimé en 1/1024e
 *
 * On va chercher le nombre d'occurrences associé à ce tag.
 * On le divise par le nombre d'occurrences associé au même POS.
 *
 * Si la fonction reçoit une liste de tags,
 * elle retourne la plus grande fraction.
 *
 */
int Lemmat::fraction(QString listTags)
{
    int frFin = 0;
    while (listTags.size() > 2)
    {
        QString t = listTags.mid(0,3);
        listTags = listTags.mid(4);
        int fr = 0;
        if (_tagOcc.contains(t))
        {
            if ((t[0] == 'a') || (t[0] == 'p') || (t[0] == 'w')) // Adj. ou pron. sans genre !
                fr = _tagOcc[t] * 341 / _tagTot[t.mid(0,1)];
            else if ((t[0] == 'v') && (t[2] == '1')) // verbe au présent
                fr = _tagOcc[t] * 512 / _tagTot[t.mid(0,1)];
            else if ((t[0] == 'v') && (t[2] == ' ')) // verbe à un autre temps
                fr = _tagOcc[t] * 256 / _tagTot[t.mid(0,1)];
            else if (t[0] == 'n') // Nom
                fr = _tagOcc[t] * 1024 / _tagTot[t.mid(0,1)];
            else fr = 1024;
            if (fr == 0) fr = 1;
            //  qDebug() << _tagOcc[t] << _tagTot[t.mid(0,1)] << fr;
        }
        //else qDebug() << t << " : Tag non trouvé !";
        if (frFin < fr) frFin = fr; // Si j'ai reçu une liste de tags, je garde la fraction la plus grande.
    }
    if (frFin == 0) return 1024;
    return frFin;
}

/**
 * @brief Lemmat::tagOcc
 * @param t : tag
 * @return Le nombre d'occurrences du tag t
 */
int Lemmat::tagOcc(QString t)
{
    return _tagOcc[t];
}

/**
 * @brief Lemmat::lignesFichier
 * @param nf : nom du fichier
 * @return : l'ensemble de lignes du fichier qui ne sont
 * ni vides ni commentées.
 *
 * Les fichiers de Collatinus ont adopté le point d'exclamation
 * en début de ligne pour introduire un commentaire.
 * Ces lignes doivent être ignorées par le programme.
 *
 */
QStringList Lemmat::lignesFichier(QString nf)
{
    QFile f(nf);
    f.open(QFile::ReadOnly);
    QTextStream flux(&f);
    flux.setCodec("UTF-8"); // Pour windôze !
    QStringList retour;
    while (!flux.atEnd())
    {
        QString lin = flux.readLine();
        if ((!lin.isEmpty()) && ((!lin.startsWith("!")) || lin.startsWith("! --- ")))
            retour.append(lin);
    }
    f.close();
    return retour;
}

/**
 * @brief Lemmat::lisMorphos
 * @param lang : langue pour les morphologies.
 * Cette langue est donnée par deux caractères "fr" ou "en",
 * pour l'instant.
 *
 * Cette routine lit le fichier morphos.* qui donne
 * les analyses morphologiques en français ou en anglais.
 * Les utilisateurs peuvent ajouter toutes les langues qu'ils maîtrisent.
 *
 * Des mots clefs essentiels sont aussi ajoutés après les 416 morphos possibles.
 *
 */
void Lemmat::lisMorphos(QString lang)
{
    QStringList lignes = lignesFichier(_resDir + "morphos." + lang);
    int max = lignes.count() - 1;
    int i = 0;
    QString l; // = "";
    QStringList morphos;
    while (i <= max) // && !l.startsWith("! --- "))
    {
        l = lignes.at(i);
        if (l.startsWith("! --- ")) break;
        if (i+1 != l.section(':',0,0).toInt())
            qDebug() <<i<<"Fichier morphos." << lang << ", erreur dans la ligne "<<l;
        else morphos.append(l.section(':',1,1));
        ++i;
    }
    _morphos.insert(lang,morphos);
    QStringList cas;
    l.clear();
    ++i;
    while (i <= max && !l.startsWith("! --- "))
    {
        l = lignes.at(i);
        cas << l;
        ++i;
    }
    _cas.insert(lang,cas);
    QStringList genres;
    l.clear();
    while (i <= max && !l.startsWith("! --- "))
    {
        l = lignes.at(i);
        genres << l;
        ++i;
    }
    _genres.insert(lang,genres);
    QStringList nombres;
    l = "";
    while (i <= max && !l.startsWith("! --- "))
    {
        l = lignes.at(i);
        nombres << l;
        ++i;
    }
    _nombres.insert(lang,nombres);
    QStringList temps;
    l.clear();
    while (i <= max && !l.startsWith("! --- "))
    {
        l = lignes.at(i);
        temps << l;
        ++i;
    }
    _temps.insert(lang,temps);
    QStringList modes;
    l.clear();
    while (i <= max && !l.startsWith("! --- "))
    {
        l = lignes.at(i);
        modes << l;
        ++i;
    }
    _modes.insert(lang,modes);
    QStringList voix;
    l.clear();
    while (i <= max && !l.startsWith("! --- "))
    {
        l = lignes.at(i);
        voix << l;
        ++i;
    }
    _voix.insert(lang,voix);
    QStringList mc;
    l.clear();
    while (i <= max && !l.startsWith("! --- "))
    {
        l = lignes.at(i);
        mc << l;
        ++i;
    }
    _motsClefs.insert(lang,mc);
}

/**
* \fn void Lemmat::ajAssims ()
* \brief définit les débuts de mots
* non assimilés, et associe à chacun sa
* forme assimilée.
*/
void Lemmat::ajAssims()
{
    // peupler la QMap assims
    QStringList lignes = lignesFichier(_resDir + "assimilations.la");
    foreach (QString lin, lignes)
    {
        QStringList liste = lin.split(':');
        assimsq.insert(liste.at(0), liste.at(1));
        assims.insert(Ch::atone(liste.at(0)), Ch::atone(liste.at(1)));
    }
}

/**
 * \fn void Lemmat::ajContractions ()
 * \brief Établit une liste qui donne, pour chaque
 * contraction, la forme non contracte qui lui
 * correspond.
 */
void Lemmat::ajContractions()
{
    // peupler la QMap _contractions
    QStringList lignes = lignesFichier(_resDir + "contractions.la");
    foreach (QString lin, lignes)
    {
        QStringList liste = lin.split(':');
        _contractions.insert(liste.at(0), liste.at(1));
    }
}

int Lemmat::aRomano(QString f)
{
    if (f.size () == 0) return 0;
    // création de la table de conversion : pourrait être créée ailleurs.
    QMap<QChar,int> conversion;
    conversion['I']=1;
    conversion['V']=5;
    conversion['X']=10;
    conversion['L']=50;
    conversion['C']=100;
    conversion['D']=500;
    conversion['M']=1000;
    // calcul du résultat : ajout d'un terme si l'ordre est normal, soustraction sinon.
    int res=0;
    int conv_c;
    int conv_s = conversion[f[0]];
    for (int i = 0; i < f.count()-1; i++)
    {
        conv_c = conv_s;
        conv_s = conversion[f[i+1]];
        if (conv_c < conv_s)
            res -= conv_c;
        else res += conv_c;
    }
    res += conv_s;
    return res;
}

/**
 * \fn void Lemmat::ajDesinence (Desinence *d)
 * \brief ajoute la désinence d dans la map des
 * désinences.
 */
void Lemmat::ajDesinence(Desinence *d)
{
    _desinences.insert(Ch::deramise(d->gr()), d);
}

bool Lemmat::estRomain(QString f)
{
    return !(f.contains(QRegExp ("[^IVXLCDM]"))
             || f.contains("IL")
             || f.contains("IVI"));
}

/**
 * \fn void Lemmat::ajRadicaux (Lemme *l)
 * \brief Calcule tous les radicaux du lemme l,
 *  en se servant des modèles, les ajoute à ce lemme,
 *  et ensuite à la map *  des radicaux de la classe Lemmat.
 *
 */
void Lemmat::ajRadicaux(Lemme *l)
{
    // ablŭo=ā̆blŭo|lego|ā̆blŭ|ā̆blūt|is, ere, lui, lutum
    //      0        1    2    3         4
    Modele *m = modele(l->grModele());
    /* insérer d'abord les radicaux définis dans lemmes.la
    qui sont prioritaires */
    foreach (int i, l->clesR())
    {
        QList<Radical *> lr = l->radical(i);
        foreach (Radical *r, lr)
            _radicaux.insert(Ch::deramise(r->gr()), r);
    }
    // pour chaque radical du modèle
    foreach (int i, m->clesR())
    {
        if (l->clesR().contains(i)) continue;
        QStringList gs = l->grq().split(',');
        foreach (QString g, gs)
        {
            Radical *r = NULL;
            {
                QString gen = m->genRadical(i);
                // si gen == 'K', le radical est la forme canonique
                if (gen == "-") continue;
                if (gen == "K")
                    r = new Radical(g, i, l);
                else
                {
                    // sinon, appliquer la règle de formation du modèle
                    int oter = gen.section(',', 0, 0).toInt();
                    QString ajouter = gen.section(',', 1, 1);
                    if (g.endsWith(0x0306)) g.chop(1);
                    g.chop(oter);
                    if (ajouter != "0") g.append(ajouter);
                    r = new Radical(g, i, l);
                }
            }
            l->ajRadical(i, r);
            _radicaux.insert(Ch::deramise(r->gr()), r);
        }
    }
}

/**
 * \fn QString Lemmat::assim (QString a)
 * \brief Cherche si la chaîne a peut subir
 *        une assimilation, et renvoie
 *        cette chaîne éventuellement assimilée.
 *        *version sans quantités*
 */
QString Lemmat::assim(QString a)
{
    foreach (QString d, assims.keys())
        if (a.startsWith(d))
        {
            a.replace(d, assims.value(d));
            return a;
        }
    return a;
}

/**
 * \fn QString Lemmat::assimq (QString a)
 * \brief Cherche si la chaîne a peut subir
 *        une assimilation, et renvoie
 *        cette chaîne éventuellement assimilée.
 *        *version avec quantités*
 */
QString Lemmat::assimq(QString a)
{
    foreach (QString d, assimsq.keys())
        if (a.startsWith(d))
        {
            a.replace(d, assimsq.value(d));
            return a;
        }
    return a;
}

/**
 * \fn QString Lemmat::cible()
 * \brief Renvoie la langue cible dans sa forme
 *        abrégée (fr, en, de, it, etc.).
 */
QString Lemmat::cible()
{
    return _cible;
}

/**
 * \fn QMap<QString,QString> Lemmat::cibles()
 * \brief Renvoie la map des langues cibles.
 *
 */
QMap<QString, QString> Lemmat::cibles()
{
    return _cibles;
}

/**
 * \fn QString Lemmat::decontracte (QString d)
 * \brief Essaie de remplacer la contractions de d
 *        par sa forme entière, et renvoie le résultat.
 */
QString Lemmat::decontracte(QString d)
{
    foreach (QString cle, _contractions.keys())
    {
        if (d.endsWith(cle))
        {
            d.chop(cle.length());
            if ((d.contains("v") || d.contains("V")))
                d.append(_contractions.value(cle));
            else
                d.append(Ch::deramise(_contractions.value(cle)));
            return d;
        }
    }
    return d;
}

/**
 * \fn QString Lemmat::desassim (QString a)
 * \brief Essaie de remplacer l'assimilation de a
 *        par sa forme non assimilée, et renvoie
 *        le résultat.
 */
QString Lemmat::desassim(QString a)
{
    foreach (QString d, assims.values())
    {
        if (a.startsWith(d))
        {
            a.replace(d, assims.key(d));
            return a;
        }
    }
    return a;
}

/**
 * \fn QString Lemmat::desassimq (QString a)
 * \brief Essaie de remplacer l'assimilation de a
 *        par sa forme non assimilée, et renvoie
 *        le résultat.
 */
QString Lemmat::desassimq(QString a)
{
    foreach (QString d, assimsq.values())
    {
        if (a.startsWith(d))
        {
            a.replace(d, assimsq.key(d));
            return a;
        }
    }
    return a;
}

/**
 * \fn MapLem Lemmat::lemmatise (QString f)
 * \brief Le cœur du lemmatiseur
 *
 *  renvoie une QMap<Lemme*,QStringlist> contenant
 *  - la liste de tous les lemmes pouvant donner
 *    la forme f;
 *  - pour chacun de ces lemmes la QStringList des morphologies
 *    correspondant à la forme.
 */
MapLem Lemmat::lemmatise(QString f)
{
    MapLem result;
    if (f.isEmpty()) return result;
    QString f_lower = f.toLower();
    int cnt_v = f_lower.count("v");
    bool V_maj = f[0] == 'V';
    int cnt_ae = f_lower.count("æ");
    int cnt_oe = f_lower.count("œ");
    if (f_lower.endsWith("æ")) cnt_ae -= 1;
    f = Ch::deramise(f);
    // formes irrégulières
    QList<Irreg *> lirr = _irregs.values(f);
    foreach (Irreg *irr, lirr)
    {
        foreach (int m, irr->morphos())
        {
            SLem sl = {irr->grq(), morpho(m), ""};
            // result[irr->lemme()].prepend (morpho (m));
            result[irr->lemme()].prepend(sl);
        }
    }
    // radical + désinence
    for (int i = 0; i <= f.length(); ++i)
    {
        QString r = f.left(i);
        QString d = f.mid(i);
        QList<Desinence *> ldes = _desinences.values(d);
        if (ldes.empty()) continue;
        // Je regarde d'abord si d est une désinence possible,
        // car il y a moins de désinences que de radicaux.
        // Je fais la recherche sur les radicaux seulement si la désinence existe.
        QList<Radical *> lrad = _radicaux.values(r);
        // ii noté ī
        // 1. Patauium, gén. Pataui : Patau.i -> Patau+i.i
        // 2. conubium, ablP conubis : conubi.s -> conubi.i+s
        if (d.startsWith('i') && !d.startsWith("ii") && !r.endsWith('i'))
            lrad << _radicaux.values(r + "i");
        if (lrad.empty()) continue;
        // Il n'y a rien à faire si le radical n'existe pas.
        foreach (Radical *rad, lrad)
        {
            Lemme *l = rad->lemme();
            foreach (Desinence *des, ldes)
            {
                if (des->modele() == l->modele() &&
                    des->numRad() == rad->numRad() &&
                    !l->estIrregExcl(des->morphoNum()))
                {
                    bool c = ((cnt_v==0)
                              ||(cnt_v == rad->grq().toLower().count("v")
                                 +des->grq().count("v")));
                    if (!c) c = (V_maj && (rad->gr()[0] == 'U')
                            && (cnt_v - 1 == rad->grq().toLower().count("v")));
                    c = c && ((cnt_oe==0)||(cnt_oe == rad->grq().toLower().count("ōe")));
                    c = c && ((cnt_ae==0)||
                              (cnt_ae == (rad->grq().toLower().count("āe") + rad->grq().toLower().count("prăe"))));
                    if (c)
                    {
                        QString fq = rad->grq() + des->grq();
                        if (!r.endsWith("i") && rad->gr().endsWith("i"))
                            fq = rad->grq().left(rad->grq().size()-1) + "ī"
                                    + des->grq().right(des->grq().size()-1);
                        SLem sl = {fq, morpho(des->morphoNum()), ""};
                        result[l].prepend(sl);
                    }
                }
            }
        }
    }
    if (_extLoaded && !_extension && !result.isEmpty())
    {
        // L'extension est chargée mais je ne veux voir les solutions qui en viennent que si toutes en viennent.
        MapLem res;
        foreach (Lemme *l, result.keys())
        {
            if (l->origin() == 0)
                res[l] = result[l];
        }

        if (!res.isEmpty()) result = res;
    }
    // romains
    if (estRomain(f) && !_lemmes.contains(f))
    {
        QString lin = QString("%1|inv|||adj. num.|1").arg(f);
        Lemme *romain = new Lemme(lin, 0, this);
        int nr = aRomano(f);
        romain->ajTrad(QString("%1").arg(nr), "fr");
        _lemmes.insert(f, romain);
        SLem sl = {f,"inv",""};
        QList<SLem> lsl;
        lsl.append(sl);
        result.insert(romain, lsl);
    }
    return result;
}

/**
 * \fn bool Lemmat::inv (Lemme *l, const MapLem ml)
 * \brief Renvoie true si le lemme l faisant partie
 *        de la MaplLem ml est invariable.
 */
bool Lemmat::inv(Lemme *l, const MapLem ml)
{
    return ml.value(l).at(0).morpho == "-";
}

QString Lemmat::k9(QString m)
{
//    qDebug() << m;
    QStringList res;
    QString cibAct = _cible;
    _cible = "k9,fr";
    MapLem mm = lemmatiseM(m);
    _cible = cibAct;
    if (mm.isEmpty()) return "\n";
    // Il faut répondre quelque chose, sinon j'attends 30 secondes !
    foreach (Lemme *l, mm.keys())
    {
        QString clef = l->cle() + ", ,";
        foreach (SLem s, mm.value(l))
        {
            QString code9 = s.morpho;
            QString forme = Ch::atone(s.grq);
            if (!s.sufq.isEmpty()) forme += "<" + Ch::atone(s.sufq) +">,";
            else forme += ",";
            if (_catLasla.contains(l->modele()->gr())) code9.replace("k9",_catLasla[l->modele()->gr()]);
//            qDebug() << clef << s.morpho << code9 << _catLasla[l->modele()->gr()];
            res << forme + clef + code9;
        }
    }

    return res.join("\n");
}

/**
 * \fn MapLem Lemmat::lemmatiseM (QString f, bool debPhr)
 * \brief Renvoie dans une MapLem les lemmatisations de la
 *        forme f. le paramètre debPhr à true indique qu'il
 *        s'agit d'un début de phrase, et la fonction
 *        peut tenir compte des majuscules pour savoir
 *        s'il s'agit d'un nom propre.
 */
MapLem Lemmat::lemmatiseM(QString f, bool debPhr, bool desas)
{
    QString res;
    QTextStream fl(&res);
    MapLem mm = lemmatise(f);
    if (f.isEmpty()) return mm;
    // suffixes
    foreach (QString suf, suffixes.keys())
    {
        if (mm.empty() && f.endsWith(suf))
        {
            QString sf = f;
            sf.chop(suf.length());
            // TODO : aequeque est la seule occurrence
            // de -queque dans le corpus classique
            mm = lemmatiseM(sf, debPhr, desas);
            // Ne pas assimiler une 2e fois.
            bool sst = false;
            if (mm.isEmpty() && (suf == "st"))
            {
                sf += "s";
                mm = lemmatiseM(sf, debPhr, desas);
                sst = true;
            }
            foreach (Lemme *l, mm.keys())
            {
                QList<SLem> ls = mm.value(l);
                for (int i = 0; i < ls.count(); ++i)
                    if (sst) mm[l][i].sufq = "t";
                    else mm[l][i].sufq += suffixes.value(suf); // Pour modoquest
            }
        }
    }
    if (debPhr && f.at(0).isUpper())
    {
        QString nf = f.toLower();
        MapLem nmm = lemmatiseM(nf);
        foreach (Lemme *nl, nmm.keys())
            mm.insert(nl, nmm.value(nl));
    }
    // assimilations
    if (!desas)
    {
    QString fa = assim(f);
    if (fa != f)
    {
        MapLem nmm = lemmatiseM(fa, debPhr, true);
        // désassimiler les résultats
        foreach (Lemme *nl, nmm.keys())
        {
            for (int i = 0; i < nmm[nl].count(); ++i)
                nmm[nl][i].grq = desassimq(nmm[nl][i].grq);
            mm.insert(nl, nmm.value(nl));
        }
    }
    else
    {
        QString fa = desassim(f);
        if (fa != f)
        {
            MapLem nmm = lemmatiseM(fa, debPhr, true);
            foreach (Lemme *nl, nmm.keys())
            {
                for (int i = 0; i < nmm[nl].count(); ++i)
                    nmm[nl][i].grq = assimq(nmm[nl][i].grq);
                mm.insert(nl, nmm.value(nl));
            }
        }
    }
    }
    // contractions
    QString fd = f;
    foreach (QString cle, _contractions.keys())
        if (fd.endsWith(cle))
        {
            fd.chop(cle.length());
            if ((fd.contains("v") || fd.contains("V")))
                fd.append(_contractions.value(cle));
            else
                fd.append(Ch::deramise(_contractions.value(cle)));
            MapLem nmm = lemmatise(fd);
            foreach (Lemme *nl, nmm.keys())
            {
                int diff = _contractions.value(cle).size() - cle.size();
                // nombre de lettres que je dois supprimer
                for (int i = 0; i < nmm[nl].count(); ++i)
                {
                    int position = f.size() - cle.size() + 1;
                    // position de la 1ère lettre à supprimer
                    if (fd.size() != nmm[nl][i].grq.size())
                    {
                        // il y a une (ou des) voyelle(s) commune(s)
                        QString debut = nmm[nl][i].grq.left(position + 2);
                        position += debut.count("\u0306"); // Faut-il vérifier que je suis sur le "v".
                    }
                    nmm[nl][i].grq = nmm[nl][i].grq.remove(position, diff);
                }
                mm.insert(nl, nmm.value(nl));
            }
        }
    // majuscule initiale
    if (mm.empty())
    {
        f[0] = f.at(0).toUpper();
        MapLem nmm = lemmatise(f);
        foreach (Lemme *nl, nmm.keys())
            mm.insert(nl, nmm.value(nl));
    }
    return mm;
}



/**
 * \fn QString Lemmat::lemmatiseT (QString &t,
 *  						   bool alpha,
 *  						   bool cumVocibus,
 *  						   bool cumMorpho,
 *  						   bool nreconnu)
 * \brief Renvoie sous forme de chaîne la lemmatisation
 *        et la morphologie de chaque mot du texte t.
 *        Les paramètres permettent de classer la sortie
 *        par ordre alphabétique ; de reproduire la
 *        forme du texte au début de chaque lemmatisation ;
 *        de donner les morphologies de chaque forme ; ou
 *        de rejeter les échecs en fin de liste. D'autres
 *        paramètres, comme le format de sortie txt ou html,
 *        sont donnés par des variables de classe.
 *	      Les paramètres et options true outrepassent les false,
 *        _majPert et _html sont dans les options de la classe.
 *
 *        Par effet de bord, la fonction modifie le texte
 *        t, passé par adresse dans le paramètre &t, en
 *        tenant compte de la liste des mots connus définie
 *        par l'utilisateur via l'option
 *        Fichier/Lire une liste de mots connus.
 *
 */
QString Lemmat::lemmatiseT(QString &t)
{
    return lemmatiseT(t, _alpha, _formeT, _morpho, _nonRec);
}

QString Lemmat::lemmatiseT(QString &t, bool alpha, bool cumVocibus,
                           bool cumMorpho, bool nreconnu)
{
    // pour mesurer :
    // QElapsedTimer timer;
    // timer.start();
/*    
    alpha = alpha || _alpha;
    cumVocibus = cumVocibus || _formeT;
    cumMorpho = cumMorpho || _morpho;
    nreconnu = nreconnu || _nonRec;
*/
    // Pour coloriser le texte
    bool cumColoribus = !_couleurs.isEmpty();
    bool listeVide = _hLem.isEmpty();
    int colPrec = 0;
    int formesConnues = 0;
    // éliminer les chiffres et les espaces surnuméraires
    t.remove(QRegExp("\\d"));
//    t = t.simplified();
    // découpage en mots
    QStringList lm = t.split(QRegExp("\\b"));
    // conteneur pour les résultats
    QStringList lsv;
    // conteneur pour les échecs
    QStringList nonReconnus;
    // lemmatisation pour chaque mot
    if (lm.size() < 2)
    {
//        qDebug() << t << lm.size() << lm;
        return "";
        // Ça peut arriver que le texte ne contienne qu"une ponctuation
    }
    for (int i = 1; i < lm.length(); i += 2)
    {
        QString f = lm.at(i);
        if (f.toInt() != 0) continue;
        // nettoyage et identification des débuts de phrase
        QString sep = lm.at(i - 1);
        bool debPhr = ((i == 1 && lm.count() !=3) || sep.contains(Ch::rePonct));
        // lemmatisation de la forme
        MapLem map = lemmatiseM(f, !_majPert || debPhr);
        // échecs
        if (map.empty())
        {
            if (nreconnu)
                nonReconnus.append(f + "\n");
            else
            {
                if (_html)
                    lsv.append("<li style=\"color:blue;\">" + f + "</li>");
                else
                    lsv.append(f + " ÉCHEC");
            }
            if (cumColoribus)
            {
                if (!listeVide)
                {
                    // La liste de mots connus n'est pas vide. Le mot en fait-il partie ?
                    QString lem = f;
                    lem.replace("j","i");
                    lem.replace("v","u");
                    lem.replace("J","I");
                    lem.replace("V","U");
                    // qDebug() << lem;
                    if (_hLem.contains(lem))
                    {
                        _hLem[lem]++;
                        if (colPrec != 0)
                        {
                            lm[i].prepend("</span><span style=\"color:"+_couleurs[0]+"\">");
                            colPrec = 0;
                        }
                    }
                    else if (colPrec != 2)
                    {
                        lm[i].prepend("</span><span style=\"color:"+_couleurs[2]+"\">");
                        colPrec = 2;
                    }
                }
            }
        }
        else
        {
            bool connu = false;
            if (cumColoribus)
            {
                if (!listeVide)
                {
                    // La liste de mots connus n'est pas vide. Un des lemmes identifiés en fait-il partie ?
                    foreach (Lemme *l, map.keys())
                        if (_hLem.contains(l->cle()))
                        {
                            connu = true;
                            _hLem[l->cle()]++;
                        }
//                        connu = connu || _hLem.contains(l->cle());
                }
                if (connu)
                {
                    formesConnues += 1;
                    if (colPrec != 0)
                    {
                        lm[i].prepend("</span><span style=\"color:"+_couleurs[0]+"\">");
                        colPrec = 0;
                    }
                }
                else if (colPrec != 1)
                {
                    lm[i].prepend("</span><span style=\"color:"+_couleurs[1]+"\">");
                    colPrec = 1;
                }
            }
            if (cumVocibus)
            {
                // avec affichage des formes du texte
                QString lin;
                QMultiMap<int,QString> listeLem;
                if (_html)
                {
                    lin = "<h4>" + f + "</h4><ul>";
                    foreach (Lemme *l, map.keys())
                    {
                        QString lem = "<li>" + l->humain(true, _cible, true);
                        int frMax = 0;
                        if (cumMorpho && !inv(l, map))
                        {
                            QMultiMap<int,QString> listeMorph;
                            foreach (SLem m, map.value(l))
                            {
                                int fr = fraction(tag(l,m.morpho));
                                if (fr > frMax) frMax = fr;
                                if (m.sufq.isEmpty())
                                    listeMorph.insert(-fr,m.grq + " " + m.morpho);
                                else
                                    listeMorph.insert(-fr,m.grq + " + " + m.sufq +
                                                      " " + m.morpho);
                            }
                            lem.append("<ul><li>");
                            QStringList lMorph = listeMorph.values();
                            lem.append(lMorph.join("</li><li>"));
                            lem.append("</li></ul>\n");
                        }
                        else foreach (SLem m, map.value(l))
                        {
                            int fr = fraction(tag(l,m.morpho));
                            if (fr > frMax) frMax = fr;
                        }
                        if (frMax == 0) frMax = 1024;
                        lem.append("</li>");
                        listeLem.insert(-frMax * l->nbOcc(),lem);
                    }
                    QStringList lLem = listeLem.values();
                    // Les valeurs sont en ordre croissant
                    lin.append(lLem.join("\n"));
                    lin.append("</ul>\n");
                }
                else
                {
                    lin = " " + f + "\n";
                    foreach (Lemme *l, map.keys())
                    {
                        lin.append("  - " + l->humain(false, _cible, true) + "\n");
                        if (cumMorpho && !inv(l, map))
                        {
                            foreach (SLem m, map.value(l))
                                if (m.sufq.isEmpty())
                                    lin.append("    . " + m.grq + " " + m.morpho +
                                               "\n");
                                else
                                    lin.append("    . " + m.grq + " + " + m.sufq +
                                               " " + m.morpho + "\n");
                        }
                    }
                }
//                lsv.append(lin);
                if (!connu || listeVide) lsv.append(lin);
                // Par défaut, pas d'aide pour les mots connus.
            }
            else  // sans les formes du texte
            {
                foreach (Lemme *l, map.keys())
                {
                    QString lin = l->humain(_html, _cible);
                    if (cumMorpho && !inv(l, map))
                    {
                        QTextStream fl(&lin);
                        if (_html)
                        {
                            fl << "<ul>";
                            foreach (SLem m, map.value(l))
                                fl << "<li>" << m.grq << " " << m.morpho << "</li>";
                            fl << "</ul>\n";
                        }
                        else
                            foreach (SLem m, map.value(l))
                                fl << "\n    . " << m.grq << " " << m.morpho;
                    }
//                    lsv.append(lin);
                    if (!connu || listeVide) lsv.append(lin);
                    // Par défaut, pas d'aide pour les mots connus.
                }
            }
        }
    }  // fin de boucle de lemmatisation pour chaque mot

    if (alpha)
    {
        lsv.removeDuplicates();
        qSort(lsv.begin(), lsv.end(), Ch::sort_i);
    }
    // peupler lRet avec les résultats
    QStringList lRet;
    if (_html) lRet.append("<ul>");
    foreach (QString item, lsv)
    {
        if (_html)
            lRet.append("<li>" + item + "</li>");
        else
            lRet.append("* " + item + "\n");
    }
    if (_html) lRet.append("</ul>\n");
    // non-reconnus en fin de liste si l'option nreconnu
    // est armée
    if (nreconnu && !nonReconnus.empty())
    {
        nonReconnus.removeDuplicates();
        QString nl;
        if (_html) nl = "<br/>";
        if (alpha) qSort(nonReconnus.begin(), nonReconnus.end(), Ch::sort_i);
        QString titreNR;
        int tot = (lm.count() - 1) / 2;
        QTextStream(&titreNR) << "--- " << nonReconnus.count() << "/"
                              << tot << " ("
                              << ((nonReconnus.count() * 100) / tot)
                              << " %) FORMES NON RECONNUES ---" << nl << "\n";
        lRet.append(titreNR + nl);
        foreach (QString nr, nonReconnus)
            lRet.append(nr + nl);
    }
    if (cumColoribus)
    {
        lm[0].append("<span style=\"color:"+_couleurs[0]+"\">");
        lm[lm.size()-1].append("</span>");
        t = lm.join("");
        t.replace("\n","<br/>\n");
        if (!listeVide)
        {
            QString stats = "<strong>Formes connues : %1 sur %2 (%3%)<br/></strong>";
            lRet.prepend(stats.arg(formesConnues).arg((lm.size()/2)).arg((200*formesConnues)/(lm.size()-1)));
        }
    }
    // fin de la mesure :
    // qDebug()<<"Eneide"<<timer.nsecsElapsed()<<"ns";
    return lRet.join("");
}

/**
 * \fn QString Lemmat::lemmatiseFichier (QString f,
 *								  bool alpha,
 *								  bool cumVocibus,
 *								  bool cumMorpho,
 *								  bool nreconnu)
 * \brief Applique lemmatiseT sur le contenu du fichier
 *        f et renvoie le résultat. Les paramètres sont
 *        les mêmes que ceux de lemmatiseT.
 */
QString Lemmat::lemmatiseFichier(QString f, bool alpha, bool cumVocibus,
                                 bool cumMorpho, bool nreconnu)
{
    // lecture du fichier
    QFile fichier(f);
    fichier.open(QFile::ReadOnly);
    QTextStream flf(&fichier);
    flf.setCodec("UTF-8"); // Pour windôze !
    QString texte = flf.readAll();
    fichier.close();
    return lemmatiseT(texte, alpha, cumVocibus, cumMorpho, nreconnu);
}

/**
 * \fn Lemme* Lemmat::lemme (QString l)
 * \brief cherche dans la liste des lemmes le lemme
 *        dont la clé est l, et retourne le résultat.
 */
Lemme *Lemmat::lemme(QString l) { return _lemmes.value(l); }
/**
 * \fn QStringList Lemmat::lemmes (MapLem lm)
 * \brief renvoie la liste des graphies des lemmes
 *        de la MapLem lm sans signes diacritiques.
 */
QStringList Lemmat::lemmes(MapLem lm)
{
    QStringList res;
    foreach (Lemme *l, lm.keys())
        res.append(l->gr());
    return res;
}

/**
 * \fn void Lemmat::lisIrreguliers()
 * \brief Chargement des formes irrégulières
 *        du fichier data/irregs.la
 */
void Lemmat::lisIrreguliers()
{
    QStringList lignes = lignesFichier(_resDir + "irregs.la");
    foreach (QString lin, lignes)
    {
        Irreg *irr = new Irreg(lin, this);
        if (irr != 0 && irr->lemme() != 0)
            _irregs.insert(Ch::deramise(irr->gr()), irr);
#ifdef DEBOG
        else
            std::cerr << "Irréguliers, erreur dans la ligne" << qPrintable(lin);
#endif
    }
    // ajouter les irréguliers aux lemmes
    foreach (Irreg *ir, _irregs)
        ir->lemme()->ajIrreg(ir);
}

/**
 * \fn void Lemmat::lisFichierLexique(filepath)
 * \brief Lecture des lemmes, synthèse et enregistrement
 *        de leurs radicaux
 */
void Lemmat::lisFichierLexique(QString filepath)
{
    int orig = 0;
    if (filepath.endsWith("ext.la")) orig = 1;
    QStringList lignes = lignesFichier(filepath);
    foreach (QString lin, lignes)
    {
        Lemme *l = new Lemme(lin, orig, this);
        //if (_lemmes.contains(l->cle()))
        //    qDebug() << lin << " existe déjà";
        _lemmes.insert(l->cle(), l);
    }
}

/**
 * \fn void Lemmat::lisLexique()
 * \brief Lecture du fichier de lemmes de base
 */
void Lemmat::lisLexique()
{
    lisFichierLexique(_resDir + "lemmes.la");
}

/**
 * \fn void Lemmat::lisExtension()
 * \brief Lecture du fichier d'extension
 */
void Lemmat::lisExtension()
{
//    if (_nbrLoaded) foreach(Lemme *l, _lemmes.values())
  //      l->clearOcc();
    // Si les nombres d'occurrences ont été chargés, je dois les ré-initialiser.
    //qDebug() << "lecture extension";
    lisFichierLexique(_resDir + "lem_ext.la");
//    lisNombres();
}

/**
 * \fn void Lemmat::lisModeles()
 * \brief Lecture des modèles, synthèse et enregistrement
 *        de leurs désinences
 */
void Lemmat::lisModeles()
{
    QStringList lignes = lignesFichier(_resDir + "modeles.la");
    int max = lignes.count()-1;
    QStringList sl;
    for (int i=0;i<=max;++i)
    {
        QString l = lignes.at(i);
        if (l.startsWith('$'))
        {
            _variables[l.section('=', 0, 0)] = l.section('=', 1, 1);
            continue;
        }
        QStringList eclats = l.split(":");
        if ((eclats.at(0) == "modele" || i == max) && !sl.empty())
        {
            Modele *m = new Modele(sl, this);
            _modeles.insert(m->gr(), m);
            sl.clear();
        }
        sl.append(l);
    }
}

/**
 * \fn void Lemmat::lisParPos()
 * \brief Lecture des règles de quantité par position
 * enregistrées dans le fichier data/parpos.txt.
 */
void Lemmat::lisParPos()
{
    QStringList lignes = lignesFichier(_resDir + "parpos.txt");
    QStringList rr;
    foreach (QString ligne, lignes)
    {
        rr = ligne.split(";");
        _reglesp.append(Reglep(QRegExp(rr.at(0)), rr.at(1)));
    }
}

/**
 * \fn void Lemmat::lisTraductions()
 * \brief Lecture des fichiers de traductions
 *        trouvés dans data/, nommés lemmes, avec
 *        un suffixe corresponant à la langue cible
 *        qu'ils fournissent.
 */
void Lemmat::lisTraductions(bool base, bool extension)
{
//    QString nrep = _resDir;
    QDir rep;
    if (!base && !extension) return;
    if (base && extension) {
        rep = QDir(_resDir, "lem*.*");
    } else if (base) {
        rep = QDir(_resDir, "lemmes.*");
    } else {
        rep = QDir(_resDir, "lem_ext.*");
    }
    QStringList ltr = rep.entryList();
#ifdef VERIF_TRAD
    qDebug() << ltr;
#endif
    if (base) {
        ltr.removeOne("lemmes.la");  // n'est pas un fichier de traductions
    }
    if (extension) {
        ltr.removeOne("lem_ext.la");  // n'est pas un fichier de traductions
    }
    foreach (QString nfl, ltr)
    {
        // suffixe
        QString suff = QFileInfo(nfl).suffix();
        QStringList lignes = lignesFichier(_resDir + nfl);
        if (base)
        {
            // lire le nom de la langue
            QString lang = lignes.takeFirst();
            //lang = lang.mid(1).simplified();
            _cibles[suff] = lang;
        }

        foreach (QString lin, lignes)
        {
            Lemme *l = lemme(Ch::deramise(lin.section(':', 0, 0)));
            if (l != 0) l->ajTrad(lin.section(':', 1), suff);
#ifdef DEBOG
            else
                qDebug() << nfl << "traduction, erreur dans la ligne" << lin
                         << " clé" << Ch::deramise(lin.section(':', 0, 0));
#endif
        }
    }
}

/**
 * \fn Modele * Lemmat::modele (QString m)
 * \brief Renvoie l'objet de la classe Modele dont le nom est m.
 */
Modele *Lemmat::modele(QString m) { return _modeles[m]; }
/**
 * \fn QString Lemmat::morpho (int m)
 * \brief Renvoie la chaîne de rang m dans la liste des morphologies
 *        donnée par le fichier data/morphos.la
 */
QString Lemmat::morpho(int m)
{
    QString l = "fr"; // La langue sélectionnée
    if (_morphos.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2);
    else if ((_cible.size() > 4) && (_morphos.keys().contains(_cible.mid(3,2))))
        l = _cible.mid(3,2);
    if (m < 0 || m > _morphos[l].count())
        return "morpho, "+QString::number(m)+" : erreur d'indice";
    if (m == _morphos[l].count()) return "-";
    return _morphos[l].at(m - 1);
}

QString Lemmat::cas(int m)
{
    QString l = "fr"; // La langue sélectionnée
    if (_cas.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2);
    else if ((_cible.size() > 4) && (_cas.keys().contains(_cible.mid(3,2))))
        l = _cible.mid(3,2);
    return _cas[l].at(m);
}

QString Lemmat::genre(int m)
{
    QString l = "fr"; // La langue sélectionnée
    if (_genres.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2);
    else if ((_cible.size() > 4) && (_genres.keys().contains(_cible.mid(3,2))))
        l = _cible.mid(3,2);
    return _genres[l].at(m);
}

QString Lemmat::nombre(int m)
{
    QString l = "fr"; // La langue sélectionnée
    if (_nombres.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2);
    else if ((_cible.size() > 4) && (_nombres.keys().contains(_cible.mid(3,2))))
        l = _cible.mid(3,2);
    return _nombres[l].at(m);
}

QString Lemmat::temps(int m)
{
    QString l = "fr"; // La langue sélectionnée
    if (_temps.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2);
    else if ((_cible.size() > 4) && (_temps.keys().contains(_cible.mid(3,2))))
        l = _cible.mid(3,2);
    return _temps[l].at(m);
}

QString Lemmat::modes(int m)
{
    QString l = "fr"; // La langue sélectionnée
    if (_modes.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2);
    else if ((_cible.size() > 4) && (_modes.keys().contains(_cible.mid(3,2))))
        l = _cible.mid(3,2);
    return _modes[l].at(m);
}

QString Lemmat::voix(int m)
{
    QString l = "fr"; // La langue sélectionnée
    if (_voix.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2);
    else if ((_cible.size() > 4) && (_voix.keys().contains(_cible.mid(3,2))))
        l = _cible.mid(3,2);
    return _voix[l].at(m);
}

QString Lemmat::motsClefs(int m)
{
    QString l = "fr"; // La langue sélectionnée
    if (_motsClefs.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2);
    else if ((_cible.size() > 4) && (_motsClefs.keys().contains(_cible.mid(3,2))))
        l = _cible.mid(3,2);
    return _motsClefs[l].at(m);
}

/**
 * \fn bool Lemmat::optAlpha()
 * \brief Accesseur de l'option alpha, qui
 *        permet de fournir par défaut des résultats dans
 *        l'ordre alphabétique.
 */
bool Lemmat::optAlpha() { return _alpha; }
/**
 * \fn bool Lemmat::optHtml()
 * \brief Accesseur de l'option html, qui
 *        permet de renvoyer les résultats au format html.
 */
bool Lemmat::optHtml() { return _html; }

/**
 * \fn bool Lemmat::optFormeT()
 * \brief Accesseur de l'option formeT,
 *        qui donne en tête de lemmatisation
 *        la forme qui a été analysée.
 */
bool Lemmat::optFormeT() { return _formeT; }

/**
 * \fn bool Lemmat::optMajPert()
 * \brief Accesseur de l'option majPert,
 *        qui permet de tenir compte des majuscules
 *        dans la lemmatisation.
 */
bool Lemmat::optMajPert() { return _majPert; }

/**
 * \fn bool Lemmat::optExtension()
 * \brief Accesseur de l'option extension,
 *        qui permet de charger l'extension.
 */
bool Lemmat::optExtension() { return _extension; }
/**
 * \fn bool Lemmat::optMorpho()
 * \brief Accesseur de l'option morpho,
 *        qui donne l'analyse morphologique
 *        des formes lemmatisées.
 */

bool Lemmat::optMorpho()
{
    return _morpho;
}

QString Lemmat::parPos(QString f)
{
    bool maj = f.at(0).isUpper();
    f = f.toLower();
    foreach (Reglep r, _reglesp)
        f.replace(r.first, r.second);
    if (maj) f[0] = f[0].toUpper();
    return f;
}

/**
 * \fn void Lemmat::setAlpha (bool a)
 * \brief Modificateur de l'option alpha.
 */
// modificateurs d'options

void Lemmat::setAlpha(bool a) { _alpha = a; }
/**
 * \fn void Lemmat::setCible(QString c)
 * \brief Permet de changer la langue cible.
 */
void Lemmat::setCible(QString c) { _cible = c; }
/**
 * \fn void Lemmat::setHtml (bool h)
 * \brief Modificateur de l'option html.
 */
void Lemmat::setHtml(bool h) { _html = h; }
/**
 * \fn void Lemmat::setFormeT (bool f)
 * \brief Modificateur de l'option formeT.
 */
void Lemmat::setFormeT(bool f) { _formeT = f; }
/**
 * \fn void Lemmat::setMajPert (bool mp)
 * \brief Modificateur de l'option majpert.
 */
void Lemmat::setMajPert(bool mp) { _majPert = mp; }
/**
 * \fn void Lemmat::setMorpho (bool m)
 * \brief Modificateur de l'option morpho.
 */
void Lemmat::setMorpho(bool m) { _morpho = m; }
void Lemmat::setNonRec(bool n) { _nonRec = n; }
/**
 * \fn QString Lemmat::variable (QString v)
 * \brief permet de remplacer la métavariable v
 *        par son contenu. Ces métavariables sont
 *        utilisées par le fichier modeles.la, pour
 *        éviter de répéter des suites de désinences.
 *        Elles sont repérées comme en PHP, par leur
 *        premier caractère $.
 */
QString Lemmat::variable(QString v) { return _variables[v]; }

/**
 * @brief Lemmat::setExtension
 * @param e : bool
 *
 * Cette routine gère l'extension du lexique.
 * Si le paramètre e est true, l'extension du lexique est active.
 * S'il n'a pas encore été chargé, il l'est.
 *
 * Lors de la lecture des préférences (à l'initialisation),
 * cette routine est appelée.
 * Si on ne charge pas l'extension du lexique,
 * je charge quand même les nombres d'occurrences.
 * Ces nombres seront ré-initialisés si on charge l'extension par la suite.
 *
 */
void Lemmat::setExtension(bool e)
{
    _extension = e;
    if (!_extLoaded && e) {
        lisExtension();
        lisTraductions(false,true);
        _extLoaded = true;
    }
//    else if (!_nbrLoaded) lisNombres();
}

/**
 * @brief Lemmat::lireHyphen
 * @param fichierHyphen : nom du fichier (avec le chemin absolu)
 * \brief stocke pour tous les lemmes contenus dans le fichier
 * l'information sur la césure étymologique (non-phonétique).
 */
void Lemmat::lireHyphen(QString fichierHyphen)
{
    foreach (Lemme *l, _lemmes.values()) l->setHyphen("");
    if (!fichierHyphen.isEmpty())
    {
        QStringList lignes = lignesFichier(fichierHyphen);
        foreach (QString linea, lignes)
        {
            QStringList ecl = linea.split('|');
#ifdef DEBOG
            if (ecl.count() != 2)
            {
                qDebug () << "ligne mal formée" << linea;
                continue;
            }
#endif
            ecl[1].replace('-',Ch::separSyll);
            Lemme *l = lemme(Ch::deramise(ecl[0]));
            if (l!=NULL)
                l->setHyphen(ecl[1]);
#ifdef DEBOG
            else qDebug () << linea << "erreur lireHyphen";
#endif
        }
    }
}

QString Lemmat::tagTexte(QString t, int p, bool affTout)
{
    // éliminer les chiffres et les espaces surnuméraires
    t.remove(QRegExp("\\d"));
//    t = t.simplified(); // Rmq : perd les retours de ligne !
    int tl = t.length() - 1;
    const QString pp = ".;!?";
    int dph = p;
    bool tout = false;
    if (p < 0)
    {
        p = 0;
        dph = 0;
        tout = true; // Pour faire tout le texte, phrase par phrase.
    }
    else
    {
        if ((dph > 0) && pp.contains(t.at(dph))) --dph;
        // Si j'ai cliqué sur une ponctuation, je traite la phrase qui précède.
        // régression au début de la phrase
        while (dph > 0 && !pp.contains(t.at(dph)) && (t.mid(dph,2) != "\n\n")) --dph;
        if (dph != 0) dph += 1; // J'élimine la ponctuation de la phrase précédente.
    }

    // conteneur pour les résultats
    QStringList lsv;
    // progression jusqu'en fin de phrase
    int fph = p;
    while (fph < tl)
    {
        while (fph < tl && !pp.contains(t.at(fph)) && (t.mid(fph,2) != "\n\n")) ++fph;
        QString phr = t.mid(dph, fph - dph).trimmed();
        // Si le texte se termine sans ponctuation, je perds le dernier caractère.
//        qDebug() << tl << fph << t.at(tl);
        if ((fph == tl) && !pp.contains(t.at(tl)) && (t.mid(tl,1) != "\n"))
            phr.append(t[tl]);
        // découpage en mots
        QStringList lm = phr.split(QRegExp("\\b"));

        if (lm.size() > 1)
        {
            // Il y a au moins un mot...
            while (Ch::abrev.contains(lm[lm.size()-2]))
            {
                // Ma phrase se terminait par une abréviation : je continue.
                fph++;
                while (fph < tl && !pp.contains(t.at(fph))) ++fph;
                phr = t.mid(dph, fph - dph).trimmed();
                if ((fph == tl) && !pp.contains(t.at(tl)) && (t.mid(tl,1) != "\n"))
                    phr.append(t[tl]);
                lm = phr.split(QRegExp("\\b"));
            }

            QList<Mot*> mots;
            // lemmatisation pour chaque mot
            for (int i = 1; i < lm.length(); i += 2)
            {
                bool debVers = !_majPert || lm[i-1].contains("\n");
                Mot * mot = new Mot(lm[i],(i-1)/2, debVers,this); // TODO : Vérifier si on a des vers avec majuscule...
                mots.append(mot);
            }  // fin de boucle de lemmatisation pour chaque mot
            Mot * mot = new Mot("",mots.size(),true,this); // Fin de phrase
            mots.append(mot); // J'ajoute un mot virtuel en fin de phrase avec le tag "snt".

            if (_trigram.isEmpty()) lisTags(true);
            // Si je n'ai pas encore chargé les trigrammes, je dois le faire maintenant.

            QStringList sequences;
            QList<double> probabilites;
            sequences.append("snt");
            probabilites.append(1.0);
            double branches = 1.0; // Pour savoir combien de branches a l'arbre.
            // Je suis en début de phrase : je n'ai que le tag "snt" et une proba de 1.
            for (int i = 0; i < mots.size(); i++)
            {
                Mot *mot = mots[i];
                QStringList lTags = mot->tags(); // La liste des tags possibles pour le mot
                QStringList nvlSeq; // Nouvelle liste des séquences possibles
                QList<double> nvlProba; // Nouvelle liste des probas.
                // Je dois ajouter tous les tags possibles à toutes les sequences et calculer les nouvelles probas.
                int sSeq = sequences.size();
                int sTag = lTags.size();
                if (sTag == 0) continue; // J'ignore pour l'instant les mots inconnus, cf. plus bas.
                branches *= sTag;
                for (int j = 0; j < sSeq; j++)
                {
                    QString bigr = sequences[j].right(7); // Le bigramme terminal
                    long prTot = 0;
                    QList<long> pr;
                    for (int k = 0; k < sTag; k++)
                    {
                        QString seq = bigr + " " + lTags[k];
                        long p = mot->proba(lTags[k]) * (4 * _trigram[seq] + 1);
                        pr << p;
                        prTot += p;
                    }
                    // J'ai tout ce qui dépend de k et la somme pour normaliser.
                    if (prTot == 0)
                    {
                        prTot = 1;
                        //qDebug() << mot->forme() << "proba nulle ! " << sequences[j];
                    }
                    for (int k = 0; k < sTag; k++)
                    {
                        nvlSeq.append(sequences[j] + " " + lTags[k]);
                        nvlProba.append(probabilites[j] * pr[k] / prTot);
                        // Si j'avais gardé toutes les séquences, ce serait une vraie probabilité (normalisée à 1)
                    }
                }
                // Ajouter les enclitiques.
                if (!mot->tagEncl().isEmpty())
                {
                    QString ajout = " " + mot->tagEncl();
                    for (int j = 0; j < nvlSeq.size(); j++) nvlSeq[j].append(ajout);
                    // Comme toutes les formes à tag unique, l'enclitique ne change pas les probabilités.
                }
                // J'ai toutes les sequences et leur proba.
                // Pour chaque bigramme terminal, je ne dois garder que la séquence la plus probable.
                // En faisant ce tri, je fais une sélection sur le tag i-2 (attention aux mots avec enclitique).
                // Si je veux garder une info sur l'ordre des tags du mot i-2, c'est maintenant !
                if (i > 1)
                {
                    // Le mot i-2 existe !
                    int debut = nvlSeq[0].size() - 11;
                    if (!mot->tagEncl().isEmpty()) debut -= 4; // Je dois reculer d'un tag de plus.
                    if (!mots[i-1]->tagEncl().isEmpty()) debut -= 4; // Je dois reculer d'un tag de plus.
                    if (!mots[i-2]->tagEncl().isEmpty()) debut -= 4; // Je dois reculer d'un tag de plus.
                    // Le tag du mot i-2 est nvlSeq[j].mid(debut, 3);
                    for (int j = 0; j < nvlSeq.size(); j++) mots[i-2]->setBestOf(nvlSeq[j].mid(debut, 3), nvlProba[j]);
                }
                sequences.clear();
                probabilites.clear();
//                qDebug() << mot->forme() << nvlProba << nvlSeq;
                for (int j = 0; j < nvlSeq.size(); j++) if (nvlProba[j] > 0)
                {
                    QString bigr = nvlSeq[j].right(7); // Les deux derniers tags
                    QString seq = "";
                    double val = -1;
                    QString seq2 = "";
                    double val2 = -1;
                    for (int k = j; k < nvlSeq.size(); k += sTag) // Pour retrouver le bigramme terminal, il faut au moins le même dernier tag.
                        if (bigr == nvlSeq[k].right(7))
                        {
                            if (val2 < nvlProba[k])
                            {
                                // J'y passe au moins une fois au début.
                                // La séquence mérite la 1ère ou la 2e place.
                                if (val < nvlProba[k])
                                {
                                    // 1ère place !
                                    val2 = val;
                                    seq2 = seq;
                                    val = nvlProba[k];
                                    seq = nvlSeq[k];
                                }
                                else
                                {
                                    // Seulement la 2e place
                                    val2 = nvlProba[k];
                                    seq2 = nvlSeq[k];
                                }
                            }
                            nvlProba[k] = -1; // Pour ne pas considérer deux fois les mêmes séquences.
                        }
                    // val et seq correspondent aux proba et séquence avec le bigramme considéré qui ont la plus grande proba.
                    sequences << seq;
                    probabilites << val;
                    if (val2 > 0)
                    {
                        // J'ai une deuxième séquence assez probable.
                        sequences << seq2;
                        probabilites << val2;
                    }
                }
        //        qDebug() << mot->forme() << sSeq << sTag << nvlSeq.size() << sequences.size();
                if (sequences.size() == 0) break;
            } // fin de la phrase.

            // Les probas associées aux tags du dernier vrai mot.
            if (mots.length() > 1)
            {
                // Le mot mots.length()-2 existe !
                int debut = sequences[0].size() - 7;
                if (!mots[mots.length()-2]->tagEncl().isEmpty()) debut -= 4; // Je dois reculer d'un tag de plus.
                // Le tag du mot mots.length()-2 est sequences[j].mid(debut, 3);
                for (int j = 0; j < sequences.size(); j++)
                    mots[mots.length()-2]->setBestOf(sequences[j].mid(debut, 3), probabilites[j]);
            }
            // Le tri final !
            QString seq = "";
            double val = -1;
            QString seq2 = "";
            double val2 = -1;
            for (int i = 0; i < sequences.size(); i++)
                if (val2 < probabilites[i])
                {
                    if (val < probabilites[i])
                    {
                        val2 = val;
                        seq2 = seq;
                        val = probabilites[i];
                        seq = sequences[i];
                    }
                    else
                    {
                        val2 = probabilites[i];
                        seq2 = sequences[i];
                    }
                }

            lsv.append(phr);
            lsv.append("<ul>");
            QString prob = "<br/> avec la proba : %1 pour %2 branches.<br/>";
            lsv.append(seq + prob.arg(val).arg(branches));
            if (val2 > 0)
            {
                prob = "Deuxième choix avec la proba : %1 <br/> %2<br/>";
                lsv.append(prob.arg(val2).arg(seq2));
            }

            seq = seq.mid(4); // Je supprime le premier tag qui est "snt".
            for (int i = 0; i < mots.size()-1; i++)
                if (!mots[i]->inconnu()) // Les mots inconnus ne figurent pas dans la séquence (cf. plus haut)
                {
                    lsv.append(mots[i]->choisir(seq.left(3), affTout));
                     // Si enclitique mid(8)
                    if (mots[i]->tagEncl().isEmpty()) seq = seq.mid(4);
                    else seq = seq.mid(5 + mots[i]->tagEncl().size());
                }
                else lsv.append("<li>" + mots[i]->forme() + " : non trouvé</li>");

            lsv.append("</ul>");
            if (tout) lsv << "<br/>";
            else return lsv.join("\n");
        }
        dph = fph + 1;
        fph++;
    }
    return lsv.join("\n");
}

void Lemmat::verbaCognita(QString fichier,bool vb)
{
    _hLem.clear();
    _couleurs.clear();
    if (vb && !fichier.isEmpty())
    {
        // Couleurs par défaut
        _couleurs << "#00A000"; // vert
        _couleurs << "#000000"; // noir
        _couleurs << "#A00000"; // rouge
        QFile file(fichier);
        if (file.open(QFile::ReadOnly | QFile::Text))
        {
            QTextStream in(&file);
            QString ligne = in.readLine();
            while (ligne.startsWith("!") || ligne.isEmpty()) ligne = in.readLine();
            // Je saute les commentaires et les lignes vides.
            int i = 0;
            while (ligne.startsWith("#") &&  !in.atEnd())
            {
                if ((i<3) && (ligne.size() == 7)) _couleurs[i] = ligne;
                i+=1;
                ligne = in.readLine();
            }
            // Je peux changer les couleurs dans le fichier
            MapLem item;
            while (!in.atEnd())
            {
                if (!ligne.startsWith("!") && !ligne.isEmpty()) // hLem.insert(ligne,1);
                {
                    item = lemmatiseM (ligne, false, false);
                    foreach (Lemme *lem, item.keys())
                        _hLem.insert(lem->cle(),0);
                }
                ligne = in.readLine();
            }
        }
    }
}

void Lemmat::verbaOut(QString fichier)
{
    if (_hLem.isEmpty()) return; // Rien à sauver !
    QString format = "%1\t%2\n";
    QFile file(fichier);
    if (file.open(QFile::WriteOnly | QFile::Text))
        foreach (QString lem, _hLem.keys())
    {
            file.write(format.arg(lem).arg(_hLem[lem]).toUtf8());
    }
}
