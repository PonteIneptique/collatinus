'''       maj.cpp      '''

#include <QApplication>
#include <QDir>
#include <QFileDialog>
#include <QFileInfo>
#include <QMessageBox>
#include <QPushButton>
#include <QVBoxLayout>

#include "maj.h"

#include <QDebug>

Maj.Maj(bool dic, *parent) : QDialog(parent)
    _dico = dic
    QLabel *icon = QLabel
    icon.setPixmap(QPixmap(":/res/collatinus.ico"))
    # label d'information
    QString texte =
        tr("Sur Collatinus peut se greffer une collection "
           "de lexiques et de dictionnaires. À l'installation, "
           "on ne dispose que d'une partie de ces ressources. "
           "Pour en ajouter, faut se rendre sur le site "
           "(<em>http:#outils.biblissima.fr/fr/collatinus/</em>), "
           "consulter la liste des fichiers disponibles et leur "
           "version, les télécharger en notant bien l'endroit "
           "où on les enregistre.<br/>\n"
           "Lorsque ce sera fait, faudra aller les chercher en "
           "cliquant sur le bouton <em>Installer les paquets téléchargés</em> "
           "ci-dessous.<br/>\n"
           "Il est conseillé de revenir régulièrement sur "
           "(<em>http:#outils.biblissima.fr/fr/collatinus/</em>) "
           "pour vérifier que l'on possède les dernières versions "
           "des lexiques et dictionnaires. Voici la liste de "
           "ce qui est installé sur cet ordinateur. "
           "Par exemple, nom\n"
           "<b>Lewis_and_Short_1879-fev16.cz</b>\n"
           "signifie que ce dictionnaire a été mis en ligne en février "
           "2016.\n<br>\n<table><tr><td>• ")
    # liste des lexiques et dictionnaires + version
    label = QLabel(self)
    label.setFont(self.font())
    label.setWordWrap(True)
    label.setAlignment(Qt.AlignJustify)
    # liste des paquets installés
    if dic:
#        texte.append("<ul>\n<li>")
        QDir chDicos(qApp.applicationDirPath() + "/data/dicos")
        lcfg = chDicos.entryList(QStringList() << "*.cfg")
        for (i = 0; i < lcfg.count(); ++i)
            lcfg[i].remove(".cfg")
            if lcfg[i][lcfg[i].size() - 6] == '-':
                date = lcfg[i].section("-",-1)
                lcfg[i] = lcfg[i].section("-",0,-2)
                lcfg[i].append("&nbsp;</td><td>&nbsp;" + date)


        texte.append(lcfg.join("</td></tr>\n<tr><td>• "))
#        texte.append(lcfg.join("</li>\n<li>"))
#        texte.append("</li>\n</ul>")

    else:
        # Les lexiques.
#        texte.append("<br>\n<table><tr><td>• ")
        QDir chDicos(qApp.applicationDirPath() + "/data")
        lcfg = chDicos.entryList(QStringList() << "lem*.*")
        for (i = 0; i < lcfg.count(); ++i)
            QFile fi(qApp.applicationDirPath() + "/data/" + lcfg[i])
            fi.open(QFile.ReadOnly|QFile.Text)
            blabla = fi.readLine()
            blabla = fi.readLine()
            if blabla.startsWith("not ")) blabla = blabla.mid(1:
            lcfg[i].append("&nbsp;</td><td>&nbsp;" + blabla)
            blabla = fi.readLine()
            lcfg[i].append("&nbsp;</td><td>&nbsp;" + blabla.mid(1))
            fi.close()

        texte.append(lcfg.join("</td></tr>\n<tr><td>• "))

    texte.append("</td></tr></table>")
    label.setText(texte)

    # barre de boutons
    QPushButton *installButton =
        QPushButton("Installer les paquets téléchargés")
    QPushButton *cloreButton = QPushButton("Fermer")
    QHBoxLayout *bottomLayout = QHBoxLayout
    bottomLayout.addStretch()
    bottomLayout.addWidget(installButton)
    bottomLayout.addWidget(cloreButton)

    QVBoxLayout *verticalLayout = QVBoxLayout(self)
    verticalLayout.addWidget(icon)
    verticalLayout.addWidget(label)
    verticalLayout.addLayout(bottomLayout)

    # Connexions
    installButton.clicked.connect(self.selectionne)
    cloreButton.clicked.connect(self.close)


def installe(self, nfcol):
    # ouverture
    QFile fcol(nfcol)
    fcol.open(QFile.ReadOnly)
    # lecture des adresses en queue de fichier
    fcol.seek(fcol.size() - 100)
    QStringList lignes
    while (not fcol.atEnd()) lignes << fcol.readLine().trimmed()
    if not lignes[1].contains(":"):
        QMessageBox.critical(
                    self, tr("Collatinus 11"),
                    tr("Impossible de comprendre le fichier" + nfcol.toUtf8() +
                       ". Le format semble être inadéquat."))
        return False

#        qDebug() << lignes

    if _dico:
        # nom du paquet
        nom = QFileInfo(nfcol).baseName()
        # Supprimer les versions antérieures
        nomSansDate = nom.section("-",0,-2) + "*.*"
        QDir rep(qApp.applicationDirPath() + "/data/dicos",nomSansDate)
        lfrem = rep.entryList()
#        qDebug() << lfrem
        for n in lfrem:
            QFile.remove(qApp.applicationDirPath() + "/data/dicos/" + n)

        # fichiers destination
        QString nf(qApp.applicationDirPath() + "/data/dicos/" + nom + ".")
        nfcz = nf + lignes[1].section(":",0,0)
        # Taille du 1er morceau
        taille = lignes[1].section(':', 1, 1).toLongLong()
        # Créations
        QFile fcz(nfcz)
        if not fcz.open(QFile.WriteOnly):
            QMessageBox.critical(
                        self, tr("Collatinus 11"),
                        tr("Impossible de créer le fichier" + nfcz.toUtf8() +
                           ". Vérifiez vos drois d'accès, éventuellent "
                           "connectez-vous en administrateur avant de lancer Collatinus."))
            return False

        # écriture cz
        fcol.reset()
        fcz.write(fcol.read(taille))
        fcz.close()
        # décompression et écriture des autres
        for (i = 2; i<lignes.size(); i++)
            fcz.setFileName(nf + lignes[i].section(":",0,0))
            taille = lignes[i].section(':', 1, 1).toLongLong()
            fcz.open(QFile.WriteOnly)
            fcz.write(qUncompress(fcol.read(taille)))
            fcz.close()

        # fermeture
        fcol.close()

    else:
        # installer un lexique
        # nom du paquet
        nom = QFileInfo(nfcol).baseName()
#        qDebug() << nom
        # fichiers destination
        QString nfDest(qApp.applicationDirPath() + "/data/")
        if nom.startsWith("lemmes")) nfDest.append("lemmes.":
        elif nom.startsWith("lem_ext")) nfDest.append("lem_ext.":
        else return False
        '''
        if QFile.exists(nfDest):
            QFile.remove(nfDest)
        # On ne peut pas copier si le fichier existe déjà
        QFile.copy(nfcol,nfDest);'''
        fcol.reset()
        QFile fcz
#        qDebug() << lignes.size() << lignes[1]
        # décompression et écriture des lexiques
        for (i = 1; i<lignes.size(); i++)
            fcz.setFileName(nfDest + lignes[i].section(":",0,0))
#            qDebug() << fcz.fileName()
            taille = lignes[i].section(':', 1, 1).toLongLong()
            fcz.open(QFile.WriteOnly)
            fcz.write(qUncompress(fcol.read(taille)))
            fcz.close()

        # fermeture
        fcol.close()

    return True


def selectionne(self):
    if _dico:
        nfichiers = QFileDialog.getOpenFileNames(
                    self, "Sélectionner un ou plusieurs paquets", QDir.homePath(),
                    "paquets dictionnaires (*.col)")
        listeF = nfichiers

    else:
        nfichiers = QFileDialog.getOpenFileNames(
                    self, "Sélectionner un ou plusieurs paquets", QDir.homePath(),
                    "paquets lexiques (*.col)")
        listeF = nfichiers

    if (listeF.empty()) return
    OK = True
    for nfcol in listeF:
        if _dico or nfcol.contains("/lemmes") or nfcol.contains("/lem_ext"):
            OK1 = installe(nfcol)
            if (OK1) qDebug() << "installé" << nfcol
            OK = False

    # info
    if (OK) QMessageBox.information(self, tr("Collatinus 11"),
                             tr("L'installation s'est bien passée. "
                                "Au prochain lancement, nouveaux lexiques "
                                "et dictionnaires seront disponibles."))
'''
    # Provisoirement, j'utilise la mise à jour pour créer les .col à partir des djvu.
    nfichiers = QFileDialog.getOpenFileNames(
        self, "Sélectionner un ou plusieurs paquets", qApp.applicationDirPath() + "/data/dicos/",
#        "dictionnaires djvu (*.djvu)")
                "lexiques (*.*)")
    listeF = nfichiers
    if (listeF.empty()) return
    OK = True
    for nfcol in listeF:
#        OK1 = djvu2col(nfcol)
        OK1 = lem2col(nfcol)
        if (OK1) qDebug() << "installé" << nfcol
        OK = False

    # info
    if (OK) QMessageBox.information(self, tr("Collatinus 11"),
                             tr("La copie s'est bien passée. "))
'''


void Maj.setFont(QFont font) { label.setFont(font);

'''*
 * @brief Maj.djvu2col
 * @param nfdjvu
 * @return
 *
 * Fonction provisoire pour créer un fichier .col à partir
 * des fichiers djvu, et cfg présents dans /data/dicos.
 * C'est une fonction que je suis seul à utiliser, seule fois.
 * Les utilisateurs utiliseront la fonction "installe" qui fait le contraire,
 * i.e. installer les fichiers djvu, et cfg dans /data/dicos
 * à partir d'un .col placé ailleurs.
 *
 '''
def djvu2col(self, nfdjvu):
    # nom du paquet
    nom = QFileInfo(nfdjvu).baseName()
    # fichiers destination
    QString nf(qApp.applicationDirPath() + "/data/dicos/" + nom)
    QString nfcol("/Users/Philippe/Documents/dicos_C11/" + nom + ".col")
    nfidx = nf + ".idx"
    nfcfg = nf + ".cfg"
    #qDebug() << nfdjvu << nfcol << nf

    if QFile.exists(nfcol):
        QFile.remove(nfcol)
    # On ne peut pas copier si le fichier existe déjà
    QFile.copy(nfdjvu,nfcol)
    # Je copie le fichier dans /Users/Philippe/Documents/dicos_C11/.
    QFile fcol(nfcol)
    if (not fcol.open(QFile.ReadWrite)) return False
    fcol.seek(fcol.size())

    QFile fzi(nfidx)
    fzi.open(QFile.ReadOnly|QFile.Text)
    lin = fzi.readAll()
    fzi.close()

    p = fcol.pos()
    #qDebug() << p
    nn = "%1:%2\n"
    ba = qCompress(lin.toUtf8(),9)
    fcol.write(ba)
    piedDeFichier = "\n"
    piedDeFichier += nn.arg("djvu").arg(p)
    piedDeFichier += nn.arg("idx").arg(ba.size())

    fzi.setFileName(nfcfg)
    fzi.open (QFile.ReadOnly|QFile.Text)
    baIn = fzi.readAll()
    fzi.close()

    ba = qCompress(baIn,9)
    p = fcol.pos()
    fcol.write(ba)
    piedDeFichier += nn.arg("cfg").arg(ba.size())

    n = 100 - piedDeFichier.size()
    #        if (n<1) n += 64
    #qDebug() << n
    piedDeFichier.prepend(QString(n,' '))
    fcol.write(piedDeFichier.toUtf8())

    fcol.close()
    return True


'''*
 * @brief Maj.lem2col
 * @param nfLem
 * @return
 *
 * Fonction provisoire pour créer un fichier .col à partir
 * des fichiers djvu, et cfg présents dans /data/dicos.
 * C'est une fonction que je suis seul à utiliser, seule fois.
 * Les utilisateurs utiliseront la fonction "installe" qui fait le contraire,
 * i.e. installer les fichiers djvu, et cfg dans /data/dicos
 * à partir d'un .col placé ailleurs.
 *
 '''
def lem2col(self, nfLem):
    # nom du paquet
    nom = QFileInfo(nfLem).baseName()
    ext = QFileInfo(nfLem).suffix()
    # fichiers destination
    QString nfcol("/Users/Philippe/Documents/dicos_C11/" + nom + "_" + ext + "-avr17.col")
    QFile fcol(nfcol)
    if (not fcol.open(QFile.WriteOnly)) return False

    QFile fLem(nfLem)
    fLem.open(QFile.ReadOnly|QFile.Text)
    lin = fLem.readAll()
    fLem.close()

    nn = "%1:%2\n"
    ba = qCompress(lin.toUtf8(),9)
    fcol.write(ba)
    piedDeFichier = "\n"
    piedDeFichier += nn.arg(ext).arg(ba.size())
    n = 100 - piedDeFichier.size()
    #        if (n<1) n += 64
    #qDebug() << n
    piedDeFichier.prepend(QString(n,' '))
    fcol.write(piedDeFichier.toUtf8())

    fcol.close()
    return True

