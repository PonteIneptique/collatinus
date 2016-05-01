/*                           lewis.cpp
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

#include "dicos.h"

#include <QDebug>

/****************
 * Dictionnaire *
 ****************/

/**
 * \fn Dictionnaire::Dictionnaire (QString cfg, QObject *parent):
 * QObject(parent)
 * \brief Initialise le dictionnaire avec les données trouvées dans le fichier
 * cfg
 * \param cfg : nom du fichier de configuration
 */
Dictionnaire::Dictionnaire(QString cfg, QObject *parent) : QObject(parent)
{
    QFileInfo fi(cfg);
    repertoire = qApp->applicationDirPath() + "/data/dicos/";
    // éviter de redéfinir partout le répertoire de travail.
    n = fi.baseName().section('.', 0);
    // lire le fichier de ressource cfg
    QSettings settings(repertoire + cfg, QSettings::IniFormat);
    settings.setIniCodec("utf-8");
    settings.beginGroup("droits");
    auteur = settings.value("auteur").toString();
    url = settings.value("url").toString();
    settings.endGroup();
    settings.beginGroup("fichiers");
    chData = repertoire + settings.value("data").toString();
    debut = settings.value("debut").toInt();
    echelle = settings.value("echelle").toString();
    if (echelle.isEmpty()) echelle = "160";
    idxJv = repertoire + n + ".idx";
    settings.endGroup();
    settings.beginGroup("remplacements");
    cond_jv = settings.value("condjv").toString();
    ji = settings.value("ji").toInt();
    JI = settings.value("JI").toInt();
    settings.endGroup();
    settings.beginGroup("style");
    xsl = settings.value("xsl").toInt();
    settings.endGroup();
    xml = QFileInfo(chData).suffix() == "cz" ||
          QFileInfo(chData).suffix() == "xml";
    djvu = !xml;
}

/**
 * \fn Dictionnaire::nom
 * \return le nom du dictionnaire
 */
QString Dictionnaire::nom() { return n; }
/**
 * \fn chopNum (const QString c)
 * \brief Renvoie une copie de c tronquée de tous les caractères
 *        numériques qui la terminent.
 */
QString Dictionnaire::chopNum(const QString c)
{
    QString ret = c;
    while (ret.right(1).at(0).isNumber()) ret.chop(1);
    return ret;
}

/**
 * \fn Dictionnaire::entree_pos
 *
 * \brief Lit l'article du dictionnaire qui débute à la position pos
 * \param pos : entier 64 avec la position du début de l'article dans le fichier
 * \return Le texte de l'article en HTML
 */
QString Dictionnaire::entree_pos(qint64 pos, qint64 taille)
{
    QFile fz(chData);
    fz.open(QFile::ReadOnly);
    fz.seek(pos);
    QByteArray ba = fz.read(taille);
    QString linea = QString::fromUtf8(qUncompress(ba));
    fz.close();
    linea.replace("H1>", "strong>");
    linea.prepend("<br/>\n");
    return linea;
}

/**
 * \fn Dictionnaire::vide_index
 * \brief * Efface l'index du dictionnaire djvu.
 *          Cf. lis_index_djvu ()
 */
void Dictionnaire::vide_index() { idxDjvu.clear(); }
/**
 * \fn Dictionnaire::vide_ligneLiens
 *
 * Efface la ligne de liens vers les divers articles qui s'affichent dans une
 * page xml
 *
 * Jamais utilisée.
 */
void Dictionnaire::vide_ligneLiens() { ligneLiens.clear(); }
/**
 * \fn Dictionnaire::lis_index_djvu
 *
 * Lit le fichier d'index du dico en djvu
 *
 * Cf. vide_index ()
 * @return false si la lecture échoue
 */
bool Dictionnaire::lis_index_djvu()
{
    QFile f(idxJv);
    if (!f.open(QIODevice::ReadOnly | QIODevice::Text)) return false;
    QTextStream ts(&f);
    while (!f.atEnd())
    {
        idxDjvu << f.readLine().trimmed();
    }
    f.close();
    return true;
}

/**
 * \fn Dictionnaire::pageDjvu
 * \brief Extrait du fichier djvu la page demandée au format TIF
 * qui sera affichée dans le navigateur.
 * \param p : numéro de la page du dictionnaire à afficher
 * \return le texte HTML pour afficher la page de dictionnaire
 */
QString Dictionnaire::pageDjvu(int p)
{
#ifdef Q_OS_MAC
    QString sortie_qt = QDir::homePath() + "/.pagefelix.tif";
    QString sortie_ddjvu = QDir::homePath() + "/.pagefelix.tif";
    QString ddjvu = "/Applications/DjView.app/Contents/bin/ddjvu";
#else
#ifdef Q_OS_WIN32
    QProcessEnvironment env = QProcessEnvironment::systemEnvironment();
    QString sortie_ddjvu =
        QDir::toNativeSeparators(env.value("TMP") + "/pagefelix.tif");
    QString sortie_qt = QDir::tempPath() + "/pagefelix.tif";
#else
    QString sortie_qt = QDir::homePath() + "/.pagefelix.tif";
    QString sortie_ddjvu = QDir::homePath() + "/.pagefelix.tif";
    QString ddjvu = "/usr/bin/ddjvu";
#endif
#endif
    QStringList args;
    args << "-format=tif"
         << "-page=" + QString::number(p) << "-scale=" + echelle << chData
         << sortie_ddjvu;
    QObject *parent = new QObject;
    QProcess *proc = new QProcess(parent);
    proc->setWorkingDirectory(qApp->applicationDirPath());
    QString pg;
#ifdef Q_OS_WIN32
    QString ddjvu = "ddjvu.exe";
    proc->start(ddjvu, args);
#else
    if (!QFile::exists(ddjvu))
    {
        QTextStream(&pg) << "<html><h2>Il faut installer DjView.app\n"
                            "dans le dossier Applications.<br>\n"
                            "<a "
                            "href=\"http://sourceforge.net/projects/djvu/files/"
                            "DjVuLibre_MacOS/\">\n"
                            "DjVuLibre_MacOS</a></h2></html>";
    }
    {
        proc->start(ddjvu, args);
    }
#endif
    proc->waitForFinished(-1);
    if ((proc->error() == QProcess::ReadError) || (proc->exitCode()))
        QTextStream(&pg) << "<html><strong>Fichier djvu ou " << sortie_ddjvu
                         << " introuvable</strong><br>\n"
                            "Sous Linux, installer le paquet djview<br>\n"
                            "Collatinux X.1 - Licence GNU-GPL</html>";
    else
    {
        QTextStream(&pg) << "<html>" << auteur << "<a href=\"" << url << "\">"
                         << url << "</a><div>" << ligneLiens
                         << "</div><div><img src=\"" << sortie_qt << "\"></div>"
                         << ligneLiens << "</html>";
    }
    delete proc;
    return pg;
}

/**
 * \fn Dictionnaire::pageDjvu
 *
 * Crée la ligne de liens correspondants aux différents lemmes présents dans la
 * requête, req.
 * Convertit la page contenant l'item n° no dans la liste req en TIF.
 * Retourne le texte HTML complet.
 *
 * Appelle pageDjvu (int p)
 * @param req : QStringList contenant le résultat de la lemmatisation
 * @param no : numéro de l'item affiché
 * @return le texte HTML qui affiche l'image de la page du dictionnaire djvu
 */
QString Dictionnaire::pageDjvu(QStringList req, int no)
{
    // seul le lemme n° noLien est affiché, les autres sont en hyperliens.
    // Si l'index chargé est le bon, inutile de le relire.
    QString leLem = req[no];
    if (idxDjvu.isEmpty())
    {
        lis_index_djvu();
    }
    pdj = debut;
    foreach (QString l, idxDjvu)
    {
        if (QString::compare(l, leLem, Qt::CaseInsensitive) > 0)
        {
            break;
        }
        ++pdj;
    }
    ligneLiens.clear();
    foreach (QString lien, req)
        ligneLiens.append("<a href=\"" + lien + "\">" + lien + "</a>&nbsp;");
    return pageDjvu(pdj);
}

/**
 * \fn QString Dictionnaire::pageXml (QStringList req)
 * \brief Renvoie les entrées du dictionnaire xml actif
 *        demandées par lReq.
 */
QString Dictionnaire::pageXml(QStringList lReq)
{
    QString pg;  // contenu de la page de retour
    QList<llew> listeE;
    QFile fi(idxJv);
    if (!fi.open(QFile::ReadOnly | QFile::Text))
    {
        prec = "error";
        suiv = "error";
        return "Error";
    }
    ligneLiens.clear();
    prec.clear();

    foreach (QString req, lReq)
    {
        qint64 debut = 0;
        qint64 fin = fi.size() - 1;
        QString lin;
        bool fini = false;
        // int idebug=0;
        int c = 1;
        qint64 milieu;
        while (!fini)
        {
            // milieu = (debut+fin)/2;
            // fi.seek(milieu);

            // Je recale milieu sur le début de ligne, pour qu'au tour
            // d'après début et fin soient sur des débuts de lignes.
            fi.seek((debut + fin) / 2);
            fi.readLine();
            milieu = fi.pos();
            if (milieu >= fin)
            {
                fi.seek(debut);
                fi.readLine();
                milieu = fi.pos();
            }
            if (milieu < fin)
            {
                lin = fi.readLine().simplified();
                QString e = lin.section(':', 0, 0);
                c = QString::compare(e, req, Qt::CaseInsensitive);
                if (c == 0)
                    fini = true;
                else if (c < 0)
                    debut = milieu;
                else
                    fin = milieu;
            }
            else
                fini = true;
        }
        // Je sors de la boucle quand j'ai trouvé la requête (c == 0)
        // ou quand elle n'est pas satisfaite et qu'il n'y a plus espoir.

        // La requête n'est pas exactement l'entrée du dico.
        // Je dois encore lire la ligne
        if (c != 0)
        {
            if (fi.atEnd())
            {
                // Le mot demandé est après le dernier du dico
                fi.seek(debut);
            }
            lin = fi.readLine().simplified();
        }

        fini = false;  // Je dois sortir au moins une ligne.
        QStringList ecl = lin.split(':');
        while (!fini)
        {
            llew dpos;
            dpos.pos = ecl.at(1).toLongLong();
            if (ecl.size() > 5)
            {
                dpos.article = ecl.at(5).trimmed();
                dpos.taille = ecl.at(2).toLongLong();
                prec = ecl.at(3);
                suiv = ecl.at(4);
                tailleprec = ecl.at(3).toLongLong();
            }
            else
            {
                dpos.article = ecl.at(0).trimmed();
                dpos.taille = ecl.at(2).toLongLong();
                prec = ecl.at(3);
                suiv = ecl.at(4);
            }
            listeE.append(dpos);
            // Ne pas lire au-delà de la fin du fichier
            if (fi.atEnd())
                fini = true;
            else
            {
                lin = fi.readLine().simplified();
                ecl = lin.split(':');
                QString eSansNum = ecl[0];
                if (eSansNum[eSansNum.size() - 1].isDigit()) eSansNum.chop(1);
                fini =
                    (QString::compare(eSansNum, req, Qt::CaseInsensitive) != 0);
            }
        }
    }
    fi.close();
    int i = 0;
    while (i < listeE.size())
    {
        if (ligneLiens.contains("<a href=\"#" + listeE[i].article + "\">"))
            listeE.removeAt(i);
        else
        {
            ligneLiens.append("<a href=\"#" + listeE[i].article + "\">" +
                              listeE[i].article + "</a> ");
            ++i;
        }
    }
    for (int i = 0; i < listeE.size(); i++)
    {
        pg.append("\n<div id=\"" + listeE[i].article + "\">");
        pg.append("</div><div>" + ligneLiens + "</div><div>");
        QString np = entree_pos(listeE[i].pos, listeE[i].taille);
        pg.append(np);
        pg.append("</div>");
    }
    if (QFile::exists(repertoire + n + ".css"))
    {
        pg.prepend("<link rel=\"stylesheet\" href=\"" + repertoire + n +
                   ".css\" type=\"text/css\" />\n");
    }
    pg.prepend(auteur + " <a href=\"http://" + url + "\">" + url + "</a> ");
    return pg;
}

/**
 * \fn QString Dictionnaire::page (QStringList req, int no)
 * \brief Fonction de relais qui oriente la requête req vers
 *        les fonctions spécialisées de consultation djvu ou xml.
 */
QString Dictionnaire::page(QStringList req, int no)
{
    if (xml)
        return pageXml(req);
    else  // djvu
    {
        _liens = req;
        return pageDjvu(req, no);  // passage de req pour les hyperliens
    }
}

/**
 * \fn bool Dictionnaire::estXml ()
 * \brief Renvoie vrai si le dictionnaire actif est au
 *        format xml, faux dans le cas contraire.
 */
bool Dictionnaire::estXml() { return xml; }
/**
 * \fn QString Dictionnaire::pgPrec ()
 * \brief Fonction de navigation, page précédente.
 */
QString Dictionnaire::pgPrec() { return prec; }
/**
 * \fn QString Dictionnaire::pgSuiv ()
 * \brief Fonction de navigation, page suivante.
 */
QString Dictionnaire::pgSuiv() { return suiv; }
/**
 * \fn int Dictionnaire::noPageDjvu ()
 * \brief Renvoie le numéro de la dernière page de
 *        dictionnaire djvu consultée.
 */
int Dictionnaire::noPageDjvu() { return pdj; }
/**
 * \fn QString Dictionnaire::indexJv ()
 * \brief Renvoie le nom du fichier du dictionnaire
 *        djvu courant.
 */
QString Dictionnaire::indexJv() { return idxJv; }
/**
 * \fn QStringList Dictionnaire::liens ()
 * \brief Renvoie le code html des liens de la page de
 *        dictionnaire affichée.
 */
QStringList Dictionnaire::liens() { return _liens; }
/****************
*    ListeDic   *
*****************/

/**
 * \fn Dictionnaire * ListeDic::dictionnaire_par_nom (QString nom)
 * \brief Renvoie L'objet Dictionnaire dont le nom
 *        correpond à la chaîne nom.
 */
Dictionnaire *ListeDic::dictionnaire_par_nom(QString nom)
{
    QMap<QString, Dictionnaire *>::iterator retour = liste.find(nom);
    if (retour == liste.end()) return NULL;
    return retour.value();
}

/**
 * \fn void ListeDic::ajoute (Dictionnaire *d)
 * \brief Ajoute le dictionnaire d à la liste des
 *        dictionnaires.
 */
void ListeDic::ajoute(Dictionnaire *d) { liste.insert(d->nom(), d); }
/**
 * \fn void ListeDic::change_courant (QString nom)
 * \brief Déclare le dictionnaire de nom nom comme
 *        dictionnaire courant.
 */
void ListeDic::change_courant(QString nom)
{
    currens = dictionnaire_par_nom(nom);
}

/**
 * \fn Dictionnaire * ListeDic::courant ()
 * \brief Renvoie l'ojet dictionnaire courant.
 *
 */
Dictionnaire *ListeDic::courant() { return currens; }
/**
 * \fn void ListeDic::change_courant2 (QString nom)
 * \brief Comme change_courant, mais pour le
 *        dictionnaire supplémentaire.
 */
void ListeDic::change_courant2(QString nom)
{
    currens2 = dictionnaire_par_nom(nom);
}

/**
 * \fn Dictionnaire * ListeDic::courant2 ()
 * \brief Comme courant(), mais pour le dictionnaire
 *        supplémentaire
 */
Dictionnaire *ListeDic::courant2() { return currens2; }
/**
 * \fn QString Dictionnaire::ramise (QString f)
 * \brief Essaie de convertir la chaîne f pour qu'elle
 *        ait une graphie ramiste (avec des 'v' et des
 *        'j'), et renvoie le résultat.
 *
 */
QString Dictionnaire::ramise(QString f)
{
    if (!ji)
        f = f.replace(QRegExp("(^|[aeo]+|^in|^ad|^per)i([aeiou])"), "\\1j\\2");
    f = f.replace(QRegExp("(^|[aeio]+|^in|^ad|^per)u([aeiou])"), "\\1v\\2");
    f = f.replace(QRegExp("(^|[\\w]+r)u([aeiou])"), "\\1v\\2");
    return f;
}

/*
   Copie du fichier téléchargé L&S en xml dans
   ressources ; Création d'un index, à ensuite
   dédoubler en transformant v en u et j en i. Il
   faudra enfin trier les deux par ordre alphabétique,
   et éliminer la première ligne, qui ne correspond à
   aucune entrée.
*/
/*
bool andromeda (QString nf)
{
    QFile fandr (nf);
    if (!fandr.open (QFile::ReadOnly | QFile::Text))
        return false;
    // QFile::copy (nf, qApp->applicationDirPath () + "/data/lewis.xml");
    QFile findex (qApp->applicationDirPath () + "/data/lewis.idx");
    // QFile::copy (nf, qApp->applicationDirPath () + "/data/ducange.xml");
    // QFile findex (qApp->applicationDirPath () + "/data/du.idx");
    if (!findex.open (QFile::WriteOnly | QFile::Text))
        return false;
    QString linea;
    QString cle;
    QTextStream fli (&findex);
    fli.setCodec ("UTF-8");
    qint64 p;
    fandr.seek (0);
    while (!fandr.atEnd ())
    {
       // flux.flush ();
       p = fandr.pos ();
       linea = fandr.readLine ();
       // int pos = exp.indexIn (linea);
       // ducange :
       //QRegExp expr ("(<H1>)([^<]+)(</H1>)");
       //int pos = expr.indexIn (linea);
       //if (pos > -1)
       //{
       //    cle = expr.cap (2);
       //   fli << cle << ":" << p  << "\n";
       //}

       // pour lewis
       QRegExp exp ("(^.*key=\")([^\"]+)(\".*$)");
       int pos = exp.indexIn (linea);
       if (pos > -1)
       {
           cle = exp.cap (2);
           fli << cle << ":" << p  << "\n";
       }
    }
    fandr.close ();
    findex.close ();
    return true;
}
*/

/*
   // Ramiste
   QStringList exceptions;
   exceptions << "Achaia" << "Aglaia" << "aio" << "ambubaia" << "baia" <<
   "Baiae"
    << "Caia" << "caiatio" << "Caieta" << "caio" << "Graii" << "Graioceli"
    << "Isaias" << "Laiades" << "maia" << "Panchaia";
*/

/*
// Dans le cas de téléchagement à partir
// d'Andromeda :
    cle.replace (QChar (0x0100), 'A');
    cle.replace (QChar (0x0101), 'a');
    cle.replace (QChar (0x0102), 'A');
    cle.replace (QChar (0x0103), 'a');
    cle.replace (QChar (0x0112), 'E');
    cle.replace (QChar (0x0113), 'e');
    cle.replace (QChar (0x0114), 'E');
    cle.replace (QChar (0x0115), 'e');
    cle.replace (QChar (0x012a), 'I');
    cle.replace (QChar (0x012b), 'i');
    cle.replace (QChar (0x012c), 'I');
    cle.replace (QChar (0x012d), 'i');
    cle.replace (QChar (0x014c), 'O');
    cle.replace (QChar (0x014d), 'o');
    cle.replace (QChar (0x014e), 'O');
    cle.replace (QChar (0x014f), 'o');
    cle.replace (QChar (0x016a), 'U');
    cle.replace (QChar (0x016b), 'u');
    cle.replace (QChar (0x016c), 'U');
    cle.replace (QChar (0x016d), 'u');
    // quelques caractères inusités :
    cle.replace (QChar (0x0233), 'y');
    cle.replace (QChar (0x0304), 'i');
    cle.replace (QChar (0x0306), 'i');
    cle.replace (QChar (0x5e), "");     // ^
    // non ramiste ! mais traiter les composés
    // de iacio
    if (cle.endsWith ("jicio"))
    {
    cle.replace ("jicio", "icio");
    }
    else
    {
    cle.replace ('j', 'i');
    }
    cle.replace ('J', 'I');
    cle.replace ('v', 'u');
    cle.replace ('V', 'U');
*/