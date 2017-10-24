#ifndef MOT_H
#define MOT_H

#include <QString>
#include <QStringList>
#include <QMap>
#include <QtCore/QCoreApplication>

#include "lemmatiseur.h"
#include "lemme.h"
#include "ch.h"

class Mot : public QObject
{
    Q_OBJECT
public:
    Mot(QString forme, int rang, bool debVers, QObject *parent = 0);
    QString choisir(QString t = "", bool tout = true);
    long proba(QString t);
    QStringList tags();
    QString forme();
    QString tagEncl();
    bool inconnu();
    void setBestOf(QString t, double pr);
    double bestOf(QString t);

private:
    Lemmat* _lemmatiseur;
    QString _forme;
    int _rang;
    QString _tagEncl;
    MapLem _mapLem;
    QStringList _lemmes;
    QStringList _morphos;
    QStringList _tags;
    QList<int> _nbOcc;
    QMap<QString,long> _probas;
    QString _maxProb;
    QMap<QString,double> _bestOf;
};

#endif // MOT_H
