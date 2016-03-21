/*         syntaxe.cpp      */

#include <QFile>
#include <QRegExp>
#include "syntaxe.h"

ElS::ElS(QString lin, RegleS *parent)
{
	_regle = parent;	
	QStringList ecl = lin.split(':', QString::KeepEmptyParts);
	_lemmes = ecl.at(1).split(',',QString::SkipEmptyParts);
	_pos    = ecl.at(2).split(',',QString::SkipEmptyParts);
	_morphos = ecl.at(3).split(' ',QString::SkipEmptyParts);
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
			if (elm.startsWith(em))
				ok = true;
		}
		if (!ok) return false;
	}
	return true;
}

bool ElS::okPos(QString p)
{
	return _pos.isEmpty() || _pos.contains(p);
}

RegleS::RegleS(QStringList lignes)
{
	QStringList cles = QStringList()
		<<"id"<<"doc"<<"pere"<<"super"<<"sub"
	//     0     1       2       3       4
		<<"sens"<<"accord"<<"tr"<<"f";
	//      5        6        7
	foreach (QString lin, lignes)
	{
		QStringList ecl = lin.split(':');
		int i = cles.indexOf(ecl.at(0));
		switch (i)
		{
			case 0: _id     = ecl.at(1);break;
			case 1: _doc    = ecl.at(1);break;
			case 2: _idPere = ecl.at(1);break;
			case 3: _super  = new ElS(lin, this);
			case 4: _sub    = new ElS(lin, this);
			case 5: _sens   = ecl.at(1);break;
			case 6: _accord = ecl.at(1);break;
			case 7: _tr     = ecl.at(1);break;
			case 8: _f      = ecl.at(1);break;
			default:break;
		}
	}
}

QString RegleS::doc()
{
	return _doc;
}

QString RegleS::id()
{
	return _id;
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

QString RegleS::fonction(Mot *super, Mot *sub)
{
	QString ret = _f;
	if (super != NULL) ret.replace("<super>", super->gr());
	if (sub != NULL) ret.replace("<sub>", sub->gr());
	return ret;
}

QString RegleS::tr()
{
	return _tr;
}

Super::Super (RegleS *r, QStringList m, Mot *parent)
{
	_regle = r;
	_morpho = m;
	_mot = parent;
}

Mot* Super::mot()
{
	return _mot;
}

RegleS* Super::regle()
{
	return _regle;
}

/**
 * \fn Mot::Mot(QString g)
 * \brief Créateur de la classe Mot.
 */
Mot::Mot(QString g)
{
	_gr = g;
}

void Mot::addRSub(RegleS *r)
{
	_rSub.append (r);
}

void Mot::addSuper(RegleS *r, QStringList m)
{
	_super.append (new Super(r, m, this));
}

QString Mot::gr()
{
	return _gr;
}

QString Mot::humain()
{
	QString ret;
	QTextStream fl(&ret);
	fl << _gr << "\n";
	foreach (Lemme *lem, _morphos.keys())
		fl << lem->grq() << "    - "<<lem->traduction("fr")<<"\n";
	return ret;
}

MapLem Mot::morphos()
{
	return _morphos;
}

QChar Mot::ponctD()
{
	return _ponctD;
}

QChar Mot::ponctG()
{
	return _ponctG;
}

void Mot::setMorphos(MapLem m)
{
	_morphos = m;
}

void Mot::setPonctD(QChar p)
{
	_ponctD = p;
}

void Mot::setPonctG(QChar p)
{
	_ponctG = p;
}

QList<Super*> Mot::super()
{
	return _super;
}

Syntaxe::Syntaxe(QString t, Lemmat *parent)
{
	_lemmatiseur = parent;
	setText (t);
	// lecture des données
	QFile fs (qApp->applicationDirPath () +"/data/syntaxe.la");
    fs.open (QFile::ReadOnly);
    QTextStream fls (&fs);
	QStringList slr; // liste des lignes de la dernière règle lue
    while (!fls.atEnd ())
	{
		QString l = fls.readLine ().simplified();
		if ((l.isEmpty() && !fls.atEnd()) || l.startsWith ("!"))
			continue;
		/*
		// variable
		if (l.startsWith ('$'))
		{
		_variables[l.section('=',0,0)]=l.section('=',1,1);
		continue;
		}
		*/
		QStringList eclats = l.split (":");
		if ((eclats.at (0) == "id" || fls.atEnd()) && !slr.empty())
		{
			_regles.append (new RegleS (slr));
			slr.clear();
		}
		else slr.append (l);
	}
    fs.close ();
}

QString Syntaxe::analyse (QString t, int p)
{
	const QList<QChar> chl;
	const int tl = t.length()-1;
	const QString pp = ".;!?";
	_motsP.clear();
	_motsS.clear();
	// avancer jusqu'à la fin du mot sous le curseur
	while (p<tl-1 && t.at(p+1).isLetter()) ++p;
	bool limite=false;
	QString m;
	QChar ponctD = '\0';
	QChar ponctG = '\0';
	// mots à gauche de motCour
	int i = p;
	while (i>-1 && !limite)
	{
		QChar c = t.at(i);
		if (c.isLetter()) m.prepend (c);
		else if (!m.isEmpty())
		{
			Mot *nm = new Mot(m);
			nm->setMorphos(_lemmatiseur->lemmatiseM(m));
			_motsP << nm;
			m.clear();
			nm->setPonctG(ponctG);
			nm->setPonctD(ponctD);
			ponctG = ponctD;
			ponctD = '\0';
		}
		limite = (pp.contains(c) 
				  || (i>0 && c=='\n' && t.at(i-1)=='\n'));
		if (!limite && c.isPunct())
			ponctD = c;
		--i;
	}
	// le premier mot de la liste est le mot Courant. 
	_motCour = _motsP.takeFirst();

	// Peuplement des listes _rSub et _rSuper
	// pour chaque règle syntaxique
	foreach (RegleS *r, _regles)
	{
		// pour chaque lemme de motCour
		foreach (Lemme *l, _motCour->morphos().keys())
		{
			// pour chaque morpho du lemme
			QList<SLem> lsl = _motCour->morphos().value(l);
			foreach (SLem sl, lsl)
			{
				QString m = sl.morpho;
				if (r->estSuper(l, m))
					_motCour->addSuper(r,m.split(' '));
			}
		}
	}
	limite = false;
	i = p+1;
	while (i<tl && !limite)
	{
		QChar c = t.at(i);
		if (c.isLetter()) m.append (c);
		else if (!m.isEmpty())
		{
			Mot *nm = new Mot(m);
			_motsS << nm;
			m.clear();
			nm->setPonctD(ponctG);
			nm->setPonctG(ponctD);
			ponctD = ponctG;
			ponctG = '\0';
		}
		limite = (pp.contains(c)
				  || (i<tl-1 && c=='\n' && t.at(i+1)=='\n'));
		if (!limite && c.isPunct())
			ponctG = c;
		++i;
	}
	// recherche des liens 
	QStringList ret;
	// pour chaque mot précédent
	for (int i=0;i<_motsP.count();++i)
	{
		Mot *mp = _motsP.at(i);
		// mp est-іl subordonné à _motCour ?
		// pour chaque Super de mp
		foreach (Super* sup, _motCour->super())
		{
			//pour chaque lemme de mp
			foreach(Lemme *l, mp->morphos().keys())
			{
				// pour chaque morpho du lemme
				QList<SLem> lsl = mp->morphos().value(l);
				foreach (SLem sl, lsl)
					if (sup->regle()->estSub(l, m, true))
					{
						ret << sup->regle()->fonction(_motCour, mp) << "<br/>\n"
							<< sup->regle()->doc() << "<br/>\n";
					}
			}
		}
		// motCour est-il subordonné à mp ?
	}
	ret.removeDuplicates();
	return ret.join (' ');
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

void Syntaxe::setText (QString t)
{
	_texte = t;
}
