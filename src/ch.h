/*       ch.h     */

#ifndef CH_H
#define CH_H

#include <QRegExp>
#include <QString>
#include <QStringList>

namespace Ch
{
    QString       accentue(QString l);
    QStringList   ajoute(QString mot, QStringList liste);
    QString       ajoutSuff(QString fq, QString suffixe, QString l_etym, int accent);
    void          allonge(QString *f);
    QString       atone(const QString a, bool bdc = false);
    QString       communes(QString g);
    void          deQuant(QString *c);
    QString const consonnes = "bcdfgjklmnpqrstvxz";
    void          genStrNum(const QString s, QString *ch, int *n);
    QString       deramise(QString r);
    QString       deAccent(QString c);
    void          elide(QString *mp);
    const QRegExp reAlphas("(\\w+)");
    const QRegExp reEspace("\\s+");
    const QRegExp reLettres("\\w");
    const QRegExp rePonct("([\\.?!;:]|$$)");
    QChar const   separSyll = 0x02CC;
    bool          sort_i(const QString &a, const QString &b);
    QString       transforme(QString k);
    QString       versPC(QString k);
    QString       versPedeCerto(QString k);
    QString const voyelles = "āăēĕīĭōŏūŭȳўĀĂĒĔĪĬŌŎŪŬȲЎ";

}
#endif
