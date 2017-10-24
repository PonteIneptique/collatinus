/*    maj.h   */

#ifndef MAJ_H
#define MAJ_H

#include <QDialog>
#include <QLabel>
#include <QStringList>

class Maj : public QDialog
{
    Q_OBJECT

   private:
    bool installe(
        QString nfcol);  // décompresse nfcol et l'installe dans data/dicos/
    bool djvu2col(QString nfdjvu);
    // Fonction pour générer un .col à partir d'un djvu dans data/dicos/
    bool lem2col(QString nfLem);
    // Fonction pour générer un .col à partir d'un fichier lemmes.* ou lem_ext.*
    QLabel *label;
    QStringList listeF;  // liste des fichiers téléchargés
    bool _dico; // Mise à jour des dicos ou des lexiques (si faux)

   private slots:
    void selectionne();  // lance un dialogue de sélection de fichier

   public:
    Maj(bool dic = true, QDialog *parent = 0);
    void setFont(QFont font);
};

#endif
