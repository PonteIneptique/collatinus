class Lemmat
    def __init(self, resDir=None):
        '''*
         * \fn Lemmat.Lemmat (QObject *parent)
         * \brief Constructeur de la classe Lemmat.
         *
         * Il définit quelques constantes, initialise
         * les options à False, appelle les fonctions
         * de lecture des données : modèles, lexique,
         * traductions et irréguliers.
         '''
        if not resDir:
            self._resDir = qApp.applicationDirPath() + "/data/"
        elif resDir.endsWith("/"):
            self._resDir = resDir
        self._resDir = resDir + "/"
        # options
        self._alpha = False
        self._formeT = False
        self._html = False
        self._majPert = False
        self._morpho = False
        self._extension = False
        self._extLoaded = False
        self._nbrLoaded = False
        # suffixes
        self.suffixes = {
            "ne" : "nĕ",
            "que" : "quĕ",
            "ue" : "vĕ",
            "ve" : "vĕ",
            "st" : "st",
        }
        # assimilations
        self.ajAssims()
        # contractions
        self.ajContractions()
        # lecture des morphos
        QDir rep
        rep = QDir(_resDir, "morphos.*")
        ltr = rep.entryList()
        ltr.removeOne("morphos.la");  # S'il traine encore...
        for nfl in ltr:
            lisMorphos(QFileInfo(nfl).suffix())
        lisModeles()
        lisLexique()
        lisTags(False)
        lisTraductions(True, False)
        lisIrreguliers()
        lisParPos()
        lisCat()
    #ifdef VERIF_TRAD
        foreach (Lemme *l, _lemmes.values())        t = l.traduction("fr")
            if (t == "") qDebug() << l.cle() << "non traduit."

    #endif


    def lisCat(self):
        lignes = lignesFichier(_resDir + "CatLASLA.txt")
        for lin in lignes:
            if lin.contains(",")) _catLasla.insert(lin.section(",",0,0),lin.section(",",1,1):



    '''*
     * \fn Lemmat.lisNombres
     * \brief Lecture du fichier nombres.la
     * et peuplement de la variable _nbOcc de chaque lemme.
     *
     * Cette routine lit le fichier nombres.la.
     * Ce fichier a été tiré de la lemmatisation de la liste
     * des formes tirées des textes du LASLA.
     * C'est un csv, la virgule comme séparateur.
     *
     * Un programme a essayé d'établir la correspondance
     * entre les lemmes de Collatinus (1er champ)
     * avec ceux du LASLA (2e champ) et
     * le nombre d'occurrences associé.
     *
     '''
    def lisNombres(self):
        lignes = lignesFichier(_resDir + "nombres.la")
        for lin in lignes:
            liste = lin.split(',')
            clef = liste[0]
            clef.remove('-')
            if _lemmes.contains(clef):
                _lemmes[clef].ajNombre(liste[2].toInt())

        _nbrLoaded = True
        # Je lis aussi le début du fichier tags.la
        lisTags(False)
        # Lorsque j'aurai besoin des trigammes pour le tagger, rappellerai lisTags(True).
        # Je commencerai avec un if _trigram.isEmpty()) lisTags(True:


    '''*
     * @brief Lemmat.lisTags
     * @param tout : bool
     *
     * Lorsque le booléen tout est False, ne lit que les nombres d'occurrences des tags.
     *
     * Lorsque le booléen tout est True, lit tout le fichier,
     * donc aussi les dénombrements des séquences de trois tags.
     *
     * Cette routine lit le fichier tags.la.
     * Ce fichier a été tiré du traitement
     * des textes lemmatisés du LASLA.
     * C'est un csv, la virgule comme séparateur.
     *
     * La première partie du fichier donne le nombre d'occurrences de chaque tag
     * que j'ai introduit pour traiter les textes du LASLA.
     * Elle établit aussi la correspondance avec les tags de Collatinus.
     *
     * La deuxième partie donne les séquences de trois tags (LASLA) et
     * le nombre d'occurrences mesuré.
     *
     '''
    def lisTags(self, tout):
        # Nouveau format des données. Le 8 novembre 2016.
        _tagOcc.clear()
        _tagTot.clear()
        _trigram.clear()
        lignes = lignesFichier(_resDir + "tags.la")
        max = lignes.count() - 1
        i = 0
        l = ""
        QStringList eclats
        while (i <= max) # and not l.startsWith("not  --- "))
            l = lignes.at(i)
            if (l.startsWith("not  --- ")) break
            eclats = l.split(',')
            _tagOcc[eclats[0]] += eclats[1].toInt()
            _tagTot[eclats[0].mid(0,1)] += eclats[1].toInt()
            ++i

        #  qDebug() << _tagOcc.size() << _tagTot.size()
        if tout:
            l.clear()
            ++i
            while (i <= max and not l.startsWith("not  --- "))
                l = lignes.at(i)
                eclats = l.split(",")
                _trigram.insert(eclats[0],eclats[1].toInt())
                ++i

            #  qDebug() << _trigram.size()



    '''*
     * @brief Lemmat.tag
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
     * Pour les verbes conjugués, donne le mode (1-4)
     * et un 1 si c'est un présent ou un espace sinon.
     * Les supins ont été joints aux impératifs autres que le présent (groupes trop peu nombreux).
     * Les formes verbales déclinées ont un "w" en tête (à la place du "v" pour verbe).
     * Pour les invariables, POS est complété avec deux espaces.
     *
     '''
    def tag(self, *l, morph):
        # Il faut encore traiter le cas des pos multiples
        lp = l.pos()
        lTags = ""
        while (lp.size() > 0)
            p = lp.mid(0,1)
            lp = lp.mid(1)
            if ((p == "n") and (morph == morpho(413))) # Locatif !
                lTags.append("n71,")
            elif ((p == "v") and (morph.contains(" -u"))) # C'est un supin
                lTags.append("v3 ,")
            else:
                p.append("%1%2,")
                if p.startsWith("v"):
                    for (int i=0; i<4; i++) if morph.contains(modes(i).toLower()):
                        if (morph.contains(temps(0))) p = p.arg(i+1).arg(1); # présent
                        p = p.arg(i+1).arg(" ")
                        lTags.append(p)
                        break


                if (p.size() > 4) # Si p == 4, c'est que c'était un verbe conjugué.
                    for (int i=0; i<6; i++) if morph.contains(cas(i)):
                        if morph.contains(nombre(1))) p = p.arg(i+1).arg(2:
                        p = p.arg(i+1).arg(1)
                        if (p.startsWith("v")) p[0] = 'w'; # Forme verbale déclinée.
                        lTags.append(p)
                        break


                if p.size() > 4:
                    p = p.arg(" ").arg(" ")
                    lTags.append(p)

                #if not _tagOcc.contains(p.mid(0,3)):
                #   qDebug() << l.cle() << morph << p << " : Tag non trouvé not "


        return lTags


    '''*
     * @brief Lemmat.fraction
     * @param t : le tag
     * @return : la fraction moyenne du tag.
     *
     * Ce résultat est un entier, en 1/1024e
     *
     * On va chercher le nombre d'occurrences associé à ce tag.
     * On le divise par le nombre d'occurrences associé au même POS.
     *
     * Si la fonction reçoit une liste de tags,
     * elle retourne la plus grande fraction.
     *
     '''
    def fraction(self, listTags):
        frFin = 0
        while (listTags.size() > 2)
            t = listTags.mid(0,3)
            listTags = listTags.mid(4)
            fr = 0
            if _tagOcc.contains(t):
                if ((t[0] == 'a') or (t[0] == 'p') or (t[0] == 'w')) # Adj. ou pron. sans genre !
                    fr = _tagOcc[t] * 341 / _tagTot[t.mid(0,1)]
                elif ((t[0] == 'v') and (t[2] == '1')) # verbe au présent
                    fr = _tagOcc[t] * 512 / _tagTot[t.mid(0,1)]
                elif ((t[0] == 'v') and (t[2] == ' ')) # verbe à un autre temps
                    fr = _tagOcc[t] * 256 / _tagTot[t.mid(0,1)]
                elif (t[0] == 'n') # Nom
                    fr = _tagOcc[t] * 1024 / _tagTot[t.mid(0,1)]
                fr = 1024
                if (fr == 0) fr = 1
                #  qDebug() << _tagOcc[t] << _tagTot[t.mid(0,1)] << fr

            #else qDebug() << t << " : Tag non trouvé not "
            if (frFin < fr) frFin = fr; # Si j'ai reçu une liste de tags, garde la fraction la plus grande.

        if (frFin == 0) return 1024
        return frFin


    '''*
     * @brief Lemmat.tagOcc
     * @param t : tag
     * @return Le nombre d'occurrences du tag t
     '''
    def tagOcc(self, t):
        return _tagOcc[t]


    '''*
     * @brief Lemmat.lignesFichier
     * @param nf : nom du fichier
     * @return : l'ensemble de lignes du fichier qui ne sont
     * ni vides ni commentées.
     *
     * Les fichiers de Collatinus ont adopté le point d'exclamation
     * en début de ligne pour introduire un commentaire.
     * Ces lignes doivent être ignorées par le programme.
     *
     '''
    def lignesFichier(self, nf):
        QFile f(nf)
        f.open(QFile.ReadOnly)
        QTextStream flux(&f)
        flux.setCodec("UTF-8"); # Pour windôze !
        QStringList retour
        while (not flux.atEnd())
            lin = flux.readLine()
            if (not lin.isEmpty()) and ((not lin.startsWith("not ")) or lin.startsWith("not  --- ")):
                retour.append(lin)

        f.close()
        return retour


    '''*
     * @brief Lemmat.lisMorphos
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
     '''
    def lisMorphos(self, lang):
        lignes = lignesFichier(_resDir + "morphos." + lang)
        max = lignes.count() - 1
        i = 0
        QString l; # = ""
        QStringList morphos
        while (i <= max) # and not l.startsWith("not  --- "))
            l = lignes.at(i)
            if (l.startsWith("not  --- ")) break
            if i+1 != l.section(':',0,0).toInt():
                qDebug() <<i<<"Fichier morphos." << lang << ", dans la ligne "<<l
            else morphos.append(l.section(':',1,1))
            ++i

        _morphos.insert(lang,morphos)
        QStringList cas
        l.clear()
        ++i
        while (i <= max and not l.startsWith("not  --- "))
            l = lignes.at(i)
            cas << l
            ++i

        _cas.insert(lang,cas)
        QStringList genres
        l.clear()
        while (i <= max and not l.startsWith("not  --- "))
            l = lignes.at(i)
            genres << l
            ++i

        _genres.insert(lang,genres)
        QStringList nombres
        l = ""
        while (i <= max and not l.startsWith("not  --- "))
            l = lignes.at(i)
            nombres << l
            ++i

        _nombres.insert(lang,nombres)
        QStringList temps
        l.clear()
        while (i <= max and not l.startsWith("not  --- "))
            l = lignes.at(i)
            temps << l
            ++i

        _temps.insert(lang,temps)
        QStringList modes
        l.clear()
        while (i <= max and not l.startsWith("not  --- "))
            l = lignes.at(i)
            modes << l
            ++i

        _modes.insert(lang,modes)
        QStringList voix
        l.clear()
        while (i <= max and not l.startsWith("not  --- "))
            l = lignes.at(i)
            voix << l
            ++i

        _voix.insert(lang,voix)
        QStringList mc
        l.clear()
        while (i <= max and not l.startsWith("not  --- "))
            l = lignes.at(i)
            mc << l
            ++i

        _motsClefs.insert(lang,mc)





    '''*
     * \fn void Lemmat.ajContractions ()
     * \brief 
     '''
    def ajContractions(self):
        # peupler la QMap _contractions
        lignes = lignesFichier(_resDir + "contractions.la")
        for lin in lignes:
            liste = lin.split(':')
            _contractions.insert(liste.at(0), liste.at(1))



    def aRomano(self, f):
        if (f.size () == 0) return 0
        # création de la table de conversion : pourrait être créée ailleurs.
        QMap<QChar, conversion
        conversion['I']=1
        conversion['V']=5
        conversion['X']=10
        conversion['L']=50
        conversion['C']=100
        conversion['D']=500
        conversion['M']=1000
        # calcul du résultat : ajout d'un terme si l'ordre est normal, sinon.
        int res=0
        int conv_c
        conv_s = conversion[f[0]]
        for (i = 0; i < f.count()-1; i++)
            conv_c = conv_s
            conv_s = conversion[f[i+1]]
            if conv_c < conv_s:
                res -= conv_c
            else res += conv_c

        res += conv_s
        return res


    '''*
     * \fn void Lemmat.ajDesinence (Desinence *d)
     * \brief 
     '''
    def ajDesinence(self, *d):
        _desinences.insert(Ch.deramise(d.gr()), d)


    def estRomain(self, f):
        return not (f.contains(QRegExp ("[^IVXLCDM]"))
                 or f.contains("IL")
                 or f.contains("IVI"))


    '''*
     * \fn void Lemmat.ajRadicaux (Lemme *l)
     * \brief Calcule tous les radicaux du lemme l,
     *  en se servant des modèles, ajoute à ce lemme,
     *  et ensuite à la map *  des radicaux de la classe Lemmat.
     *
     '''
    def ajRadicaux(self, *l):
        # ablŭo=ā̆blŭo|lego|ā̆blŭ|ā̆blūt|is, ere, lui, lutum
        #      0        1    2    3         4
        Modele *m = modele(l.grModele())
        ''' insérer d'abord les radicaux définis dans lemmes.la
        qui sont prioritaires '''
        for i in l.clesR():
            QList<Radical *> lr = l.radical(i)
            foreach (Radical *r, lr)
                _radicaux.insert(Ch.deramise(r.gr()), r)

        # pour chaque radical du modèle
        for i in m.clesR():
            if (l.clesR().contains(i)) continue
            gs = l.grq().split(',')
            for g in gs:
                Radical *r = NULL
                    gen = m.genRadical(i)
                    # si gen == 'K', radical est la forme canonique
                    if (gen == "-") continue
                    if gen == "K":
                        r = Radical(g, i, l)
                    else:
                        # sinon, la règle de formation du modèle
                        oter = gen.section(',', 0, 0).toInt()
                        ajouter = gen.section(',', 1, 1)
                        if g.endsWith(0x0306)) g.chop(1:
                        g.chop(oter)
                        if ajouter != "0") g.append(ajouter:
                        r = Radical(g, i, l)


                l.ajRadical(i, r)
                _radicaux.insert(Ch.deramise(r.gr()), r)




    '''*
     * \fn QString Lemmat.assim (QString a)
     * \brief Cherche si la chaîne a peut subir
     *        une assimilation, renvoie
     *        cette chaîne éventuellement assimilée.
     *        *version sans quantités*
     '''
    def assim(self, a):
        for d in assims.keys():
            if a.startsWith(d):
                a.replace(d, assims.value(d))
                return a

        return a


    '''*
     * \fn QString Lemmat.assimq (QString a)
     * \brief Cherche si la chaîne a peut subir
     *        une assimilation, renvoie
     *        cette chaîne éventuellement assimilée.
     *        *version avec quantités*
     '''
    def assimq(self, a):
        for d in assimsq.keys():
            if a.startsWith(d):
                a.replace(d, assimsq.value(d))
                return a

        return a


    '''*
     * \fn QString Lemmat.cible()
     * \brief Renvoie la langue cible dans sa forme
     *        abrégée (fr, en, de, it, etc.).
     '''
    def cible(self):
        return _cible


    '''*
     * \fn QMap<QString, Lemmat.cibles()
     * \brief Renvoie la map des langues cibles.
     *
     '''
    QMap<QString, Lemmat.cibles()
        return _cibles


    '''*
     * \fn QString Lemmat.decontracte (QString d)
     * \brief Essaie de remplacer la contractions de d
     *        par sa forme entière, renvoie le résultat.
     '''
    def decontracte(self, d):
        for cle in _contractions.keys():
            if d.endsWith(cle):
                d.chop(cle.length())
                if (d.contains("v") or d.contains("V")):
                    d.append(_contractions.value(cle))
                else:
                    d.append(Ch.deramise(_contractions.value(cle)))
                return d


        return d


    '''*
     * \fn QString Lemmat.desassim (QString a)
     * \brief Essaie de remplacer l'assimilation de a
     *        par sa forme non assimilée, renvoie
     *        le résultat.
     '''
    def desassim(self, a):
        for d in assims.values():
            if a.startsWith(d):
                a.replace(d, assims.key(d))
                return a


        return a


    '''*
     * \fn QString Lemmat.desassimq (QString a)
     * \brief Essaie de remplacer l'assimilation de a
     *        par sa forme non assimilée, renvoie
     *        le résultat.
     '''
    def desassimq(self, a):
        for d in assimsq.values():
            if a.startsWith(d):
                a.replace(d, assimsq.key(d))
                return a


        return a


    '''*
     * \fn MapLem Lemmat.lemmatise (QString f)
     * \brief Le cœur du lemmatiseur
     *
     *  renvoie une QMap<Lemme*, contenant
     *  - la liste de tous les lemmes pouvant donner
     *    la forme f
     *  - pour chacun de ces lemmes la QStringList des morphologies
     *    correspondant à la forme.
     '''
    def lemmatise(self, f):
        MapLem result
        if (f.isEmpty()) return result
        f_lower = f.toLower()
        cnt_v = f_lower.count("v")
        V_maj = f[0] == 'V'
        cnt_ae = f_lower.count("æ")
        cnt_oe = f_lower.count("œ")
        if (f_lower.endsWith("æ")) cnt_ae -= 1
        f = Ch.deramise(f)
        # formes irrégulières
        QList<Irreg *> lirr = _irregs.values(f)
        foreach (Irreg *irr, lirr)
            for m in irr.morphos():
                sl = {irr.grq(), morpho(m), ""
                # result[irr.lemme()].prepend (morpho (m))
                result[irr.lemme()].prepend(sl)


        # radical + désinence
        for (i = 0; i <= f.length(); ++i)
            r = f.left(i)
            d = f.mid(i)
            QList<Desinence *> ldes = _desinences.values(d)
            if (ldes.empty()) continue
            # Je regarde d'abord si d est une désinence possible,
            # car il y a moins de désinences que de radicaux.
            # Je fais la recherche sur les radicaux seulement si la désinence existe.
            QList<Radical *> lrad = _radicaux.values(r)
            # ii noté ī
            # 1. Patauium, gén. Pataui : Patau.i . Patau+i.i
            # 2. conubium, conubis : conubi.s . conubi.i+s
            if d.startsWith('i') and not d.startsWith("ii") and not r.endsWith('i'):
                lrad << _radicaux.values(r + "i")
            if (lrad.empty()) continue
            # Il n'y a rien à faire si le radical n'existe pas.
            foreach (Radical *rad, lrad)
                Lemme *l = rad.lemme()
                foreach (Desinence *des, ldes)
                    if (des.modele() == l.modele() and
                        des.numRad() == rad.numRad() and
                        not l.estIrregExcl(des.morphoNum()))
                        c = ((cnt_v==0)
                                  or(cnt_v == rad.grq().toLower().count("v")
                                     +des.grq().count("v")))
                        if not c) c = (V_maj and (rad.gr()[0] == 'U':
                                and (cnt_v - 1 == rad.grq().toLower().count("v")))
                        c = c and ((cnt_oe==0)or(cnt_oe == rad.grq().toLower().count("ōe")))
                        c = c and ((cnt_ae==0)or
                                  (cnt_ae == (rad.grq().toLower().count("āe") + rad.grq().toLower().count("prăe"))))
                        if c:
                            fq = rad.grq() + des.grq()
                            if not r.endsWith("i") and rad.gr().endsWith("i"):
                                fq = rad.grq().left(rad.grq().size()-1) + "ī"
                                        + des.grq().right(des.grq().size()-1)
                            sl = {fq, morpho(des.morphoNum()), ""
                            result[l].prepend(sl)





        if _extLoaded and not _extension and not result.isEmpty():
            # L'extension est chargée mais je ne veux voir les solutions qui en viennent que si toutes en viennent.
            MapLem res
            foreach (Lemme *l, result.keys())
                if l.origin() == 0:
                    res[l] = result[l]


            if (not res.isEmpty()) result = res

        # romains
        if estRomain(f) and not _lemmes.contains(f):
            lin = QString("%1|invor|adj. num.|1").arg(f)
            Lemme *romain = Lemme(lin, 0, self)
            nr = aRomano(f)
            romain.ajTrad(QString("%1").arg(nr), "fr")
            _lemmes.insert(f, romain)
            sl = {f,"inv",""
            QList<SLem> lsl
            lsl.append(sl)
            result.insert(romain, lsl)

        return result


    '''*
     * \fn bool Lemmat.inv (Lemme *l, ml)
     * \brief Renvoie True si le lemme l faisant partie
     *        de la MaplLem ml est invariable.
     '''
    def inv(self, *l, ml):
        return ml.value(l).at(0).morpho == "-"


    def k9(self, m):
    #    qDebug() << m
        QStringList res
        cibAct = _cible
        _cible = "k9,fr"
        mm = lemmatiseM(m)
        _cible = cibAct
        if (mm.isEmpty()) return "\n"
        # Il faut répondre quelque chose, j'attends 30 secondes !
        foreach (Lemme *l, mm.keys())
            clef = l.cle() + ", ,"
            for s in mm.value(l):
                code9 = s.morpho
                forme = Ch.atone(s.grq)
                if (not s.sufq.isEmpty()) forme += "<" + Ch.atone(s.sufq) +">,"
                else forme += ","
                if _catLasla.contains(l.modele().gr())) code9.replace("k9",_catLasla[l.modele().gr()]:
    #            qDebug() << clef << s.morpho << code9 << _catLasla[l.modele().gr()]
                res << forme + clef + code9



        return res.join("\n")


    '''*
     * \fn MapLem Lemmat.lemmatiseM (QString f, debPhr)
     * \brief Renvoie dans une MapLem les lemmatisations de la
     *        forme f. le paramètre debPhr à True indique qu'il
     *        s'agit d'un début de phrase, la fonction
     *        peut tenir compte des majuscules pour savoir
     *        s'il s'agit d'un nom propre.
     '''
    def lemmatiseM(self, f, debPhr, desas):
        QString res
        QTextStream fl(&res)
        mm = lemmatise(f)
        if (f.isEmpty()) return mm
        # suffixes
        for suf in suffixes.keys():
            if mm.empty() and f.endsWith(suf):
                sf = f
                sf.chop(suf.length())
                # TODO : aequeque est la seule occurrence
                # de -queque dans le corpus classique
                mm = lemmatiseM(sf, debPhr, desas)
                # Ne pas assimiler une 2e fois.
                sst = False
                if mm.isEmpty() and (suf == "st"):
                    sf += "s"
                    mm = lemmatiseM(sf, debPhr, desas)
                    sst = True

                foreach (Lemme *l, mm.keys())
                    QList<SLem> ls = mm.value(l)
                    for (i = 0; i < ls.count(); ++i)
                        if (sst) mm[l][i].sufq = "t"
                        else mm[l][i].sufq += suffixes.value(suf); # Pour modoquest



        if debPhr and f.at(0).isUpper():
            nf = f.toLower()
            nmm = lemmatiseM(nf)
            foreach (Lemme *nl, nmm.keys())
                mm.insert(nl, nmm.value(nl))

        # assimilations
        if not desas:
        fa = assim(f)
        if fa != f:
            nmm = lemmatiseM(fa, debPhr, True)
            # désassimiler les résultats
            foreach (Lemme *nl, nmm.keys())
                for (i = 0; i < nmm[nl].count(); ++i)
                    nmm[nl][i].grq = desassimq(nmm[nl][i].grq)
                mm.insert(nl, nmm.value(nl))


        else:
            fa = desassim(f)
            if fa != f:
                nmm = lemmatiseM(fa, debPhr, True)
                foreach (Lemme *nl, nmm.keys())
                    for (i = 0; i < nmm[nl].count(); ++i)
                        nmm[nl][i].grq = assimq(nmm[nl][i].grq)
                    mm.insert(nl, nmm.value(nl))




        # contractions
        fd = f
        for cle in _contractions.keys():
            if fd.endsWith(cle):
                fd.chop(cle.length())
                if (fd.contains("v") or fd.contains("V")):
                    fd.append(_contractions.value(cle))
                else:
                    fd.append(Ch.deramise(_contractions.value(cle)))
                nmm = lemmatise(fd)
                foreach (Lemme *nl, nmm.keys())
                    diff = _contractions.value(cle).size() - cle.size()
                    # nombre de lettres que je dois supprimer
                    for (i = 0; i < nmm[nl].count(); ++i)
                        position = f.size() - cle.size() + 1
                        # position de la 1ère lettre à supprimer
                        if fd.size() != nmm[nl][i].grq.size():
                            # il y a une (ou des) voyelle(s) commune(s)
                            debut = nmm[nl][i].grq.left(position + 2)
                            position += debut.count("\u0306"); # Faut-il vérifier que je suis sur le "v".

                        nmm[nl][i].grq = nmm[nl][i].grq.remove(position, diff)

                    mm.insert(nl, nmm.value(nl))


        # majuscule initiale
        if mm.empty():
            f[0] = f.at(0).toUpper()
            nmm = lemmatise(f)
            foreach (Lemme *nl, nmm.keys())
                mm.insert(nl, nmm.value(nl))

        return mm




    '''*
     * \fn QString Lemmat.lemmatiseT (QString &t,
     *  						   bool alpha,
     *  						   bool cumVocibus,
     *  						   bool cumMorpho,
     *  						   bool nreconnu)
     * \brief Renvoie sous forme de chaîne la lemmatisation
     *        et la morphologie de chaque mot du texte t.
     *        Les paramètres permettent de classer la sortie
     *        par ordre alphabétique ; de reproduire la
     *        forme du texte au début de chaque lemmatisation 
     *        de donner les morphologies de chaque forme ; ou
     *        de rejeter les échecs en fin de liste. D'autres
     *        paramètres, le format de sortie txt ou html,
     *        sont donnés par des variables de classe.
     *	      Les paramètres et options True outrepassent les False,
     *        _majPert et _html sont dans les options de la classe.
     *
     *        Par effet de bord, fonction modifie le texte
     *        t, par adresse dans le paramètre &t, en
     *        tenant compte de la liste des mots connus définie
     *        par l'utilisateur via l'option
     *        Fichier/Lire une liste de mots connus.
     *
     '''
    def lemmatiseT(self, &t):
        return lemmatiseT(t, _alpha, _formeT, _morpho, _nonRec)


    QString Lemmat.lemmatiseT(QString &t, alpha, cumVocibus,
                               bool cumMorpho, nreconnu)
        # pour mesurer :
        # QElapsedTimer timer
        # timer.start()
    '''    
        alpha = alpha or _alpha
        cumVocibus = cumVocibus or _formeT
        cumMorpho = cumMorpho or _morpho
        nreconnu = nreconnu or _nonRec
    '''
        # Pour coloriser le texte
        cumColoribus = not _couleurs.isEmpty()
        listeVide = _hLem.isEmpty()
        colPrec = 0
        formesConnues = 0
        # éliminer les chiffres et les espaces surnuméraires
        t.remove(QRegExp("\\d"))
    #    t = t.simplified()
        # découpage en mots
        lm = t.split(QRegExp("\\b"))
        # conteneur pour les résultats
        QStringList lsv
        # conteneur pour les échecs
        QStringList nonReconnus
        # lemmatisation pour chaque mot
        if lm.size() < 2:
    #        qDebug() << t << lm.size() << lm
            return ""
            # Ça peut arriver que le texte ne contienne qu"une ponctuation

        for (i = 1; i < lm.length(); i += 2)
            f = lm.at(i)
            if (f.toInt() != 0) continue
            # nettoyage et identification des débuts de phrase
            sep = lm.at(i - 1)
            debPhr = ((i == 1 and lm.count() !=3) or sep.contains(Ch.rePonct))
            # lemmatisation de la forme
            map = lemmatiseM(f, _majPert or debPhr)
            # échecs
            if map.empty():
                if nreconnu:
                    nonReconnus.append(f + "\n")
                else:
                    if _html:
                        lsv.append("<li style=\"color:blue;\">" + f + "</li>")
                    else:
                        lsv.append(f + " ÉCHEC")

                if cumColoribus:
                    if not listeVide:
                        # La liste de mots connus n'est pas vide. Le mot en fait-il partie ?
                        lem = f
                        lem.replace("j","i")
                        lem.replace("v","u")
                        lem.replace("J","I")
                        lem.replace("V","U")
                        # qDebug() << lem
                        if _hLem.contains(lem):
                            _hLem[lem]++
                            if colPrec != 0:
                                lm[i].prepend("</span><span style=\"color:"+_couleurs[0]+"\">")
                                colPrec = 0


                        elif colPrec != 2:
                            lm[i].prepend("</span><span style=\"color:"+_couleurs[2]+"\">")
                            colPrec = 2




            else:
                connu = False
                if cumColoribus:
                    if not listeVide:
                        # La liste de mots connus n'est pas vide. Un des lemmes identifiés en fait-il partie ?
                        foreach (Lemme *l, map.keys())
                            if _hLem.contains(l.cle()):
                                connu = True
                                _hLem[l.cle()]++

    #                        connu = connu or _hLem.contains(l.cle())

                    if connu:
                        formesConnues += 1
                        if colPrec != 0:
                            lm[i].prepend("</span><span style=\"color:"+_couleurs[0]+"\">")
                            colPrec = 0


                    elif colPrec != 1:
                        lm[i].prepend("</span><span style=\"color:"+_couleurs[1]+"\">")
                        colPrec = 1


                if cumVocibus:
                    # avec affichage des formes du texte
                    QString lin
                    QMultiMap<int, listeLem
                    if _html:
                        lin = "<h4>" + f + "</h4><ul>"
                        foreach (Lemme *l, map.keys())
                            lem = "<li>" + l.humain(True, _cible, True)
                            frMax = 0
                            if cumMorpho and not inv(l, map):
                                QMultiMap<int, listeMorph
                                for m in map.value(l):
                                    fr = fraction(tag(l,m.morpho))
                                    if (fr > frMax) frMax = fr
                                    if m.sufq.isEmpty():
                                        listeMorph.insert(-fr,m.grq + " " + m.morpho)
                                    else:
                                        listeMorph.insert(-fr,m.grq + " + " + m.sufq +
                                                          " " + m.morpho)

                                lem.append("<ul><li>")
                                lMorph = listeMorph.values()
                                lem.append(lMorph.join("</li><li>"))
                                lem.append("</li></ul>\n")

                            else for m in map.value(l):
                                fr = fraction(tag(l,m.morpho))
                                if (fr > frMax) frMax = fr

                            if (frMax == 0) frMax = 1024
                            lem.append("</li>")
                            listeLem.insert(-frMax * l.nbOcc(),lem)

                        lLem = listeLem.values()
                        # Les valeurs sont en ordre croissant
                        lin.append(lLem.join("\n"))
                        lin.append("</ul>\n")

                    else:
                        lin = " " + f + "\n"
                        foreach (Lemme *l, map.keys())
                            lin.append("  - " + l.humain(False, _cible, True) + "\n")
                            if cumMorpho and not inv(l, map):
                                for m in map.value(l):
                                    if m.sufq.isEmpty():
                                        lin.append("    . " + m.grq + " " + m.morpho +
                                                   "\n")
                                    else:
                                        lin.append("    . " + m.grq + " + " + m.sufq +
                                                   " " + m.morpho + "\n")



    #                lsv.append(lin)
                    if not connu or listeVide) lsv.append(lin:
                    # Par défaut, d'aide pour les mots connus.

                else  # sans les formes du texte
                    foreach (Lemme *l, map.keys())
                        lin = l.humain(_html, _cible)
                        if cumMorpho and not inv(l, map):
                            QTextStream fl(&lin)
                            if _html:
                                fl << "<ul>"
                                for m in map.value(l):
                                    fl << "<li>" << m.grq << " " << m.morpho << "</li>"
                                fl << "</ul>\n"

                            else:
                                for m in map.value(l):
                                    fl << "\n    . " << m.grq << " " << m.morpho

    #                    lsv.append(lin)
                        if not connu or listeVide) lsv.append(lin:
                        # Par défaut, d'aide pour les mots connus.



        }  # fin de boucle de lemmatisation pour chaque mot

        if alpha:
            lsv.removeDuplicates()
            qSort(lsv.begin(), lsv.end(), Ch.sort_i)

        # peupler lRet avec les résultats
        QStringList lRet
        if _html) lRet.append("<ul>":
        for item in lsv:
            if _html:
                lRet.append("<li>" + item + "</li>")
            else:
                lRet.append("* " + item + "\n")

        if _html) lRet.append("</ul>\n":
        # non-reconnus en fin de liste si l'option nreconnu
        # est armée
        if nreconnu and not nonReconnus.empty():
            nonReconnus.removeDuplicates()
            QString nl
            if (_html) nl = "<br/>"
            if alpha) qSort(nonReconnus.begin(), nonReconnus.end(), Ch.sort_i:
            QString titreNR
            tot = (lm.count() - 1) / 2
            QTextStream(&titreNR) << "--- " << nonReconnus.count() << "/"
                                  << tot << " ("
                                  << ((nonReconnus.count() * 100) / tot)
                                  << " %) FORMES NON RECONNUES ---" << nl << "\n"
            lRet.append(titreNR + nl)
            for nr in nonReconnus:
                lRet.append(nr + nl)

        if cumColoribus:
            lm[0].append("<span style=\"color:"+_couleurs[0]+"\">")
            lm[lm.size()-1].append("</span>")
            t = lm.join("")
            t.replace("\n","<br/>\n")
            if not listeVide:
                stats = "<strong>Formes connues : %1 sur %2 (%3%)<br/></strong>"
                lRet.prepend(stats.arg(formesConnues).arg((lm.size()/2)).arg((200*formesConnues)/(lm.size()-1)))


        # fin de la mesure :
        # qDebug()<<"Eneide"<<timer.nsecsElapsed()<<"ns"
        return lRet.join("")


    '''*
     * \fn QString Lemmat.lemmatiseFichier (QString f,
     *								  bool alpha,
     *								  bool cumVocibus,
     *								  bool cumMorpho,
     *								  bool nreconnu)
     * \brief Applique lemmatiseT sur le contenu du fichier
     *        f et renvoie le résultat. Les paramètres sont
     *        les mêmes que ceux de lemmatiseT.
     '''
    QString Lemmat.lemmatiseFichier(QString f, alpha, cumVocibus,
                                     bool cumMorpho, nreconnu)
        # lecture du fichier
        QFile fichier(f)
        fichier.open(QFile.ReadOnly)
        QTextStream flf(&fichier)
        flf.setCodec("UTF-8"); # Pour windôze !
        texte = flf.readAll()
        fichier.close()
        return lemmatiseT(texte, alpha, cumVocibus, cumMorpho, nreconnu)


    '''*
     * \fn Lemme* Lemmat.lemme (QString l)
     * \brief cherche dans la liste des lemmes le lemme
     *        dont la clé est l, retourne le résultat.
     '''
    Lemme *Lemmat.lemme(QString l) { return _lemmes.value(l);
    '''*
     * \fn QStringList Lemmat.lemmes (MapLem lm)
     * \brief renvoie la liste des graphies des lemmes
     *        de la MapLem lm sans signes diacritiques.
     '''
    def lemmes(self, lm):
        QStringList res
        foreach (Lemme *l, lm.keys())
            res.append(l.gr())
        return res


    '''*
     * \fn void Lemmat.lisIrreguliers()
     * \brief Chargement des formes irrégulières
     *        du fichier data/irregs.la
     '''
    def lisIrreguliers(self):
        lignes = lignesFichier(_resDir + "irregs.la")
        for lin in lignes:
            Irreg *irr = Irreg(lin, self)
            if irr != 0 and irr.lemme() != 0:
                _irregs.insert(Ch.deramise(irr.gr()), irr)
    #ifdef DEBOG
            else:
                std.cerr << "Irréguliers, dans la ligne" << qPrintable(lin)
    #endif

        # ajouter les irréguliers aux lemmes
        foreach (Irreg *ir, _irregs)
            ir.lemme().ajIrreg(ir)


    '''*
     * \fn void Lemmat.lisFichierLexique(filepath)
     * \brief Lecture des lemmes, et enregistrement
     *        de leurs radicaux
     '''
    def lisFichierLexique(self, filepath):
        orig = 0
        if (filepath.endsWith("ext.la")) orig = 1
        lignes = lignesFichier(filepath)
        for lin in lignes:
            Lemme *l = Lemme(lin, orig, self)
            #if _lemmes.contains(l.cle()):
            #    qDebug() << lin << " existe déjà"
            _lemmes.insert(l.cle(), l)



    '''*
     * \fn void Lemmat.lisLexique()
     * \brief Lecture du fichier de lemmes de base
     '''
    def lisLexique(self):
        lisFichierLexique(_resDir + "lemmes.la")


    '''*
     * \fn void Lemmat.lisExtension()
     * \brief Lecture du fichier d'extension
     '''
    def lisExtension(self):
    #    if _nbrLoaded) foreach(Lemme *l, _lemmes.values():
      #      l.clearOcc()
        # Si les nombres d'occurrences ont été chargés, dois les ré-initialiser.
        #qDebug() << "lecture extension"
        lisFichierLexique(_resDir + "lem_ext.la")
    #    lisNombres()


    '''*
     * \fn void Lemmat.lisModeles()
     * \brief Lecture des modèles, et enregistrement
     *        de leurs désinences
     '''
    def lisModeles(self):
        lignes = lignesFichier(_resDir + "modeles.la")
        max = lignes.count()-1
        QStringList sl
        for (int i=0;i<=max;++i)
            l = lignes.at(i)
            if l.startsWith('$'):
                _variables[l.section('=', 0, 0)] = l.section('=', 1, 1)
                continue

            eclats = l.split(":")
            if (eclats.at(0) == "modele" or i == max) and not sl.empty():
                Modele *m = Modele(sl, self)
                _modeles.insert(m.gr(), m)
                sl.clear()

            sl.append(l)



    '''*
     * \fn void Lemmat.lisParPos()
     * \brief Lecture des règles de quantité par position
     * enregistrées dans le fichier data/parpos.txt.
     '''
    def lisParPos(self):
        lignes = lignesFichier(_resDir + "parpos.txt")
        QStringList rr
        for ligne in lignes:
            rr = ligne.split(";")
            _reglesp.append(Reglep(QRegExp(rr.at(0)), rr.at(1)))



    '''*
     * \fn void Lemmat.lisTraductions()
     * \brief Lecture des fichiers de traductions
     *        trouvés dans data/, lemmes, avec
     *        un suffixe corresponant à la langue cible
     *        qu'ils fournissent.
     '''
    def lisTraductions(self, base, extension):
    #    nrep = _resDir
        QDir rep
        if (not base and not extension) return
        if base and extension:        rep = QDir(_resDir, "lem*.*")
        } elif base:        rep = QDir(_resDir, "lemmes.*")
        } else:
            rep = QDir(_resDir, "lem_ext.*")

        ltr = rep.entryList()
    #ifdef VERIF_TRAD
        qDebug() << ltr
    #endif
        if base:        ltr.removeOne("lemmes.la");  # n'est pas un fichier de traductions

        if extension:        ltr.removeOne("lem_ext.la");  # n'est pas un fichier de traductions

        for nfl in ltr:
            # suffixe
            suff = QFileInfo(nfl).suffix()
            lignes = lignesFichier(_resDir + nfl)
            if base:
                # lire le nom de la langue
                lang = lignes.takeFirst()
                #lang = lang.mid(1).simplified()
                _cibles[suff] = lang


            for lin in lignes:
                Lemme *l = lemme(Ch.deramise(lin.section(':', 0, 0)))
                if l != 0) l.ajTrad(lin.section(':', 1), suff:
    #ifdef DEBOG
                else:
                    qDebug() << nfl << "traduction, dans la ligne" << lin
                             << " clé" << Ch.deramise(lin.section(':', 0, 0))
    #endif




    '''*
     * \fn Modele * Lemmat.modele (QString m)
     * \brief Renvoie l'objet de la classe Modele dont le nom est m.
     '''
    Modele *Lemmat.modele(QString m) { return _modeles[m];
    '''*
     * \fn QString Lemmat.morpho (int m)
     * \brief Renvoie la chaîne de rang m dans la liste des morphologies
     *        donnée par le fichier data/morphos.la
     '''
    def morpho(self, m):
        l = "fr"; # La langue sélectionnée
        if _morphos.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2:
        elif (_cible.size() > 4) and (_morphos.keys().contains(_cible.mid(3,2))):
            l = _cible.mid(3,2)
        if m < 0 or m > _morphos[l].count():
            return "morpho, "+QString.number(m)+" : erreur d'indice"
        if (m == _morphos[l].count()) return "-"
        return _morphos[l].at(m - 1)


    def cas(self, m):
        l = "fr"; # La langue sélectionnée
        if _cas.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2:
        elif (_cible.size() > 4) and (_cas.keys().contains(_cible.mid(3,2))):
            l = _cible.mid(3,2)
        return _cas[l].at(m)


    def genre(self, m):
        l = "fr"; # La langue sélectionnée
        if _genres.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2:
        elif (_cible.size() > 4) and (_genres.keys().contains(_cible.mid(3,2))):
            l = _cible.mid(3,2)
        return _genres[l].at(m)


    def nombre(self, m):
        l = "fr"; # La langue sélectionnée
        if _nombres.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2:
        elif (_cible.size() > 4) and (_nombres.keys().contains(_cible.mid(3,2))):
            l = _cible.mid(3,2)
        return _nombres[l].at(m)


    def temps(self, m):
        l = "fr"; # La langue sélectionnée
        if _temps.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2:
        elif (_cible.size() > 4) and (_temps.keys().contains(_cible.mid(3,2))):
            l = _cible.mid(3,2)
        return _temps[l].at(m)


    def modes(self, m):
        l = "fr"; # La langue sélectionnée
        if _modes.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2:
        elif (_cible.size() > 4) and (_modes.keys().contains(_cible.mid(3,2))):
            l = _cible.mid(3,2)
        return _modes[l].at(m)


    def voix(self, m):
        l = "fr"; # La langue sélectionnée
        if _voix.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2:
        elif (_cible.size() > 4) and (_voix.keys().contains(_cible.mid(3,2))):
            l = _cible.mid(3,2)
        return _voix[l].at(m)


    def motsClefs(self, m):
        l = "fr"; # La langue sélectionnée
        if _motsClefs.keys().contains(_cible.mid(0,2))) l = _cible.mid(0,2:
        elif (_cible.size() > 4) and (_motsClefs.keys().contains(_cible.mid(3,2))):
            l = _cible.mid(3,2)
        return _motsClefs[l].at(m)


    '''*
     * \fn bool Lemmat.optAlpha()
     * \brief Accesseur de l'option alpha, qui
     *        permet de fournir par défaut des résultats dans
     *        l'ordre alphabétique.
     '''
    bool Lemmat.optAlpha() { return _alpha;
    '''*
     * \fn bool Lemmat.optHtml()
     * \brief Accesseur de l'option html, qui
     *        permet de renvoyer les résultats au format html.
     '''
    bool Lemmat.optHtml() { return _html;

    '''*
     * \fn bool Lemmat.optFormeT()
     * \brief Accesseur de l'option formeT,
     *        qui donne en tête de lemmatisation
     *        la forme qui a été analysée.
     '''
    bool Lemmat.optFormeT() { return _formeT;

    '''*
     * \fn bool Lemmat.optMajPert()
     * \brief Accesseur de l'option majPert,
     *        qui permet de tenir compte des majuscules
     *        dans la lemmatisation.
     '''
    bool Lemmat.optMajPert() { return _majPert;

    '''*
     * \fn bool Lemmat.optExtension()
     * \brief Accesseur de l'option extension,
     *        qui permet de charger l'extension.
     '''
    bool Lemmat.optExtension() { return _extension;
    '''*
     * \fn bool Lemmat.optMorpho()
     * \brief Accesseur de l'option morpho,
     *        qui donne l'analyse morphologique
     *        des formes lemmatisées.
     '''

    def optMorpho(self):
        return _morpho


    def parPos(self, f):
        maj = f.at(0).isUpper()
        f = f.toLower()
        for r in _reglesp:
            f.replace(r.first, r.second)
        if maj) f[0] = f[0].toUpper(:
        return f


    '''*
     * \fn void Lemmat.setAlpha (bool a)
     * \brief Modificateur de l'option alpha.
     '''
    # modificateurs d'options

    void Lemmat.setAlpha(bool a) { _alpha = a;
    '''*
     * \fn void Lemmat.setCible(QString c)
     * \brief Permet de changer la langue cible.
     '''
    void Lemmat.setCible(QString c) { _cible = c;
    '''*
     * \fn void Lemmat.setHtml (bool h)
     * \brief Modificateur de l'option html.
     '''
    void Lemmat.setHtml(bool h) { _html = h;
    '''*
     * \fn void Lemmat.setFormeT (bool f)
     * \brief Modificateur de l'option formeT.
     '''
    void Lemmat.setFormeT(bool f) { _formeT = f;
    '''*
     * \fn void Lemmat.setMajPert (bool mp)
     * \brief Modificateur de l'option majpert.
     '''
    void Lemmat.setMajPert(bool mp) { _majPert = mp;
    '''*
     * \fn void Lemmat.setMorpho (bool m)
     * \brief Modificateur de l'option morpho.
     '''
    void Lemmat.setMorpho(bool m) { _morpho = m;
    void Lemmat.setNonRec(bool n) { _nonRec = n;
    '''*
     * \fn QString Lemmat.variable (QString v)
     * \brief 
     *        
     *        
     *        
     *        
     *        
     '''

    '''*
     * @brief Lemmat.setExtension
     * @param e : bool
     *
     * Cette routine gère l'extension du lexique.
     * Si le paramètre e est True, l'extension du lexique est active.
     * S'il n'a pas encore été chargé, l'est.
     *
     * Lors de la lecture des préférences (à l'initialisation),
     * cette routine est appelée.
     * Si on ne charge pas l'extension du lexique,
     * je charge quand même les nombres d'occurrences.
     * Ces nombres seront ré-initialisés si on charge l'extension par la suite.
     *
     '''
    def setExtension(self, e):
        _extension = e
        if not _extLoaded and e:        lisExtension()
            lisTraductions(False,True)
            _extLoaded = True

    #    elif not _nbrLoaded) lisNombres(:


    '''*
     * @brief Lemmat.lireHyphen
     * @param fichierHyphen : nom du fichier (avec le chemin absolu)
     * \brief stocke pour tous les lemmes contenus dans le fichier
     * l'information sur la césure étymologique (non-phonétique).
     '''
    def lireHyphen(self, fichierHyphen):
        foreach (Lemme *l, _lemmes.values()) l.setHyphen("")
        if not fichierHyphen.isEmpty():
            lignes = lignesFichier(fichierHyphen)
            for linea in lignes:
                ecl = linea.split('|')
    #ifdef DEBOG
                if ecl.count() != 2:
                    qDebug () << "ligne mal formée" << linea
                    continue

    #endif
                ecl[1].replace('-',Ch.separSyll)
                Lemme *l = lemme(Ch.deramise(ecl[0]))
                if l!=NULL:
                    l.setHyphen(ecl[1])
    #ifdef DEBOG
                else qDebug () << linea << "erreur lireHyphen"
    #endif




    def tagTexte(self, t, p, affTout):
        # éliminer les chiffres et les espaces surnuméraires
        t.remove(QRegExp("\\d"))
    #    t = t.simplified(); # Rmq : perd les retours de ligne !
        tl = t.length() - 1
         pp = ".;not ?"
        dph = p
        tout = False
        if p < 0:
            p = 0
            dph = 0
            tout = True; # Pour faire tout le texte, par phrase.

        else:
            if ((dph > 0) and pp.contains(t.at(dph))) --dph
            # Si j'ai cliqué sur une ponctuation, traite la phrase qui précède.
            # régression au début de la phrase
            while (dph > 0 and not pp.contains(t.at(dph)) and (t.mid(dph,2) != "\n\n")) --dph
            if (dph != 0) dph += 1; # J'élimine la ponctuation de la phrase précédente.


        # conteneur pour les résultats
        QStringList lsv
        # progression jusqu'en fin de phrase
        fph = p
        while (fph < tl)
            while (fph < tl and not pp.contains(t.at(fph)) and (t.mid(fph,2) != "\n\n")) ++fph
            phr = t.mid(dph, fph - dph).trimmed()
            # Si le texte se termine sans ponctuation, perds le dernier caractère.
    #        qDebug() << tl << fph << t.at(tl)
            if (fph == tl) and not pp.contains(t.at(tl)) and (t.mid(tl,1) != "\n"):
                phr.append(t[tl])
            # découpage en mots
            lm = phr.split(QRegExp("\\b"))

            if lm.size() > 1:
                # Il y a au moins un mot...
                while (Ch.abrev.contains(lm[lm.size()-2]))
                    # Ma phrase se terminait par une abréviation : je continue.
                    fph++
                    while (fph < tl and not pp.contains(t.at(fph))) ++fph
                    phr = t.mid(dph, fph - dph).trimmed()
                    if (fph == tl) and not pp.contains(t.at(tl)) and (t.mid(tl,1) != "\n"):
                        phr.append(t[tl])
                    lm = phr.split(QRegExp("\\b"))


                QList<Mot*> mots
                # lemmatisation pour chaque mot
                for (i = 1; i < lm.length(); i += 2)
                    debVers = not _majPert or lm[i-1].contains("\n")
                    Mot mot = Mot(lm[i],(i-1)/2, debVers,self); # TODO : Vérifier si on a des vers avec majuscule...
                    mots.append(mot)
                }  # fin de boucle de lemmatisation pour chaque mot
                Mot mot = Mot("",mots.size(),True,self); # Fin de phrase
                mots.append(mot); # J'ajoute un mot virtuel en fin de phrase avec le tag "snt".

                if _trigram.isEmpty()) lisTags(True:
                # Si je n'ai pas encore chargé les trigrammes, dois le faire maintenant.

                QStringList sequences
                QList<double> probabilites
                sequences.append("snt")
                probabilites.append(1.0)
                branches = 1.0; # Pour savoir combien de branches a l'arbre.
                # Je suis en début de phrase : je n'ai que le tag "snt" et une proba de 1.
                for (i = 0; i < mots.size(); i++)
                    Mot *mot = mots[i]
                    lTags = mot.tags(); # La liste des tags possibles pour le mot
                    QStringList nvlSeq; # Nouvelle liste des séquences possibles
                    QList<double> nvlProba; # Nouvelle liste des probas.
                    # Je dois ajouter tous les tags possibles à toutes les sequences et calculer les nouvelles probas.
                    sSeq = sequences.size()
                    sTag = lTags.size()
                    if (sTag == 0) continue; # J'ignore pour l'instant les mots inconnus, cf. plus bas.
                    branches *= sTag
                    for (j = 0; j < sSeq; j++)
                        bigr = sequences[j].right(7); # Le bigramme terminal
                        prTot = 0
                        QList<long> pr
                        for (k = 0; k < sTag; k++)
                            seq = bigr + " " + lTags[k]
                            p = mot.proba(lTags[k]) * (4 * _trigram[seq] + 1)
                            pr << p
                            prTot += p

                        # J'ai tout ce qui dépend de k et la somme pour normaliser.
                        if prTot == 0:
                            prTot = 1
                            #qDebug() << mot.forme() << "proba nulle not  " << sequences[j]

                        for (k = 0; k < sTag; k++)
                            nvlSeq.append(sequences[j] + " " + lTags[k])
                            nvlProba.append(probabilites[j] * pr[k] / prTot)
                            # Si j'avais gardé toutes les séquences, serait une vraie probabilité (normalisée à 1)


                    # Ajouter les enclitiques.
                    if not mot.tagEncl().isEmpty():
                        ajout = " " + mot.tagEncl()
                        for (j = 0; j < nvlSeq.size(); j++) nvlSeq[j].append(ajout)
                        # Comme toutes les formes à tag unique, l'enclitique ne change pas les probabilités.

                    # J'ai toutes les sequences et leur proba.
                    # Pour chaque bigramme terminal, ne dois garder que la séquence la plus probable.
                    # En faisant ce tri, fais une sélection sur le tag i-2 (attention aux mots avec enclitique).
                    # Si je veux garder une info sur l'ordre des tags du mot i-2, c'est maintenant !
                    if i > 1:
                        # Le mot i-2 existe !
                        debut = nvlSeq[0].size() - 11
                        if (not mot.tagEncl().isEmpty()) debut -= 4; # Je dois reculer d'un tag de plus.
                        if (not mots[i-1].tagEncl().isEmpty()) debut -= 4; # Je dois reculer d'un tag de plus.
                        if (not mots[i-2].tagEncl().isEmpty()) debut -= 4; # Je dois reculer d'un tag de plus.
                        # Le tag du mot i-2 est nvlSeq[j].mid(debut, 3)
                        for (j = 0; j < nvlSeq.size(); j++) mots[i-2].setBestOf(nvlSeq[j].mid(debut, 3), nvlProba[j])

                    sequences.clear()
                    probabilites.clear()
    #                qDebug() << mot.forme() << nvlProba << nvlSeq
                    for (j = 0; j < nvlSeq.size(); j++) if nvlProba[j] > 0:
                        bigr = nvlSeq[j].right(7); # Les deux derniers tags
                        seq = ""
                        val = -1
                        seq2 = ""
                        val2 = -1
                        for (k = j; k < nvlSeq.size(); k += sTag) # Pour retrouver le bigramme terminal, faut au moins le même dernier tag.
                            if bigr == nvlSeq[k].right(7):
                                if val2 < nvlProba[k]:
                                    # J'y passe au moins une fois au début.
                                    # La séquence mérite la 1ère ou la 2e place.
                                    if val < nvlProba[k]:
                                        # 1ère place !
                                        val2 = val
                                        seq2 = seq
                                        val = nvlProba[k]
                                        seq = nvlSeq[k]

                                    else:
                                        # Seulement la 2e place
                                        val2 = nvlProba[k]
                                        seq2 = nvlSeq[k]


                                nvlProba[k] = -1; # Pour ne pas considérer deux fois les mêmes séquences.

                        # val et seq correspondent aux proba et séquence avec le bigramme considéré qui ont la plus grande proba.
                        sequences << seq
                        probabilites << val
                        if val2 > 0:
                            # J'ai une deuxième séquence assez probable.
                            sequences << seq2
                            probabilites << val2


            #        qDebug() << mot.forme() << sSeq << sTag << nvlSeq.size() << sequences.size()
                    if (sequences.size() == 0) break
                } # fin de la phrase.

                # Les probas associées aux tags du dernier vrai mot.
                if mots.length() > 1:
                    # Le mot mots.length()-2 existe !
                    debut = sequences[0].size() - 7
                    if (not mots[mots.length()-2].tagEncl().isEmpty()) debut -= 4; # Je dois reculer d'un tag de plus.
                    # Le tag du mot mots.length()-2 est sequences[j].mid(debut, 3)
                    for (j = 0; j < sequences.size(); j++)
                        mots[mots.length()-2].setBestOf(sequences[j].mid(debut, 3), probabilites[j])

                # Le tri final !
                seq = ""
                val = -1
                seq2 = ""
                val2 = -1
                for (i = 0; i < sequences.size(); i++)
                    if val2 < probabilites[i]:
                        if val < probabilites[i]:
                            val2 = val
                            seq2 = seq
                            val = probabilites[i]
                            seq = sequences[i]

                        else:
                            val2 = probabilites[i]
                            seq2 = sequences[i]



                lsv.append(phr)
                lsv.append("<ul>")
                prob = "<br/> avec la proba : %1 pour %2 branches.<br/>"
                lsv.append(seq + prob.arg(val).arg(branches))
                if val2 > 0:
                    prob = "Deuxième choix avec la proba : %1 <br/> %2<br/>"
                    lsv.append(prob.arg(val2).arg(seq2))


                seq = seq.mid(4); # Je supprime le premier tag qui est "snt".
                for (i = 0; i < mots.size()-1; i++)
                    if not mots[i].inconnu()) # Les mots inconnus ne figurent pas dans la séquence (cf. plus haut:
                        lsv.append(mots[i].choisir(seq.left(3), affTout))
                         # Si enclitique mid(8)
                        if mots[i].tagEncl().isEmpty()) seq = seq.mid(4:
                        seq = seq.mid(5 + mots[i].tagEncl().size())

                    else lsv.append("<li>" + mots[i].forme() + " : non trouvé</li>")

                lsv.append("</ul>")
                if (tout) lsv << "<br/>"
                else return lsv.join("\n")

            dph = fph + 1
            fph++

        return lsv.join("\n")


    def verbaCognita(self, fichier, vb):
        _hLem.clear()
        _couleurs.clear()
        if vb and not fichier.isEmpty():
            # Couleurs par défaut
            _couleurs << "#00A000"; # vert
            _couleurs << "#000000"; # noir
            _couleurs << "#A00000"; # rouge
            QFile file(fichier)
            if file.open(QFile.ReadOnly | QFile.Text):
                QTextStream in(&file)
                ligne = in.readLine()
                while (ligne.startsWith("not ") or ligne.isEmpty()) ligne = in.readLine()
                # Je saute les commentaires et les lignes vides.
                i = 0
                while (ligne.startsWith("#") and  not in.atEnd())
                    if ((i<3) and (ligne.size() == 7)) _couleurs[i] = ligne
                    i+=1
                    ligne = in.readLine()

                # Je peux changer les couleurs dans le fichier
                MapLem item
                while (not in.atEnd())
                    if not ligne.startsWith("not ") and not ligne.isEmpty()) # hLem.insert(ligne,1:
                        item = lemmatiseM (ligne, False, False)
                        foreach (Lemme *lem, item.keys())
                            _hLem.insert(lem.cle(),0)

                    ligne = in.readLine()





    def verbaOut(self, fichier):
        if (_hLem.isEmpty()) return; # Rien à sauver !
        format = "%1\t%2\n"
        QFile file(fichier)
        if file.open(QFile.WriteOnly | QFile.Text):
            for lem in _hLem.keys():
                file.write(format.arg(lem).arg(_hLem[lem]).toUtf8())


