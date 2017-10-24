'''       ch.h     '''

#ifndef CH_H
#define CH_H

#include <QRegExp>
#include <QString>
#include <QStringList>

namespace Ch
abrev = QStringList()
    <<"Agr"<<"Ap"<<"A"<<"K"<<"D"<<"F"<<"C"
    <<"Cn"<<"Kal"<<"L"<<"Mam"<<"M\""<<"M"<<"N"<<"Oct"
    <<"Opet"<<"Post"<<"Pro"<<"P"<<"Q"<<"Sert"
    <<"Ser"<<"Sex"<<"S"<<"St"<<"Ti"<<"T"<<"V"
    <<"Vol"<<"Vop"<<"Pl"
# Liste des abréviations prise dans Praelector le 11/11/2016
def ajoute(self, mot, liste):
def allonge(self, *f):
def atone(self, a, bdc = False):
def communes(self, g):
def deQuant(self, *c):
consonnes = "bcdfgjklmnpqrstvxz"
def genStrNum(self, s, *ch, *n):
def deramise(self, r):
def deAccent(self, c):
def elide(self, *mp):
 QRegExp reAlphas("(\\w+)")
 QRegExp reEspace("\\s+")
 QRegExp reLettres("\\w")
 QRegExp rePonct("([\\.?not ;:])")
#  QRegExp rePonct("([\\.?not ;:]|$$)")
def sort_i(self, &a, &b):
def inv_sort_i(self, &a, &b):
def versPC(self, k):
def versPedeCerto(self, k):
voyelles = "āăēĕīĭōŏūŭȳўĀĂĒĔĪĬŌŎŪŬȲЎ"

#separSyll = 0x02CC
#separSyll = 0x00AD
separSyll = 0x00B7
def transforme(self, k):
def accentue(self, l):
def ajoutSuff(self, fq, suffixe, l_etym, accent):

#endif
