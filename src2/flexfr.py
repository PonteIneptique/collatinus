#
   # flexfr - module de flexion pour la langue française.
   # Copyright (C) 2001-2004 Yves Ouvrard.
# 
   # Ce programme est un logiciel libre ; vous pouvez le redistribuer et/ou le
   # modifier conformément aux dispositions de la Licence Publique Générale GNU,
   # telle que publiée par la Free Software Foundation ; version 2 de la licence,
   # ou encore (à votre choix) toute version ultérieure.
   # Ce programme est distribué dans l'espoir qu'il sera utile, mais SANS AUCUNE
   # GARANTIE ; sans même la garantie implicite de COMMERCIALISATION ou
   # D'ADAPTATION
   # A UN OBJET PARTICULIER.
   # Pour plus de détail, voir la Licence Publique Générale GNU .
   # Vous devez avoir reçu un exemplaire de la Licence Publique Générale GNU en
   # même
   # temps que ce programme ; si ce n'est pas le cas, écrivez à la
   # Free Software Foundation Inc., 675 Mass Ave, Cambridge, MA 02139, Etats-Unis.
   # Pour tout contact avec l'auteur : yves.ouvrard@collatinus.org
  # 

#include <flexfr.h>
#include <QStringList>
#include <QTextStream>

#include <QDebug>

using namespace std

# chaînes de champs morpho
QString personne[7] = {" ", "je", "tu", "i", "nous", "vous", "ils"
#
# QString temps[9] = {" ", "présent", "futur", "imparfait", "passé simple",
    # "passé [composé]", "futur antérieur",
    # "plus-que-parfait", "passé antérieur"}
# 

QString mode[8] = {" ",         "indicatif", "subjonctif", "conditionnel",
                   "impératif", "infinitif", "participe",  "gérondif"
# QString voix[3] = {" ", "actif", "passif"}

QString genre[3] = {" ", "masculin", "féminin"
QString nombre[3] = {" ", "singulier", "pluriel"
QStringList AuxEtre = QStringList() << "accourir"
                                    << "advenir"
                                    << "aller"
                                    << "arriver"
                                    << "décéder"
                                    << "devenir"
                                    << "échoir"
                                    << "enlaidir"
                                    << "entrer,"
                                    << "intervenir"
                                    << "monter"
                                    << "mourir"
                                    << "naître"
                                    << "obvenir"
                                    << "partir"
                                    << "parvenir"
                                    << "provenir"
                                    << "redevenir"
                                    << "rentrer"
                                    << "reparaître"
                                    << "repartir"
                                    << "ressortir"
                                    << "rester"
                                    << "retomber"
                                    << "retourner"
                                    << "revenir"
                                    << "sortir"
                                    << "survenir"
                                    << "tomber"
                                    << "venir"

QStringList Eter = QStringList() << "acheter"
                                 << "racheter"
                                 << "bégueter"
                                 << "corseter"
                                 << "crocheter"
                                 << "fileter"
                                 << "fureter"
                                 << "haleter"
                                 << "celer"
                                 << "déceler"
                                 << "receler"
                                 << "ciseler"
                                 << "démanteler"
                                 << "écarteler"
                                 << "encasteler"
                                 << "geler"
                                 << "dégeler"
                                 << "congeler"
                                 << "surgeler"
                                 << "marteler"
                                 << "modeler"
                                 << "peler"

QStringList intransitifs = QStringList() << "aboutir"
                                         << "agir"
                                         << "appartenir"
                                         << "bavarder"
                                         << "boiter"
                                         << "bondir"
                                         << "bourdonner"
                                         << "briller"
                                         << "circuler"
                                         << "consister"
                                         << "contribuer"
                                         << "daigner"
                                         << "déjeuner"
                                         << "déplaire"
                                         << "dîner"
                                         << "durer"
                                         << "errer"
                                         << "étinceler"
                                         << "exister"
                                         << "falloir"
                                         << "frémir"
                                         << "frissonner"
                                         << "gambader"
                                         << "grelotter"
                                         << "grincer"
                                         << "hésiter"
                                         << "insister"
                                         << "jouir"
                                         << "luire"
                                         << "lutter"
                                         << "marcher"
                                         << "mentir"
                                         << "obéir"
                                         << "paître"
                                         << "parler"
                                         << "paraître"
                                         << "plaire"
                                         << "pleuvoir"
                                         << "pouvoir"
                                         << "procéder"
                                         << "profiter"
                                         << "réagir"
                                         << "résonner"
                                         << "resplendir"
                                         << "ressembler"
                                         << "retentir"
                                         << "rire"
                                         << "ronronner"
                                         << "rougir"
                                         << "ruisseler"
                                         << "sembler"
                                         << "sévir"
                                         << "souper"
                                         << "sourire"
                                         << "suffire"
                                         << "tarder"
                                         << "tinter"
                                         << "tournoyer"
                                         << "tressaillir"
                                         << "triompher"
                                         << "voltiger"
                                         << "voyager"

const actif = 1
const passif = 2

const ind = 1
const subj = 2
const cond = 3
const imper = 4
const infin = 5
const part = 6
# const int ger = 7

const pres = 1
const fut = 2
const impf = 3
const psimple = 4
const pcompose = 5
const futant = 6
const pqp = 7
# const int pant = 8

QChar derniere(QString s)
    return s.at(s.length() - 1)
    #
    # if (s.isEmpty ()) return '\0'
    # return s[s.length () - 1]
   # 

QString dernieres(QString s, size_t n)
    return s.right(n)
    #
    # if (s.isEmpty ()) return ""
    # return s.substr (s.length () - n, n)
   # 

QString deuxder(QString s) { return s.right(2); }
QString npremieres(QString s, n)
    return s.left(n)
    # return s.substr (0, n)

QString otepremieres(QString s, n)
    return s.remove(0, n)
    # return s.substr (n, s.length ())

QString otedernieres(QString s, n)
    s.chop(n)
    return s

#
  # Renvoie le numéro d'item de la chaîne s dans
  # le tableau t de taille limite.
 # 
def index_t(QString t[], QString s, limite):
    for i in range(limite+1):
        if t[i] == s:
            return i
    return -1

# élargit la chaîne s jusqu'à la largeur l
QString augmente(QString s, l = 25)
    while s.length() < l) s.push_back(' ':
    return s

def IsLast(QString chaine, QString mot):
    # vrai si mot se termine par chaine
    return mot.endsWith(chaine)

def pas_de_passif(QString inf):
    if (inf.startsWith("s'") or inf.startsWith("se ")) return True
    #
    # inf.insert (0, 1, ','); inf.push_back (',')
    # if (npremieres (inf, 2) == "s'" || npremieres (inf, 3) == "se ") return
    # true
   # 
    return (intransitifs.contains(inf) or AuxEtre.contains(inf))

#
  # Verbe est la classe de base. J'ai pris le premier groupe comme référence,
  # puisqu'il représente la majorité des verbes}
 # 
Verbe::Verbe(QString i)
    inf = i
    pronominal = 0
    modele = "Verbe"

Verbe::~Verbe() {}
const QStringList personnes = QStringList() << "1ère"
                                            << "2ème"
                                            << "3ème"
const QStringList temps = QStringList() << "présent"
                                        << "futur"
                                        << "imparfait"
                                        << "parfait"  #"passé simple"
                                        << "passé composé"
                                        << "futur antérieur"
                                        << "plus-que-parfait"
                                        << "passé antérieur"
const QStringList modes = QStringList() << "indicatif"
                                        << "subjonctif"
                                        << "conditionnel"
                                        << "impératif"
                                        << "infinitif"
                                        << "participe"
                                        << "gérondif"
const QStringList voix = QStringList() << "actif"
                                       << "passif"
const QStringList genres = QStringList() << "masculin"
                                         << "féminin"
const QStringList nombres = QStringList() << "singulier"
                                          << "pluriel"

#
# QString Verbe::conjnat(QString inf, QString morpho)
# {
    # int p=0
    # int nb=0
    # int t=0
    # int m=0
    # int v=0
    # int g=0
# 
    # int n=0
    # foreach (QString trait, morpho)
    # {
        # n = personnes.indexOf(trait); if (n >= 0) {p = n+1;continue;}
        # n = nombres.indexOf(trait);   if (n >= 0) {nb = n+1;continue;}
        # n = temps.indexOf(trait);     if (n >= 0) {t = n+1;continue;}
        # n = modes.indexOf(trait);     if (n >= 0) {t = n+1;continue;}
        # n = voix.indexOf(trait);      if (n >= 0) {v = n+1;continue;}
        # n = genres.indexOf(trait);    if (n >= 0) {g = n+1;continue;}
    # }
    # int pnb = p * nb
    # return conjugue(pnb, t, m, v, (p!=3), g, nb)
   # /QString Verbe::conjugue (int P, int T, int M, int V, bool pr, int g, int n)
# }
# 

QString Verbe::GetModele() { return modele; }
QString Verbe::GetDesFut(index)
    QString D[7] = {"", "ai", "as", "a", "ons", "ez", "ont"    return D[index]

QString Verbe::GetDesImpf(index)
    QString D[7] = {"", "ais", "ais", "ait", "ions", "iez", "aient"    return D[index]

QString Verbe::GetDesPsAi(index)
    QString D[7] = {"", "ai", "as", "a", "âmes", "âtes", "èrent"    return D[index]

QString Verbe::GetDesPsI(index)
    QString D[7] = {"", "is", "is", "it", "îmes", "îtes", "irent"    return D[index]

QString Verbe::GetDesPsU(index)
    QString D[7] = {"", "us", "us", "ut", "ûmes", "ûtes", "urent"    return D[index]

QString Verbe::GetDesSubjPres(index)
    QString D[7] = {"", "e", "es", "e", "ions", "iez", "ent"    return D[index]

# utiles
QString Verbe::circonflexe()
    QString result = IndPs(2)
    result = otedernieres(result, 1)
    # QString der = result.substr (result.length ()-1, 1)
    QString der = result.right(1)
    QString d
    if (der == "a")
        d = "â"
    elif (der == "i" or der == "î")
        d = "î"
    elif (der == "u" or der == "û")
        d = "û"
    else:
        d = ""
    result = otedernieres(result, 1)
    result.append(d)
    #
       # wchar_t der = derniere (result)
       # wchar_t d
       # if (der == 'a') d = L'â'
       # else if (der == 'i' || der == L'î') d = L'î'
       # else if (der == 'u' || der == L'û') d = L'û'
       # else d = '\0'
       # result[result.size () - 1] = d
      # 
    return result

# auxiliaire
QString Verbe::auxiliaire()
    if AuxEtre.contains(inf): return "être"
    return "avoir"

# radicaux
QString Verbe::RadPres(P)
    if P < 1 or P > 6: return "numéro de personne invalide "
    return otedernieres(inf, 2)

QString Verbe::RadFut()
    if inf.endsWith('r'): return inf
    return otedernieres(inf, 1)

QString Verbe::RadPs() { return otedernieres(inf, 2); }
# manipulations : pronoms-radical-désinence
QString Verbe::elide(QString A, QString B)
    QString voyelles = "aâeéêiîoôuûy"
    # if (A.endsWith ('a') && voyelles.contains (B[0]))
    if A.endsWith('e') and voyelles.contains(B[0]):
        return otedernieres(A, 1) + "'" + B
    return A + " " + B

QString Verbe::Pron(P, QString F, refl)
    QString PR[7] = {"", "me", "te", "se", "nous", "vous", "se"    QString result = personne[P]
    if refl: result = result + " " + PR[P]
    # élision
    return elide(result, F)

QString Verbe::RD(QString R, QString D)
    # RD joint radical et désinence en gérant
    # les -e- et les cédilles.
    if not D.isEmpty(: and QString("oauâû").contains(D[0]))
    {
        if R.endsWith('c'):
            R.replace(R.length() - 1, 1, "ç")
        elif R.endsWith('g'):
            R.append("e")
    return R + D

# temps
QString Verbe::IndPres(P)
    QString R = RadPres(P)
    if (R == "") return ""
    QString D[7] = {"", "e", "es", "e", "ons", "ez", "ent"    return RD(R, D[P])

QString Verbe::IndFut(P) { return RD(RadFut(), GetDesFut(P)); }
QString Verbe::IndImpf(P) { return RD(RadPres(4), GetDesImpf(P)); }
QString Verbe::IndPs(P)
    if RadPs().isEmpty(): return ""
    return RD(RadPs(), GetDesPsAi(P))

QString Verbe::SubjPres(P)
    if P == 4 or P == 5) return RadPres(4) + GetDesSubjPres(P:
    return RD(RadPres(6), GetDesSubjPres(P))

QString Verbe::ImperPres(P)
    if P == 2:
        if deuxder(inf: == "er") return otedernieres(inf, 1)
        return IndPres(2)
    elif P == 4 or P == 5:
        return IndPres(P)
    return ""

QString Verbe::PartPres() { return RadPres(4) + "ant"; }
QString Verbe::OteReflechi(QString F)
    # éliminer le pronom réfléchi.
    if (npremieres(F, sizeof("s'")) == "s'")
        return otepremieres(F, sizeof("s'"))
    elif npremieres(F, 3: == "se ")
        return otepremieres(F, 3)
    return F

QString Verbe::PP()
    # return otedernieres (inf, 2).append ("é")
    return RD(otedernieres(inf, 2), "é")

# procédure de flexion
QString Verbe::conjugue(P, T, M, V, pr, g, n)
    QString aux = ""
    PPPP = False
    QString result = ""
    # vérifier la validité du champ P(ersonne)

    # pronominal
    if npremieres(inf, 2: == "s'" or npremieres(inf, 3) == "se ")
    {
        pronominal = True
        inf = OteReflechi(inf)
        aux = "être"
    else:
        pronominal = False
        aux = auxiliaire()
    # invalider le passif des intransitifs
    if V > 1 and pas_de_passif(inf) and M != part: return ""  # pas de passif

    # prévoir le PPPP (part. présent ou passé pronominal)
    PPPP = ((M == part) and pronominal)

    # éliminer le pronom sujet
    if M == imper or M == part or M == infin: pr = False

    # 1. voix
    if V == actif:
        if M == ind:  # indicatif actif
        {
            if T == pres:
                result = IndPres(P)
            elif T == fut:
                result = IndFut(P)
            elif T == impf:
                result = IndImpf(P)
            elif T == psimple:
                result = IndPs(P)
            else:
                result = compose(aux, P, T - 4, ind, actif)
        elif M == subj:  # subjonctif actif
        {
            if T == pres:
                result = SubjPres(P)
            elif T == impf:
                if not RadPs().isEmpty():
                    if P == 3:
                        result = circonflexe() + "t"
                    else:
                        result = IndPs(2) + "s" + GetDesSubjPres(P)
                else:
                    result = ""
            elif T == pcompose:  # 5
                result = compose(aux, P, pres, subj, actif)
            elif T == pqp:
                result = compose(aux, P, impf, subj, actif)
            else:
                result = ""
        elif M == cond:
            if T == pres:
                # calcul à partir du futur
                result = RD(RadFut(), GetDesImpf(P))
            elif T == pcompose:
                result = compose(aux, P, pres, cond, actif)
            else:
                result = ""
        elif M == imper:
            if P == 1 or P == 3 or P == 6:
                result = ""
            else:
                if T == pres:
                    result = ImperPres(P)
                elif T == pcompose:
                    result = compose(aux, P, pres, imper, actif)
        elif M == infin:  # inf:
        {
            if T == pres:
                result = inf
            elif T == pcompose:
                result = compose(aux, P, pres, infin, actif)
        elif M == part:
            if T == pres:
                result = PartPres()
            elif T == pcompose:
                result = compose(aux, P, pres, part, actif)
    elif V == passif:
        # si seul le part passé est demandé 
        if M == part:
            switch T:
                case pres:
                    return PartPres()
                case psimple:
                {
                    QString res = PP()
                    if g == 2: res.append("e")
                    if (n == 2 and (not res.endsWith("s"))) res.append("s")
                    return res
                default:
                    break
        if PP(: > "" and (aux == "avoir") and (inf != "être"))
            result = compose("être", P, T, M, actif)
        else:
            result = ""
    if result.isEmpty(): return ""
    # éliminer le pronom
    if result.size() > 2:
        if npremieres(result, 2: == "s'")
            result = otepremieres(result, 2)
        elif npremieres(result, 3: == "se ")
            result = otepremieres(result, 3)
    if pr:
        result = Pron(P, result, pronominal)
    elif PPPP:
        result = elide("se", result)
    return result

QString TVeter::RD(QString R, QString D)
    # repérer le futur/conditionnel par la finale du radical
    desR = (R.endsWith('r'))
    # repérer la dernière occurence de e dans le radical
    # if (desR) p = R.rfind('e', R.length()-3)
    if desR:
        p = R.lastIndexOf('e', R.length() - 3)
    else:
        p = R.lastIndexOf('e', R.length() - 2)
    # transformer en è si l''initiale de D est e
    if (D.startsWith('e') and (not D.endsWith('z'))) or desR: R.replace(p, 1, "è")
    return R + D

QString TVettell::RD(QString R, QString D)
    # repérer le futur/conditionnel par la finale du radical
    desR = R.endsWith('r')
    # repérer la dernière occurence de e dans le radical
    if desR:
        p = R.lastIndexOf('e', R.length() - 3)
    else:
        p = R.lastIndexOf('e', R.length() - 1)
    # transformer en è si l''initiale de D est e
    if (D[0] == 'e' and not D.endsWith('z')) or desR:  # R[-1] == 'r'
    {
        # QString redoubl = R.substr (p+1,1)
        # R.insert (p+1, redoubl)
        R.insert(p + 1, R.at(p + 1))
    return R + D

QString TVebrer::RD(QString R, QString D)
    # repérer la dernière occurence de é dans le radical
    size_t p = R.lastIndexOf("é")
    # transformer en è si l''initiale de D est e.
    if (p < string::npos and D[0] == 'e' and \
        (not D.endsWith('z') or R.endsWith('r')))
        R.replace(p, 1, "è")
    return R + D

QString TVyer::RD(QString R, QString D)
    # transformer en i si l''initiale de D est e.
    if D[0] == 'e' and not D.endsWith('z')) R = otedernieres(R, 1: + "i"
    return R + D

QString TVyer::RadFut()
    if (IsLast("envoyer", inf)) return otedernieres(inf, 4) + "err"
    return otedernieres(inf, 3) + "ier"

QString TVavoir::RadFut() { return "aur"; }
QString TVavoir::IndPres(P)
    QString D[7] = {"", "ai", "as", "a", "avons", "avez", "ont"    return D[P]

QString TVavoir::IndImpf(P) { return RD("av", GetDesImpf(P)); }
QString TVavoir::IndPs(P) { return RD("e", TVavoir::GetDesPsU(P)); }
QString TVavoir::SubjPres(P)
    QString D[7] = {"", "aie", "aies", "ait", "ayons", "ayez", "aient"    return D[P]

QString TVavoir::ImperPres(P)
    QString D[7] = {"", "", "aie", "", "ayons", "ayez", ""    return D[P]

QString TVavoir::PartPres() { return "ayant"; }
QString TVavoir::PP() { return "eu"; }
QString TVetre::RadFut() { return "ser"; }
QString TVetre::RadPs() { return "f"; }
QString TVetre::IndPres(P)
    QString D[7] = {"", "suis", "es", "est", "sommes", "êtes", "sont"    return D[P]

QString TVetre::IndImpf(P) { return RD("ét", GetDesImpf(P)); }
QString TVetre::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVetre::SubjPres(P)
    QString D[7] = {"", "sois", "sois", "soit", "soyons", "soyez", "soient"    return D[P]

QString TVetre::ImperPres(P)
    if P == 2 or P == 4 or P == 5:
        return SubjPres(P)
    else:
        return ""

QString TVetre::PartPres() { return "étant"; }
QString TVetre::PP() { return "été"; }
QString TValler::RadFut() { return otedernieres(inf, 5) + "ir"; }
QString TValler::IndPres(P)
    QString D[7] = {"", "vais", "vas", "va", "allons", "allez", "vont"    return D[P]

QString TValler::SubjPres(P)
    QString D = GetDesSubjPres(P)
    if P == 4 or P == 5: return "all" + D
    return "aill" + D

QString TValler::ImperPres(P)
    if P == 2:
        return otedernieres(inf, 5) + "va"
    else:
        return Verbe::ImperPres(P)

QString TVcueillir::RadFut()
    QString R = inf
    R.replace(R.length() - 2, 1, "e")
    return R

QString TVcueillir::PP() { return otedernieres(inf, 2) + "i"; }
QString TVsst::RadPres(P)
    if P < 1 or P > 6: return "numéro de personne invalide "
    return otedernieres(inf, 2)

QString TVsst::IndPres(P)
    QString R = RadPres(P)
    QString D
    if R.isEmpty(): return ""
    if P < 3:
        D = "s"
    elif P == 3:
        D = "t"
    else:
        return Verbe::IndPres(P)
    return RD(R, D)

QString TVsst::IndPs(P)
    if RadPs().isEmpty(): return ""
    return RD(RadPs(), GetDesPsI(P))

QString TVsst::PP()
    # QString radical = RadPs() + "i"
    return RadPs() + "i"

# héritiers de TVsst

TVaitre::TVaitre(QString i) : TVsst(i)
    modele = "TVaitre"
    pcirc = inf.lastIndexOf("î")  #, inf.length ())

QString TVaitre::RadPres(P)
    # pcirc = inf.rfind ("î", inf.length ())
    if P == 1 or P == 2) return npremieres(inf, pcirc: + "i"
    if P == 3) return otedernieres(inf, 3:
    return npremieres(inf, pcirc) + "iss"

QString TVaitre::RadPs() { return otedernieres(inf, 5); }
QString TVaitre::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVaitre::PP()
    # QString result = RadPs() + "u"
    return RadPs() + "u"

QString TVnaitre::RadPs() { return npremieres(inf, pcirc) + "qu"; }
QString TVnaitre::PP() { return npremieres(inf, pcirc - 1) + "é"; }
QString TVnaitre::IndPs(P) { return RadPs() + GetDesPsI(P); }
QString TVpaitre::IndPs(P)
    if (inf == "paître") return ""
    return RadPs() + GetDesPsU(P)

QString TVpaitre::RadPs() { return otedernieres(inf, 5); }
QString TVpaitre::PP()
    if (inf == "paître") return ""
    return RadPs() + "u"

QString TVboire::RadPres(P)
    if P < 4) return otedernieres(inf, 2:
    if P < 6) return otedernieres(inf, 4: + "uv"
    return otedernieres(inf, 2) + "v"

QString TVboire::RadPs() { return otedernieres(inf, 4); }
QString TVboire::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVboire::SubjPres(P)
    if P == 4 or P == 5) return RadPres(4) + GetDesSubjPres(P:
    return TVsst::SubjPres(P)

QString TVboire::PP() { return RadPs() + "u"; }
QString TVbouillir::RadPres(P)
    if P > 3) return otedernieres(inf, 2:
    return otedernieres(inf, 5)

QString TVcevoir::RadPres(P)
    if P < 4) return otedernieres(inf, 6: + "çoi"
    if P < 6) return otedernieres(inf, 3:
    return otedernieres(inf, 6) + "çoiv"

QString TVcevoir::RadFut() { return otedernieres(inf, 3) + "r"; }
QString TVcevoir::RadPs() { return otedernieres(inf, 6) + "c"; }
QString TVcevoir::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVcevoir::PP() { return RD(RadPs(), "u"); }
QString TVchoir::RadPres(P)
    if P < 1 or P > 6: return "numéro de personne invalide "
    return otedernieres(inf, 1)

QString TVchoir::RadPs() { return otedernieres(inf, 3); }
QString TVchoir::IndPres(P)
    if (inf == "déchoir")
    {
        if P == 4) return otedernieres(inf, 2: + "yons"
        if P == 5) return otedernieres(inf, 2: + "yez"
    if P == 4 or P == 5: return ""
    return TVsst::IndPres(P)

QString TVchoir::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVchoir::SubjPres(P)
    if (inf == "échoir") return TVsst::SubjPres(P)
    return ""

QString TVchoir::PP() { return RadPs() + "u"; }
QString TVclore::RadPres(P)
    if P < 3) return otedernieres(inf, 2:
    if P == 3) return otedernieres(inf, 3: + "ô"
    if P < 6:
        if (inf != "clore") return otedernieres(inf, 2) + "s"
        return ""
    return otedernieres(inf, 2) + "s"

QString TVclore::IndPres(P)
    if RadPres(P: > "") return TVsst::IndPres(P)
    return ""

QString TVclore::IndPs(P)
    if P < 1 or P > 6: return "numéro de personne invalide "
    return ""

QString TVclore::PP() { return otedernieres(inf, 2) + "s"; }
QString TVclure::RadPs() { return otedernieres(inf, 3); }
QString TVclure::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVclure::PP() { return RadPs() + "u"; }
QString TVconfire::RadPres(P)
    if P < 4) return otedernieres(inf, 2:
    if (inf != "frire") return otedernieres(inf, 2) + "s"
    return ""

QString TVconfire::RadPs() { return otedernieres(inf, 3); }
QString TVconfire::PP() { return RadPs() + "it"; }
QString TVcourir::RadFut() { return otedernieres(inf, 2) + "r"; }
QString TVcourir::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVcourir::PP() { return RadPs() + "u"; }
QString TVcroire::RadPres(P)
    if P == 4 or P == 5) return otedernieres(inf, 3: + "y"
    return otedernieres(inf, 2)

QString TVcroire::RadPs()
    # return otedernieres (inf, 4)
    return "cr"

QString TVcroire::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVcroire::PP() { return RadPs() + "u"; }
QString TVcroitre::RadPres(P)
    if P < 4) return otedernieres(inf, 3:
    return otedernieres(inf, 4) + "iss"

QString TVcroitre::RadPs() { return otedernieres(inf, 5) + "û"; }
QString TVcroitre::IndPs(P)
    QString D[7] = {"", "s", "s", "t", "mes", "tes", "rent"    return RD(RadPs(), D[P])

QString TVcroitre::PP() { return otedernieres(inf, 4) + "û"; }
QString TVdevoir::RadPres(P)
    if P < 4) return otedernieres(inf, 5: + "oi"
    if P < 6) return otedernieres(inf, 3:
    return otedernieres(inf, 5) + "oiv"

QString TVdevoir::RadFut() { return otedernieres(inf, 3) + "r"; }
QString TVdevoir::RadPs() { return otedernieres(inf, 5); }
QString TVdevoir::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVdevoir::PP() { return RadPs() + "û"; }
QString TVdire::RadPres(P)
    if P > 0 and P < 4) return otedernieres(inf, 2:
    return otedernieres(inf, 2) + "s"

QString TVdire::RadPs() { return otedernieres(inf, 3); }
QString TVdire::IndPres(P)
    if (inf == "dire" and P == 5) return "dites"
    return TVsst::IndPres(P)

QString TVdire::PP() { return otedernieres(inf, 2) + "t"; }
QString TVdormir::RadPres(P)
    if P > 3) return otedernieres(inf, 2:
    return otedernieres(inf, 3)

QString TVecrire::RadPres(P)
    if P > 3) return otedernieres(inf, 2: + "v"
    return otedernieres(inf, 2)

QString TVecrire::RadPs() { return RadPres(4); }
QString TVecrire::PP() { return otedernieres(inf, 2) + "t"; }
QString TVfaillir::IndPres(P)
    QString D[7] = {"",         "faux",    "faux",    "faut",
                    "faillons", "faillez", "faillent"    return D[P]

QString TVfaire::RadPres(P)
    if P > 3) return TVsst::RadPres(P: + "s"
    return TVsst::RadPres(P)

QString TVfaire::RadFut() { return otedernieres(inf, 4) + "er"; }
QString TVfaire::RadPs() { return otedernieres(inf, 4); }
QString TVfaire::IndPres(P)
    if P == 5) return otedernieres(inf, 2: + "tes"
    if P == 6) return otedernieres(inf, 4: + "ont"
    return TVsst::IndPres(P)

QString TVfaire::SubjPres(P)
    return otedernieres(inf, 3) + "ss" + GetDesSubjPres(P)

QString TVfaire::PP() { return IndPres(3); }
QString TVfuir::RadPres(P)
    if P == 4 or P == 5) return otedernieres(inf, 2: + "y"
    return otedernieres(inf, 1)

QString TVgesir::RadPres(P)
    if P < 3: return "gi"
    if P == 3: return "gî"
    return "gis"

QString TVgesir::IndFut(P)
    if P < 1 or P > 6: return "numéro de personne invalide "
    return ""

QString TVgesir::IndPs(P)
    if P < 1 or P > 6: return "numéro de personne invalide "
    return ""

QString TVgesir::PP() { return ""; }
QString TVindre::RadPres(P)
    if P < 4:
        return otedernieres(inf, 3)
    else:
        return otedernieres(inf, 4) + "gn"

QString TVindre::RadPs() { return RadPres(4); }
QString TVindre::PP() { return IndPres(3); }
QString TVir::RadPres(P)
    QString result = otedernieres(inf, 1)
    if P > 3: return result + "ss"
    return result

QString TVir::IndPs(P) { return RD(RadPs(), GetDesPsI(P)); }
QString TVir::PP() { return otedernieres(inf, 2) + "i"; }
QString TVlire::RadPres(P)
    if P > 3) return otedernieres(inf, 2: + "s"
    return otedernieres(inf, 2)

QString TVlire::RadPs() { return otedernieres(inf, 3); }
QString TVlire::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVlire::PP() { return RadPs() + "u"; }
QString TVtaire::RadPs() { return otedernieres(inf, 4); }
QString TVtaire::IndPs(P) { return RadPs() + GetDesPsU(P); }
QString TVmettre::RadPres(P)
    if P == 1 or P == 2) return otedernieres(inf, 3:
    if P == 3) return otedernieres(inf, 4:
    return otedernieres(inf, 2)

QString TVmettre::RadPs() { return otedernieres(inf, 5); }
QString TVmettre::PP() { return RadPs() + "is"; }
QString TVmourir::RadPres(P)
    if P == 4 or P == 5: return "mour"
    return "meur"

QString TVmourir::RadFut() { return otedernieres(inf, 2) + "r"; }
QString TVmourir::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVmourir::PP() { return "mort"; }
QString TVmouvoir::RadPres(P)
    if P < 4) return otedernieres(inf, 6: + "eu"
    if P < 6) return otedernieres(inf, 3:
    return otedernieres(inf, 6) + "euv"

QString TVmouvoir::RadFut() { return otedernieres(inf, 3) + "r"; }
QString TVmouvoir::RadPs() { return otedernieres(inf, 6); }
QString TVmouvoir::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVmouvoir::PP()
    if (inf == "mouvoir") return "mû"
    return RadPs() + "u"

QString TVouir::RadPres(P)
    if P == 4 or P == 5: return "oy"
    return "oi"

QString TVouir::IndPs(P)
    QString D[7] = {"", "ouïs", "ouïs", "ouït", "ouîmes", "ouîtes", "ouïrent"    return D[P]

QString TVouir::PP() { return "ouï"; }
QString TVplaire::RadPres(P)
    if P < 3) return otedernieres(inf, 2:
    if P == 3) return otedernieres(inf, 3: + "î"
    return otedernieres(inf, 2) + "s"

QString TVplaire::RadPs() { return otedernieres(inf, 4); }
QString TVplaire::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVplaire::PP() { return RadPs() + "u"; }
QString TVpleuvoir::IndPres(P)
    if P == 3) return otedernieres(inf, 4: + "t"
    if P == 6) return otedernieres(inf, 3: + "ent"
    return ""

QString TVpleuvoir::RadFut() { return otedernieres(inf, 3) + "r"; }
QString TVpleuvoir::RadPs() { return otedernieres(inf, 6); }
QString TVpleuvoir::IndPs(P)
    # if P == 3 || P == 6: return RD(RadPs(), GetDesPsU(P))
    return RD(RadPs(), GetDesPsU(P))
    return ""

QString TVpleuvoir::IndImpf(P)
    return otedernieres(inf, 3) + GetDesImpf(P)

QString TVpleuvoir::SubjPres(P)
    if P == 3 or P == 6) return otedernieres(inf, 3) + GetDesSubjPres(P:
    return ""

QString TVpleuvoir::PP() { return RadPs() + "u"; }
QString TVpleuvoir::conjugue(P, T, M, V, Pr)
    if P == 3 or P == 6) return Verbe::conjugue(P, T, M, V, P, Pr:
    return ""

QString TVpouvoir::RadFut() { return otedernieres(inf, 4) + "rr"; }
QString TVpouvoir::RadPs() { return "p"; }
QString TVpouvoir::IndPres(P)
    QString D[7] = {"", "peux", "peux", "peut", "pouvons", "pouvez", "peuvent"    return D[P]

QString TVpouvoir::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVpouvoir::SubjPres(P) { return "puiss" + GetDesSubjPres(P); }
QString TVpouvoir::PP() { return "pu"; }
QString TVpourvoir::RadPres(P)
    if P == 4 or P == 5) return otedernieres(inf, 2: + "y"
    return otedernieres(inf, 1)

QString TVpourvoir::RadPs() { return otedernieres(inf, 3); }
QString TVpourvoir::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVpourvoir::PP() { return RadPs() + "u"; }
QString TVvoir::RadPres(P)
    if P == 4 or P == 5) return otedernieres(inf, 2: + "y"
    return otedernieres(inf, 1)

#
   # QString TVvoir::RadFut()
   # {
   # if (inf == "voir" || inf == "revoir") return otedernieres (inf, 4) + "ier"
   # if (P < 6) return R + "ér"
   # return R + "ièr"
   # }
  # 

QString TVvoir::RadFut() { return otedernieres(inf, 3) + "err"; }
QString TVvoir::RadPs() { return otedernieres(inf, 3); }
QString TVvoir::PP() { return otedernieres(inf, 3) + "u"; }
QString TVrire::RadPs() { return otedernieres(inf, 3); }
QString TVsavoir::RadPres(P)
    if P < 4) return otedernieres(inf, 4: + "i"
    return otedernieres(inf, 3)

QString TVsavoir::RadFut() { return otedernieres(inf, 4) + "ur"; }
QString TVsavoir::RadPs() { return otedernieres(inf, 5); }
QString TVsavoir::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVsavoir::SubjPres(P)
    return otedernieres(inf, 4) + "ch" + GetDesSubjPres(P)

QString TVsavoir::ImperPres(P)
    QString D[7] = {"", "e", "", "ons", "ez", ""    if (D[P] > "") return otedernieres(inf, 4) + "ch" + D[P]
    return ""

QString TVsavoir::PartPres() { return otedernieres(inf, 4) + "chant"; }
QString TVsavoir::PP() { return RadPs() + "u"; }
QString TVservir::RadPres(P)
    if P < 4) return otedernieres(inf, 3:
    return otedernieres(inf, 2)

QString TVquerir::RadPres(P)
    if P < 4) return otedernieres(inf, 4: + "ier"
    if P == 6) return otedernieres(inf, 4: + "ièr"
    return otedernieres(inf, 2)

QString TVquerir::PP() { return otedernieres(inf, 4) + "is"; }
QString TVquerir::RadPs() { return otedernieres(inf, 4); }
QString TVquerir::IndPs(P) { return RD(RadPs(), GetDesPsI(P)); }
QString TVsoudre::RadPres(P)
    if P < 4) return otedernieres(inf, 3:
    return otedernieres(inf, 4) + "lv"

QString TVsoudre::RadPs() { return otedernieres(inf, 4) + ""; }
QString TVsoudre::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVsoudre::PP() { return RadPs() + "u"; }
QString TVsuivre::RadPres(P)
    if P < 4) return otedernieres(inf, 3:
    return otedernieres(inf, 2)

QString TVvivre::RadPs() { return otedernieres(inf, 4) + "éc"; }
QString TVvivre::IndPs(P) { return RadPs() + GetDesPsU(P); }
QString TVvivre::PP() { return RadPs() + "u"; }
QString TVsurseoir::RadPres(P)
    QString F = "surso"
    if P == 4 or P == 5: return F + "y"
    return F + "i"

QString TVsurseoir::RadPs() { return otedernieres(inf, 4); }
QString TVsurseoir::IndPs(P)
    if (inf == "seoir") return ""
    return TVsst::IndPs(P)

QString TVsurseoir::PP() { return IndPs(1); }
QString TVvenir::RadFut() { return otedernieres(inf, 4) + "iendr"; }
QString TVvenir::circonflexe() { return otedernieres(inf, 4) + "în"; }
QString TVvenir::RadPres(P)
    if P < 4) return otedernieres(inf, 4: + "ien"
    if P < 6) return otedernieres(inf, 2:
    return otedernieres(inf, 4) + "ienn"

QString TVvenir::IndPs(P)
    QString D[7] = {"", "ins", "ins", "int", "înmes", "întes", "inrent"    return otedernieres(inf, 4) + D[P]

QString TVvenir::PP() { return otedernieres(inf, 2) + "u"; }
# ne pas permuter les 2 suivants

QString TVvetir::RadPres(P)
    if P == 3) return otedernieres(inf, 3:
    return TVsst::RadPres(P)

QString TVvetir::PP() { return RadPs() + "u"; }
QString TVtir::RadPres(P)
    if P < 4) return otedernieres(inf, 3:
    return TVsst::RadPres(P)

QString TVtir::IndPs(P) { return RD(RadPs(), GetDesPsI(P)); }
# ne pas permuter les 2 précédents

QString TVuire::RadPres(P)
    if P > 3) return TVsst::RadPres(P: + "s"
    return TVsst::RadPres(P)

QString TVuire::RadPs() { return RadPres(4); }
QString TVuire::PP()
    if (inf == "luire" or inf == "nuire") return otedernieres(inf, 2)
    return IndPres(3)

QString TVtraire::RadPres(P)
    if P == 4 or P == 5) return otedernieres(inf, 3: + "y"
    return otedernieres(inf, 2)

QString TVtraire::RadPs() { return ""; }
QString TVtraire::PP() { return IndPres(3); }
QString TVvaincre::RadPres(P)
    if P < 4) return otedernieres(inf, 2:
    return otedernieres(inf, 3) + "qu"

QString TVvaincre::IndPres(P)
    if P == 3) return RadPres(3:
    return TVsst::IndPres(P)

QString TVvaincre::RadPs() { return RadPres(4); }
QString TVvaincre::PP() { return otedernieres(inf, 3) + "cu"; }
# fin des héritiers de TVsst

# TVxxt, classe abstraite
QString TVxxt::RadPs() { return otedernieres(inf, 3); }
QString TVxxt::IndPres(P)
    if P < 3) return RadPres(P: + "x"
    return TVsst::IndPres(P)

QString TVxxt::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
#  héritiers de TVxxt

QString TVvaloir::RadPres(P)
    if P < 4) return otedernieres(inf, 4: + "u"
    return otedernieres(inf, 3)

QString TVvaloir::RadFut() { return otedernieres(inf, 4) + "udr"; }
QString TVvaloir::SubjPres(P)
    if P == 4 or P == 5) return otedernieres(inf, 3) + GetDesSubjPres(P:
    return RD(otedernieres(inf, 4) + "ill", GetDesSubjPres(P))

QString TVvaloir::PP() { return RadPs() + "u"; }
QString TVfalloir::IndPres(P)
    if P == 3: return "faut"
    return ""

QString TVfalloir::IndFut(P)
    if P == 3: return "faudra"
    return ""

QString TVfalloir::IndPs(P)
    if P == 3: return "fallut"
    return ""

QString TVfalloir::SubjPres(P)
    if P == 3: return "faille"
    return ""

QString TVfalloir::conjugue(P, T, M, V, pr)
    if P != 3: return ""
    return Verbe::conjugue(P, T, M, V, pr)

QString TVvouloir::RadPres(P)
    if P < 4) return otedernieres(inf, 6: + "eu"
    if P < 6) return otedernieres(inf, 3:
    return otedernieres(inf, 6) + "eul"

QString TVvouloir::RadFut() { return otedernieres(inf, 4) + "dr"; }
QString TVvouloir::SubjPres(P)
    QString D = GetDesSubjPres(P)
    QString R
    if D[1] == 'e':
        R = "veuill"
    else:
        R = "voul"
    return R + D

QString TVvouloir::PP() { return RadPs() + "u"; }
QString TVdre::IndPres(P)
    QString D
    if P < 3:
        D = "s"
    elif P == 3:
        D = ""
    else:
        return Verbe::IndPres(P)
    return RD(RadPres(P), D)

QString TVdre::IndPs(P) { return RD(RadPs(), GetDesPsI(P)); }
QString TVdre::PP() { return RadPs() + "u"; }
QString TVasseoir::RadPres(P)
    if P < 4) return otedernieres(inf, 4: + "ie"
    return otedernieres(inf, 3) + "y"

QString TVasseoir::IndImpf(P)
    return RD(otedernieres(inf, 3) + "y", GetDesImpf(P))

QString TVasseoir::RadPs() { return otedernieres(inf, 4); }
QString TVasseoir::IndPres(P)
    QString D
    if P < 3:
        D = "ds"
    elif P == 3:
        D = "d"
    else:
        return TVdre::IndPres(P)
    return RD(RadPres(P), D)

QString TVasseoir::PP() { return RadPs() + "is"; }
QString TVcoudre::RadPres(P)
    if P < 4) return TVdre::RadPres(P:
    return otedernieres(inf, 3) + "s"

QString TVcoudre::RadPs() { return RadPres(4); }
QString TVmoudre::RadPres(P)
    if P < 4) return TVdre::RadPres(P:
    return otedernieres(inf, 3) + ""

QString TVmoudre::RadPs() { return RadPres(4); }
QString TVmoudre::IndPs(P) { return RD(RadPs(), GetDesPsU(P)); }
QString TVprendre::RadPres(P)
    if P < 4) return otedernieres(inf, 2:
    if P < 6) return otedernieres(inf, 3:
    return otedernieres(inf, 3) + "n"

QString TVprendre::RadPs() { return otedernieres(inf, 5); }
QString TVprendre::SubjPres(P)
    QString D = GetDesSubjPres(P)
    QString R = RadPres(4)
    if D[0] == 'e': R += "n"
    return R + D

QString TVprendre::PP() { return IndPs(1); }
QString TVouvrir::IndPs(P) { return RD(RadPs(), GetDesPsI(P)); }
QString TVouvrir::ImperPres(P)
    if P == 2) return otedernieres(inf, 2: + "e"
    return Verbe::ImperPres(P)

QString TVouvrir::PP() { return otedernieres(inf, 3) + "ert"; }
QString TVbattre::RadPres(P)
    if P == 3) return otedernieres(inf, 4:
    return TVtir::RadPres(P)

QString TVbattre::PP() { return RadPs() + "u"; }
QString Verbe::compose(QString A, P, T, M, V)
    QString partp = PP()
    # vérifier l'existence du participe passé
    if not partp.isEmpty():
        Verbe *aux
        if (A == "avoir")
            aux = new TVavoir("avoir")
        else:
            aux = new TVetre("être")
        QString fx = aux.conjugue(P, T, M, V, False, 0, 0)
        delete aux
        QString result
        if not fx.isEmpty():
            result = fx + " " + partp
        else:
            return ""
        if ((P > 3 and A == "être") and not result.endsWith('s'))
            result.append("s")  # = result + "s"
        return result
    return ""

Verbe *verbe_m(QString inf)
    Verbe *Vb
    # lexique
    #  auxiliaires

    Vb = NULL
    if (inf == "être")
        Vb = new TVetre(inf)
    elif (inf == "avoir")
        Vb = new TVavoir(inf)
    elif (inf == "pouvoir")
        Vb = new TVpouvoir(inf)
    elif (inf == "vouloir")
        Vb = new TVvouloir(inf)

    # autres verbes
    elif (inf == "aller")
        Vb = new TValler(inf)
    elif (inf == "asservir")
        Vb = new TVir(inf)
    elif (inf == "faillir")
        Vb = new TVfaillir(inf)
    elif (inf == "frire" or inf == "circoncire")
        Vb = new TVconfire(inf)
    elif (inf == "gésir")
        Vb = new TVgesir(inf)
    elif (inf == "mourir")
        Vb = new TVmourir(inf)
    elif (inf == "offrir")
        Vb = new TVouvrir(inf)
    elif (inf == "ouïr")
        Vb = new TVouir(inf)
    elif (inf == "rire" or inf == "sourire")
        Vb = new TVrire(inf)
    elif (inf == "voir" or inf == "prévoir" or inf == "revoir")
        Vb = new TVvoir(inf)
    elif (inf == "se voir" or inf == "se revoir")
        Vb = new TVvoir(inf)
    elif (inf == "surseoir")
        Vb = new TVsurseoir(inf)
    elif (inf == "taire")
        Vb = new TVtaire(inf)

    # variantes du premier groupe
    elif Eter.contains(inf:  # find (" "+inf+" ", 0) < QString::npos
 or IsLast("emer", inf) or IsLast("ener", inf) or \
             IsLast("eper", inf) or IsLast("erer", inf) or \
             IsLast("eser", inf) or IsLast("ever", inf) or IsLast("evrer", inf))
        Vb = new TVeter(inf)
    elif (IsLast("ébrer", inf) or IsLast("écer", inf) or \
             IsLast("écher", inf) or IsLast("écrer", inf) or \
             IsLast("éder", inf) or IsLast("éger", inf) or \
             IsLast("égler", inf) or IsLast("égner", inf) or \
             IsLast("égrer", inf) or IsLast("éguer", inf) or \
             IsLast("éler", inf) or IsLast("émer", inf) or \
             IsLast("éner", inf) or IsLast("éper", inf) or \
             IsLast("équer", inf) or IsLast("érer", inf) or \
             IsLast("éser", inf) or IsLast("éter", inf) or \
             IsLast("étrer", inf) or IsLast("évrer", inf) or \
             IsLast("éyer", inf))
    {
        Vb = new TVebrer(inf)
    elif (IsLast("eler", inf) or IsLast("eter", inf))
        Vb = new TVettell(inf)

    elif (IsLast("yer", inf))
        Vb = new TVyer(inf)

    # modèle général 1er groupe
    elif (IsLast("er", inf))
        Vb = new Verbe(inf)

    # naître, paître et paraître : ne pas séparer
    elif (IsLast("naître", inf) and inf.size() < 8)  # != connaître
        Vb = new TVnaitre(inf)
    elif (IsLast("paître", inf))
        Vb = new TVpaitre(inf)
    elif (IsLast("aître", inf))
        Vb = new TVaitre(inf)
    # ne pas séparer les 3 précédentes
    elif (IsLast("asseoir", inf))
        Vb = new TVasseoir(inf)
    elif (IsLast("battre", inf))
        Vb = new TVbattre(inf)
    elif (IsLast("boire", inf))
        Vb = new TVboire(inf)
    elif (IsLast("bouillir", inf))
        Vb = new TVbouillir(inf)
    elif (IsLast("cevoir", inf))
        Vb = new TVcevoir(inf)
    elif (IsLast("choir", inf))
        Vb = new TVchoir(inf)
    elif (IsLast("clore", inf))
        Vb = new TVclore(inf)
    elif (IsLast("clure", inf))
        Vb = new TVclure(inf)
    elif (IsLast("confire", inf))
        Vb = new TVconfire(inf)
    elif (IsLast("courir", inf))
        Vb = new TVcourir(inf)
    elif (IsLast("croire", inf))
        Vb = new TVcroire(inf)
    elif (IsLast("croître", inf))
        Vb = new TVcroitre(inf)
    elif (IsLast("cueillir", inf))
        Vb = new TVcueillir(inf)
    elif (IsLast("devoir", inf))
        Vb = new TVdevoir(inf)
    elif (IsLast("dire", inf))
        Vb = new TVdire(inf)
    elif (IsLast("dormir", inf))
        Vb = new TVdormir(inf)
    elif (IsLast("faire", inf))
        Vb = new TVfaire(inf)
    elif (IsLast("écrire", inf) or IsLast("scrire", inf))
        Vb = new TVecrire(inf)
    elif (IsLast("fuir", inf))
        Vb = new TVfuir(inf)
    elif (IsLast("lire", inf))
        Vb = new TVlire(inf)
    elif (IsLast("mouvoir", inf))
        Vb = new TVmouvoir(inf)
    elif (IsLast("ouvrir", inf))
        Vb = new TVouvrir(inf)
    elif (IsLast("mettre", inf))
        Vb = new TVmettre(inf)
    elif (IsLast("plaire", inf))
        Vb = new TVplaire(inf)
    elif (IsLast("pleuvoir", inf))
        Vb = new TVpleuvoir(inf)
    elif (IsLast("pourvoir", inf))
        Vb = new TVpourvoir(inf)
    elif (IsLast("prendre", inf))
        Vb = new TVprendre(inf)
    elif (IsLast("quérir", inf))
        Vb = new TVquerir(inf)
    elif (IsLast("saillir", inf))
        Vb = new Verbe(inf)
    elif (IsLast("savoir", inf))
        Vb = new TVsavoir(inf)
    elif (IsLast("servir", inf))
        Vb = new TVservir(inf)
    elif (IsLast("soudre", inf))
        Vb = new TVsoudre(inf)
    elif (IsLast("suivre", inf))
        Vb = new TVsuivre(inf)
    elif (IsLast("traire", inf))
        Vb = new TVtraire(inf)
    elif (IsLast("vaincre", inf))
        Vb = new TVvaincre(inf)
    elif (IsLast("venir", inf) or IsLast("tenir", inf))
        Vb = new TVvenir(inf)
    elif (IsLast("uire", inf))
        Vb = new TVuire(inf)
    elif (IsLast("valoir", inf))
        Vb = new TVvaloir(inf)
    elif (inf == "falloir")
        Vb = new TVfalloir(inf)
    elif (IsLast("vivre", inf))
        Vb = new TVvivre(inf)

    # -dre
    elif (IsLast("indre", inf))
        Vb = new TVindre(inf)
    elif (IsLast("coudre", inf))
        Vb = new TVcoudre(inf)
    elif (IsLast("moudre", inf))
        Vb = new TVmoudre(inf)
    elif (IsLast("dre", inf))
        Vb = new TVdre(inf)
    # -tir
    elif (IsLast("vêtir", inf))
        Vb = new TVvetir(inf)
    elif (IsLast("mentir", inf) or IsLast("sentir", inf) or \
             IsLast("partir", inf) or IsLast("repentir", inf) or \
             IsLast("sortir", inf))
        Vb = new TVtir(inf)

    # 2ème groupe
    elif (IsLast("ir", inf))
        Vb = new TVir(inf)

    else:
        Vb = NULL

    return Vb

QString conjugue(QString inf, P, T, M, V, Pr, g, n)
    Verbe *Vb

    Vb = verbe_m(inf)
    # lexique
    #  auxiliaires
    if Vb != NULL:
        QString result = Vb.conjugue(P, T, M, V, Pr, g, n)
        delete Vb
        return result
    return ""

QString conjnat(QString inf, QString morpho)
    p = 0
    nb = 0
    t = 0
    m = 0
    v = 0
    g = 0

    n = 0
    QStringList lm = morpho.split(' ')
    foreach (QString trait, lm)
    {
        n = personnes.indexOf(trait)
        if n >= 0:
            p = n + 1
            continue
        n = nombres.indexOf(trait)
        if n >= 0:
            nb = n + 1
            continue
        n = temps.indexOf(trait)
        if n >= 0:
            t = n + 1
            continue
        n = modes.indexOf(trait)
        if n >= 0:
            m = n + 1
            continue
        n = voix.indexOf(trait)
        if n >= 0:
            v = n + 1
            continue
        n = genres.indexOf(trait)
        if n >= 0:
            g = n + 1
            continue
    pnb = p * nb
    return conjugue(inf, pnb, t, m, v, (p != 3), g, nb)

QString tableau(QString verbe, voix)
    # wostringstream flux
    QString ret
    QTextStream flux(&ret)
    Verbe *v = verbe_m(verbe)
    for m in range(1, 5):
        flux << endl << mode[m] << endl
        for t in range(1, 5): flux << augmente(temps[t])
        flux << endl
        for p in range(1, 7):
            for t in range(1, 5):
                flux << augmente(v.conjugue(p, t, m, voix, True))
            flux << endl
        flux << endl

        for t in range(5, 9): flux << augmente(temps[t])
        flux << endl
        for p in range(1, 7):
            for t in range(5, 9):
                flux << augmente(v.conjugue(p, t, m, voix, True))
            flux << endl
    delete v
    return ret
    # return flux.str ()

# ------------------------------------------------------------
#  Flexion des noms
# ------------------------------------------------------------

Nom::Nom(QString s)
    sing = s
    modele = "Nom"

Nom::~Nom() {}
QString Nom::getModele() { return modele; }
QString Nom::pluriel()
    const QStringList als = QStringList() << "bal"
                                          << "cal"
                                          << "carnaval"
                                          << "chacal"
                                          << "festival"
                                          << "récital"
                                          << "régal"

    if (sing == "oeil" or sing == "œil")
        return "yeux"
    elif (sing == "ail")
        return "aulx"
    return sing + "s"

QString NomSXZ::pluriel() { return sing; }
QString NomAL::pluriel() { return otedernieres(sing, 2) + "aux"; }
QString NomAIL::pluriel() { return otedernieres(sing, 3) + "aux"; }
QString NomAUEU::pluriel() { return sing + "x"; }
Nom *nom_m(QString n)
    QString als[11] = {"bal",      "cal", "carnaval", "cérémonial", "chacal",
                       "festival", "pal", "récital",  "régal",      "santal"    QString ail[7] = {"bail",    "corail",  "émail",  "soupirail",
                      "travail", "vantail", "vitrail"    QString aueus[6] = {"landau", "sarrau", "bleu",
                        "pneu",   "émeu",   "lieu (poisson)"    QString oux[7] = {"bijou", "caillou", "chou", "genou",
                      "hibou", "joujou",  "pou"    QString inex = "pas de plurie"
    QString result = "nom_m Échec de la recherche"
    # QString nom = Nom(n)
    Nom *nom = NULL
    QChar d = derniere(n)
    # if (d == 's' || d == 'x' || d == 'z') nom = new NomSXZ (n)
    if (QString("sxz").contains(d))
        nom = new NomSXZ(n)
    elif deuxder(n: == "al" and index_t(als, n, 11) < 0)
        nom = new NomAL(n)
    elif (n == "bétail")
        result = inex
    elif dernieres(n, 3: == "ail" and index_t(ail, n, 6) > -1)
        nom = new NomAIL(n)
    elif ((IsLast("eu", n) or IsLast("au", n)) and index_t(aueus, n, 5) < 0)
        nom = new NomAUEU(n)
    elif index_t(oux, n, 6) > -1:
        nom = new NomAUEU(n)  # result = n + "x"
    else:
        nom = new Nom(n)
    return nom

# ------------------------------------------------------------
#  Flexion des adjectifs
# ------------------------------------------------------------

Adjectif::Adjectif(QString a)
    graphie = a
    modele = "Adjectif"

Adjectif::~Adjectif() {}
QString Adjectif::getModele() { return modele; }
QString Adjectif::feminin()
    QString mascs[13] = {"bénin", "doux",   "faux", "favori", "fou",
                         "frais", "jaloux", "long", "malin",  "mou",
                         "muet",  "roux",   "sot"    QString fems[13] = {"bénigne", "douce",   "fausse", "favorite", "folle",
                        "fraîche", "jalouse", "longue", "maligne",  "molle",
                        "muette",  "rousse",  "sotte"    i = index_t(mascs; 12)
    if i > -1: return fems[i]
    if derniere(graphie) == 'e': return graphie
    return graphie + "e"

QString Adjectif::pluriel(fem)
    Nom *nom
    if fem:
        nom = new Nom(feminin())
    else:
        nom = nom_m(graphie)
    QString result = nom.pluriel()
    return result

QString Adjectif::accorde(g, n)
    QString ret
    if g == 1:
        ret = feminin()
    else:
        ret = graphie
    if n == 1) ret = pluriel(g > 0:
    return ret

# irrégularités :
# gu - guë

QString Gras::feminin() { return graphie + "se"; }
QString Aigu::feminin() { return graphie + "ë"; }
QString ElEil::feminin() { return graphie + "le"; }
QString Al::pluriel(fem)
    if fem) return Adjectif::pluriel(1:
    QString liste_al[7] = {"banal",   "bancal", "fatal", "final",
                           "glacial", "natal",  "naval"    if index_t(liste_al, graphie, 6) > -1:
        if fem: return graphie + "es"
        return graphie + "s"
    return otedernieres(graphie, 1) + "ux"

QString Al::accorde(g, n)
    if n) return pluriel(g:
    return Adjectif::accorde(g, 0)

QString Eux::feminin()
    if (graphie == "vieux") return "vieille"
    return otedernieres(graphie, 1) + "se"

QString El::feminin() { return otedernieres(graphie, 2) + "elle"; }
QString Er::feminin() { return otedernieres(graphie, 2) + "ère"; }
QString AdjF::feminin() { return otedernieres(graphie, 1) + "ve"; }
QString AdjC::feminin()
    QString mascs[4] = {"caduc", "grec", "public", "sec"    QString fems[4] = {"caduque", "grecque", "publique", "sèche"    i = index_t(mascs; 3)
    if i > -1: return fems[i]
    return graphie + "he"

QString Eau::feminin() { return otedernieres(graphie, 2) + "lle"; }
QString Et::feminin()
    QString liste[10] = {"complet",   "concret",   "désuet",  "discret",
                         "incomplet", "indiscret", "inquiet", "quiet",
                         "replet",    "secret"    if index_t(liste, graphie, 9) > -1:
        return otedernieres(graphie, 2) + "ète"
    return graphie + "te"

QString Mon::feminin() { return otedernieres(graphie, 2) + "a"; }
QString Mon::pluriel(fem)
    if fem:# éviter un avertissement du compilateur
    return otedernieres(graphie, 2) + "es"

QString Bon::feminin() { return graphie + "ne"; }
QString Tout::pluriel(fem)
    if fem: return "toutes"
    return "tous"

Pronom::Pronom()
    map.insert("ce", "cette,ces,ces")
    map.insert("celui", "celle,ceux,celles")
    map.insert("celui-ci", "celle-ci,ceux-ci,celles-ci")
    map.insert("le", "la,les,les")
    map.insert("un", "une,des,des")

QString Pronom::accorde(QString p, QString m)
    p = p.simplified()
    if not map.keys().contains(p)) return p.append('*':
    if (m.contains("fém"))
    {
        if (m.contains("plur")) return map.value(p).section(',', 2, 2)
        return map.value(p).section(',', 0, 0)
    elif (m.contains("plur"))
    {
        return map.value(p).section(',', 1, 1)
    else:
        return p

QString pluriel(QString l, QString n)
    if (n == "singulier") return l
    QString irregs[6] = {"bonhomme", "grand-mère",   "grand-père",
                         "madame",   "mademoiselle", "monsieur"    QString irregp[6] = {"bonshommes", "grands-mères",   "grands-pères",
                         "mesdames",   "mesdemoiselles", "messieurs"    i = index_t(irregs; 6)
    if i > -1: return irregp[i]
    QString result
    Nom *nom = nom_m(l)
    if nom != NULL:
        result = nom.pluriel()
        delete nom
        return result
    return "Échec de la recherche"

QString accorde(QString adj, QString m)
    QString result
    genre = 0
    nombre = 0
    if (m.contains("féminin")) genre = 1
    if (m.contains("pluriel")) nombre = 1
    Adjectif *inst = NULL
    if (IsLast("el", adj) or IsLast("eil", adj) or adj == "gentil" or \
        adj == "nul")
        inst = new ElEil(adj)
    elif (IsLast("al", adj))
        inst = new Al(adj)
    elif (IsLast("gu", adj))
        inst = new Aigu(adj)
    elif (IsLast("eux", adj))
        inst = new Eux(adj)
    elif (IsLast("el", adj))
        inst = new El(adj)
    elif (IsLast("er", adj))
        inst = new Er(adj)
    elif (IsLast("f", adj))
        inst = new AdjF(adj)
    elif (IsLast("c", adj))
        inst = new AdjC(adj)
    elif (IsLast("eau", adj))
        inst = new Eau(adj)
    elif (IsLast("et", adj))
        inst = new Et(adj)
    elif (adj == "las" or adj == "gras" or adj == "gros")
        inst = new Gras(adj)
    elif (QStringList(: << "mon"
                            << "ton"
                            << "son")
                 .contains(adj))
        inst = new Mon(adj)
    elif (IsLast("ien", adj) or IsLast("on", adj) or IsLast("yen", adj))
        inst = new Bon(adj)
    elif (adj == "tout")
        inst = new Tout(adj)
    else:
        inst = new Adjectif(adj)
    if inst != NULL:
        result = inst.accorde(genre, nombre)
        delete inst
    else:
        result = "Échec de la recherche."
    return result
