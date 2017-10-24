'''   mainwindow.cpp
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
#include <QPrintDialog>
#include <QPrinter>

#include "flexion.h"
#include "mainwindow.h"
#include "maj.h"

'''*
 * \fn EditLatin.EditLatin (QWidget *parent): QTextEdit (parent)
 * \brief Créateur de la classe EditLatin, de
 * QTextEdit afin de pouvoir redéfinir l'action
 * connectée au clic de souris sur un mot ou après
 * sélection d'une portion de texte.
 '''
EditLatin.EditLatin(QWidget *parent) : QTextEdit(parent)
    mainwindow = qobject_cast<MainWindow *>(parent)


'''*
 * \fn bool EditLatin.event(QEvent *event)
 * \brief Captation du survol de la souris pour
 *        afficher dans une bulle lemmatisation et
 *        analyses morphologiques.
 '''
def event(self, *event):
    switch (event.type())
        case QEvent.ToolTip:
            QHelpEvent *helpEvent = static_cast<QHelpEvent *>(event)
            P = mapFromGlobal(helpEvent.globalPos())
            tc = cursorForPosition(P)
            tc.select(QTextCursor.WordUnderCursor)
            mot = tc.selectedText()
            if mot.isEmpty ():
                return QWidget.event (event)
            txtBulle = mainwindow.lemmatiseur.lemmatiseT(
                mot, True, True, True, False)
            if (txtBulle.isEmpty()) return True
            # S'il n'y a qu'une ponctuation sous le curseur la lemmatisation donne un string vide.
            txtBulle.prepend("<p style='white-space:pre'>")
            txtBulle.append("</p>")
            QRect rect(P.x()-20,P.y()-10,40,40); # Je définis un rectangle autour de la position actuelle.
            QToolTip.setFont(font())
            QToolTip.showText(helpEvent.globalPos(), txtBulle.trimmed(),
                               self, rect); # La bulle disparaît si le curseur sort du rectangle.
            return True

        default:
            return QTextEdit.event(event)



'''*
 * \fn void EditLatin.mouseReleaseEvent (QMouseEvent *e)
 * \brief Captation de la fin du clic de souris : ajout
 *        des lemmatisations et analyses morpho dans
 *        le dock correspondant.
 '''
def mouseReleaseEvent(self, *e):
    cursor = textCursor()
    if not cursor.hasSelection()) cursor.select(QTextCursor.WordUnderCursor:
    st = cursor.selectedText()
    unSeulMot = not st.contains(' ')
    ml = mainwindow.lemmatiseur.lemmatiseM(st)
    # 1. dock de lemmatisation
    if not mainwindow.dockLem.visibleRegion().isEmpty():
        if unSeulMot and mainwindow.calepAct.isChecked():
            foreach (Lemme *l, ml.keys())
                mainwindow.textEditLem.append(l.ambrogio())
        else:
            if mainwindow.html():
                texteHtml = mainwindow.textEditLem.toHtml()
                texteHtml.insert(texteHtml.indexOf("</body>"),mainwindow.lemmatiseur.lemmatiseT(st))
                mainwindow.textEditLem.setText(texteHtml)
                mainwindow.textEditLem.moveCursor(QTextCursor.End)

            else:
                mainwindow.textEditLem.insertPlainText(
                    mainwindow.lemmatiseur.lemmatiseT(st))


    # 2. dock scansion
    if not mainwindow.dockScand.visibleRegion().isEmpty():
        accent = mainwindow.lireOptionsAccent()
        mainwindow.textEditScand.append(
            mainwindow.lemmatiseur.scandeTxt(st, accent, False))

    if unSeulMot:
        # 3. dock de flexion
        if not mainwindow.dockFlex.visibleRegion().isEmpty():
            if not ml.empty():
                mainwindow.textBrowserFlex.clear()
                mainwindow.textBrowserFlex.append(
                    mainwindow.flechisseur.tableaux(&ml))
                mainwindow.textBrowserFlex.moveCursor(QTextCursor.Start)


        # 4. dock dictionnaires
        lemmes = mainwindow.lemmatiseur.lemmes(ml)
        if not mainwindow.dockDic.visibleRegion().isEmpty():
            mainwindow.afficheLemsDic(lemmes)
        if mainwindow.wDic.isVisible() and mainwindow.syncAct.isChecked():
            mainwindow.afficheLemsDicW(lemmes)
        # 5. dock Syntaxe
        if not mainwindow.dockTag.visibleRegion().isEmpty():
            mainwindow.tagger(toPlainText(),textCursor().position())


    QTextEdit.mouseReleaseEvent(e)


'''*
 * \fn MainWindow.MainWindow()
 * \brief Créateur de la fenêtre de l'appli.
 *        Les différentes tâches sont regrouppées
 *        et confiées à des fonctions spécialisées.
 '''
MainWindow.MainWindow()
    QFile styleFile(":/res/collatinus.css")
    styleFile.open(QFile.ReadOnly)
    QString style(styleFile.readAll())
    qApp.setStyleSheet(style)

    editLatin = EditLatin(self)
    setCentralWidget(editLatin)

    lemmatiseur = Lemmat(self)
    flechisseur = Flexion(lemmatiseur)

    setLangue()

    createStatusBar()
    createActions()
    createDockWindows()
    createDicWindow()
    createMenus()
    createToolBars()
    createConnections()
    createDicos()
    createDicos(False)
    createCibles()

    setWindowTitle(tr("Collatinus 11"))
    setWindowIcon(QIcon(":/res/collatinus.svg"))

    setUnifiedTitleAndToolBarOnMac(True)

    # setTabPosition(Qt.BottomDockWidgetArea, QTabWidget.North )

    readSettings()


'''*
 * \fn void MainWindow.afficheLemsDic (bool litt, prim)
 * \brief Surcharge. Récupère le contenu de la ligne de saisie du
 *        dock des dictionnaires si prim est à True,
 *        sinon la ligne de saisie de la fenêtre
 *        supplémentaire. Ce contenu est lemmatisé si litt
 *        est à False, la ou les pages/entrées
 *        correspondantes sont affichées, dans le
 *        dock, dans la fenêtre supplémentaire.
 '''
def afficheLemsDic(self, litt, prim):
    QLineEdit *lineEdit
    if prim:
        lineEdit = lineEditDic
    else:
        lineEdit = lineEditDicW
    if (lineEdit.text().isEmpty()) return
    lemsDic.clear()
    QStringList requete
    if not litt:
        lm = lemmatiseur.lemmatiseM(lineEdit.text(), True)
        requete = lemmatiseur.lemmes(lm)

    else:
        t = lineEdit.text()
        t.replace("æ","ae")
        t.replace("Æ","Ae")
        t.replace("œ","oe")
        t.replace("Œ","Oe")
        requete << t

    if requete.empty()) requete << lineEdit.text(:
    requete.removeDuplicates()
    if syncAct.isChecked():
        if not dockDic.visibleRegion().isEmpty():
            afficheLemsDic(requete, 0)
        if wDic.isVisible():
            afficheLemsDicW(requete, 0)

    elif prim:
        afficheLemsDic(requete, 0)
    else:
        afficheLemsDicW(requete, 0)
    lineEdit.selectAll()
    lineEdit.setFocus()


'''*
 * \fn void MainWindow.afficheLemsDicLitt()
 * \brief Fonction de relais permettant d'utiliser
 *        la connexion entre une action et la fonction
 *        afficheLemsDic().
 '''
def afficheLemsDicLitt(self):
    afficheLemsDic(True)


'''*
 * \fn void MainWindow.afficheLemsDicW () * \brief Fonction de relais
 * permettant d'utiliser
 *        la connexion entre une action et la fonction
 *        afficheLemsDicW().
 *
 '''
def afficheLemsDicW(self):
    afficheLemsDic(False, False)


'''*
 * \fn afficheLemsDic(True,False)
 * \brief
 * \brief Fonction de relais permettant d'utiliser
 *        la connexion entre une action et la fonction
 *        afficheLemsDicW(), lemmatisation.
 '''
def afficheLemsDicLittW(self):
    afficheLemsDic(True, False)


'''*
 * \fn void MainWindow.afficheLemsDic(QStringList ll, no)
 * \brief Affiche la page ou les entrées de
 * dictionnaire correspondant au lemme d'ordre no de la
 * liste ll, règle le texte des boutons de
 * navigation.
 '''
def afficheLemsDic(self, ll, no):
    if (textBrowserDic == 0) return
    lemsDic = ll
    if (ll.empty() or no < 0 or listeD.courant() == NULL) return
    textBrowserDic.clear()
    textBrowserDic.setHtml(listeD.courant().page(ll, no))
    lineEditDic.setText(ll.at(no))
    if listeD.courant().estXml():
        anteButton.setText(listeD.courant().pgPrec())
        postButton.setText(listeD.courant().pgSuiv())

    else:
        anteButton.setText(tr("Retro"))
        postButton.setText(tr("Porro"))
        labelLewis.setText(QString.number(listeD.courant().noPageDjvu()))

    textBrowserDic.moveCursor(QTextCursor.Start)


'''*
 * \fn void MainWindow.afficheLemsDicW(QStringList ll, no)
 * \brief comme afficheLemsDic, pour le
 * dictionnaire supplémentaire.
 *
 '''
def afficheLemsDicW(self, ll, no):
    if (textBrowserW == 0) return
    # lemsDic = ll
    if (ll.empty() or no < 0 or listeD.courant2() == NULL) return
    textBrowserW.clear()
    textBrowserW.setHtml(listeD.courant2().page(ll, no))
    lineEditDicW.setText(ll.at(no))
    if listeD.courant2().estXml():
        anteButtonW.setText(listeD.courant2().pgPrec())
        postButtonW.setText(listeD.courant2().pgSuiv())

    else:
        anteButtonW.setText(tr("Retro"))
        postButtonW.setText(tr("Porro"))
        labelLewisW.setText(QString.number(listeD.courant2().noPageDjvu()))

    textBrowserW.moveCursor(QTextCursor.Start)


'''*
 * \fn void MainWindow.afficheLien (QUrl url)
 * \brief Prend en charge l'affichage des hyperliens de
 *        navigations insérés dans les pages/entrées
 *        des dictionnaires.
 *
 '''
def afficheLien(self, url):
    if (listeD.courant().estXml()) return
    # la ligne de liens en tête de page doit être gardée
    liens = listeD.courant().liens()
    no = liens.indexOf(url.toString())
    if (no < 0) no = 0
    afficheLemsDic(liens, no)


'''*
 * \fn void MainWindow.afficheLienW (QUrl url)
 * \brief Comme afficheLien, le dictionnaire
 * supplémentaire.
 '''
def afficheLienW(self, url):
    if (listeD.courant2().estXml()) return
    # la ligne de liens en tête de page doit être gardée
    liens = listeD.courant2().liens()
    no = liens.indexOf(url.toString())
    if (no < 0) no = 0
    afficheLemsDicW(liens, no)


'''*
 * \fn void MainWindow.alpha()
 * \brief Force la lemmatisation alphabétique de
 *        tout le texte, que soit l'option alpha
 *        du lemmatiseur.
 '''
def alpha(self):
    # pour que l'action provoque le basculement à True
    # de l'option alpha du lemmatiseur, la
    # première et la dernière ligne.
    tmpAlpha = lemmatiseur.optAlpha()
    lemmatiseur.setAlpha(True)
    lancer()
    #	lemmatiseTxt()
    lemmatiseur.setAlpha(tmpAlpha)


'''*
 * \fn void MainWindow.apropos ()
 * \brief Affiche les informations essentielles au
 *        sujet de Collatinus 11.
 '''
def apropos(self):
    QMessageBox.about(
        self, tr("Collatinus 11"),
        tr("<b>COLLATINVS</b><br/>\n"
           "<i>Linguae latinae lemmatizatio </i><br/>\n"
           "Licentia GPL, © Yves Ouvrard, 2009 - 2016 <br/>\n"
           "Nonnullas partes operis scripsit Philippe Verkerk<br/>\n"
           "Versio " VERSION "<br/><br/>\n"
           "Gratias illis habeo :<br/><ul>\n"
           "<li>William Whitaker †</li>\n"
           "<li>Jose Luis Redrejo</li>\n"
           "<li>Georges Khaznadar</li>\n"
           "<li>Matthias Bussonier</li>\n"
           "<li>Gérard Jeanneau</li>\n"
           "<li>Jean-Paul Woitrain</li>\n"
           "<li><a href='http:#www.perseus.tufts.edu'>Perseus Digital Library </a></li>\n"
           "<li>Dominique Longrée et le <a href='http:#web.philo.ulg.ac.be/lasla/'>LASLA</a>\n</li></ul>"))


'''*
 * \fn void MainWindow.changeGlossarium (QString nomDic)
 * \brief Change le dictionnaire actif du dock
 * dictionnaires.
 *
 '''
def changeGlossarium(self, nomDic):
    listeD.change_courant(nomDic)
    if (listeD.courant() == NULL) return
    if listeD.courant().estXml():
        labelLewis.setText("↔");  # "\u2194"
    else:
        listeD.courant().vide_index()
        labelLewis.clear()

    if not lemsDic.empty():
        afficheLemsDic(lemsDic, lemsDic.indexOf(lineEditDic.text()))
    elif not lineEditDic.text().isEmpty():
        afficheLemsDic(QStringList() << lineEditDic.text())


'''*
 * \fn void MainWindow.changeGlossariumW (QString nomDic)
 * \brief Comme ChangeGlossarium, le dictionnaire
 *        supplémentaire.
 '''
def changeGlossariumW(self, nomDic):
    listeD.change_courant2(nomDic)
    if (listeD.courant2() == NULL) return
    if listeD.courant2().estXml():
        labelLewisW.setText("↔");  # "\u2194"
    else:
        listeD.courant2().vide_index()
        labelLewisW.clear()

    if not lemsDic.empty():
        afficheLemsDicW(lemsDic, lemsDic.indexOf(lineEditDicW.text()))
    elif not lineEditDicW.text().isEmpty():
        afficheLemsDicW(QStringList() << lineEditDicW.text())


'''*
 * \fn void MainWindow.changePageDjvu (int p, prim)
 * \brief Change la page d'un dictionnaire au format
 *        djvu, le dock dictionnaire si prim est à
 *        True, pour le dictionnaire
 *        supplémentaire.
 '''
def changePageDjvu(self, p, prim):
    QTextBrowser *browser
    QLabel *label
    if prim:
        browser = textBrowserDic
        label = labelLewis

    else:
        browser = textBrowserW
        label = labelLewisW

    browser.clear()
    if prim:
        browser.setHtml(listeD.courant().pageDjvu(p))
    else:
        browser.setHtml(listeD.courant2().pageDjvu(p))
    label.setText(QString.number(p))
    browser.moveCursor(QTextCursor.Start)


'''*
 * \fn void MainWindow.charger (QString f)
 * \brief Charge le fichier nommé f dans l'éditeur
 *        de texte latin.
 '''
def charger(self, f):
    QFile file(f)
    if not file.open(QFile.ReadOnly | QFile.Text):
        QMessageBox.warning(self, tr("Collatinus"),
                             tr("%1: Lecture impossible,\n%2.")
                                 .arg(nfAb)
                                 .arg(file.errorString()))
        return

    QTextStream in(&file)
    in.setCodec("UTF-8"); # Pour windôze !
    QApplication.setOverrideCursor(Qt.WaitCursor)
    contenu = in.readAll()
    file.close()
    editLatin.setPlainText(contenu)
    QApplication.restoreOverrideCursor()


'''*
 * \fn void MainWindow.clicAnte ()
 * \brief Gère le passage à la page précédente.
 '''
def clicAnte(self):
    if (not listeD.courant()) return
    listeD.courant().vide_ligneLiens()
    if listeD.courant().estXml():
        QStringList lBouton
        lBouton << anteButton.text()
        afficheLemsDic(lBouton)
        if syncAct.isChecked() and wDic.isVisible():
            afficheLemsDicW(lBouton)

    else:
        p = labelLewis.text().toInt()
        if p > 0) changePageDjvu(labelLewis.text().toInt() - 1:



'''*
 * \fn void MainWindow.clicAnteW()
 * \brief Comme clicAnte, le dictionnaire
 * supplémentaire.
 *
 '''
def clicAnteW(self):
    if (not listeD.courant2()) return
    listeD.courant2().vide_ligneLiens()
    if listeD.courant2().estXml():
        QStringList lBouton
        lBouton << anteButtonW.text()
        afficheLemsDicW(lBouton)
        if syncAct.isChecked() and not dockDic.visibleRegion().isEmpty():
            afficheLemsDic(lBouton)

    else:
        p = labelLewisW.text().toInt()
        if p > 0) changePageDjvu(labelLewisW.text().toInt() - 1, False:



'''*
 * \fn void MainWindow.clicPost ()
 * \brief Gère le passage du dictionnaire à la page
 *        suivante.
 '''
def clicPost(self):
    if (not listeD.courant()) return
    listeD.courant().vide_ligneLiens()
    if listeD.courant().estXml():
        QStringList lBouton
        lBouton << postButton.text()
        afficheLemsDic(lBouton)
        if syncAct.isChecked() and wDic.isVisible():
            afficheLemsDicW(lBouton)

    else:
        p = labelLewis.text().toInt()
        if (p < 8888)  # ATTENTION, la dernière page dans les cfg !
            changePageDjvu(labelLewis.text().toInt() + 1)



'''*
 * \fn void MainWindow.clicPostW()
 * \brief Comme clicPost, le dictionnaire
 *        supplémentaire.
 *
 '''
def clicPostW(self):
    if (not listeD.courant2()) return
    listeD.courant2().vide_ligneLiens()
    if listeD.courant2().estXml():
        QStringList lBouton
        lBouton << postButtonW.text()
        afficheLemsDicW(lBouton)
        if syncAct.isChecked() and not dockDic.visibleRegion().isEmpty():
            afficheLemsDic(lBouton)

    else:
        p = labelLewisW.text().toInt()
        if (p < 8888)  # ATTENTION, la dernière page dans les cfg !
            changePageDjvu(labelLewisW.text().toInt() + 1, False)



'''*
 * \fn void MainWindow.closeEvent(QCloseEvent *event)
 * \brief Enregistre certains paramètres le la session
 *        avant fermeture de l'application.
 '''
def closeEvent(self, *event):
    QSettings settings("Collatinus", "collatinus11")
    settings.beginGroup("interface")
    settings.setValue("langue", langueI)
    settings.endGroup()
    settings.beginGroup("fenetre")
    settings.setValue("geometry", saveGeometry())
    settings.setValue("windowState", saveState())
    settings.endGroup()
    settings.beginGroup("fichiers")
    if not nfAb.isEmpty()) settings.setValue("nfAb", nfAb:
    settings.endGroup()
    settings.beginGroup("options")
    # settings.setValue("police", font.family())
    settings.setValue("zoom", editLatin.font().pointSize())
    # options
    settings.setValue("alpha", alphaOptAct.isChecked())
    settings.setValue("html", htmlAct.isChecked())
    settings.setValue("formetxt", formeTAct.isChecked())
    settings.setValue("extensionlexique", extensionWAct.isChecked())
    settings.setValue("majpert", majPertAct.isChecked())
    settings.setValue("morpho", morphoAct.isChecked())
    settings.setValue("nonrec", nonRecAct.isChecked())
    settings.setValue("cible", lemmatiseur.cible())
    # accentuation
    settings.setValue("accentuation", accentAct.isChecked())
    settings.setValue("longue", longueAct.isChecked())
    settings.setValue("breve", breveAct.isChecked())
    settings.setValue("ambigue", ambigueAct.isChecked())
    settings.setValue("illius", illiusAct.isChecked())
    settings.setValue("hyphenation", hyphenAct.isChecked())
    settings.setValue("repHyphen", repHyphen)
    settings.setValue("ficHyphen", ficHyphen)
    settings.setValue("tagAffTout", affToutAct.isChecked())
    settings.setValue ("repVerba", repVerba)
    settings.endGroup()
    settings.beginGroup("dictionnaires")
    settings.setValue("courant", comboGlossaria.currentIndex())
    settings.setValue("wdic", wDic.isVisible())
    settings.setValue("courantW", comboGlossariaW.currentIndex())
    settings.setValue("posw", wDic.pos())
    settings.setValue("sizew", wDic.size())
    settings.setValue("sync", syncAct.isChecked())
    settings.setValue("secondDic",visibleWAct.isChecked())
    settings.endGroup()
    delete wDic
    QMainWindow.closeEvent(event)


def copie(self):
    QClipboard *clipboard = QApplication.clipboard()
    clipboard.clear()

    QString texte
    # if cbTexteLatin.isChecked()) texte.append(editLatin.toPlainText():
    if cbTexteLatin.isChecked()) texte.append(editLatin.toHtml():
    if cbLemmatisation.isChecked()) texte.append(textEditLem.toHtml():
    if cbScansion.isChecked()) texte.append(textEditScand.toHtml():
    QMimeData *mime = QMimeData
    mime.setHtml(texte)
    clipboard.setMimeData(mime)


'''*
 * \fn void MainWindow.createActions()
 * \brief Fonction appelée par le créateur. Initialise
 *        toutes les actions utilisées par
 *        l'application.
 '''
def createActions(self):
    '''
    undoAct = QAction(QIcon(":/images/undo.png"), tr("&Undo"), self)
    undoAct.setShortcuts(QKeySequence.Undo)
    undoAct.setStatusTip(tr("Undo the last editing action"))
    undoAct.triggered.connect(self.undo)
    # aussi SLOT(redo())
    '''
    alphaAct = QAction(QIcon(":res/edit-alpha.svg"),
                           tr("Lancer et classer &alphabétiquement"), self)
    aproposAct =
        QAction(QIcon(":/res/collatinus.svg"), tr("à &Propos"), self)
    auxAct =
        QAction(QIcon(":res/help-browser.svg"), tr("aide"), self)
    balaiAct = QAction(QIcon(":res/edit-clear.svg"),
                           tr("&Effacer les résultats"), self)
    copieAct = QAction(QIcon(":res/copie.svg"),
                           tr("&Copier dans un traitement de textes"), self)
    deZoomAct = QAction(QIcon(":res/dezoom.svg"), tr("Plus petit"), self)
    findAct = QAction(QIcon(":res/edit-find.svg"), tr("&Chercher"), self)
    fontAct = QAction(tr("Police de caractères"), self)
    lancAct = QAction(QIcon(":res/gear.svg"), tr("&Lancer"), self)
    majDicAct = QAction(tr("Installer les dictionnaires téléchargés"), self)
    majLexAct = QAction(tr("Installer les lexiques téléchargés"), self)
    nouvAct =
        QAction(QIcon(":/res/document-new.svg"), tr("&Nouveau"), self)
    ouvrirAct =
        QAction(QIcon(":/res/document-open.svg"), tr("&Ouvrir"), self)
    exportAct = QAction(QIcon(":res/pdf.svg"), tr("Exporter en pdf"), self)
    printAct = QAction(QIcon(":res/print.svg"), tr("Im&primer"), self)
    quitAct = QAction(QIcon(":/res/power.svg"), tr("&Quitter"), self)
    quitAct.setStatusTip(tr("Quitter l'application"))
    oteAAct = QAction(tr("Ôter les accents"), self)
    reFindAct = QAction(tr("Chercher &encore"), self)
    statAct = QAction(QIcon(":res/abacus.svg"), tr("S&tatistiques"), self)
    zoomAct = QAction(QIcon(":res/zoom.svg"), tr("Plus gros"), self)

    # langues d'interface
    enAct = QAction(tr("English Interface"), self)
    enAct.setCheckable(True)
    frAct = QAction(tr("Interface en français"), self)
    frAct.setCheckable(True)

    # raccourcis
    findAct.setShortcut(QKeySequence.Find)
    nouvAct.setShortcuts(QKeySequence.New)
    ouvrirAct.setShortcuts(QKeySequence.Open)
    printAct.setShortcuts(QKeySequence.Print)
    reFindAct.setShortcut(QKeySequence.FindNext)
#    reFindAct.setShortcut(QKeySequence(tr("Ctrl+J")))
    quitAct.setShortcut(
        QKeySequence(tr("Ctrl+Q")));  # QKeySequence.Quit inopérant
    lancAct.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_L)); # Raccourci pour lancer la lemmatisation ou la scansion du texte.

    # lemmatisation et options
    # ordre alpha
    alphaOptAct = QAction(tr("ordre alpha"), self)
    alphaOptAct.setCheckable(True)
    # calepino
    calepAct = QAction(tr("Calepino"), self)
    calepAct.setCheckable(True)
    # formes du texte dans la lemmatisation
    formeTAct = QAction(tr("avec formes"), self)
    formeTAct.setCheckable(True)
    # lemmatisation en html
    htmlAct = QAction(tr("format html"), self)
    htmlAct.setCheckable(True)
    # prise en compte des majuscules
    majPertAct = QAction(tr("majuscules"), self)
    majPertAct.setCheckable(True)
    # analyses morpho dans la lemmatisation
    morphoAct = QAction(tr("Morpho"), self)
    morphoAct.setCheckable(True)
    # non reconnus en fin de lemmatisation
    nonRecAct = QAction(tr("grouper échecs"), self)
    nonRecAct.setCheckable(True)

    # actions pour les accents
    accentAct = QAction(tr("accentuer"), self)
    accentAct.setCheckable(True)
    accentAct.setChecked(False)
    optionsAccent = QActionGroup(self)
    longueAct = QAction(tr("   -̆ => ¯ "), self)
    longueAct.setCheckable(True)
    breveAct = QAction(tr("   -̆ => ˘ "), self)
    breveAct.setCheckable(True)
    ambigueAct = QAction(tr("   -̆ => pas d'accent"), self)
    ambigueAct.setCheckable(True)
    ambigueAct.setChecked(True)
    illiusAct = QAction(tr("except illíus"), self)
    illiusAct.setCheckable(True)
    illiusAct.setChecked(True)
    hyphenAct = QAction(tr("marquer les syllabes"), self)
    hyphenAct.setCheckable(True)
    hyphenAct.setEnabled(False)
    optionsAccent.addAction(longueAct)
    optionsAccent.addAction(breveAct)
    optionsAccent.addAction(ambigueAct)
    optionsAccent.setEnabled(False)
    lireHyphenAct = QAction(tr("Lire les césures"),self)
    actionVerba_cognita = QAction(tr("Lire une liste de mots connus"),self)
    actionVerba_cognita.setCheckable(True)
    actionVerba_cognita.setChecked(False)
    verba_cognita_out = QAction(tr("Écrire l'emploi des mots connus"),self)

    # actions pour le serveur
    serverAct = QAction(tr("Serveur"), self)
    serverAct.setCheckable(True)
    serverAct.setChecked(False)

    # actions pour le tagger
    affToutAct = QAction(tr("tout afficher"),self)
    affToutAct.setCheckable(True)
    affToutAct.setChecked(True)

    # Restauration des docks
    dockRestoreAct = QAction(tr("Restaurer les docks"),self)

    # actions pour les dictionnaires
    dicAct = QAction(QIcon(":/res/dicolem.svg"),
                         tr("Lemmatiser et chercher"), self)
    dicLittAct = QAction(QIcon(":/res/dicolitt.svg"), tr("Chercher"), self)
    dicActW = QAction(QIcon(":/res/dicolem.svg"),
                          tr("Lemmatiser et chercher"), self)
    dicLittActW =
        QAction(QIcon(":/res/dicolitt.svg"), tr("Chercher"), self)
    # synchronisation des deux dictionnaires
    syncAct = QAction(tr("sync+"), self)
    syncAct.setCheckable(True);  # synchronisation des deux fenêtres
    syncDWAct = QAction(tr("sync."), self)
    syncWDAct = QAction(tr("<-sync"), self)
    visibleWAct = QAction(tr("Dictionnaire +"), self)
    visibleWAct.setCheckable(True)
    extensionWAct = QAction(tr("Extension du lexique"), self)
    extensionWAct.setCheckable(True)


'''*
 * \fn void MainWindow.createCibles()
 * \brief Initialise toutes les actions liées aux
 *        fonctions de traduction.
 '''
def createCibles(self):
    grCibles = QActionGroup(lexMenu)
    for cle in lemmatiseur.cibles().keys():
        QAction *action = QAction(grCibles)
        action.setText(lemmatiseur.cibles()[cle])
        action.setCheckable(True)
        lexMenu.addAction(action)
        action.triggered.connect(self.setCible)



'''*
 * \fn void MainWindow.createConnections()
 * \brief Initialisation des connections qui lancent
 *        toutes les actions des menus et des barres d'outils.
 '''
def createConnections(self):
    # synchroniser zoom et dezoom
    zoomAct.triggered.connect(editLatin.zoomIn)
    zoomAct.triggered.connect(textBrowserDic.zoomIn)
    zoomAct.triggered.connect(textBrowserW.zoomIn)
    zoomAct.triggered.connect(textBrowserFlex.zoomIn)
    zoomAct.triggered.connect(textEditLem.zoomIn)
    zoomAct.triggered.connect(textEditScand.zoomIn)

    deZoomAct.triggered.connect(editLatin.zoomOut)
    deZoomAct.triggered.connect(textBrowserDic.zoomOut)
    deZoomAct.triggered.connect(textBrowserW.zoomOut)
    deZoomAct.triggered.connect(textBrowserFlex.zoomOut)
    deZoomAct.triggered.connect(textEditLem.zoomOut)
    deZoomAct.triggered.connect(textEditScand.zoomOut)

    # connexions des lignes de saisie
    lineEditLem.returnPressed.connect(self.lemmatiseLigne)
    lineEditFlex.returnPressed.connect(self.flechisLigne)
    lineEditScand.returnPressed.connect(self.scandeLigne)

    # options et actions du lemmatiseur
    connect(alphaOptAct, SIGNAL(toggled(bool)), lemmatiseur,
            SLOT(setAlpha(bool)))
    connect(formeTAct, SIGNAL(toggled(bool)), lemmatiseur,
            SLOT(setFormeT(bool)))
    htmlAct.toggled.connect(self.setHtml)
    connect(majPertAct, SIGNAL(toggled(bool)), lemmatiseur,
            SLOT(setMajPert(bool)))
    connect(morphoAct, SIGNAL(toggled(bool)), lemmatiseur,
            SLOT(setMorpho(bool)))
    connect(nonRecAct, SIGNAL(toggled(bool)), lemmatiseur,
            SLOT(setNonRec(bool)))
    extensionWAct.toggled.connect(lemmatiseur.setExtension)

    # actions et options de l'accentuation
    accentAct.toggled.connect(self.setAccent)
    lireHyphenAct.triggered.connect(self.lireFichierHyphen)
    oteAAct.triggered.connect(self.oteDiacritiques)

    # lancer ou arrêter le serveur
    serverAct.toggled.connect(self.lancerServeur)
    # restaurer les docks
    dockRestoreAct.triggered.connect(self.dockRestore)

    # actions des dictionnaires
    anteButton.clicked.connect(self.clicAnte)
    connect(comboGlossaria, SIGNAL(currentIndexChanged(QString)), self,
            SLOT(changeGlossarium(QString)))
    dicAct.triggered.connect(self.afficheLemsDic)
    dicLittAct.triggered.connect(self.afficheLemsDicLitt)
    lineEditDic.returnPressed.connect(self.afficheLemsDicLitt)
    postButton.clicked.connect(self.clicPost)
    syncDWAct.triggered.connect(self.syncDW)
    connect(textBrowserDic, SIGNAL(anchorClicked(QUrl)), self,
            SLOT(afficheLien(QUrl)))

    anteButtonW.clicked.connect(self.clicAnteW)
    connect(comboGlossariaW, SIGNAL(currentIndexChanged(QString)), self,
            SLOT(changeGlossariumW(QString)))
    dicActW.triggered.connect(self.afficheLemsDicW)
    connect(dicLittActW, SIGNAL(triggered()), self,
            SLOT(afficheLemsDicLittW()))
    connect(lineEditDicW, SIGNAL(returnPressed()), self,
            SLOT(afficheLemsDicLittW()))
    majDicAct.triggered.connect(self.majDic)
    majLexAct.triggered.connect(self.majLex)
    postButtonW.clicked.connect(self.clicPostW)
    syncWDAct.triggered.connect(self.syncWD)
    connect(textBrowserW, SIGNAL(anchorClicked(QUrl)), self,
            SLOT(afficheLienW(QUrl)))
    visibleWAct.toggled.connect(self.montreWDic)

    # langue d'interface
    frAct.triggered.connect(self.langueInterface)
    enAct.triggered.connect(self.langueInterface)

    # autres actions
    alphaAct.triggered.connect(self.alpha)
    aproposAct.triggered.connect(self.apropos)
    auxAct.triggered.connect(self.auxilium)
    balaiAct.triggered.connect(self.effaceRes)
    copieAct.triggered.connect(self.dialogueCopie)
    exportAct.triggered.connect(self.exportPdf)
    findAct.triggered.connect(self.recherche)
    fontAct.triggered.connect(self.police)
    lancAct.triggered.connect(self.lancer)
    nouvAct.triggered.connect(self.nouveau)
    ouvrirAct.triggered.connect(self.ouvrir)
    printAct.triggered.connect(self.imprimer)
    quitAct.triggered.connect(self.close)
    reFindAct.triggered.connect(self.rechercheBis)
    statAct.triggered.connect(self.stat)
    actionVerba_cognita.toggled.connect(self.verbaCognita)
    verba_cognita_out.triggered.connect(self.verbaOut)


'''*
 * \fn void MainWindow.createDicos(bool prim)
 * \brief Chargement des index et des fichiers de
 *        configuration des dictionnaires.
 '''
def createDicos(self, prim):
    QComboBox *combo = 0
    if prim:
        combo = comboGlossaria
    else:
        combo = comboGlossariaW
    combo.clear()
    QDir chDicos(qApp.applicationDirPath() + "/data/dicos")
    lcfg = chDicos.entryList(QStringList() << "*.cfg")
    ldic.clear()
    for fcfg in lcfg:
        Dictionnaire *d = Dictionnaire(fcfg)
        listeD.ajoute(d)
        ldic << d.nom()

    combo.insertItems(0, ldic)


'''*
 * \fn void MainWindow.createMenus()
 * \brief Initialisation des menus à partir des actions définies
 *        dans MainWindow.createActions().
 *
 '''
def createMenus(self):
    fileMenu = menuBar().addMenu(tr("&Fichier"))
    fileMenu.addAction(nouvAct)
    fileMenu.addAction(ouvrirAct)
    fileMenu.addSeparator()
    fileMenu.addAction(copieAct)
    fileMenu.addAction(exportAct)
    fileMenu.addAction(printAct)
    fileMenu.addSeparator()
    fileMenu.addAction(oteAAct)
    fileMenu.addAction(lireHyphenAct)
    fileMenu.addAction(actionVerba_cognita)
    fileMenu.addAction(verba_cognita_out)
    fileMenu.addSeparator()
    fileMenu.addAction(quitAct)

    editMenu = menuBar().addMenu(tr("&Edition"))
    editMenu.addAction(findAct)
    editMenu.addAction(reFindAct)
    # editMenu.addAction(undoAct)

    viewMenu = menuBar().addMenu(tr("&Vue"))
    viewMenu.addAction(balaiAct)
    viewMenu.addAction(zoomAct)
    viewMenu.addAction(deZoomAct)
    viewMenu.addAction(fontAct)
    viewMenu.addSeparator()
    viewMenu.addAction(visibleWAct)
    viewMenu.addAction(dockRestoreAct)
    viewMenu.addSeparator()
    QActionGroup *frEngAg = QActionGroup(self)
    frAct.setActionGroup(frEngAg)
    enAct.setActionGroup(frEngAg)
    viewMenu.addAction(frAct)
    viewMenu.addAction(enAct)
    if langueI == "fr":
        frAct.setChecked(True)
    elif langueI == "en":
        enAct.setChecked(True)

    lexMenu = menuBar().addMenu(tr("&Lexique"))
    lexMenu.addAction(lancAct)
    lexMenu.addAction(alphaAct)
    lexMenu.addAction(statAct)
    lexMenu.addSeparator()
    lexMenu.addAction(extensionWAct)
    lexMenu.addSeparator()

    optMenu = menuBar().addMenu(tr("&Options"))
    optMenu.addAction(alphaOptAct)
    optMenu.addAction(formeTAct)
    optMenu.addAction(htmlAct)
    optMenu.addAction(majPertAct)
    optMenu.addAction(morphoAct)
    optMenu.addAction(nonRecAct)
    optMenu.addSeparator()
    optMenu.addAction(accentAct)
    #    optMenu.addAction(optionsAccent)
    optMenu.addAction(longueAct)
    optMenu.addAction(breveAct)
    optMenu.addAction(ambigueAct)
    optMenu.addAction(illiusAct)
    optMenu.addAction(hyphenAct)
    optMenu.addSeparator()
    optMenu.addAction(affToutAct)
#    optMenu.addAction(fontAct)
#    optMenu.addAction(majAct)

    extraMenu = menuBar().addMenu(tr("Extra"))
    extraMenu.addAction(serverAct)
    extraMenu.addAction(majDicAct)
    extraMenu.addAction(majLexAct)

    helpMenu = menuBar().addMenu(tr("&Aide"))
    helpMenu.addAction(auxAct)
    helpMenu.addAction(aproposAct)


'''*
 * \fn void MainWindow.createToolBars()
 * \brief Initialisation de la barre d'outils à partir
 *        des actions.
 '''
def createToolBars(self):
    toolBar = QToolBar(self)
    toolBar.setObjectName("toolbar")
    addToolBar(Qt.TopToolBarArea, toolBar)

    toolBar.addAction(nouvAct)
    toolBar.addAction(ouvrirAct)
    toolBar.addAction(copieAct)
    toolBar.addAction(zoomAct)
    toolBar.addAction(deZoomAct)
    toolBar.addAction(findAct)
    toolBar.addSeparator()
    toolBar.addAction(lancAct)
    toolBar.addAction(alphaAct)
    toolBar.addAction(statAct)
    toolBar.addAction(calepAct)
    toolBar.addAction(visibleWAct)
    toolBar.addAction(balaiAct)
    toolBar.addSeparator()
    toolBar.addAction(quitAct)


'''*
 * \fn void MainWindow.createStatusBar()
 * \brief Initialisation de la barre d'état. À compléter.
 *
 '''
void MainWindow.createStatusBar() {
'''*
 * \fn void MainWindow.createDockWindows()
 * \brief Initialisation des différents docks.
 *
 '''
def createDockWindows(self):
    dockLem = QDockWidget(tr("Lexique et morphologie"), self)
    dockLem.setObjectName("docklem")
    dockLem.setAllowedAreas(Qt.BottomDockWidgetArea |
                             Qt.RightDockWidgetArea)
    dockLem.setFloating(False)
    dockLem.setFeatures(QDockWidget.DockWidgetFloatable |
                         QDockWidget.DockWidgetMovable)
    dockWidgetLem = QWidget(dockLem)
    dockWidgetLem.setSizePolicy(QSizePolicy.Expanding,
                                 QSizePolicy.Expanding)
    QVBoxLayout *vLayoutLem = QVBoxLayout(dockWidgetLem)
    QHBoxLayout *hLayoutLem = QHBoxLayout()
    lineEditLem = QLineEdit(dockWidgetLem)
    # boutons d'options
    QToolButton *tbCalep = QToolButton(self)
    tbCalep.setDefaultAction(calepAct)
    QToolButton *tbMorpho = QToolButton(self)
    tbMorpho.setDefaultAction(morphoAct)
    QToolButton *tbAlpha = QToolButton(self)
    tbAlpha.setDefaultAction(alphaOptAct)
    QToolButton *tbFormeT = QToolButton(self)
    tbFormeT.setDefaultAction(formeTAct)
    QToolButton *tbHtml = QToolButton(self)
    tbHtml.setDefaultAction(htmlAct)
    QToolButton *tbMajPert = QToolButton(self)
    tbMajPert.setDefaultAction(majPertAct)
    QToolButton *tbNonRec = QToolButton(self)
    tbNonRec.setDefaultAction(nonRecAct)
    QSpacerItem *hSpacerLem = QSpacerItem(40, 20)
    hLayoutLem.addWidget(lineEditLem)
    hLayoutLem.addWidget(tbCalep)
    hLayoutLem.addWidget(tbMorpho)
    hLayoutLem.addWidget(tbAlpha)
    hLayoutLem.addWidget(tbFormeT)
    hLayoutLem.addWidget(tbHtml)
    hLayoutLem.addWidget(tbMajPert)
    hLayoutLem.addWidget(tbNonRec)
    hLayoutLem.addItem(hSpacerLem)
    textEditLem = QTextEdit(dockWidgetLem)
    vLayoutLem.addLayout(hLayoutLem)
    vLayoutLem.addWidget(textEditLem)
    dockLem.setWidget(dockWidgetLem)
#    qDebug() << dockLem.testAttribute(Qt.WA_DeleteOnClose) << dockWidgetLem.testAttribute(Qt.WA_DeleteOnClose)

    dockDic = QDockWidget(tr("Dictionnaires"), self)
    dockDic.setObjectName("dockdic")
    dockDic.setFloating(False)
    dockDic.setFeatures(QDockWidget.DockWidgetFloatable |
                         QDockWidget.DockWidgetMovable)
    dockDic.setAllowedAreas(Qt.BottomDockWidgetArea)
    dockWidgetDic = QWidget(dockDic)
    QVBoxLayout *vLayoutDic = QVBoxLayout(dockWidgetDic)
    QHBoxLayout *hLayoutDic = QHBoxLayout()
    lineEditDic = QLineEdit(dockWidgetDic)
    lineEditDic.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Fixed)
    lineEditDic.setMinimumWidth(40)
    # Lemmatisation + recherche
    QToolButton *tbDic = QToolButton(self)
    tbDic.setDefaultAction(dicAct)
    # recherche sans lemmatisation
    QToolButton *tbDicLitt = QToolButton(self)
    tbDicLitt.setDefaultAction(dicLittAct)
    # dictionnaire
    QToolButton *tbSync = QToolButton(self)
    tbSync.setDefaultAction(syncAct)
    tbSync.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed)
    tbSync.setMinimumWidth(40)
    tbSync.setMaximumSize(60, 24)
    QToolButton *tbDicW = QToolButton(self)
    tbDicW.setDefaultAction(visibleWAct)
    tbDicW.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Fixed)
    tbDicW.setMinimumWidth(40)
    tbDicW.setMaximumSize(90, 24)
    QToolButton *tbSyncDW = QToolButton(self)
    tbSyncDW.setDefaultAction(syncDWAct)
    tbSyncDW.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed)
    tbSyncDW.setMinimumWidth(40)
    tbSyncDW.setMaximumSize(60, 24)
    # choix des dictionnaires
    comboGlossaria = QComboBox(self)
    anteButton = QPushButton(self)
    labelLewis = QLabel(self)
    postButton = QPushButton(self)
#    QSpacerItem *hSpacerDic = QSpacerItem(40, 20)
    #, QSizePolicy.Expanding, QSizePolicy.Minimum)
    hLayoutDic.addWidget(lineEditDic)
    hLayoutDic.addWidget(tbDic)
    hLayoutDic.addWidget(tbDicLitt)
    hLayoutDic.addWidget(comboGlossaria)
    hLayoutDic.addWidget(anteButton)
    hLayoutDic.addWidget(labelLewis)
    hLayoutDic.addWidget(postButton)
#    hLayoutDic.addItem(hSpacerDic)
    hLayoutDic.addStretch()
    hLayoutDic.addWidget(tbSync)
    hLayoutDic.addWidget(tbDicW)
    hLayoutDic.addWidget(tbSyncDW)
    textBrowserDic = QTextBrowser(dockWidgetDic)
    textBrowserDic.setOpenExternalLinks(True)
    vLayoutDic.addLayout(hLayoutDic)
    vLayoutDic.addWidget(textBrowserDic)
    dockDic.setWidget(dockWidgetDic)

    dockScand = QDockWidget(tr("Scansion"), self)
    dockScand.setObjectName("dockscand")
    dockScand.setFloating(False)
    dockScand.setFeatures(QDockWidget.DockWidgetFloatable |
                           QDockWidget.DockWidgetMovable)
    dockScand.setAllowedAreas(Qt.BottomDockWidgetArea |
                               Qt.RightDockWidgetArea)
    dockWidgetScand = QWidget(dockScand)
    QVBoxLayout *vLayoutScand = QVBoxLayout(dockWidgetScand)
    QHBoxLayout *hLayoutScand = QHBoxLayout()
    lineEditScand = QLineEdit(dockWidgetScand)
    #QSpacerItem *hSpacerScand =
    #   QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    hLayoutScand.addWidget(lineEditScand)
    # ajouter ici des boutons...
    QToolButton *tbAccent = QToolButton(self)
    tbAccent.setDefaultAction(accentAct)
    QToolButton *tbLongue = QToolButton(self)
    tbLongue.setDefaultAction(longueAct)
    QToolButton *tbBreve = QToolButton(self)
    tbBreve.setDefaultAction(breveAct)
    QToolButton *tbAmbigue = QToolButton(self)
    tbAmbigue.setDefaultAction(ambigueAct)
    QToolButton *tbIllius = QToolButton(self)
    tbIllius.setDefaultAction(illiusAct)
    QToolButton *tbHyphen = QToolButton(self)
    tbHyphen.setDefaultAction(hyphenAct)
    hLayoutScand.addWidget(tbAccent)
    hLayoutScand.addWidget(tbLongue)
    hLayoutScand.addWidget(tbBreve)
    hLayoutScand.addWidget(tbAmbigue)
    hLayoutScand.addWidget(tbIllius)
    hLayoutScand.addWidget(tbHyphen)
    #    hLayoutScand.addItem (hSpacerScand)
    textEditScand = QTextEdit(dockWidgetScand)
    vLayoutScand.addLayout(hLayoutScand)
    vLayoutScand.addWidget(textEditScand)
    dockScand.setWidget(dockWidgetScand)

    dockFlex = QDockWidget(tr("Flexion"), self)
    dockFlex.setObjectName("dockflex")
    dockFlex.setFloating(False)
    dockFlex.setFeatures(QDockWidget.DockWidgetFloatable |
                          QDockWidget.DockWidgetMovable)
    dockFlex.setAllowedAreas(Qt.BottomDockWidgetArea)
    dockWidgetFlex = QWidget(dockFlex)
    QVBoxLayout *vLayoutFlex = QVBoxLayout(dockWidgetFlex)
    QHBoxLayout *hLayoutFlex = QHBoxLayout()
    lineEditFlex = QLineEdit(dockWidgetFlex)
    QSpacerItem *hSpacerFlex =
        QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    hLayoutFlex.addWidget(lineEditFlex)
    hLayoutFlex.addItem(hSpacerFlex)
    textBrowserFlex = QTextBrowser(dockWidgetFlex)
    textBrowserFlex.setSizePolicy(QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
    vLayoutFlex.addLayout(hLayoutFlex)
    vLayoutFlex.addWidget(textBrowserFlex)
    dockFlex.setWidget(dockWidgetFlex)

    dockTag = QDockWidget(tr("Tagger"), self)
    dockTag.setObjectName("dockTag")
    dockTag.setFloating(False)
    dockTag.setFeatures(QDockWidget.DockWidgetFloatable |
                          QDockWidget.DockWidgetMovable)
    dockTag.setAllowedAreas(Qt.BottomDockWidgetArea)
    dockWidgetTag = QWidget(dockTag)
    QVBoxLayout *vLayoutTag = QVBoxLayout(dockWidgetTag)
    QHBoxLayout *hLayoutTag = QHBoxLayout()
    textBrowserTag = QTextBrowser(dockWidgetTag)
    textBrowserTag.setSizePolicy(QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
    QLabel *lasla = QLabel(tr("Tagger probabiliste dérivé des <a href='http:#web.philo.ulg.ac.be/lasla/textes-latins-traites/'>textes du LASLA</a>"),self)
    lasla.setOpenExternalLinks(True)
    QToolButton *tbMajPertTag = QToolButton(self)
    tbMajPertTag.setDefaultAction(majPertAct)
    QToolButton *tbAffTout = QToolButton(self)
    tbAffTout.setDefaultAction(affToutAct)
    hLayoutTag.addWidget(lasla)
    hLayoutTag.addStretch()
    hLayoutTag.addWidget(tbMajPertTag)
    hLayoutTag.addWidget(tbAffTout)
    vLayoutTag.addLayout(hLayoutTag)
    vLayoutTag.addWidget(textBrowserTag)
    dockTag.setWidget(dockWidgetTag)

    addDockWidget(Qt.BottomDockWidgetArea, dockLem)
    addDockWidget(Qt.BottomDockWidgetArea, dockDic)
    addDockWidget(Qt.BottomDockWidgetArea, dockScand)
    addDockWidget(Qt.BottomDockWidgetArea, dockFlex)
    addDockWidget(Qt.BottomDockWidgetArea, dockTag)

    tabifyDockWidget(dockLem, dockDic)
    tabifyDockWidget(dockDic, dockScand)
    tabifyDockWidget(dockScand, dockFlex)
    tabifyDockWidget(dockScand, dockTag)

    setTabPosition(Qt.BottomDockWidgetArea, QTabWidget.North)
    dockLem.raise()


'''*
 * \fn void MainWindow.createDicWindow()
 * \brief Initialisation du widget de dictionnaire
 *        supplémentaire.
 '''
def createDicWindow(self):
    wDic = QWidget()
    wDic.setObjectName("wDic")
    QVBoxLayout *vLayout = QVBoxLayout(wDic)
    QHBoxLayout *hLayout = QHBoxLayout()
    lineEditDicW = QLineEdit(wDic)
    lineEditDicW.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Fixed)
    lineEditDicW.setMinimumWidth(40)
    # Lemmatisation + recherche
    QToolButton *tbDicW = QToolButton(self)
    tbDicW.setDefaultAction(dicActW)
    # recherche sans lemmatisation
    QToolButton *tbDicLittW = QToolButton(self)
    tbDicLittW.setDefaultAction(dicLittActW)
    comboGlossariaW = QComboBox(self)
    anteButtonW = QPushButton(self)
    labelLewisW = QLabel(self)
    postButtonW = QPushButton(self)
#    QSpacerItem *hSpacerDic = QSpacerItem(40, 20)
    #, QSizePolicy.Expanding, QSizePolicy.Minimum)
    QToolButton *tbSyncWD = QToolButton(self)
    tbSyncWD.setDefaultAction(syncWDAct)
    tbSyncWD.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed)
    tbSyncWD.setMinimumWidth(40)
    tbSyncWD.setMaximumSize(60, 24)
    hLayout.addWidget(lineEditDicW)
    hLayout.addWidget(tbDicW)
    hLayout.addWidget(tbDicLittW)
    hLayout.addWidget(comboGlossariaW)
    hLayout.addWidget(anteButtonW)
    hLayout.addWidget(labelLewisW)
    hLayout.addWidget(postButtonW)
#    hLayout.addItem(hSpacerDic)
    hLayout.addStretch()
    hLayout.addWidget(tbSyncWD)
    textBrowserW = QTextBrowser(wDic)
    textBrowserW.setOpenExternalLinks(True)
    vLayout.addLayout(hLayout)
    vLayout.addWidget(textBrowserW)


'''*
 * \fn void MainWindow.dialogueCopie()
 * \brief Ouvre une boite de dialogue qui permet de
 *        sélectionner les parties à copier, et
 *        les place dans le presse-papier du système
 '''
def dialogueCopie(self):
    QLabel *icon = QLabel
    icon.setPixmap(QPixmap(":/res/collatinus.ico"))
    QLabel *text = QLabel
    text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    text.setWordWrap(True)
    text.setText(
        "<p>Pour récupérer et modifier votre travail, meilleure manière est "
        "d'ouvrir le traitement de textes de votre choix, de sélectionner "
        "ci-dessous ce que vous voulez utiliser. Cliquez ensuite sur le bouton "
        "«Appliquer». Pour terminer, dans votre traitement de texte, "
        "et copiez votre sélection avec un raccourci clavier, l'option de "
        "menu <b>Édition/Coller</b>.")

    cbTexteLatin = QCheckBox(tr("Texte latin"))
    cbLemmatisation = QCheckBox(tr("Lemmatisation"))
    cbScansion = QCheckBox(tr("Scansion"))

    QPushButton *appliButton = QPushButton(tr("Appliquer"))
    QPushButton *cloreButton = QPushButton(tr("Fermer"))

    QVBoxLayout *topLayout = QVBoxLayout
    topLayout.addWidget(icon)
    topLayout.addWidget(text)

    QHBoxLayout *bottomLayout = QHBoxLayout
    bottomLayout.addStretch()
    bottomLayout.addWidget(appliButton)
    bottomLayout.addWidget(cloreButton)
    bottomLayout.addStretch()

    QVBoxLayout *mainLayout = QVBoxLayout
    mainLayout.addLayout(topLayout)
    topLayout.addWidget(cbTexteLatin)
    topLayout.addWidget(cbLemmatisation)
    topLayout.addWidget(cbScansion)
    mainLayout.addLayout(bottomLayout)

    QDialog dCopie(self)
    dCopie.setModal(True)
    dCopie.setWindowTitle(tr("Récupérer son travail"))
    dCopie.setLayout(mainLayout)

    appliButton.clicked.connect(self.copie)
    cloreButton.clicked.connect(&dCopie.close)
    dCopie.exec()


'''*
 * \fn bool MainWindow.dockVisible (QDockWidget *d)
 * \brief renvoie True si le dock d est visible.
 *
 '''
def dockVisible(self, *d):
    return not d.visibleRegion().isEmpty()


'''*
 * \fn void MainWindow.effaceRes()
 * \brief Efface le contenu des docs visibles.
 '''
def effaceRes(self):
    if dockVisible(dockLem)) textEditLem.clear(:
    if dockVisible(dockFlex)) textBrowserFlex.clear(:
    if dockVisible(dockScand)) textEditScand.clear(:
    if dockVisible(dockTag)) textBrowserTag.clear(:


'''*
 * \fn
 * \brief
 *
 '''
def exportPdf(self):
#ifndef QT_NO_PRINTER
    QString nf =
        QFileDialog.getSaveFileName(self, "Export PDF", QString(), "*.pdf")
    if not nf.isEmpty():
        if QFileInfo(nf).suffix().isEmpty()) nf.append(".pdf":
        QPrinter printer(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(nf)
        QTextEdit *tmpTE = QTextEdit()
        tmpTE.setHtml(editLatin.toHtml())
        tmpTE.append(textEditLem.toHtml())
        tmpTE.document().print(&printer)
        delete tmpTE

#endif


'''*
 * \fn void MainWindow.imprimer()
 * \brief Lance le dialogue d'impression pour la lemmatisation.
 '''
def imprimer(self):
#if not defined(QT_NO_PRINTER) and not defined(QT_NO_PRINTDIALOG)
    QPrinter printer(QPrinter.HighResolution)
    QPrintDialog *dlg = QPrintDialog(&printer, self)
    if textEditLem.textCursor().hasSelection():
        dlg.addEnabledOption(QAbstractPrintDialog.PrintSelection)
    dlg.setWindowTitle(tr("Imprimer le texte et le lexique"))
    if dlg.exec() == QDialog.Accepted:
        QTextEdit *tmpTE = QTextEdit()
        tmpTE.setHtml(editLatin.toHtml())
        tmpTE.append(textEditLem.toHtml())
        tmpTE.print(&printer)
        delete tmpTE

    delete dlg
#endif


'''*
 * \fn void MainWindow.langueInterface()
 * \brief Sonde les actions frAct et enAct, et
 *        bascule l'interface dans la langue de l'action cochée.
 '''
def langueInterface(self):
    if frAct.isChecked():
        langueI = "fr"

    elif enAct.isChecked():
        langueI = "en"

    else:
        langueI = "fr"
    QMessageBox.about(self, tr("Collatinus 11"),
                       tr("Le changement de langue prendra effet"
                          "au prochain lancement de Collatinus."))


'''*
 * \fn void MainWindow.flechisLigne()
 * \brief Provoque l'affichage des lemmes pouvant donner
 *        la forme affichée dans la ligne de saisie du dock
 *        Flexion.
 '''
def flechisLigne(self):
    ml = lemmatiseur.lemmatiseM(lineEditFlex.text())
    if not ml.empty():
        textBrowserFlex.clear()
        textBrowserFlex.append(flechisseur.tableaux(&ml))
        # foreach (Lemme *l, ml.keys())
        #	textBrowserFlex.append (flechisseur.tableau(l))



'''*
 * \fn bool MainWindow.html()
 * \brief Renvoie vrai si l'option html du lemmatiseur
 *        est armée.
 '''
bool MainWindow.html() { return htmlAct.isChecked();
'''*
 * \fn void MainWindow.lancer()
 * \brief Lance la lemmatisation et la scansion si
 *        les docks correspondants sont visibles.
 '''
def lancer(self):
    if dockVisible(dockLem)) lemmatiseTxt(:
    if dockVisible(dockScand)) scandeTxt(:
    if dockVisible(dockTag)) tagger(editLatin.toPlainText(),-1:


'''*
 * \fn void MainWindow.lemmatiseLigne()
 * \brief Lance la lemmatisation des formes *
 *        présentes dans la ligne de saisie du dock
 *        lemmatisation.
 '''
def lemmatiseLigne(self):
    txt = lineEditLem.text()
    if html():
    texteHtml = textEditLem.toHtml()
    texteHtml.insert(texteHtml.indexOf("</body>"),
                     lemmatiseur.lemmatiseT(txt))
    textEditLem.setText(texteHtml)

    else textEditLem.insertPlainText(lemmatiseur.lemmatiseT(txt))
    textEditLem.moveCursor(QTextCursor.End)


'''*
 * \fn void MainWindow.lemmatiseTxt()
 * \brief Lance la lemmatisation de la totalité du
 *        texte contenu dans l'éditeur editLatin (partie supérieure
 *        de la fenêtre de l'application).
 '''
def lemmatiseTxt(self):
    # si la tâche dure trop longtemps :
    # setUpdatesEnabled(False)
    txt = editLatin.toPlainText()
    res = lemmatiseur.lemmatiseT(txt)
    if html():
        textEditLem.setHtml(res)
    else:
        textEditLem.setPlainText(res)
    # setUpdatesEnabled(True)
    if txt.contains("<span"):
        editLatin.setHtml(txt)
    # Le texte a été modifié, colorisé.


'''*
 * \fn void MainWindow.majDic()
 * \brief Lance le dialogue de mise à jour des
 *        lexiques et dictionnaires.
 '''

def majDic(self):
    Maj *majDial = Maj(True)
    majDial.setFont(editLatin.font())
    majDial.exec()
    createDicos()
    createDicos(False)


'''*
 * \fn void MainWindow.majLex()
 * \brief Lance le dialogue de mise à jour des
 *        lexiques et dictionnaires.
 '''

def majLex(self):
    Maj *majDial = Maj(False)
    majDial.setFont(editLatin.font())
    majDial.exec()


'''*
 * \fn void MainWindow.montreWDic(bool visible)
 * \brief Rend visible le dictionnaire supplémentaire,
 *        et met à jour son contenu.
 '''
def montreWDic(self, visible):
    wDic.move(x() + width() + 80, y())
    wDic.setVisible(visible)
    lineEditDicW.setText(lineEditDic.text())
    afficheLemsDicW()
    lineEditDicW.clearFocus()


'''*
 * \fn void MainWindow.nouveau()
 * \brief Après confirmation efface le texte et les résultats,
 *        permettant à l'utilisateur de recommencer /ab initio/
 '''
def nouveau(self):
    if (precaution()) return
    editLatin.clear()
    textEditLem.clear()
    textEditScand.clear()


'''*
 * \fn void MainWindow.ouvrir()
 * \brief Affiche le dialogue d'ouverture de fichier.
 '''
def ouvrir(self):
    if (precaution()) return
    nfAb = QFileDialog.getOpenFileName(self, "Collatinus - Ouvrir un fichier",
                                        repertoire)
    if (nfAb.isEmpty()) return
    charger(nfAb)
    nfAd = nfAb
    nfAd.prepend("coll-")


def police(self):
    bool ok
    police = QFontDialog.getFont(&ok, font, self)
    if ok:
        font = police
        editLatin.setFont(font)
        textEditLem.setFont(font)
        textBrowserDic.setFont(font)
        textBrowserW.setFont(font)
        textEditScand.setFont(font)
        textBrowserFlex.setFont(font)



'''*
 * \fn bool MainWindow.precaution()
 * \brief Dialogue de précaution avant l'effacement du texte latin.
 *        Renvoie False si Oui/Yes a été cliqué.
 '''
def precaution(self):
    if (not editLatin.document().isEmpty() or
        not textEditLem.document().isEmpty() or
        not textEditScand.document().isEmpty())
        ret = QMessageBox.warning(
            self, tr("Collatinus"), tr("Un ou plusieurs onglets ont été "
                                       "modifiés. Effacer leur contenu ?"),
            QMessageBox.Yes | QMessageBox.Default, QMessageBox.No,
            QMessageBox.Cancel | QMessageBox.Escape)
        if (ret == QMessageBox.Yes) return False
        return True

    return False


'''*
 * \fn void MainWindow.readSettings()
 * \brief Appelée à l'initialisation de l'application,
 *        pour retrouver les paramètres importants de
 *        la dernière session.
 '''
def readSettings(self):
    QSettings settings("Collatinus", "collatinus11")
    # état de la fenêtre
    settings.beginGroup("fenetre")
    restoreGeometry(settings.value("geometry").toByteArray())
    restoreState(settings.value("windowState").toByteArray())
    settings.endGroup()
    # dernier fichier chargé
    settings.beginGroup("fichiers")
    nfAb = settings.value("nfAb").toString()
    if not nfAb.isEmpty():
        charger(nfAb)
        nfAd = nfAb
        nfAd.prepend("coll-")

    settings.endGroup()
    settings.beginGroup("options")
    # police
    font.setPointSize(settings.value("zoom").toInt())
    # font.setFamily(settings.value("police").toString())
    editLatin.setFont(font)
    textEditLem.setFont(font)
    textBrowserDic.setFont(font)
    textBrowserW.setFont(font)
    textEditScand.setFont(font)
    textBrowserFlex.setFont(font)
    # options de lemmatisation
    alphaOptAct.setChecked(settings.value("alpha").toBool())
    formeTAct.setChecked(settings.value("formetxt").toBool())
    extensionWAct.setChecked(settings.value("extensionlexique").toBool())
    htmlAct.setChecked(settings.value("html").toBool())
    majPertAct.setChecked(settings.value("majpert").toBool())
    morphoAct.setChecked(settings.value("morpho").toBool())
    nonRecAct.setChecked(settings.value("nonrec").toBool())
    # options d'accentuation
    accentAct.setChecked(settings.value("accentuation").toBool())
    optionsAccent.setEnabled(settings.value("accentuation").toBool())
    longueAct.setChecked(settings.value("longue").toBool())
    breveAct.setChecked(settings.value("breve").toBool())
    ambigueAct.setChecked(settings.value("ambigue").toBool())
    illiusAct.setChecked(settings.value("illius").toBool())
    hyphenAct.setChecked(settings.value("hyphenation").toBool())
    repHyphen = settings.value("repHyphen").toString()
    ficHyphen = settings.value("ficHyphen").toString()
    affToutAct.setChecked(settings.value("tagAffTout").toBool())
    repVerba = settings.value("repVerba").toString()
    if (repVerba.isEmpty()) repVerba = "~"
    if repHyphen.isEmpty() or ficHyphen.isEmpty():
        repHyphen = qApp.applicationDirPath() + "/data"

    l = settings.value("cible").toString()
    if (l.size() < 2) l = "fr"
    lemmatiseur.setCible(l)
    foreach (QAction *action, grCibles.actions())
        if action.text() == lemmatiseur.cibles()[l.mid(0,2)]:
            action.setChecked(True)
    settings.endGroup()
    # options appliquées au lemmatiseur
    lemmatiseur.setAlpha(alphaOptAct.isChecked())
    lemmatiseur.setFormeT(formeTAct.isChecked())
    lemmatiseur.setExtension(extensionWAct.isChecked())
    if not ficHyphen.isEmpty()) lemmatiseur.lireHyphen(ficHyphen:
    # Le fichier hyphen.la doit être lu après l'extension.
    lemmatiseur.setHtml(htmlAct.isChecked())
    lemmatiseur.setMajPert(majPertAct.isChecked())
    lemmatiseur.setMorpho(morphoAct.isChecked())
    settings.beginGroup("dictionnaires")
    comboGlossaria.setCurrentIndex(settings.value("courant").toInt())
    wDic.move(settings.value("posw").toPoint())
    wDic.resize(settings.value("sizew").toSize())
    wDic.setVisible(settings.value("wdic").toBool())
    comboGlossariaW.setCurrentIndex(settings.value("courantW").toInt())
    syncAct.setChecked(settings.value("sync").toBool())
    visibleWAct.setChecked(settings.value("secondDic").toBool())
    settings.endGroup()


'''*
 * \fn void MainWindow.recherche()
 * \brief Recherche dans l'éditeur de texte latin.
 '''
def recherche(self):
    bool ok
    rech = QInputDialog.getText(self, tr("Recherche"), tr("Chercher :"),
                                 QLineEdit.Normal, rech, &ok)
    if ok and not rech.isEmpty():
        if not editLatin.find(rech):
            rech = QInputDialog.getText(self, tr("Chercher"),
                                         tr("Retour au début ?"),
                                         QLineEdit.Normal, rech, &ok)
            if ok and not rech.isEmpty():
                # Retourner au debut
                editLatin.moveCursor(QTextCursor.Start)
                # Chercher à nouveau
                editLatin.find(rech)





'''*
 * \fn void MainWindow.rechercheBis()
 * \brief Suite de la recherche.
 *
 '''
def rechercheBis(self):
    if (rech.isEmpty()) return
    ok = editLatin.find(rech)
    if not ok:
        tc = editLatin.textCursor()
        editLatin.moveCursor(QTextCursor.Start)
        ok = editLatin.find(rech)
        if not ok) editLatin.setTextCursor(tc:



'''*
 * \fn void MainWindow.scandeLigne()
 * \brief scande le contenu de la ligne de saisie du
 *        dock Scansion, affiche le résultat.
 '''
def scandeLigne(self):
    accent = lireOptionsAccent()
    textEditScand.setHtml(
        lemmatiseur.scandeTxt(lineEditScand.text(), accent, False))


'''*
 * \fn void MainWindow.scandeTxt()
 * \brief Lance la scansion du texte latin, affiche le
 *        résultat dans le dock scansion.
 '''
def scandeTxt(self):
    accent = lireOptionsAccent()
    textEditScand.setHtml(
        lemmatiseur.scandeTxt(editLatin.toPlainText(), accent, False))


'''*
 * \fn void MainWindow.setCible()
 * \brief Coordonne la langue cible cochée dans le menu
 *        et la langue cible du lemmatiseur.
 '''
def setCible(self):
    QAction *action = grCibles.checkedAction()
    for cle in lemmatiseur.cibles().keys():
        if lemmatiseur.cibles()[cle] == action.text():
            if cle == "fr":
                lemmatiseur.setCible(cle + ".en.de")
            elif cle == "en":
                lemmatiseur.setCible(cle + ".fr.de")
            else:
                # Les deux langues principales sont le français et l'anglais.
                # Pour les autres langues, donne le choix de la 2e langue.
                QMessageBox msg
                msg.setIcon(QMessageBox.Question)
                msg.setText("Choisir une 2nde langue  \nChoose a 2nd language")
                QAbstractButton *frButton = msg.addButton("Français",QMessageBox.AcceptRole)
                QAbstractButton *enButton = msg.addButton("English",QMessageBox.AcceptRole)
                msg.exec()
                if msg.clickedButton() == frButton:
                    lemmatiseur.setCible(cle + ".fr.en")
                elif msg.clickedButton() == enButton:
                    lemmatiseur.setCible(cle + ".en.fr")
                else lemmatiseur.setCible(cle + ".en.fr")

            break




'''*
 * \fn void MainWindow.setLangue()
 * \brief lis la langue d'interface, et
 *        procède aux initialisations.
 '''
def setLangue(self):
    QSettings settings("Collatinus", "collatinus11")
    settings.beginGroup("interface")
    langueI = settings.value("langue").toString()
    settings.endGroup()
    if not langueI.isEmpty():
        translator = QTranslator(qApp)
        translator.load(qApp.applicationDirPath() + "/collatinus_" + langueI)
        qApp.installTranslator(translator)

    else:
        langueI = "fr"


'''*
 * \fn void MainWindow.stat()
 * \brief Affiche les statistiques de lemmatisation et
 *        de scansion si le dock correspondant est visible.
 '''
def stat(self):
    if dockVisible(dockLem):
        textEditLem.setHtml(
            lemmatiseur.frequences(editLatin.toPlainText()).join(""))

    if dockVisible(dockScand):
        textEditScand.setHtml(
            lemmatiseur.scandeTxt(editLatin.toPlainText(), 0, True))


'''*
 * \fn void MainWindow.syncDW()
 * \brief effectue dans le dictionnaire supplémentaire
 *        la même recherche que celle qui a été faite dans le
 *        principal.
 '''
def syncDW(self):
    if wDic.isVisible():
        lineEditDicW.setText(lineEditDic.text())
        afficheLemsDicW()

    else:
        montreWDic(True)


'''*
 * \fn void MainWindow.syncWD()
 * \brief effectue dans le dictionnaire principal
 *        la même recherche que celle qui a été faite dans le
 *        supplémentaire.
 '''
def syncWD(self):
    lineEditDic.setText(lineEditDicW.text())
    afficheLemsDic()


def setAccent(self, b):
    optionsAccent.setEnabled(b)
    illiusAct.setEnabled(b)
    hyphenAct.setEnabled(b)


def lireOptionsAccent(self):
    retour = 0
    if accentAct.isChecked():
        if (illiusAct.isChecked()) retour += 8
        if (hyphenAct.isChecked()) retour += 4
        if (longueAct.isChecked()) return retour + 1
        if (breveAct.isChecked()) return retour + 2
        retour += 3

    return retour


def lireFichierHyphen(self):
    ficHyphen = QFileDialog.getOpenFileName(self, "Capsam legere", repHyphen+"/hyphen.la")
    if not ficHyphen.isEmpty()) repHyphen = QFileInfo (ficHyphen).absolutePath (:
    lemmatiseur.lireHyphen(ficHyphen)
    # Si le nom de fichier est vide, efface les données précédentes.


def oteDiacritiques(self):
    texte = editLatin.toPlainText()
    texte.replace("ç","s")
    texte.replace("Ç","S")
    texte = texte.normalized(QString.NormalizationForm_D, QChar.currentUnicodeVersion())
    texte.remove("\u0300")
    texte.remove("\u0301")
    texte.remove("\u0302")
    texte.remove("\u0304")
    texte.remove("\u0306")
    texte.remove("\u0308")
    editLatin.setText(texte)


def lancerServeur(self, run):
    if run:
        QMessageBox.about(self,
             tr("Serveur de Collatinus"), startServer())


    else:
        QMessageBox.about(self,
             tr("Serveur de Collatinus"), stopServer())




void MainWindow.connexion ()
    soquette = serveur.nextPendingConnection ()
    soquette.readyRead.connect(self.exec)


void MainWindow.exec ()
    octets = soquette.readAll ()
    requete = QString (octets).trimmed()
    if (requete.isEmpty()) requete = "-?"
    texte = ""
    rep = ""
    nonHTML = True
    fichierSortie = ""
    if requete.contains("-o "):
        # La requête contient un nom de fichier de sortie
        nom = requete.section("-o ",1,1).trimmed()
        requete = requete.section("-o ",0,0).trimmed()
        # En principe, le -o vient à la fin. Mais...
        if nom.contains(" "):
            fichierSortie = nom.section(" ",0,0)
            # Le nom de fichier ne peut pas contenir d'espace !
            if requete.isEmpty()) requete = nom.section(" ",1:
            else requete.append(" " + nom.section(" ",1))

        fichierSortie = nom

    if requete.contains("-f "):
        # La requête contient un nom de fichier
        nom = requete.section("-f ",1,1).trimmed()
        requete = requete.section("-f ",0,0).trimmed()
        QFile fichier(nom)
        if fichier.open(QFile.ReadOnly):
            texte = fichier.readAll()
            fichier.close()

        rep = "fichier non trouvé not \n"

    if rep == "":
    if (requete[0] == '-') and (requete.size() > 1):
        a = requete[1].toLatin1()
        options = requete.mid(0,requete.indexOf(" "))
        lang = lemmatiseur.cible(); # La langue actuelle
        html = lemmatiseur.optHtml(); # L'option HTML actuelle
        MP = lemmatiseur.optMajPert()
        lemmatiseur.setHtml(False); # Sans HTML, priori
        optAcc = 0
        if texte == "":
            texte = requete.mid(requete.indexOf(" ")+1)
        lemmatiseur.setMajPert(requete[1].isUpper())
        switch (a)
        case 'S':
        case 's':
            if (options.size() > 2) and (options[2].isDigit()):
                optAcc = options[2].digitValue() & 7
            rep = lemmatiseur.scandeTxt(texte,0,optAcc==1)
            if (optAcc==1) nonHTML = False
            break
        case 'A':
        case 'a':
            optAcc = 3; # Par défaut : un mot dont la pénultième est commune n'est pas accentué.
            if (options.size() > 2) and (options[2].isDigit()):
                optAcc = options[2].digitValue()
                if (options.size() > 3) and (options[3].isDigit()):
                    optAcc = 10 * optAcc + options[3].digitValue()

            rep = lemmatiseur.scandeTxt(texte,optAcc,False)
            break
        case 'H':
        case 'h':
            lemmatiseur.setHtml(True)
            nonHTML = False
        case 'L':
        case 'l':
            if (options.size() > 2) and (options[2].isDigit()):
                optAcc = options[2].digitValue()
                options = options.mid(3)
                if (options.size() > 0) and (options[0].isDigit()):
                    optAcc = 10*optAcc+options[0].digitValue()
                    options = options.mid(1)


            options = options.mid(2); # Je coupe le "-l".
            if (options.size() == 2) and lemmatiseur.cibles().keys().contains(options):
                lemmatiseur.setCible(options)
            elif ((options.size() == 5) or (options.size() == 8)) and lemmatiseur.cibles().keys().contains(options.mid(0,2)):
                lemmatiseur.setCible(options)
            if optAcc > 15) rep = lemmatiseur.frequences(texte).join("":
            rep = lemmatiseur.lemmatiseT(texte,optAcc&1,optAcc&2,optAcc&4,optAcc&8)
            lemmatiseur.setCible(lang); # Je rétablis les langue et option HTML.
            break
        case 'X':
        case 'x':
#            rep = lemmatiseur.txt2XML(requete)
            rep = "Pas encore disponible"
            break
        case 'K':
        case 'k':
            rep = lemmatiseur.k9(texte)
            break
        case 'c':
            if options.size() > 2:
                lemmatiseur.setMajPert(options[2] == '1')
            break
        case 't':
            options = options.mid(2); # Je coupe le "-t".
            if (((options.size() == 2) or (options.size() == 5) or (options.size() == 8)) and
                    lemmatiseur.cibles().keys().contains(options.mid(0,2)))
                lemmatiseur.setCible(options)

            else:
                clefs = lemmatiseur.cibles().keys()
                rep = "Les langues connues sont : " + clefs.join(" ") + "\n"

            break
#        case '?':
        default: # Tout caractère non-affecté affiche l'aide.
            rep = "La syntaxe est '[commande] [texte]' ou '[commande] -f nom_de_fichier'.\n"
            rep += "Éventuellement complétée par '-o nom_de_fichier_de_sortie'.\n"
            rep += "Par défaut (sans commande), obtient la scansion du texte.\n"
            rep += "Les commandes possibles sont : \n"
            rep += "\t-s : Scansion du texte (-s1 : avec recherche des mètres).\n"
            rep += "\t-a : Accentuation du texte (avec options -a1..-a15).\n"
            rep += "\t-l : Lemmatisation du texte (avec options -l0..-l15, -l16 pour les fréquences).\n"
            rep += "\t-h : Lemmatisation du texte en HTML (mêmes options que -l).\n"
            rep += "\t-S, -A, -L, -H : Les mêmes avec Majuscules pertinentes.\n"
            rep += "\t-t : Langue cible pour les traductions (par exemple -tfr, -ten).\n"
            rep += "\t-C : Majuscules pertinentes.\n"
            rep += "\t-c : Majuscules non-pertinentes.\n"
            rep += "\t-? : Affichage de l'aide.\n"
 #           rep += "\t-x : Mise en XML du texte.\n"
            break

        lemmatiseur.setHtml(html)
        if (a != 'C') and (a != 'c'):
            lemmatiseur.setMajPert(MP)

    elif texte != "") rep= lemmatiseur.scandeTxt(texte:
    rep = lemmatiseur.scandeTxt(requete)

    if nonHTML:
        rep.remove("<br />"); # Avec -H/h, j'ai la lemmatisation en HTML
        rep.remove("<br/>"); # Avec -H/h, j'ai la lemmatisation en HTML

#    rep.replace("<br />","\n")
    if fichierSortie == "":
        QClipboard *clipboard = QApplication.clipboard()
        clipboard.setText(rep)

    else:
        QFile ficOut(fichierSortie)
        if ficOut.open(QFile.WriteOnly):
            ficOut.write(rep.toUtf8())
            ficOut.close()
            rep = "Done not \n"

        rep = "Unable to write not \n"

    ba = rep.toUtf8()
    soquette.write(ba)


def startServer(self):
    serveur = QTcpServer (self)
    serveur.newConnection.connect(self.connexion)
    if not serveur.listen (QHostAddress.LocalHost, 5555):
        return "Ne peux écouter."

    return "Le serveur est lancé."


def stopServer(self):
    serveur.close()
    delete serveur
    return "Le serveur est éteint."


def dockRestore(self):
    dockLem.setFloating(False)
    dockLem.show()
    dockScand.setFloating(False)
    dockScand.show()
    dockDic.setFloating(False)
    dockDic.show()
    dockFlex.setFloating(False)
    dockFlex.show()
    dockTag.setFloating(False)
    dockTag.show()


def tagger(self, t, p):
    if t.length() > 2:
        # Sans texte, ne fais rien.
        tl = t.length() - 1
        if (p > tl) p = tl
        textBrowserTag.setHtml(lemmatiseur.tagTexte(t, p, affToutAct.isChecked()))



def verbaCognita(self, vb):
    QString fichier
    if vb) fichier = QFileDialog.getOpenFileName(self, "Verba cognita", repVerba:
    if not fichier.isEmpty()) repVerba = QFileInfo (fichier).absolutePath (:
    lemmatiseur.verbaCognita(fichier,vb)


def setHtml(self, h):
    # Passer en html ne pose pas de problème
    if h or textEditLem.toPlainText().isEmpty()) lemmatiseur.setHtml(h:
    elif alerte():
        # L'inverse (html -. non-html) mettrait les nouveaux résultats en items du dernier lemme.
        blabla = textEditLem.toHtml()
#        qDebug() << blabla
        textEditLem.clear()
        pCourante = 0
        while (blabla.indexOf("<li ", pCourante) != -1)
            pCourante = blabla.indexOf("<li ", pCourante) + 4
            pCourante = blabla.indexOf(">",pCourante) + 1
            toto = blabla.mid(0,pCourante).lastIndexOf("-qt-list-indent: ")
            niveau = blabla.mid(toto + 17,1).toInt()
#            niveau = blabla.mid(0,pCourante).count("<ul ") - blabla.mid(0,pCourante).count("</ul>")
            switch (niveau)
            case 1:
                blabla.insert(pCourante,"* ")
                break
            case 2:
                blabla.insert(pCourante," - ")
                break
            case 3:
                blabla.insert(pCourante,"   . ")
                break
            default:
                break


        textEditLem.setHtml(blabla)
        blabla = textEditLem.toPlainText()
        blabla.append("\n\n")
        textEditLem.clear()
        # J'efface les résultats précédents
        textEditLem.setText(blabla)
        textEditLem.moveCursor(QTextCursor.End)
        lemmatiseur.setHtml(h)

    else htmlAct.setChecked(True)


def alerte(self):
    QMessageBox attention(QMessageBox.Warning,tr("Alerte not "),
                          tr("Quitter le mode HTML perd la mise en forme des résultats précédents not "))
    QPushButton *annulerButton =
          attention.addButton(tr("Annuler"), QMessageBox.ActionRole)
    QPushButton *ecraserButton =
          attention.addButton(tr("Continuer"), QMessageBox.ActionRole)
    attention.setDefaultButton(ecraserButton)
    attention.exec()
    if (attention.clickedButton() == annulerButton) return False
    return True



def auxilium(self):
    QDesktopServices.openUrl(QUrl("file:" + qApp.applicationDirPath() + "/doc/index.html"))


def verbaOut(self):
    # Pour sauver un fichier avec l'utilisation des mots connus.
    QString fichier
    fichier = QFileDialog.getSaveFileName(self, "Verba cognita", repVerba)
    if not fichier.isEmpty():
        repVerba = QFileInfo (fichier).absolutePath ()
        lemmatiseur.verbaOut(fichier)


