:- encoding(utf8).

:- discontiguous etablissement/5.

:- discontiguous filiere/6.

:- discontiguous serie_bac/1.

:- discontiguous secteur_formation/1.

:- discontiguous plateforme/2.

:- discontiguous specialite/2.

:- discontiguous debouche_associe/2.

:- discontiguous institution/9.
:- discontiguous institution/10.
:- discontiguous specialisation/4.
:- discontiguous specialisation/5.
:- discontiguous document_requis/3.
:- discontiguous document_requis/4.

:- discontiguous conseil_orientation/4.

:- discontiguous recommandation_profil/4.

:- discontiguous debouches_filiere/2.

:- discontiguous detail_ecole/4.

:- discontiguous localisation/2.

:- discontiguous definition/2.

:- discontiguous info/2.

:- discontiguous stat/3.

:- discontiguous ville_chance/1.

:- discontiguous detail_bac/5.

:- discontiguous detail_domaine/4.

:- discontiguous info_type/4.

:- discontiguous strategie_profil/3.

:- discontiguous check_compatibilite/4.



% =======================================================

% BASE DE CONNAISSANCES - PFE EXPERT (CLEAN VERSION)

% =======================================================



% -------------------------------------------------------

% 1. ORIENTATION & STRATEGIE (Regles Decisionnelles)

% -------------------------------------------------------



% A. RECOMMANDATIONS PAR BAC (debouche/4)

debouche('PC', 'Ingenierie', 'ENSA / FST', 'Recommande. Concours ou dossier. (Maths/Physique importants)').

debouche('PC', 'Ingenierie d''Excellence', 'UM6P / EMI', 'Si moyenne > 15 ou via CNC.').

debouche('PC', 'CPGE (Prepas)', 'MPSI / PCSI', 'Voie royale pour les grandes ecoles. Moyenne > 15 conseillee.').

debouche('SM', 'Top Ingenierie', 'EMI / ENSIAS', 'Via CPGE ou CNC. Profil tres recherche.').

debouche('SM', 'Informatique & Data', 'ENSIAS / INPT', 'Excellent choix pour les matheux.').

debouche('SM', 'Architecture', 'ENA', 'Concours specifique.').

debouche('SVT', 'Medecine & Pharmacie', 'FMP / FMD', 'Filiere de predilection. Moyenne > 13 conseillee.').

debouche('SVT', 'Sante (Paramedical)', 'ISPITS / IFCS', 'Via concours. Bonnes perspectives.').

debouche('SVT', 'Biologie / Agro', 'FST / APESA', 'Cycle ingenieur agronome IAV possible.').

debouche('ECO', 'Commerce & Gestion', 'ENCG', 'Top ecole publique (Via TAFEM).').

debouche('ECO', 'Management', 'ISCAE', 'Apres prepa ou licence. Tres prestigieux.').

debouche('ECO', 'Droit / Eco', 'Facultes', 'Filieres ouvertes. Maitrise du francais/arabe requise.').



% B. REGLES D'ELIGIBILITE MEDECINE

peut_faire_medecine(Bac, Note, '✅ Admissible (Favorable)') :-

    (Bac = 'SVT'), Note >= 13.

peut_faire_medecine(Bac, Note, '⚠️ Admissible mais dossier juste (Risque)') :-

    (Bac = 'PC'; Bac = 'SM'), Note >= 12.

peut_faire_medecine(_, _, '❌ Moyenne insuffisante (<12) ou Bac inadapte. Tentez le Prive.').



% C. STRATEGIE SELON MOYENNE (conseil_note/2)

conseil_note(High, 'Viser l''Excellence : Medecine, ENSA Rabat, EMI, Architecture.') :- High >= 15.

conseil_note(Med, 'Viser Strategique : ENSA (Villes moins demandees : Safi, Khouribga), FST, EST.') :- Med >= 13, Med < 15.

conseil_note(Low, 'Viser Securite : Facultes, BTS, ISTA, ou Ecoles Privees (si budget).') :- Low < 13.



% D. COMPATIBILITE BAC-FILIERE (Nouveau - Avertissements)

% compatibilite_bac_filiere(Bac, Filiere, Statut, Message).

% This is now handled by check_compatibilite/4 at the end of file for robustness.



% -------------------------------------------------------

% 2. CARTOGRAPHIE & VILLES (Geographie)

% -------------------------------------------------------



% Villes a forte concurrence

ville_concurrence('Casablanca').

ville_concurrence('Rabat').

ville_concurrence('Marrakech').

ville_concurrence('Fes').

ville_concurrence('Tanger').



% Villes "Opportunite"

ville_chance('Beni Mellal').

ville_chance('Safi').

ville_chance('Khouribga').

ville_chance('El Jadida').

ville_chance('Taza').

ville_chance('Errachidia').

ville_chance('Al Hoceima').



% Localisation des Etablissements Publics

localisation('Universite Hassan II', 'Casablanca').

localisation('Universite Hassan II', 'Mohammedia').

localisation('Universite Mohammed V', 'Rabat').

localisation('Universite Cadi Ayyad', 'Marrakech').

localisation('Universite Ibn Zohr', 'Agadir').

localisation('Universite Abdelmalek Essaadi', 'Tetouan').

localisation('ENSA', 'Agadir').

localisation('ENSA', 'Fes').

localisation('ENSA', 'Marrakech').

localisation('ENSA', 'Tanger').

localisation('ENSA', 'Tetouan').

localisation('ENSA', 'Khouribga').

localisation('ENSA', 'Safi').

localisation('ENSA', 'El Jadida').

localisation('ENSA', 'Berrechid').

localisation('ENSA', 'Beni Mellal').

localisation('ENSA', 'Oujda').

localisation('ENSA', 'Al Hoceima').

localisation('ENSAM', 'Meknes').

localisation('ENSAM', 'Casablanca').

localisation('ENSAM', 'Rabat').

localisation('ENSIAS', 'Rabat').

localisation('EMI', 'Rabat').

localisation('FST', 'Fes').

localisation('FST', 'Settat').

localisation('FST', 'Mohammedia').

localisation('FST', 'Beni Mellal').

localisation('FST', 'Errachidia').

localisation('UM6P', 'Benguerir').

localisation('Universite Al Akhawayn', 'Ifrane').



% Localisation du Prive

localisation('EMSI', 'Casablanca').

localisation('EMSI', 'Rabat').

localisation('EMSI', 'Marrakech').

localisation('EMSI', 'Fes').

localisation('UIR', 'Rabat').

localisation('SUPINFO', 'Casablanca').

localisation('HEM', 'Casablanca').

localisation('ESCA', 'Casablanca').

localisation('UIASS', 'Rabat').

localisation('UPSAT', 'Casablanca').



% -------------------------------------------------------

% 3. ECOLES PRIVEES (Details & Frais)

% -------------------------------------------------------

detail_ecole('EMSI', 'Ingenierie (Prive)', 'Genie Info, Indus, Civil', '28 000 - 38 000 DH/an').

detail_ecole('UIR', 'Universite Semi-Public', 'Aero, Info, Business, Sc.Po', '65 000 - 95 000 DH/an').

detail_ecole('SUPINFO', 'IT (Prive)', 'Full Stack, Cloud, Cyber', '45 000 - 60 000 DH/an').

detail_ecole('HEM', 'Business (Prive)', 'Management, Marketing', '35 000 - 60 000 DH/an').

detail_ecole('ESCA', 'Business (Prive)', 'Finance, Audit', '45 000 - 70 000 DH/an').

detail_ecole('UIASS', 'Sante (Semi-Prive)', 'Medecine, Dentaire', '80 000 - 130 000 DH/an').

detail_ecole('UPSAT', 'Sante (Prive)', 'Medecine, Pharma', '70 000 - 110 000 DH/an').

detail_ecole('ISITT Prive', 'Tourisme', 'Management Hotelier', '20 000 - 30 000 DH/an').



% -------------------------------------------------------

% 4. STATISTIQUES & CHIFFRES CLES

% -------------------------------------------------------

stat('Global', 'Etudiants Maroc', '1.25 Million').

stat('Global', 'Filieres', '+1000 accreditees').

stat('Places', 'Medecine (Total)', '~4 800 places').

stat('Places', 'Medecine (Casa)', '~200 places').

stat('Places', 'ENSA (Total)', '~4 000 places').

stat('Places', 'ENSA (Casa)', '~350 places').

stat('Places', 'ENSA (Beni Mellal)', '~150 places').

stat('Selectivite', 'Medecine', '1 admis pour 22 candidats').

stat('Selectivite', 'ENSA', '1 admis pour 21 candidats').

stat('Salaires', 'Ingenieur Debutant', '8 000 - 12 000 DH/mois').

stat('Salaires', 'Medecin Public', '12 000 - 15 000 DH/mois').



% -------------------------------------------------------

% 5. CONSEILS & METHODOLOGIE (info/2)

% -------------------------------------------------------

info('Organisation', 'Fais un planning realiste. Ne charge pas trop tes journees.').

info('Organisation', 'Utilise la methode Pomodoro (25min travail / 5min pause).').

info('Organisation', 'Dors au moins 7h/nuit. Le cerveau memorise en dormant.').

info('Organisation', 'Cree un agenda hebdomadaire avec horaires fixes pour etudes et revisions.').



info('Methode', 'Revise avec des fiches de synthese (formules, dates, definitions).').

info('Methode', 'Pratique sur les ANNALES des annees precedentes. C''est crucial.').

info('Methode', 'Explique ton cours a voix haute (Technique Feynman) pour verifier ta comprehension.').



info('Examens', 'Revise regulierement pour eviter le stress de derniere minute.').

info('Examens', 'Priorise les matieres cles mais ne neglige pas les "faciles" qui ameliorent la moyenne.').

info('Examens', 'Divise les chapitres par semaine pour un plan d''etude progressif.').



info('Assiduite', 'Assiste a TOUS les cours et TD/TP. L''absence cree des lacunes.').

info('Assiduite', 'Participe activement aux travaux pratiques et projets.').



info('Ressources', 'Utilise bibliotheques, plateformes en ligne, notes partagees par anciens.').

info('Ressources', 'Rejoins tutorats ou groupes d''etudes pour renforcer tes connaissances.').



info('Competences', 'Francais et anglais indispensables. Renforce ton niveau via cours ou apps.').

info('Competences', 'Maitrise Excel, Word, PowerPoint et logiciels specifiques a ta filiere.').



info('Medecine', 'Revisions continues pour cours volumineux. Groupes de travail pour anatomie/physiologie.').

info('Commerce', 'Pratique cas reels, etudes de marche, exercices financiers.').



info('Strategie', 'Plan A / Plan B : Toujours avoir une filiere "Securite" (Fac, Prive) si ton 1er choix echoue.').

info('Strategie', 'Regarde les debouches REELS (Offres d''emploi sur LinkedIn) avant de choisir.').

info('Strategie', 'Pense aux villes "Opportunite" (Beni Mellal, Safi...) si ta note est juste.').



info('Vie Pro', 'Les stages sont obligatoires pour un bon CV. Cherche des la 1ere annee.').

info('Vie Pro', 'Anglais = Salaire. Passe le TOEIC ou TOEFL si tu peux.').



info('Budget', 'Bourses : Minhaty, Erasmus (Europe), Fulbright (USA). Renseigne-toi tot.').

info('Budget', 'Logement : Les cites universitaires sont prioritaires pour ceux qui habitent loin.').



% -------------------------------------------------------

% 6. DEFINITIONS (Systeme LMD)

% -------------------------------------------------------

definition('LMD', 'Systeme Licence (3 ans) -> Master (+2 ans) -> Doctorat (+3 ans). Standard mondial.').

definition('CPGE', 'Classes Prepas (2 ans intensifs). Prepare aux concours des Grandes Ecoles d''ingenieurs (CNC).').

definition('BTS', 'Brevet Technicien Superieur (2 ans). Formation courte, pratique, bonne insertion pro.').

definition('DUT', 'Diplome Universitaire Technologie (2 ans). Souvent en EST. Plus academique que le BTS.').

definition('Master', 'Bac+5. Specialisation necessaire pour les postes de cadres/responsabilite.').

definition('Ingenieur', 'Titre protege Bac+5. Formation technique et manageriale de haut niveau.').

definition('ENSA', 'Ecole Nationale des Sciences Appliquees (5 ans). Formation d''ingenieur d''etat. Acces post-bac ou bac+2.').

definition('ENCG', 'Ecole Nationale de Commerce et de Gestion (5 ans). Formation management/commerce. Acces par concours TAFEM.').

definition('EST', 'Ecole Superieure de Technologie (2 ans). Delivre le DUT. Formation technique courte.').

definition('FST', 'Faculte des Sciences et Techniques. Systeme LMD hybride (Tronc commun + Specialite). Acces sur dossier.').

definition('OFPPT', 'Office de la Formation Professionnelle. Formations courtes (2 ans) type Technicien Specialise. Pratique et insertion rapide.').



% -------------------------------------------------------

% API LOGIQUE (Predicats appeles par Python)

% -------------------------------------------------------



% Recommandation simple

recommander_orientation(Bac, Domaine, Ecole) :- detail_bac(Bac, Ideales, _, _, _), sub_string(Ideales, _, _, _, Domaine), Ecole = 'Voir detail'.



% Extraction de conseils par theme

conseil(Theme, Texte) :- info(Theme, Texte).



% -------------------------------------------------------

% 7. STRATEGIE AVANCEE (Check_Compatibilite + Details)

% -------------------------------------------------------



% Types d'etablissements & Pros/Cons

info_type(public_ouvert, 

    'Filieres ouvertes (Facs, Droit, Eco). Pas de selection.',

    '✅ Gratuit, Large choix, Accessible tous niveaux.',

    '⚠️ Effectifs charges, Moins de suivi, Peu de stages.').



info_type(public_regule, 

    'Filieres selectives (Medecine, ENSA, ENCG). Concours.',

    '✅ Diplome prestigieux, Excellent insertion pro, Gratuit.',

    '⚠️ Tres forte concurrence, Stress, Selection dure.').



info_type(prive, 

    'Ecoles privees (UIR, EMSI, HEM...). Payant.',

    '✅ Acces plus souple, Programmes modernes, Stages integres.',

    '⚠️ Cout eleve, Verifier la reconnaissance du diplome.').





% Logique de Strategie (strategie_profil/3)

% Usage: strategie_profil(Note, Bac, Conseil).



% Cas 1 : Excellente moyenne (>15)

strategie_profil(Note, _, '🌟 Profil EXCELLENT : Visez les filieres REGULEES (Public).\n👉 Medecine, ENSA, ENCG, CPGE.\n👉 Visez les grandes villes (Rabat, Casa) mais gardez un Plan B.') :-

    Note >= 15, !.



% Cas 2 : Bonne moyenne (13-15)

strategie_profil(Note, _, '📈 Profil BON : Strategie de "Contournement".\n👉 Visez les filieres regulees dans les VILLES MOYENNES (Safi, Khouribga, El Jadida) ou la concurrence est moindre.\n👉 Pensez aux FST qui sont un excellent compromis.') :-

    Note >= 13, Note < 15, !.



% Cas 3 : Moyenne Moyenne (11-13)

strategie_profil(Note, _, '🤔 Profil MOYEN : Choix Tactique necessaire.\n👉 1. Universites Publiques (Filieres Ouvertes) pour exceller et tenter des passerelles.\n👉 2. Ecoles Privees (si budget) pour un encadrement plus serre.\n👉 3. EST/BTS pour un diplome court et pro.') :-

    Note >= 11, Note < 13, !.



% Cas 4 : Moyenne Juste (<11)

strategie_profil(Note, _, '⚠️ Profil JUSTE : Ne prenez pas de risques.\n👉 Privilegiez un BTS/DTS (OFPPT) pour un metier rapide.\n👉 Ou une ecole Privee qui mise sur la pratique.\n👉 Evitez les facs surchargees si vous manquez d''autonomie.') :-

    Note < 11, !.



% Helpers

get_info_type(T, D, A, I) :- info_type(T, D, A, I).

get_strategie_profil(N, B, C) :- strategie_profil(N, B, C).



% -------------------------------------------------------

% 8. PROFILS BAC DETAILLES

% -------------------------------------------------------

% detail_bac(Bac, Ideales, Avantages, Limites, Conseil).



detail_bac('PC', 

    'Ingenierie (ENSA, EMI...), Informatique/IT, Sciences fondamentales.',

    '✅ Acces a presque toutes les filieres scientifiques. Bonne base pour concours.',

    '⚠️ Concurrence elevee en ingenierie.',

    '💡 Ideal si motive par les sciences exactes. Moyenne >= 13-14 recommandee pour le public selectif.').



detail_bac('SVT',

    'Medecine, Pharmacie, Dentaire, Biologie, Paramedical.',

    '✅ Voie royale pour la Sante. Profil polyvalent.',

    '⚠️ Difficile pour l''ingenierie mecanique/info pure dans le public.',

    '💡 Moyenne >= 14-15 imperative pour Medecine. Sinon, viser le Prive ou les filieres Bio.').



detail_bac('SM',

    'Maths, Statistique, Data Science, Ingenierie Top Niveau, Architecture.',

    '✅ Tres polyvalent. Acces privilegie aux Prepas (MPSI) et Grandes Ecoles.',

    '⚠️ Rythme intense.',

    '💡 Excellent pour combiner sciences et economie/finance de haut niveau.').



detail_bac('ECO',

    'Economie, Gestion, Commerce (ENCG/ISCAE), Droit, Finance.',

    '✅ Debouches nombreux en entreprise. Filieres bancaires.',

    '⚠️ Difficile pour l''ingenierie et les sciences dures.',

    '💡 Viser les ecoles de commerce selectives si bonne note. Sinon, Fac d''Eco/Droit.').



detail_bac('LITT',

    'Lettres, Langues, Communication, Journalisme, Sciences Humaines, Droit.',

    '✅ Acces aux metiers de la culture, medias et enseignement.',

    '⚠️ Difficile pour l''informatique et les sciences.',

    '💡 Explorer les ecoles privees pour les programmes modernes (Com, Digital Media).').



% Helper pour Python

get_detail_bac(Bac, I, A, L, C) :- detail_bac(Bac, I, A, L, C).





% -------------------------------------------------------

% 9. COMPATIBILITE (check_compatibilite/4)

% -------------------------------------------------------

% check_compatibilite(Bac, Filiere, Statut, Message).



% --- MEDECINE ---

check_compatibilite(Bac, medecine, impossible, '⛔ Incompatible : Medecine exige un Bac Scientifique (PC, SVT, SM).') :-

    member(Bac, ['ECO', 'LITT', 'TECH', 'ART']), !.



check_compatibilite(Bac, medecine, excellent, '✅ Excellent : Voie royale pour Medecine.') :-

    member(Bac, ['SVT']), !.



check_compatibilite(Bac, medecine, possible, '✅ Possible : Accessible, mais moins de Biologie au lycee donc un effort en 1ere annee.') :-

    member(Bac, ['SM', 'PC']), !.



% --- INGENIERIE ---

check_compatibilite(Bac, ingenierie, impossible, '⛔ Incompatible : Les ecoles d''ingenieurs publiques demandent un Bac Scientifique.') :-

    member(Bac, ['LITT', 'ART']), !.



check_compatibilite(Bac, ingenierie, difficile, '⚠️ Difficile : Peu de places pour Bac Eco/Technique dans le public, mais possible dans le PRIVE ou via des passerelles (BTS/DUT).') :-

    member(Bac, ['ECO', 'TECH']), !.



check_compatibilite(Bac, ingenierie, excellent, '✅ Excellent : Vous avez le profil ideal (Maths/Physique).') :-

    member(Bac, ['SM', 'PC']), !.



check_compatibilite(Bac, ingenierie, possible, '✅ Possible : Accessible (ENSA/FST), mais attention aux Maths.') :-

    member(Bac, ['SVT']), !.



% --- INFORMATIQUE ---

check_compatibilite(Bac, informatique, impossible, '⛔ Incompatible : Difficile sans bases logiques, mais possible via ecoles prives de code (Bootcamps).') :-

    member(Bac, ['LITT', 'ART']), !.



check_compatibilite(Bac, informatique, possible, '✅ Possible : Accessible via FST, EST ou Prive. Le Bac Eco permet l''informatique de gestion (MIAGE).') :-

    member(Bac, ['ECO']), !.



check_compatibilite(Bac, informatique, excellent, '✅ Excellent : Profil ideal pour le developpement et l''algo.') :-

    member(Bac, ['SM', 'PC']), !.



check_compatibilite(Bac, informatique, possible, '✅ Possible : Accessible notamment via les EST et FST.') :-

    member(Bac, ['SVT']), !.



% --- COMMERCE/GESTION ---

check_compatibilite(_, commerce, possible, '✅ Possible : Les filieres Commerce sont ouvertes a TOUS les Bacs (Scientifiques, Eco, Lettres). Le concours TAFEM est la cle.') :- !.



% --- LETTRES/DROIT ---

check_compatibilite(_, lettres, possible, '✅ Possible : Ouvert a tous les profils.') :- !.



% --- Fallback ---

check_compatibilite(_, _, inconnu, 'Je n''ai pas d''info specifique sur cette combinaison.').



% -------------------------------------------------------

% 10. DETAIL DOMAINE (detail_domaine/4)

% -------------------------------------------------------



detail_domaine(medecine,

    'Medecin, Pharmacien, Dentiste, Recherche biomedicale.',

    'Universites Publiques (FMP, FMD) et Privees (UPM, UIASS).',

    '💡 Bac Scientifique Obligatoire. Concours selectif.').



detail_domaine(ingenierie,

    'Ingenieur Civil, Mecanique, Indus, Data Scientist.',

    'ENSA, EMI, ENSIAS, UM6P. (Toutes villes).',

    '💡 Bac PC ou SM recommande. Prepa (CPGE) est la voie classique.').



detail_domaine(informatique,

    'Developpeur, Data Scientist, Cybersecurite, Consultant.',

    'EMSI, SUPINFO, UIR, ENSIAS, INPT, EST.',

    '💡 Tres forte demande. Diplome moins important que la competence reelle.').



detail_domaine(commerce,

    'Manager, Analyste Financier, Auditeur, Marketing, RH.',

    'ENCG, ISCAE, HEM, ESCA, UIR.',

    '💡 Bac ES ou SM recommande. Anglais crucial.').



detail_domaine(shs,

    'Journaliste, Psychologue, Sociologue, Enseignant.',

    'Facultes de Lettres & Sciences Humaines (FLSH), Droit.',

    '💡 Culture generale et expression ecrite sont les cles.').



detail_domaine(archi,

    'Architecte, Urbaniste, Designer, Styliste.',

    'ENA (Architecture), INBA (Beaux-Arts).',

    '💡 Concours specifique (Dessin + Maths). 6 ans d''etudes.').



get_detail_domaine(D, M, E, C) :- detail_domaine(D, M, E, C).



% -------------------------------------------------------

% 11. FINANCE, LOGEMENT, PROCEDURES

% -------------------------------------------------------



financement(public, 'Frais tres faibles. Ideal budget limite.', 'Accessible tous.').

financement(bourses_gouvernementales, 'Minhaty.', 'Verifier criteres sur minhaty.ma.').



get_financement(T, D, C) :- financement(T, D, C).



procedure('Inscription Fac', '1. Pre-inscription site. 2. Depot dossier.').

procedure('Dossier Minhaty', '1. Inscription minhaty.ma. 2. Depot dossier physique.').

procedure('Legalisation', 'Toujours legaliser copies Bac et Releves.').



get_procedure(T, D) :- procedure(T, D).



logement('Cite Universitaire', 'Logement public. 40-50 DH/mois.', 'Demande ONOUHC.').

logement('Internat', 'CPGE et Lycees Excellence.', 'Se renseigner aupres du lycee.').



get_logement(T, D, C) :- logement(T, D, C).



% -------------------------------------------------------

% 12. DATES & SEUILS

% -------------------------------------------------------

seuil('ENSA', 2023, 13.5).

seuil('Medecine', 2023, 12.0).

seuil('ENCG', 2023, 12.0).



get_seuil(E, A, N) :- seuil(E, A, N).



date_concours('Concours Medecine', 'Juillet (mi-juillet)').

date_concours('Concours ENSA', 'Juillet (fin juillet)').

date_concours('Concours ENCG (TAFEM)', 'Juillet').



get_date_concours(E, D) :- date_concours(E, D).



lien('CursusSup', 'https://www.cursussup.gov.ma').

lien('Minhaty', 'https://www.minhaty.ma').



get_lien(N, U) :- lien(N, U).



% -------------------------------------------------------

% 13. DATA SUPPLEMENTAIRE (Filiere/6)

% -------------------------------------------------------



% SÃ©ries Bac (Clean)

serie_bac('Sciences mathematiques A').

serie_bac('Sciences physiques').

serie_bac('Sciences de la Vie et de la Terre').

serie_bac('Sciences economiques').

serie_bac('Lettres').



% Exemples de filieres (Data echantillon pour le test)

filiere('Sciences mathematiques A', 'Sciences, technologie et industrie', 'CPGE MPSI', 'Lydex', 2, 'Attestation').

filiere('Sciences mathematiques A', 'Developpement Digital et IA', 'Genie Logiciel', 'ENSIAS', 3, 'Ingenieur').



filiere('Sciences physiques', 'Sciences, technologie et industrie', 'Genie Civil', 'EHTP', 3, 'Ingenieur').

filiere('Sciences physiques', 'Secteur medical et paramedical', 'Medecine Generale', 'FMP Rabat', 7, 'Doctorat').



filiere('Sciences de la Vie et de la Terre', 'Secteur medical et paramedical', 'Medecine Dentaire', 'FMD Casa', 6, 'Doctorat').



filiere('Sciences economiques', 'Economie, gestion et logistique', 'Commerce International', 'ENCG Setatt', 5, 'Master').


% -------------------------------------------------------
% 14. FORMATION PRO (OFPPT)
% -------------------------------------------------------
formation_pro('Technicien Specialise', 'Formation Bac+2. Diplome Technicien Specialise (DTS).', 'Acces : Bac. Duree : 2 ans. Debouches : Insertion pro rapide ou Licence Pro.').
formation_pro('Technicien', 'Formation Niveau Bac. Diplome Technicien (DT).', 'Acces : Niveau Bac (2eme annee). Duree : 2 ans.').
formation_pro('Qualification', 'Formation Niveau 3eme College. Diplome Qualification (DQ).', 'Acces : 3eme College. Duree : 2 ans.').

get_formation_pro(N, D, C) :- formation_pro(N, D, C).



% -------------------------------------------------------
% 15. CONCOURS & ADMISSIONS (Nouveau)
% -------------------------------------------------------
:- discontiguous concours_admission/3.

concours_admission(medecine, '4 Epreuves QCM (30-45min chacune) : Maths, SVT, Physique, Chimie. (Coef 1).', '?? Seuil 2024 : 13.00/20 (Moyenne Bac). \n?? Astuce : La rapidite est cle. Utilisez des astuces mathematiques, ne calculez pas tout.').
concours_admission(ingenierie_public, 'Concours Commun (ENSA/ENSAM/Mundiapolis...). Epreuves QCM : Maths, Physique, Anglais.', '?? Entrainez-vous sur les concours des annees precedentes (ConcoursMaroc.com). Gestion du temps cruciale.').
concours_admission(commerce, 'TAFEM (ENCG) : QCM vari (Memorisation, Maths, Culture G, Langues).', '?? Le test de memorisation se joue au debut. Soyez attentif et rapide.').
concours_admission(ecoles_privees, 'Selection sur Dossier + Test d''admission (Logique/Anglais) + Entretien.', '?? L''entretien de motivation est le plus important. Preparez votre projet professionnel.').

get_concours_admission(K, E, C) :- concours_admission(K, E, C).



% FIX UTF8
concours_admission(medecine, 'Epreuves QCM (Coef 1) : Maths, SVT, Physique-Chimie.', '?? Seuil 2024 : 13.00/20. \n?? Astuce : Soyez rapide, utilisez des astuces mathematiques (ne calculez pas tout). \n?? 3 Epreuves QCM (Maths et SVT sont cruciales).').


:- discontiguous concours_admission/3.



% =======================================================
% BASE DE CONNAISSANCES V2 (APPENDED)
% =======================================================


% BASE DE CONNAISSANCES (Version 2)

% ------------------------------------------------------------------------------
% 1. SÉRIES DE BACCALAURÉAT
% ------------------------------------------------------------------------------
serie_bac('Sciences mathématiques A').
serie_bac('Sciences mathématiques B').
serie_bac('Sciences physiques').
serie_bac('Sciences de la Vie et de la Terre').
serie_bac('Sciences agricoles').
serie_bac('Sciences économiques').
serie_bac('Sciences de gestion comptable').
serie_bac('Sciences et technologies électriques').
serie_bac('Sciences et technologies mécaniques').
serie_bac('Arts appliqués').
serie_bac('Lettres').
serie_bac('Sciences humaines').
serie_bac('Langue arabe').
serie_bac('Sciences de la charia').
serie_bac('Bac Pro Industriel').
serie_bac('Bac Pro Services').
serie_bac('Bac Pro Agriculture').

% ------------------------------------------------------------------------------
% 2. SECTEURS DE FORMATION
% ------------------------------------------------------------------------------
secteur_formation('Sciences, technologie et industrie').
secteur_formation('Secteur médical et paramédical').
secteur_formation('Économie, gestion et logistique').
secteur_formation('Agriculture, élevage et médecine vétérinaire').
secteur_formation('Architecture et Travaux Publics').
secteur_formation('Secteur militaire et paramilitaire').
secteur_formation('Secteur du travail social').
secteur_formation('Tourisme et hôtellerie').
secteur_formation('Arts, Culture et Patrimoine').
secteur_formation('Audiovisuel et Cinéma').
secteur_formation('Sport et Éducation Physique').
secteur_formation('Langues, Lettres et Sciences Humaines').
secteur_formation('Secteur de l''éducation').
secteur_formation('Sciences religieuses').
secteur_formation('Développement Digital et IA').

% ------------------------------------------------------------------------------
% 3. ÉTABLISSEMENTS PUBLICS (Standardisés par Acronymes)
% Format: etablissement(Acronyme, Ville, Diplome, Duree, Acces).
% ------------------------------------------------------------------------------

% --- Ingénierie (ENSA, ENSAM, FST) ---
etablissement('ENSA', 'Tanger', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSA', 'Agadir', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSA', 'Oujda', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSA', 'Marrakech', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSA', 'Safi', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSA', 'Fès', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSA', 'Khouribga', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSA', 'Kénitra', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSA', 'Tétouan', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSA', 'El Jadida', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSA', 'Al Hoceima', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSA', 'Berrchid', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSA', 'Beni Mellal', 'Ingénieur d''État', 5, 'selection_concours').

etablissement('ENSAM', 'Meknès', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSAM', 'Casablanca', 'Ingénieur d''État', 5, 'selection_concours').
etablissement('ENSAM', 'Rabat', 'Ingénieur d''État', 5, 'selection_concours').

etablissement('FST', 'Mohammedia', 'DEUST', 2, 'selection').
etablissement('FST', 'Mohammedia', 'Ingénieur d''État', 5, 'selection').
etablissement('FST', 'Settat', 'DEUST', 2, 'selection').
etablissement('FST', 'Fès', 'DEUST', 2, 'selection').
etablissement('FST', 'Marrakech', 'DEUST', 2, 'selection').
etablissement('FST', 'Tanger', 'DEUST', 2, 'selection').

% --- Nouvelles Écoles d'Ingénieurs Spécialisées ---
etablissement('ENIAD', 'Berkane', 'Ingénieur IA', 5, 'selection_concours').
etablissement('ENSC', 'Kénitra', 'Ingénieur Chimie', 5, 'selection_concours').
etablissement('ESITH', 'Casablanca', 'Ingénieur Textile', 5, 'selection_concours').
etablissement('ESITH', 'Casablanca', 'Licence Pro', 3, 'selection').

% --- Commerce (ENCG, ISCAE) ---
etablissement('ENCG', 'Settat', 'Diplôme ENCG', 5, 'selection_concours').
etablissement('ENCG', 'Tanger', 'Diplôme ENCG', 5, 'selection_concours').
etablissement('ENCG', 'Agadir', 'Diplôme ENCG', 5, 'selection_concours').
etablissement('ENCG', 'Marrakech', 'Diplôme ENCG', 5, 'selection_concours').
etablissement('ENCG', 'Oujda', 'Diplôme ENCG', 5, 'selection_concours').
etablissement('ENCG', 'Kénitra', 'Diplôme ENCG', 5, 'selection_concours').
etablissement('ENCG', 'El Jadida', 'Diplôme ENCG', 5, 'selection_concours').
etablissement('ENCG', 'Fès', 'Diplôme ENCG', 5, 'selection_concours').
etablissement('ENCG', 'Casablanca', 'Diplôme ENCG', 5, 'selection_concours').
etablissement('ENCG', 'Dakhla', 'Diplôme ENCG', 5, 'selection_concours').
etablissement('ENCG', 'Beni Mellal', 'Diplôme ENCG', 5, 'selection_concours').
etablissement('ENCG', 'Meknès', 'Diplôme ENCG', 5, 'selection_concours').

etablissement('ISCAE', 'Casablanca', 'Diplôme Grande École', 3, 'selection_concours').

% --- Médecine & Santé ---
etablissement('FMP', 'Rabat', 'Doctorat en Médecine', 7, 'selection_concours').
etablissement('FMP', 'Casablanca', 'Doctorat en Médecine', 7, 'selection_concours').
etablissement('FMP', 'Marrakech', 'Doctorat en Médecine', 7, 'selection_concours').
etablissement('FMP', 'Fès', 'Doctorat en Médecine', 7, 'selection_concours').
etablissement('FMP', 'Oujda', 'Doctorat en Médecine', 7, 'selection_concours').
etablissement('FMP', 'Tanger', 'Doctorat en Médecine', 7, 'selection_concours').
etablissement('FMP', 'Agadir', 'Doctorat en Médecine', 7, 'selection_concours').

etablissement('FMP', 'Rabat', 'Doctorat en Pharmacie', 6, 'selection_concours').
etablissement('FMP', 'Casablanca', 'Doctorat en Pharmacie', 6, 'selection_concours').

etablissement('FMD', 'Rabat', 'Doctorat Dentaire', 6, 'selection_concours').
etablissement('FMD', 'Casablanca', 'Doctorat Dentaire', 6, 'selection_concours').

etablissement('ISPITS', 'Multi-villes', 'Licence Infirmier', 3, 'selection_concours').
etablissement('I3S', 'Settat', 'Licence Sc. Santé', 3, 'selection_concours').

% --- Facultés (Accès Direct) ---
etablissement('Faculté des Sciences', 'Rabat', 'DEUG', 2, 'direct').
etablissement('Faculté des Sciences', 'Rabat', 'Licence Fondamentale', 3, 'direct').
etablissement('Faculté des Sciences', 'Casablanca', 'Licence Fondamentale', 3, 'direct').
etablissement('FSJES', 'Multi-villes', 'Licence Droit/Éco', 3, 'direct').
etablissement('FLSH', 'Multi-villes', 'Licence Lettres', 3, 'direct').

% --- Prépas & Autres ---
etablissement('CPGE', 'Multi-villes', 'CPGE', 2, 'selection').
etablissement('EST', 'Multi-villes', 'DUT', 2, 'selection').
etablissement('BTS', 'Multi-villes', 'BTS', 2, 'selection').
etablissement('OFPPT', 'Multi-villes', 'Technicien Spécialisé', 2, 'selection').

% --- Secteur Militaire ---
etablissement('ARM', 'Meknès', 'Officier (Bac+5)', 5, 'selection_concours').
etablissement('ERA', 'Marrakech', 'Officier Pilote', 5, 'selection_concours').
etablissement('ERN', 'Casablanca', 'Officier Marine', 5, 'selection_concours').
etablissement('ERSSM', 'Rabat', 'Médecin Militaire', 7, 'selection_concours').

% --- Arts & Sport ---
etablissement('INBA', 'Tétouan', 'Diplôme Beaux-Arts', 4, 'selection_concours').
etablissement('ISADAC', 'Rabat', 'Diplôme Art Dramatique', 4, 'selection_concours').
etablissement('IRFC/JS', 'Salé', 'Licence Pro Sport', 3, 'selection_concours').

% --- Architecture & Urbanisme ---
etablissement('ENA', 'Rabat', 'Architecte', 6, 'selection_concours').
etablissement('ENA', 'Fès', 'Architecte', 6, 'selection_concours').
etablissement('ENA', 'Marrakech', 'Architecte', 6, 'selection_concours').
etablissement('INAU', 'Rabat', 'Diplôme Urbanisme', 5, 'selection_concours').

% ------------------------------------------------------------------------------
% 4. FILIÈRES DE FORMATION (Lien Bac -> Formation)
% ------------------------------------------------------------------------------

% === Pour Bac Sciences Maths A & B ===
filiere('Sciences mathématiques A', 'Sciences, technologie et industrie', 'Génie Informatique', 'ENSA', '5 ans', 'Ingénieur d''État').
filiere('Sciences mathématiques A', 'Sciences, technologie et industrie', 'Génie Civil', 'EHTP', '5 ans', 'Ingénieur d''État').
filiere('Sciences mathématiques A', 'Sciences, technologie et industrie', 'Classes Prépas MPSI', 'CPGE', '2 ans', 'CPGE').
filiere('Sciences mathématiques A', 'Architecture et Travaux Publics', 'Architecture', 'ENA', '6 ans', 'Architecte').
filiere('Sciences mathématiques A', 'Secteur militaire et paramilitaire', 'Officier Ingénieur', 'ARM', '5 ans', 'Officier').
filiere('Sciences mathématiques B', 'Sciences, technologie et industrie', 'Génie Industriel', 'ENSA', '5 ans', 'Ingénieur d''État').
filiere('Sciences mathématiques B', 'Sciences, technologie et industrie', 'Pilotage', 'ERA', '5 ans', 'Officier Pilote').

% === Pour Bac Sciences Physiques (PC) ===
filiere('Sciences physiques', 'Sciences, technologie et industrie', 'Génie Mécatronique', 'ENSA', '5 ans', 'Ingénieur d''État').
filiere('Sciences physiques', 'Sciences, technologie et industrie', 'Génie Mécanique', 'ENSAM', '5 ans', 'Ingénieur d''État').
filiere('Sciences physiques', 'Sciences, technologie et industrie', 'Intelligence Artificielle', 'ENIAD', '5 ans', 'Ingénieur IA').
filiere('Sciences physiques', 'Sciences, technologie et industrie', 'Classes Prépas PCSI', 'CPGE', '2 ans', 'CPGE').
filiere('Sciences physiques', 'Secteur médical et paramédical', 'Soins Infirmiers', 'ISPITS', '3 ans', 'Licence Infirmier').
filiere('Sciences physiques', 'Secteur médical et paramédical', 'Kinésithérapie', 'ISPITS', '3 ans', 'Licence Kiné').
filiere('Sciences physiques', 'Secteur militaire et paramilitaire', 'Officier Marine', 'ERN', '5 ans', 'Officier Marine').

% === Pour Bac SVT ===
filiere('Sciences de la Vie et de la Terre', 'Secteur médical et paramédical', 'Médecine Générale', 'FMP', '7 ans', 'Doctorat en Médecine').
filiere('Sciences de la Vie et de la Terre', 'Secteur médical et paramédical', 'Médecine Dentaire', 'FMD', '6 ans', 'Doctorat Dentaire').
filiere('Sciences de la Vie et de la Terre', 'Secteur médical et paramédical', 'Pharmacie', 'FMP', '6 ans', 'Doctorat en Pharmacie').
filiere('Sciences de la Vie et de la Terre', 'Agriculture, élevage et médecine vétérinaire', 'Agronomie', 'IAV Hassan II', '5 ans', 'Ingénieur Agronome').
filiere('Sciences de la Vie et de la Terre', 'Sciences, technologie et industrie', 'Génie des Procédés', 'ENSA', '5 ans', 'Ingénieur d''État').

% === Pour Bac Économie & Gestion ===
filiere('Sciences économiques', 'Économie, gestion et logistique', 'Commerce International', 'ENCG', '5 ans', 'Diplôme ENCG').
filiere('Sciences économiques', 'Économie, gestion et logistique', 'Management', 'ENCG', '5 ans', 'Diplôme ENCG').
filiere('Sciences économiques', 'Économie, gestion et logistique', 'Licence Économie', 'FSJES', '3 ans', 'Licence').
filiere('Sciences économiques', 'Classes Prépas ECT', 'CPGE', '2 ans', 'CPGE').
filiere('Sciences de gestion comptable', 'Économie, gestion et logistique', 'Audit et Contrôle', 'ENCG', '5 ans', 'Diplôme ENCG').
filiere('Sciences de gestion comptable', 'Économie, gestion et logistique', 'Expertise Comptable', 'ISCAE', '3 ans', 'Diplôme Grande École').

% === Pour Bac Lettres & Humaines ===
filiere('Lettres', 'Langues, Lettres et Sciences Humaines', 'Études Anglaises', 'FLSH', '3 ans', 'Licence').
filiere('Lettres', 'Communication et médias', 'Journalisme', 'ISIC', '3 ans', 'Licence Info-Com').
filiere('Lettres', 'Tourisme et hôtellerie', 'Animation Touristique', 'ISITT', '3 ans', 'Diplôme Cycle Normal').
filiere('Sciences humaines', 'Secteur du travail social', 'Action Sociale', 'INAS', '3 ans', 'Diplôme INAS').
filiere('Sciences humaines', 'Langues, Lettres et Sciences Humaines', 'Psychologie', 'FLSH', '3 ans', 'Licence').

% === Pour Bac Technique (Élec/Méca) ===
filiere('Sciences et technologies électriques', 'Sciences, technologie et industrie', 'Génie Électrique', 'ENSET', '5 ans', 'Ingénieur d''État').
filiere('Sciences et technologies électriques', 'Sciences, technologie et industrie', 'Électromécanique', 'BTS', '2 ans', 'BTS').
filiere('Sciences et technologies mécaniques', 'Sciences, technologie et industrie', 'Génie Mécanique', 'ENSAM', '5 ans', 'Ingénieur d''État').
filiere('Sciences et technologies mécaniques', 'Sciences, technologie et industrie', 'Maintenance Industrielle', 'EST', '2 ans', 'DUT').

% === Pour Bac Arts Appliqués ===
filiere('Arts appliqués', 'Beaux-Arts et Design', 'Arts Plastiques', 'INBA', '4 ans', 'Diplôme Beaux-Arts').
filiere('Arts appliqués', 'Beaux-Arts et Design', 'Architecture d''Intérieur', 'ESBA', '4 ans', 'Diplôme Beaux-Arts').
filiere('Arts appliqués', 'Architecture et Travaux Publics', 'Architecture', 'ENA', '6 ans', 'Architecte').

% ------------------------------------------------------------------------------
% 5. PLATEFORMES D'ACCÈS
% ------------------------------------------------------------------------------
plateforme('FST', 'www.tawjihi.ma').
plateforme('ENSA', 'www.ensa-concours.ma').
plateforme('ENCG', 'www.tafem.ma').
plateforme('CPGE', 'www.cpge.ac.ma').
plateforme('EST', 'www.tawjihi.ma').
plateforme('FMP', 'www.cursussup.gov.ma').
plateforme('FMD', 'www.cursussup.gov.ma').
plateforme('ISPITS', 'ispits.sante.gov.ma').

% ------------------------------------------------------------------------------
% 6. SPÉCIALITÉS PAR ÉTABLISSEMENT (Exemples)
% ------------------------------------------------------------------------------
specialite('Faculté des Sciences', 'Mathématiques').
specialite('Faculté des Sciences', 'Physique').
specialite('FST', 'Informatique').
specialite('FST', 'Génie Civil').
specialite('ENSA', 'Génie Informatique').
specialite('ENSA', 'Génie Industriel').
specialite('ENSAM', 'Génie Mécanique').
specialite('CPGE', 'MPSI').
specialite('CPGE', 'PCSI').
specialite('CPGE', 'ECT').

% ------------------------------------------------------------------------------
% 7. DÉBOUCHÉS PROFESSIONNELS
% ------------------------------------------------------------------------------
debouche_associe('Génie Informatique', 'Développeur, Architecte Logiciel').
debouche_associe('Médecine Générale', 'Médecin Généraliste').
debouche_associe('Médecine Dentaire', 'Dentiste').
debouche_associe('Pharmacie', 'Pharmacien d''officine ou industriel').
debouche_associe('Génie Civil', 'Ingénieur BTP, Chef de chantier').
debouche_associe('Commerce International', 'Manager Export, Acheteur').
debouche_associe('Audit et Contrôle', 'Auditeur financier, Contrôleur de gestion').
debouche_associe('Journalisme', 'Journaliste, Rédacteur web').
debouche_associe('Soins Infirmiers', 'Infirmier polyvalent').
debouche_associe('Architecture', 'Architecte urbaniste').



%  RÈGLES D'ORIENTATION POST-BAC - MAROC 

% ------------------------------------------------------------------------------
% 1. Orientation Générale
% ------------------------------------------------------------------------------

% Règle 1: Orientation vers les filières scientifiques
orientation_scientifique(Etablissement, Diplome, Ville) :-
    etablissement(Etablissement, Ville, Diplome, _, _),
    member(Diplome, ['DEUG', 'Licence Fondamentale', 'DEUST', 'Ingénieur d''État', 'Ingénieur IA', 'Ingénieur Chimie']).

% Règle 2: Orientation médecine pour Bac Sciences
orientation_medecine(Etablissement, Diplome, Ville) :-
    etablissement(Etablissement, Ville, Diplome, _, 'selection_concours'),
    member(Diplome, ['Doctorat en Médecine', 'Doctorat en Pharmacie', 'Doctorat Dentaire']).

% Règle 3: Orientation prépas scientifiques
orientation_prepas(Etablissement) :-
    etablissement(Etablissement, _, 'CPGE', _, 'selection').

% ------------------------------------------------------------------------------
% 2. Règles d'Accès
% ------------------------------------------------------------------------------

% Règle 4: Accès direct pour les facultés
acces_direct(Etablissement, Diplome) :-
    etablissement(Etablissement, _, Diplome, _, 'direct').

% Règle 5: Accès par sélection/concours
acces_concours(Etablissement, Diplome) :-
    etablissement(Etablissement, _, Diplome, _, Acces),
    member(Acces, ['selection', 'selection_concours', 'concours_national']).

% ------------------------------------------------------------------------------
% 3. Règles par Durée de Formation
% ------------------------------------------------------------------------------

% Règle 6: Formations longues (≥5 ans)
formation_longue(Etablissement, Diplome) :-
    etablissement(Etablissement, _, Diplome, Duree, _),
    Duree >= 5.

% Règle 7: Formations courtes (2-3 ans)
formation_courte(Etablissement, Diplome) :-
    etablissement(Etablissement, _, Diplome, Duree, _),
    Duree =< 3.

% Règle 8: Formations moyennes (4 ans)
formation_moyenne(Etablissement, Diplome) :-
    etablissement(Etablissement, _, Diplome, 4, _).

% ------------------------------------------------------------------------------
% 4. Règles de Spécialité & Recherche Avancée
% ------------------------------------------------------------------------------

% Règle 9: Vérification de spécialité disponible
specialite_disponible(Etablissement, Specialite) :-
    specialite(Etablissement, Specialite).

% Règle 10: Filières accessibles par série de bac
filiere_accessibles(Bac, Filiere, Secteur, Etablissement, Duree, Diplome) :-
    serie_bac(Bac),
    filiere(Bac, Secteur, Filiere, Etablissement, Duree, Diplome).

% Règle 11: Filières par secteur d'intérêt
filiere_par_secteur(Bac, Secteur, Filiere, Etablissement, Duree, Diplome) :-
    serie_bac(Bac),
    secteur_formation(Secteur),
    filiere(Bac, Secteur, Filiere, Etablissement, Duree, Diplome).

% Règle 12: Filières par durée spécifique
filiere_par_duree(Bac, Duree, Filiere, Secteur, Etablissement, Diplome) :-
    filiere(Bac, Secteur, Filiere, Etablissement, Duree, Diplome).

% Règle 13: Établissements par type d'accès
etablissement_par_acces(Nom, Ville, Diplome, Duree, Acces) :-
    etablissement(Nom, Ville, Diplome, Duree, Acces).

% ------------------------------------------------------------------------------
% 15. MÉTIERS D'AVENIR & NOUVEAUX DÉBOUCHÉS (Appended for Upgrade)
% ------------------------------------------------------------------------------
metier_avenir('Intelligence Artificielle', 'Data Scientist, Ingénieur ML', 'Très Forte', 'Formation: ENSIAS, INPT, ENIAD, FST (Master Data). Salaires attractifs dès la sortie.').
metier_avenir('Santé Numérique', 'Bio-informaticien', 'Forte', 'Formation: FMP, UM6P, FST. Demande croissante pour l''analyse de données médicales.').
metier_avenir('Cybersécurité', 'Consultant Cyber', 'Très Forte', 'Formation: ENSIAS, ENSA, UIR. Pénurie de profils au Maroc et à l''international.').
metier_avenir('Énergies Renouvelables', 'Ingénieur Énergétique', 'Moyenne/Forte', 'Formation: ENSA, FST, UM6P. Enjeu majeur du Maroc (Noor).').

get_metier_avenir(Domaine, Metier, Demande, Conseils) :- metier_avenir(Domaine, Metier, Demande, Conseils).

% ------------------------------------------------------------------------------
% 16. BOURSES DE MÉRITE (Privé)
% ------------------------------------------------------------------------------
bourse_merite('UIR', 'Excellence (100%)', 'Moyenne Bac >= 16/20').
bourse_merite('UIR', 'Partielle (50%)', 'Moyenne Bac >= 14/20 ou sur étude dossier social').
bourse_merite('UM6P', 'Bourse Fondation OCP', 'Excellence académique + Dossier social').
bourse_merite('EMSI', 'Bourse d''Encouragement', 'Pour les majors de promotion').
bourse_merite('EFA', 'Bourse d''excellence (Filles)', 'Très bonnes notes + Milieu rural').

get_bourse_merite(Ecole, Type, Condition) :- bourse_merite(Ecole, Type, Condition).

% Règle 15: Filières avec accès direct (sans concours)
filiere_acces_direct(Bac, Filiere, Etablissement) :-
    filiere(Bac, _, Filiere, Etablissement, _, _),
    etablissement(Etablissement, _, _, _, 'direct').

% ------------------------------------------------------------------------------
% 5. Règles de Conseil et Recommandation
% ------------------------------------------------------------------------------

% Règle 17: Conseils d'orientation basés sur les notes
conseil_orientation(Bac, Note_Maths, Note_Physique, Recommandation) :-
    serie_bac(Bac),
    (Note_Maths >= 15, Note_Physique >= 14 ->
        Recommandation = 'Ingénierie, Médecine ou Architecture recommandées (CPGE/ENSA/ENA)';
    Note_Maths >= 15 ->
        Recommandation = 'Sciences exactes, Ingénierie et Technologies (ENSA/FST)';
    Note_Physique >= 14 ->
        Recommandation = 'Sciences de la vie, Médical et Paramédical (FMP/ISPITS)';
    Recommandation = 'Toutes les filières universitaires et techniques sont accessibles selon vos intérêts').

% Règle 18: Recommandation par profil étudiant
recommandation_profil(Bac, Interet, Filiere, Etablissement) :-
    serie_bac(Bac),
    secteur_formation(Interet),
    filiere(Bac, Interet, Filiere, Etablissement, _, _).

% Règle 19: Comparaison de filières par durée
comparer_duree(Filiere1, Filiere2, Resultat) :-
    filiere(_, _, Filiere1, _, Duree1, _),
    filiere(_, _, Filiere2, _, Duree2, _),
    (Duree1 < Duree2 -> Resultat = 'plus_courte';
     Duree1 > Duree2 -> Resultat = 'plus_longue';
     Resultat = 'meme_duree').

% Règle 20: Débouchés professionnels (DYNAMIQUE)
% Cette règle va maintenant chercher dans la base de faits unifiée
debouches_filiere(Filiere, Debouche) :-
    debouche_associe(Filiere, Debouche).

% ------------------------------------------------------------------------------
% 6. Règles Utilitaires
% ------------------------------------------------------------------------------
% Règle 21: Vérification de compatibilité bac-filière
compatible_bac_filiere(Bac, Filiere) :-
    filiere(Bac, _, Filiere, _, _, _).

% Règle 22: Établissements dans une ville donnée
etablissements_ville(Ville, Etablissement, Diplome) :-
    etablissement(Etablissement, Ville, Diplome, _, _).

% Règle 23: Toutes les options pour un bac donné (Retourne une liste unique)
options_bac(Bac, Options) :-
    findall(Filiere, filiere(Bac, _, Filiere, _, _, _), FilieresList),
    list_to_set(FilieresList, Options).

% Règle 24: Recherche floue (Insensible à la casse)
recherche_floue_etablissement(_Requete, Resultat) :-
    etablissement(Resultat, _, _, _, _),
% ------------------------------------------------------------------------------
% 7. FRAIS DE SCOLARITÉ (Nouveau - Logic Training)
% ------------------------------------------------------------------------------
frais_scolarite('EMSI', '35 000 DH a 40 000 DH / an', 'Frais inscription non inclus. Paiement par tranches possible.').
frais_scolarite('UIR', '72 000 DH a 90 000 DH / an', 'Variable selon la filiere. Logement en sus.').
frais_scolarite('UM6P', '75 000 DH a 100 000 DH / an', 'Bourses de merite genereux de la Fondation OCP.').
frais_scolarite('HEM', '65 000 DH a 75 000 DH / an', 'Ecole de commerce privee prestigieuse.').
frais_scolarite('ESCA', '60 000 DH a 70 000 DH / an', 'Specialisee en Management et Finance.').
frais_scolarite('ENSA', 'Gratuit (0 DH)', 'Ecole publique d''Etat. Quelques frais administratifs minimes (~500 DH). Pas de frais de scolarite !').
frais_scolarite('ENCG', 'Gratuit (0 DH)', 'Ecole publique d''Etat. Droits d''inscription simboliques (~1 000 DH/an).').
frais_scolarite('FST', 'Gratuit (0 DH)', 'Faculte universitaire publique. Frais d''inscription legaux (~300 DH/an).').
frais_scolarite('ENSIAS', 'Gratuit (0 DH)', 'Grande ecole publique d''ingenierie. Acces sur concours, formatioon gratuite.').

get_frais_scolarite(Ecole, Prix, Note) :- frais_scolarite(Ecole, Prix, Note).

% ------------------------------------------------------------------------------
% 8. PROCÉDURES D'ADMISSION DÉTAILLÉES
% ------------------------------------------------------------------------------
procedure_etape('Minhaty', 1, 'Creer un compte sur le portail minhaty.ma pendant la periode fixee (souvent Juin).').
procedure_etape('Minhaty', 2, 'Saisir les informations personnelles, familiales et le code Massar.').
procedure_etape('Minhaty', 3, 'Valider la demande. Le dossier est ensuite traite sur base de critères sociaux (revenu parents).').
procedure_etape('Minhaty', 4, 'Verification de l''attribution de la bourse via le site ou recu par courrier/SMS.').

procedure_etape('Medecine', 1, 'Pre-inscription en ligne sur la plateforme nationale CursusSup.ma.').
procedure_etape('Medecine', 2, 'Selection sur base de la moyenne du Bac (Seuil).').
procedure_etape('Medecine', 3, 'Passage du concours ecrit (Maths, SVT, PC).').

get_procedure_details(Cible, Etape, Txt) :- procedure_etape(Cible, Etape, Txt).

% ------------------------------------------------------------------------------
% 9. DÉFINITIONS ET INFOS GÉNÉRALES (GENERAL_INFO)
% ------------------------------------------------------------------------------
definition('ENCG', 'Ecole Nationale de Commerce et de Gestion', 'Un reseau d''ecoles publiques d''excellence pour les cadres en commerce et gestion. Acces tres selectif.').
definition('ENSA', 'Ecole Nationale des Sciences Appliquees', 'Un reseau d''ecoles d''ingenieurs publiques avec cycle preparatoire integre (5 ans). Tres demandees.').
definition('UM6P', 'Universite Mohammed VI Polytechnique', 'Une universite privee d''excellence situee a Benguerir. Elle offre beaucoup de bourses sociales et finance la recherche.').
definition('FST', 'Faculte des Sciences et Techniques', 'Des facultes offrant des cursus pratiques (Licence, Master, Cycle Ingenieur). Ideal si tu cherches du concret.').
definition('FMP', 'Faculte de Medecine et de Pharmacie', 'La faculte pour devenir docteur ou pharmacien. Les annees sont longues et difficiles mais les debouches sont garantis.').

get_definition(Acronyme, Nom, Detail) :- definition(Acronyme, Nom, Detail).

% ------------------------------------------------------------------------------
% 10. SEUILS HISTORIQUES ET AUTRES (Edge cases)
% ------------------------------------------------------------------------------
seuil_historique('medecine', '2023', 'Environ 14.00 (mais a baisse recemment)').
seuil_historique('medecine', '2022', 'Environ 13.50').

get_seuil_historique(Filiere, Annee, Seuil) :- seuil_historique(Filiere, Annee, Seuil).

% ------------------------------------------------------------------------------
% 11. RECOMMANDATIONS & SOFT SKILLS
% ------------------------------------------------------------------------------
recommandation('informatique', 'Les meilleures ecoles sont l''ENSIAS, INPT, ENSA et l''UM6P. Dans le prive, l''UIR et l''EMSI se demarquent.').
recommandation('commerce', 'L''ENCG reste la reference publique. Dans le prive, l''ISCAE (elite) et HEM/UIR/ESCA sont d''excellentes options.').

get_recommandation(Domaine, Texte) :- recommandation(Domaine, Texte).

soft_skills('stress', 'Pour le stress du bac : 1. Fais des nuits de 8h (le sommeil fixe la memoire). 2. Utilise la technique Pomodoro (25min travail / 5min pause). 3. Respire avant l''epreuve. Tu vas y arriver !').
soft_skills('organisation', 'Cree un planning fixe. Alterne entre les matieres scientifiques (le matin quand tu es frais) et les matieres litteraires (l''apres-midi).').

get_soft_skills(Sujet, Conseil) :- soft_skills(Sujet, Conseil).

% ------------------------------------------------------------------------------
% 12. AVIS & OPINIONS (OPINION questions: 'L\'ENCG c'est bien ?')
% ------------------------------------------------------------------------------
avis_ecole('ENCG', 'Excellent (4.5/5)', 'Reseau solide, formation publique de qualite, forte reputation chez les employeurs marocains.', 'Tres selectif, peu de places, concours difficile.').
avis_ecole('EMSI', 'Tres bien (4/5)', 'Ecole privee sérieuse en IT, bons insertions pro, double cursus possible.', 'Frais eleves (~40k/an), certifications pratiques parfois superficielles.').
avis_ecole('UIR', 'Excellent (4.5/5)', 'Campus moderne, filières internationales, business et ingénierie de qualite.', 'Tres cher (70-90k/an). Acces en anglais partiel.').
avis_ecole('UM6P', 'Exceptionnel (5/5)', 'Recherche de pointe, bourses tres genereux, environnement innovant de classe mondiale.', 'Tres selectif, loin des grandes villes (Benguerir).').
avis_ecole('FST', 'Bien (3.5/5)', 'Formation publique solide en sciences et techniques, quasi gratuite.', 'Promotion de masse, peu de suivi individuel.').
avis_ecole('ENSA', 'Tres bien (4.5/5)', 'Meilleur rapport qualite/prix : ecole d''ingenieur gratuite (publique) reconnue par les entreprises.', 'Concours selectif. Peu de debouches internationaux sans effort supplementaire.').

get_avis_ecole(Ecole, Note, Positif, Negatif) :- avis_ecole(Ecole, Note, Positif, Negatif).


% ============================================================================
% Base de Connaissances Prolog - Guide d'Orientation Post-Baccalauréat
% Région de l'Est - Maroc 2025/2026
% Conversion du PDF en Prolog structuré avec traduction FR
% ============================================================================

% ============================================================================
% 1. INSTITUTIONS SUPÉRIEURES ET LEURS CARACTÉRISTIQUES
% ============================================================================

% Instituts Supérieurs d'Arts et de Communication
institution(isic, nom('Institut Supérieur d\'Information et de Communication'),
    type(institut_superieur),
    domaine(communication_media),
    adresse('Fnideq, Tanger'),
    email('https://preinscription.isic.ma'),
    site('www.isic.ac.ma'),
    duree_formation(3)).

institution(ismac, nom('Institut Supérieur des Métiers Audiovisuels et du Cinéma'),
    type(institut_superieur),
    domaine(cinema_audiovisuel),
    adresse('Fès'),
    description('Formation en cinéma et production audiovisuelle'),
    site('www.ismac.ac.ma'),
    duree_formation(3)).

% Instituts Supérieurs d'Arts Plastiques
institution(insap, nom('Institut National de Sciences Appliquées et de Pédagogie'),
    type(institut_superieur),
    domaine('sciences_appliquees'),
    adresse('Fès'),
    description('Formation en sciences et pédagogie'),
    specialisations(['astronomie', 'modélisation', 'enseignement']),
    duree_formation(4)).

institution(inba, nom('Institut National des Beaux-Arts'),
    type(institut_superieur),
    domaine(beaux_arts),
    adresse('Tanger'),
    description('Formation en arts plastiques'),
    sections(['art', 'design_publicitaire', 'bande_dessinee']),
    duree_formation(4),
    email('concoursinba2025@gmail.com')).

institution(esba, nom('École Supérieure des Beaux-Arts'),
    type(ecole_superieure),
    domaine(beaux_arts),
    adresse('Casablanca'),
    description('Formation en arts et design'),
    specialisations(['design_interieur', 'design_publicitaire', 'arts_plastiques']),
    duree_formation(4),
    email('esba.casablanca@gmail.com')).

% Écoles de Design et Arts Appliqués
institution(ensad, nom('École Nationale Supérieure d\'Arts et de Design'),
    type(ecole_superieure),
    domaine(arts_design),
    adresse('Casablanca'),
    description('Formation supérieure en arts et design'),
    specialisations(['design_graphique', 'design_digital', 'photographie']),
    duree_formation(4),
    site('www.ensad.ma')).

institution(esith, nom('École Supérieure Textile et Habillement'),
    type(ecole_superieure),
    domaine(textile_mode),
    adresse('Casablanca'),
    description('Formation en textile et habillement'),
    specialisations(['production_vetements', 'developpement_vetements', 
                     'gestion_logistique', 'recherche_approvisionnement']),
    duree_formation(3),
    site('www.esith.ac.ma')).

% Académies d'Arts Traditionnel
institution(aat_casablanca, nom('Académie Traditionnelle Arts - Casablanca'),
    type(academie),
    domaine('arts_traditionnel'),
    adresse('Casablanca'),
    description('Formation aux métiers de l\'artisanat et arts traditionnels'),
    specialites(['calligraphie_arabe', 'calligraphie_fresco', 'arts_cuir']),
    age_requis(18, 30),
    site('www.aat.fmh.edu.ma'),
    email('aat.fmh2@gmail.com')).

% Institut de Tourisme
institution(isitt, nom('Institut Supérieur International du Tourisme'),
    type(institut),
    domaine(tourisme_hotellerie),
    adresse('Tangier, Fès'),
    description('Formation en tourisme et gestion hôtelière'),
    specialisations(['gestion_hotellerie_restauration', 'gestion_tourisme']),
    duree_formation(3),
    site('www.isitt.ma'),
    email('concours.isitt.ma')).

% Institut du Patrimoine
institution(insap_heritage, nom('Institut National des Sciences Archéologiques'),
    type(institut),
    domaine(patrimoine_culture),
    adresse('Fès'),
    description('Formation en archéologie et sciences du patrimoine'),
    sections(['archéologie', 'anthropologie', 'ethnographie']),
    duree_formation(3),
    site('insap.ac.ma')).

% ============================================================================
% 2. CRITÈRES D'ADMISSION ET RÉGLEMENTATION
% ============================================================================

% Conditions générales d'admission
condition_admission(diplome_requis(baccalaureat)).
condition_admission(limite_age(25)) :- 
    contexte(concours_admission_general).

condition_admission(note_bac_minimum(14, 20)).

% Exigences générales pour les concours
exigence_concours(identite_officielle).
exigence_concours(certificat_scolarite).
exigence_concours(dossier_administratif).

% Dossier de candidature
dossier_candidature(element(certificat_baccalaureat_original)).
dossier_candidature(element(copie_cni_attestation)).
dossier_candidature(element(photo_recente)).
dossier_candidature(element(releve_notes_baccalaureat)).
dossier_candidature(element(relevance_notes_enseignement_secondaire)).

% ============================================================================
% 3. PROCESSUS ET MODALITÉS TESTS D'ADMISSION
% ============================================================================

% Test écrit général
test(test_ecrit_general,
    matiere('Culture générale'),
    duree(heures(1)),
    coefficient(2),
    format(qcm)).

test(test_ecrit_general,
    matiere('Questions civisme'),
    duree(minutes(15)),
    coefficient(4),
    langue(francais)).

% Test spécialisé selon l'institution
test_specialise(institution(isic),
    matiere('Langue française'),
    duree(heures(1, 30)),
    coefficient(2)).

test_specialise(institution(isic),
    matiere('Langue étrangère'),
    duree(heures(1, 30)),
    coefficient(1)).

test_specialise(institution(insap),
    matiere('Traduction arabe-français'),
    duree(heures(1, 30)),
    coefficient(2)).

test_specialise(institution(insap),
    matiere('Langue étrangère'),
    duree(heures(1, 30)),
    coefficient(1)).

test_specialise(institution(insap),
    matiere('Psychologie-technique'),
    duree(heures(1, 30)),
    coefficient(2)).

% Test de compétence artistique
test_artistic(inba,
    composante('Examen dessin'),
    duree(heures(2)),
    points_requis(30, 60)).

test_artistic(inba,
    composante('Examen peinture'),
    duree(heures(2)),
    points_requis(30, 60)).

test_artistic(inba,
    composante('Portfolio artistique'),
    presentation(numerique(usb))).

% Examen oral
examen_oral(institution(general),
    langue(francais),
    duree(minutes(15)),
    contenu('Culture générale et vie quotidienne'),
    evaluateurs(ensemble_jury)).

% ============================================================================
% 4. SPÉCIALISATIONS PAR INSTITUTION
% ============================================================================

specialisation(isic, diplome(licence_communication),
    parcours(['journalisme', 'relations_publiques', 'audiovisuel']),
    domaine_competence('Communication et médias')).

specialisation(ismac, diplome(licence_cinema),
    parcours(['direction_cinematographique', 'production', 
              'montage_son', 'direction_photographie', 'script']),
    domaine('Cinéma et audiovisuel')).

specialisation(inba, diplome(beaux_arts),
    departements(['art', 'design_publicitaire', 'bande_dessinee']),
    annees_etudes(4)).

specialisation(esba, diplome(beaux_arts),
    departements(['design_interieur', 'design_publicitaire', 'arts_plastiques']),
    passage_palier_selection(phase(1, 60)),
    passage_palier_final(phase(2, 40))).

specialisation(aat_casablanca, domaine(arts_traditionnel),
    cursus(['cursus1_calligraphie', 'cursus2_arts_decoratifs']),
    validation(test_ecrit(arabe_francais), test_pratique, portfolio(3))).

specialisation(isitt, diplome(tourisme),
    parcours(['gestion_hotellerie', 'gestion_tourisme']),
    duree(3)).

specialisation(esith, diplome(textile),
    specialites(['production_vetements', 'developpement_vetements', 
                 'gestion_logistique', 'gestion_approvisionnement']),
    duree(3)).

% ============================================================================
% 5. CRITÈRES DE SÉLECTION ET BARÈMES
% ============================================================================

critere_selection(moyenne_baccalaureat_minimum, 14/20).

critere_selection(moyennes_evaluees(
    examen_national: '75%',
    examen_regional: '25%'
)).

% Barème spécifique pour les formations technologiques
bareme_selection(cpge,
    priorite('Filière demandée'),
    pourcentage_acceptation(90, ['Filière scientifique'])).

bareme_selection(formationArtistique,
    note_mini_dessin(20, 80),
    note_mini_peinture(20, 80),
    score_total_requis(40, 160, 'accepté')).

% ============================================================================
% 6. CALENDRIER ET PROCÉDURES
% ============================================================================

% Phases de admission
phase_admission(phase(1, 'Inscription en ligne'),
    plateforme('e-services gouvernementaux')).

phase_admission(phase(2, 'Examens écrits'),
    contexte('Sélection initiale par résultats BAC')).

phase_admission(phase(3, 'Examens spécialisés'),
    description('Tests de compétence institution-spécifique')).

phase_admission(phase(4, 'Examens oraux'),
    description('Entretien pour finaliser la sélection')).

phase_admission(phase(5, 'Listes d\'admission finale'),
    source('Website institution'),
    format(numerique)).

% Calendrier des inscriptions
periode(inscription_en_ligne, debut(date(2026, 1, 15)), fin(date(2026, 2, 28))).
periode(examens_admission, debut(date(2026, 3, 15)), fin(date(2026, 4, 30))).
periode(resultats, debut(date(2026, 5, 1)), fin(date(2026, 5, 15))).

% ============================================================================
% 7. TYPES DE FORMATIONS POST-BACCALAURÉAT
% ============================================================================

type_formation(licence, duree_annees(3), diplome(baccaloureat_specialise)).
type_formation(cpge, duree_annees(2), diplome(baccalaureat_technique)).
type_formation(bts, duree_annees(2), diplome('diplôme technique supérieur')).
type_formation(master, duree_annees(2), prerequis(licence)).
type_formation(cycle_ingenieur, duree_annees(3), prerequis(cpge)).

% ============================================================================
% 8. SECTEURS PROFESSIONNELS
% ============================================================================

secteur_professionnel('Arts et Médias',
    metiers(['graphiste', 'designer', 'journaliste', 'cinéaste']),
    formations([isic, ismac, inba, esba])).

secteur_professionnel('Textile et Mode',
    metiers(['créateur_mode', 'gestionnaire_production', 'contrôleur_qualité']),
    formations([esith])).

secteur_professionnel('Tourisme et Hôtellerie',
    metiers(['hôtelier', 'guide_touristique', 'gestionnaire_événements']),
    formations([isitt])).

secteur_professionnel('Patrimoine et Culture',
    metiers(['archéologue', 'conservateur', 'expert_patrimoine']),
    formations([insap_heritage])).

% ============================================================================
% 9. EXIGENCES LINGUISTIQUES
% ============================================================================

exigence_langue(institution(general),
    langue(arabe_classique), niveau(intermediaire)).

exigence_langue(institution(general),
    langue(francais), niveau(intermediaire)).

exigence_langue(institution(isic),
    langue(francais), niveau(avance)).

exigence_langue(institution(international),
    langue(anglais), niveau(intermediaire)).

% ============================================================================
% 10. DOCUMENTS À FOURNIR - CHECKLIST
% ============================================================================

document_requis(certificat_baccalaureat_original,
    type(officiel),
    traduit_si_etranger(oui)).

document_requis(photocopie_cni,
    type(photocopie_certifiee),
    recto_verso(oui)).

document_requis(photo_identite,
    format('3x4 ou 4x6'),
    nombre(1),
    date_recente(moins_6_mois)).

document_requis(releve_notes_complet,
    source(examen_bac_national),
    necessite_attestation(oui)).

document_requis(certificat_scolarite,
    pour(institutions([cpge, bts])),
    delivre_par(etablissement_secondaire)).

% ============================================================================
% 11. CONDITIONS DE FINANCEMENT ET BOURSES
% ============================================================================

frais_inscription(montant(500, dirham),
    pour(tous_candidats)).

frais_formation_annual(montant(25000, dirham),
    divisible_en_2_versements,
    premier_versement(12500),
    deuxieme_versement(12500, epoque(janvier))).

aide_financiere(bourse_partielle,
    condition(etudiant_meritant),
    reduction(50, pourcent)).

% ============================================================================
% 12. PARCOURS PÉDAGOGIQUES DÉTAILLÉS
% ============================================================================

% Parcours ISIC - Communication et Médias
cours_semestre(isic, semestre(1),
    matieres([
        'Théorie de la communication',
        'Techniques de rédaction',
        'Histoire des médias',
        'Cultures audiovisuelles'
    ])).

cours_semestre(isic, semestre(3),
    formation_pratique('Stage en entreprise média')).

projet_annuel(isic,
    an(1),
    description('Création micro-project audiovisuels'),
    evaluation(groupe)).

projet_annuel(isic,
    an(3),
    description('Projet professionnel en contexte réel'),
    evaluation(individuel)).

% ============================================================================
% 13. PERSPECTIVES DE CARRIÈRE
% ============================================================================

carriere_possible(domaine(communication),
    metiers_accessibles([
        'Journaliste',
        'Producteur audiovisuel',
        'Community manager',
        'Chargé relations publiques',
        'Directeur communication'
    ]),
    secteurs_emploi([
        'Médias publics',
        'Médias privés',
        'Entreprises',
        'ONG',
        'Secteur public'
    ]),
    salaire_debut(range(12000, 18000, dirham))).

carriere_possible(domaine(arts_design),
    metiers_accessibles([
        'Graphiste',
        'Designer industriel',
        'Directeur artistique',
        'Illustrateur'
    ]),
    secteurs_emploi([
        'Agences créatives',
        'Industrie',
        'Publishing',
        'Secteur numérique'
    ]),
    salaire_debut(range(10000, 16000, dirham))).

% ============================================================================
% 14. RÈGLES DE LOGIQUE PROLOG
% ============================================================================

% Règle: Vérifier l'éligibilité à une institution
peut_postuler(Personne, _Institution) :-
    etudiant(Personne),
    diplome(Personne, baccalaureat),
    age(Personne, Age),
    Age >= 17,
    Age =< 25,
    moyenne_bac(Personne, Moyenne),
    Moyenne >= 14.

% Règle: Déterminer le parcours recommandé
parcours_recommande(Personne, Institution, Specialisation) :-
    profil(Personne, Profil),
    interet_principal(Personne, Domaine),
    specialisation(Institution, _, _, domaine(Domaine)),
    correspond_aux_competences(Profil, Specialisation).

% Règle: Vérifier l'accomplissement dossier
dossier_valide(Personne) :-
    forall(document_requis(Doc, _, _, _), 
           fourni(Personne, Doc)),
    \+ non_conforme(Personne, _).

% Règle: Calculer la note finale
note_finale(Personne, Institution, Note) :-
    note_ecrit(Personne, NE),
    note_specialise(Personne, Institution, NS),
    note_oral(Personne, NO),
    Note is (NE * 0.3) + (NS * 0.4) + (NO * 0.3).

% Règle: Vérifier l'admission
admis(Personne, Institution) :-
    note_finale(Personne, Institution, Note),
    Note >= 40,
    dossier_valide(Personne).

% ============================================================================
% 15. CONTACTS ET RESSOURCES
% ============================================================================

contact(isic, telephone('+212 5377 72789')).
contact(isic, site('www.isic.ac.ma')).
contact(ismac, site('www.ismac.ac.ma')).
contact(inba, email('concoursinba2025@gmail.com')).
contact(esba, email('esba.casablanca@gmail.com')).
contact(esith, site('www.esith.ac.ma')).
contact(aat_casablanca, email('aat.fmh2@gmail.com')).
contact(isitt, site('www.isitt.ma')).

% ============================================================================
% 16. PLATEFORMES NUMÉRIQUES D'INSCRIPTION
% ============================================================================

plateforme_inscription(e_services,
    url('www.concours.dgsn.gov.ma'),
    type(officielle)).

plateforme_inscription(massarservice,
    url('massarservice.men.gov.ma/moutamadris'),
    type(nationale)).

plateforme_inscription(cpge,
    url('www.cpge.ac.ma'),
    type(formation)).

plateforme_inscription(cursussup,
    url('www.cursussup.gov.ma'),
    type(placement)).

% ============================================================================
% FIN BASE DE CONNAISSANCES ORIENTATION POST-BAC
% ============================================================================

% ============================================================================
% Règles d'Inférence Avancées - Base Orientation Post-Baccalauréat
% Fichier complémentaire: inference_rules.pl
% ============================================================================

% ============================================================================
% SECTION 1: RÈGLES DE RECOMMANDATION PERSONNALISÉE
% ============================================================================

% Recommander une institution basée sur le profil
recommander_institution(Profil, Institution, Score) :-
    evaluator_profil(Profil, _Scores),
    institution(Institution, _, _, _, _, _, _),
    calculate_match_score(Profil, Institution, Score),
    Score > 65.

% Évaluer les compétences du profil
evaluator_profil(profil(_Domaine, _Langues, Competences), Scores) :-
    findall(Score, competence_score(Competences, Score), Scores).

% Calculer le score de correspondance
calculate_match_score(Profil, Institution, FinalScore) :-
    profil(Personne, Profil),
    interet(Personne, Domaine),
    institution(Institution, _, _, domaine(D), _, _, _),
    score_domaine(Domaine, D, DScore),
    score_langues(Profil, Institution, LScore),
    FinalScore is (DScore * 0.5) + (LScore * 0.3).

% ============================================================================
% SECTION 2: RÈGLES DE PRÉREQUISITION
% ============================================================================

% Vérifier les prerequis complets
verifie_prerequis(Personne, Cursus) :-
    prerequis_cursus(Cursus, RequiredCourses),
    forall(member(Course, RequiredCourses),
           cours_suivi(Personne, Course)).

% Chemin de progression académique
progression_possible(Année1, Année2) :-
    niveau_academique(Année1, N1),
    niveau_academique(Année2, N2),
    N2 > N1,
    coherence_parcours(Année1, Année2).

% Parcours parallèles autorisés
parcours_parallele(Licence, Master) :-
    domaine(Licence, D),
    domaine(Master, D),
    duree_formation(Licence, Dur1),
    duree_formation(Master, Dur2),
    DurTotal is Dur1 + Dur2,
    DurTotal =< 6.

% ============================================================================
% SECTION 3: RÈGLES D'ADMISSION ET SÉLECTION
% ============================================================================

% Vérifier l'éligibilité complète
eligible(Personne, Institution) :-
    % Vérifier le diplôme
    diplome(Personne, baccalaureat),
    
    % Vérifier l'âge
    age(Personne, Age),
    age_compatible(Institution, Age),
    
    % Vérifier les notes
    moyenne_generale(Personne, Moyenne),
    note_minimum(Institution, MinNota),
    Moyenne >= MinNota,
    
    % Vérifier les documents
    documents_complets(Personne),
    
    % Vérifier les conditions spécifiques
    conditions_specifiques(Institution, Personne).

% Déterminer la catégorie de candidat
categorie_candidat(Personne, Catégorie) :-
    age(Personne, Age),
    (Age < 20 -> Catégorie = 'Jeune candidat';
     Age < 25 -> Catégorie = 'Candidat standard';
     Catégorie = 'Candidat senior').

% Score d'admission prévisible
score_admission_previsionnel(Personne, Institution, ScoreTotal) :-
    note_ecrit(Personne, NoteEcrit),
    note_orale(Personne, NoteOrale),
    note_pratique(Personne, Institution, NotePratique),
    coefficient_ecrit(Institution, CoeffE),
    coefficient_oral(Institution, CoeffO),
    coefficient_pratique(Institution, CoeffP),
    ScoreBrut is (NoteEcrit * CoeffE + NoteOrale * CoeffO + NotePratique * CoeffP),
    SommCoeff is CoeffE + CoeffO + CoeffP,
    ScoreTotal is ScoreBrut / SommCoeff.

% ============================================================================
% SECTION 4: RÈGLES DE CALCUL ET STATISTIQUES
% ============================================================================

% Moyenne pondérée du baccalauréat
moyenne_bac_ponderee(Personne, MoyenneFinal) :-
    matiere_bac(Personne, _Matiere, Note, Coefficient),
    findall(Note*Coefficient, matiere_bac(Personne, _, Note, Coefficient), Produits),
    sumlist(Produits, SommeProduits),
    findall(Coefficient, matiere_bac(Personne, _, _, Coefficient), Coeff),
    sumlist(Coeff, SommeCoeff),
    MoyenneFinal is SommeProduits / SommeCoeff.

% Taux de réussite prévisible
taux_reussite(Institution, TauxReussite) :-
    candidats_acceptes(Institution, Acceptes),
    candidats_totaux(Institution, Total),
    TauxReussite is (Acceptes / Total) * 100.

% Projection salariale basée sur le diplôme
projection_salaire(Domaine, AnneeExperience, SalairePrevisionnel) :-
    salaire_initial(Domaine, SalaireInit),
    coefficient_progression(Domaine, Coeff),
    SalairePrevisionnel is SalaireInit * (1 + Coeff)^AnneeExperience.

% ============================================================================
% SECTION 5: RÈGLES DE PLANIFICATION ET ORIENTATION
% ============================================================================

% Planifier le cursus optimal
cursus_optimal(Personne, ListeCours, CheminProgressif) :-
    profil(Personne, _Profil),
    objectif(Personne, Objectif),
    institution_cible(Objectif, _InstCible),
    findall(Cours, cours_pertinent(Objectif, Cours), ListeCours),
    ordonner_par_prerequis(ListeCours, CheminProgressif).

% Plan de préparation personnalisé
plan_preparation(_Personne, Institution, Schedule) :-
    examens_requis(Institution, _Exams),
    findall(tache(Exam, Preparation, Deadline),
            preparation_exam(Exam, Preparation, Deadline),
            Schedule).

% Analyser les forces et faiblesses
analyse_profil(Personne, Rapport) :-
    competences(Personne, Comps),
    faiblesses(Personne, Faib),
    opportunites(Personne, Opp),
    menaces(Personne, Men),
    Rapport = rapport(Comps, Faib, Opp, Men).

% ============================================================================
% SECTION 6: RÈGLES DE COMPATIBILITÉ ET PROXIMITÉ
% ============================================================================

% Vérifier la compatibilité domaine-personne
compatible_domaine(Personne, Domaine) :-
    competences(Personne, Competences),
    domaine(Domaine, RequiredComps),
    intersection(Competences, RequiredComps, Common),
    length(Common, N),
    length(RequiredComps, Total),
    pourcentage(N, Total, Percent),
    Percent >= 70.

% Calculer la similarité entre deux institutions
similarite_institutions(Inst1, Inst2, Score) :-
    institution(Inst1, _, _, domaine(D1), _, _, _),
    institution(Inst2, _, _, domaine(D2), _, _, _),
    domaines_similar(D1, D2, ScoreDomain),
    formations_similaires(Inst1, Inst2, ScoreForm),
    Score is (ScoreDomain + ScoreForm) / 2.

% Distance géographique (pour critère de proximité)
distance_institution(Personne, Institution, Distance) :-
    localisation(Personne, Lieu),
    institution(Institution, _, _, _, adresse(Adresse), _, _),
    calcul_distance(Lieu, Adresse, Distance).

% ============================================================================
% SECTION 7: RÈGLES DE VALIDITÉ ET CONFORMITÉ
% ============================================================================

% Vérifier la validité d'un dossier complet
est_dossier_complet(Personne, Institution) :-
    % Documents obligatoires
    documents_obligatoires(Institution, Docs),
    forall(member(Doc, Docs), fourni_par(Personne, Doc)),
    
    % Documents valides
    forall(fourni_par(Personne, Doc), document_valide(Doc, Personne)),
    
    % Dates respectées
    respecte_calendrier(Personne),
    
    % Cohérence du dossier
    coherence_dossier(Personne).

% Vérifier la plausibilité des notes
plausibilite_notes(Personne) :-
    note_ecrit(Personne, NE),
    note_oral(Personne, NO),
    note_pratique(Personne, NP),
    between(0, 100, NE),
    between(0, 100, NO),
    between(0, 100, NP),
    covariance_notes(NE, NO, NP, Corr),
    Corr < 0.95.  % Pas de corrélation parfaite (suspicion)

% ============================================================================
% SECTION 8: DÉDUCTIONS ET INFÉRENCES COMPLEXES
% ============================================================================

% Prédire la réussite académique
prediction_reussite(Personne, Institution, Probabilite) :-
    score_admission(Personne, Institution, Score),
    (Score >= 75 -> BaseProbability = 0.95;
     Score >= 60 -> BaseProbability = 0.75;
     Score >= 45 -> BaseProbability = 0.50;
     BaseProbability = 0.25),
    
    % Facteur d'adaptation
    facteur_adaptation(Personne, Institution, FA),
    
    % Facteur de motivation
    facteur_motivation(Personne, FM),
    
    Probabilite is BaseProbability * FA * FM.

% Déterminer le mode de financement
mode_financement_optimal(Personne, Financement) :-
    revenu_famille(Personne, Revenu),
    (Revenu < 50000 -> Financement = 'Bourse intégrale';
     Revenu < 100000 -> Financement = 'Bourse partielle';
     Financement = 'Autofinancé').

% Tracer le parcours professionnel probable
parcours_professionnel_previsionnel(Personne, Institution, Parcours) :-
    specialisation(Institution, _, Specialisations, _),
    member(Spec, Specialisations),
    competences_spec(Spec, CompetencesRequises),
    competences(Personne, CompetencesActuelles),
    gain_competences(CompetencesRequises, CompetencesActuelles, Gain),
    metiers_accessibles_apres(Spec, Metiers),
    Parcours = [Spec, Metiers, Gain].

% ============================================================================
% SECTION 9: RÈGLES DE GROUPE COHÉSION CLASSE
% ============================================================================

% Recommander une classe hétérogène
equilibre_classe(Institution, ListeEtudiants) :-
    findall(Etudiant, 
            (admis(Etudiant, Institution),
             competences(Etudiant, _Comp),
             moyenne_generale(Etudiant, _Moy)),
            Tous),
    
    % Sélectionner pour équilibre
    % Top 30%, Moyen 40%, Nécessitant soutien 30%
    length(Tous, Total),
    TopCount is floor(Total * 0.30),
    MidCount is floor(Total * 0.40),
    
    split_by_performance(Tous, Top, Mid, Bottom),
    length(Top, TopCount),
    length(Mid, MidCount),
    
    append(Top, Mid, Premiers),
    append(Premiers, Bottom, ListeEtudiants).

% ============================================================================
% SECTION 10: REQUÊTES UTILES POUR L'IA
% ============================================================================

% Requête: Quelles institutions acceptent un candidat?
institutions_accessibles(Personne, Institutions) :-
    findall(Inst, eligible(Personne, Inst), Institutions).

% Requête: Quel est le cursus recommandé?
cursus_recommande(Personne, Institution, Specialisation) :-
    profil(Personne, _Profil),
    interet_principal(Personne, Domaine),
    institution(Institution, _, _, domaine(Domaine), _, _, _),
    specialisation(Institution, _, Specialisation, _),
    compatible_domaine(Personne, Domaine).

% Requête: Quels sont les examens à passer?
examens_concernant(_Personne, Institution, ListeExamens) :-
    institution(Institution, _, _, _, _, _, _),
    test(_, _, _, _, _),
    findall(Exam, test_pour_institution(Institution, Exam), ListeExamens).

% Requête: Quelle est la probabilité d'admission?
probabilite_admission(Personne, Institution, Probabilite) :-
    prediction_reussite(Personne, Institution, Probabilite).

% Requête: Quels métiers après cette formation?
metiers_apres(Institution, Specialisation, Metiers) :-
    specialisation(Institution, _, Specialisation, _),
    findall(M, metier_accessible(Specialisation, M), Metiers).

% ============================================================================
% FIN - RÈGLES D'INFÉRENCE
% ============================================================================

% ============================================================================
% Fichier d'Intégration - YAFI avec Base Orientation Post-Bac
% Mode d'emploi et mappings question-réponse
% ============================================================================

% ============================================================================
% SECTION 1: CHARGEMENT DES BASES DE CONNAISSANCE
% ============================================================================

% Charger les fichier basis Prolog



% ============================================================================
% SECTION 2: DÉCLENCHEURS DE RÈGLES PAR TYPE DE QUESTION
% ============================================================================

% Type: Question d'Orientation Générale
regle_orientation(Q, R) :-
    atom_string(Q, StringQ),
    (string_contains(StringQ, 'institution') ->
        trouver_institution_recommandee(R);
     string_contains(StringQ, 'cursus') ->
        trouver_cursus_optimal(R);
     string_contains(StringQ, 'specialisation') ->
        lister_specialisations(R);
     string_contains(StringQ, 'admission') ->
        expliquer_admission(R)).

% Type: Question d'Admissibilité
regle_admissibilite(Profil, Institution, Response) :-
    eligible(Profil, Institution),
    format(atom(Response), 
           'Vous êtes éligible à ~w. Conditions: Baccalauréat requis, âge 17-25, moyenne >= 14/20',
           [Institution]).

% Type: Question de Sélection
regle_selection(Personne, Institution, Score) :-
    score_admission_previsionnel(Personne, Institution, Score),
    (Score >= 75 -> _Verdict = 'Très bon potentiel';
     Score >= 60 -> _Verdict = 'Bon potentiel';
     Score >= 45 -> _Verdict = 'Potentiel acceptable';
     _Verdict = 'Révision recommandée').

% Type: Question de Procédures
regle_procedure(Q, Steps) :-
    atom_string(Q, StringQ),
    (string_contains(StringQ, 'inscription') ->
        Steps = ['Se connecter à la plateforme', 
                 'Remplir le formulaire',
                 'Télécharger les documents',
                 'Soumettre le dossier'];
     string_contains(StringQ, 'examen') ->
        Steps = ['Consulter le calendrier',
                 'Se préparer',
                 'Se présenter le jour',
                 'Consulter les résultats'];
     string_contains(StringQ, 'dossier') ->
        Steps = ['Préparer les documents',
                 'Vérifier la complétude',
                 'Soumettre avant la deadline',
                 'Attendre confirmation']).

% ============================================================================
% SECTION 3: MAPPINGS QUESTIONS-RÉPONSES FRÉQUENTES
% ============================================================================

% FAQ Intégrée
reponse_faq('Comment m\'inscrire?',
    'Inscription en ligne via www.cursussup.gov.ma. Vous devez avoir votre baccalauréat et créer un compte utilisateur avec vos identifiants.').

reponse_faq('Quelles sont les conditions d\'admission?',
    'Vous devez: (1) Avoir le baccalauréat, (2) Avoir au minimum 14/20 de moyenne, (3) Être âgé de 17 à 25 ans, (4) Soumettre un dossier complet.').

reponse_faq('Quels documents dois-je fournir?',
    'Documents requis: Certificat original baccalauréat, Copie CIN, Photo récente, Relevé complet notes, Certificat scolarité (si nécessaire).').

reponse_faq('Quand sont les examens?',
    'Le calendrier dépend de l\'institution. Généralement: Inscriptions janvier-février, Examens mars-avril, Résultats mai.').

reponse_faq('Combien coûte l\'inscription?',
    'Frais inscription: 500 DH. Formation annuelle: 25 000 DH (divisible en 2 versements: 12 500 DH à l\'inscription, 12 500 DH en janvier).').

reponse_faq('Peut-on s\'inscrire à plusieurs institutions?',
    'Oui, vous pouvez postuler à plusieurs institutions. Vous devez mettre à jour votre dossier pour chaque candidature.').

reponse_faq('Comment fonctionne le système de points?',
    'Les points sont généralement: Examen écrit (30%), Test spécialisé (40%), Examen oral (30%). Total minimum pour admission: souvent 40/80.').

reponse_faq('Y a-t-il des bourses?',
    'Oui, bourses partielles pour étudiants méritants. Conditions basées sur les résultats académiques et la situation financière.').

reponse_faq('Qu\'est-ce qu\'une CPGE?',
    'Classes Préparatoires aux Grandes Écoles (CPGE). Formation 2 ans après BAC pour préparer l\'accès aux écoles d\'ingénieurs et de commerce.').

reponse_faq('Quelle est la différence entre BTS et Licence?',
    'BTS: 2 ans, diplôme technique, accent pratique. Licence: 3 ans, diplôme académique, accent théorique + pratique.').

% ============================================================================
% SECTION 4: GÉNÉRATEUR DE RÉPONSES CONTEXTUELLES
% ============================================================================

% Répondre basé sur le constexte de l'utilisateur
generer_reponse(Contexte, Question, Réponse) :-
    determine_sujet(Question, Sujet),
    obtenez_infos_contexte(Contexte, Profil),
    (Sujet = orientation ->
        recommander_avec_profil(Profil, Réponse);
     Sujet = admission ->
        evaluer_admissibilite_avec_profil(Profil, Réponse);
     Sujet = procedures ->
        expliquer_procedures(Réponse);
     generer_reponse_generique(Question, Réponse)).

% Déterminer le sujet d'une question
determine_sujet(Question, Sujet) :-
    atom_string(Question, Str),
    (string_contains(Str, 'cursus|orientation|domaine|specialite|diplôme') ->
        Sujet = orientation;
     string_contains(Str, 'admission|eligible|condition|quorum|note') ->
        Sujet = admission;
     string_contains(Str, 'inscription|process|dossier|examen|procedure') ->
        Sujet = procedures;
     string_contains(Str, 'metier|emploi|salaire|carriere') ->
        Sujet = carriere;
     Sujet = general).

% ============================================================================
% SECTION 5: RECOMMANDATIONS INTELLIGENTES
% ============================================================================

% Recommandation basée sur le profil
recommandation_adaptee(Personne, ListeRecommandations) :-
    profil(Personne, Profil),
    competences(Personne, _Comps),
    interets(Personne, _Interets),
    
    % Trouver les institutions compatibles
    findall(Inst-Score,
            (institution(Inst, _, _, _, _, _, _),
             compatible_domaine(Personne, _),
             calculate_match_score(Profil, Inst, Score),
             Score > 65),
            Paires),
    
    % Trier par score
    sort(2, @>=, Paires, Sorted),
    
    % Formater les recommandations
    format_recommandations(Sorted, 3, ListeRecommandations).

% Générer un plan d'action personnalisé
plan_action(Personne, Institution, Action) :-
    findall(Étape,
            action_step(Personne, Institution, Étape),
            Actions),
    Action = plan_detaille(Actions).

action_step(Personne, Institution, 'Vérifier l\'éligibilité') :-
    eligible(Personne, Institution).

action_step(_Personne, Institution, 'Préparer les documents') :-
    documents_obligatoires(Institution, _).

action_step(_Personne, Institution, 'S\'entraîner aux examens') :-
    examens_requis(Institution, _).

action_step(_Personne, Institution, 'Pratiquer l\'interview') :-
    test_oral_requis(Institution).

% ============================================================================
% SECTION 6: TRAITEMENT DES EXCEPTIONS
% ============================================================================

% Gestion des cas limites d'admission
cas_special_admission(Personne, _Institution, ManipulationSpeciale) :-
    % Cas 1: Note limite
    (moyenne_generale(Personne, M),
     M >= 13.5, M < 14 ->
        ManipulationSpeciale = 'Peut demander révision / circonstances atténuantes';
     
     % Cas 2: Dossier incomplet mais reçu à temps
     documents_non_complets(Personne) ->
        ManipulationSpeciale = 'Demander au secrétariat les documents manquants';
     
     % Cas 3: Limite d'âge
     age(Personne, Age),
     Age > 25 ->
        ManipulationSpeciale = 'Consulter pour cas limite d\'âge';
     
     ManipulationSpeciale = 'Cas standard').

% ============================================================================
% SECTION 7: PRÉDICATS HELPER
% ============================================================================

% Vérifier si une chaîne contient une sous-chaîne
string_contains(String, Pattern) :-
    atom_string(Pattern, PatternStr),
    sub_string(String, _, _, _, PatternStr), !.

% Formater des recommandations
format_recommandations([], _, []).
format_recommandations(_, Max, []) :- Max =< 0.
format_recommandations([Inst-Score|Rest], Max, 
                       [rec(Inst, Score, Desc)|ResiRecs]) :-
    Max > 0,
    institution(Inst, nom(_Nom), _, _, _, _, _),
    format(atom(Desc), 'Score de correspondance: ~1f%', [Score]),
    Max1 is Max - 1,
    format_recommandations(Rest, Max1, ResiRecs).

% Obtenir des infos du contexte utilisateur
obtenez_infos_contexte(contexte(Donnees), Profil) :-
    extract_profile(Donnees, Profil).

% ============================================================================
% SECTION 8: INTÉGRATION AVEC SYSTÈME YAFI
% ============================================================================

% Interface pour YAFI
%query_yafi_orientation(Question, Réponse) :-
%    regle_orientation(Question, Réponse), !.
%
%query_yafi_orientation(Question, Réponse) :-
%    reponse_faq(Question, Réponse), !.
%
%query_yafi_orientation(_, 'Je ne dispose pas d\'information spécifique à ce sujet. Consultez www.cursussup.gov.ma ou contactez directement l\'institution.').

% ============================================================================
% SECTION 9: EXEMPLES DE REQUÊTES
% ============================================================================

% Exemple: Qui peut entrer à ISIC?
exemple(1) :-
    write('Candidats éligibles à ISIC:'), nl,
    findall(P, eligible(P, isic), Candidats),
    forall(member(C, Candidats), (write(' - '), write(C), nl)).

% Exemple: Quel cursus pour Jean?
exemple(2) :-
    write('Cursus recommandé pour Jean:'), nl,
    cursus_recommande(jean, Institution, Specialisation),
    write('Institution: '), write(Institution), nl,
    write('Spécialisation: '), write(Specialisation), nl.

% Exemple: Taux d'admission ISMAC?
exemple(3) :-
    write('Statistiques ISMAC:'), nl,
    taux_reussite(ismac, Taux),
    format('Taux de réussite: ~1f%~n', [Taux]).

% ============================================================================
% SECTION 10: NOTES D'UTILISATION POUR YAFI
% ============================================================================

% Cette base de connaissances peut être interrogée de plusieurs façons:
%
% 1. ORIENTATION SIMPLE
%    ?- reponse_faq('Comment m\'inscrire?', R).
%
% 2. VÉRIFICATION ÉLIGIBILITÉ
%    ?- eligible(jean, isic).
%
% 3. RECOMMANDATIONS PERSONNALISÉES
%    ?- recommandation_adaptee(marie, Recs).
%
% 4. PARCOURS PROFESSIONNEL
%    ?- parcours_professionnel_previsionnel(ahmed, esba, Parcours).
%
% 5. PROBABILITÉ D'ADMISSION
%    ?- prediction_reussite(fatima, inba, P).
%
% 6. LISTE EXAMENS
%    ?- examens_concernant(kevin, isit, Examens).
%
% 7. MÉTIERS ACCESSIBLES
%    ?- metiers_apres(ismac, specialisation_cinema, Metiers).
%
% 8. PLAN D'ACTION
%    ?- plan_action(sophie, esith, Plan).

% ============================================================================
% FIN - INTÉGRATION YAFI
% ============================================================================




% ============================================================================
% NOUVEAU MODULE 1: BAREME DECODER (Convertisseur de Notes et Percentiles)
% ============================================================================

% Seuils d'admission theoriques en percentiles (0-100)
bareme_percentile('EMSI', 50, 100).
bareme_percentile('UIR', 60, 100).
bareme_percentile('ENSA', 70, 100).
bareme_percentile('FMP', 80, 100).
bareme_percentile('FMD', 80, 100).
bareme_percentile('ENCG', 75, 100).
bareme_percentile('ISCAE', 85, 100).
bareme_percentile('FST', 60, 100).
bareme_percentile('Faculte des Sciences', 10, 100).

% Convertir une note sur 20 en percentile
note_vers_percentile(Note, Percentile) :-
    Note >= 0, Note =< 20,
    Percentile is (Note / 20) * 100.

% Trouver les institutions correspondant a une note
institutions_par_note(Note, Institutions) :-
    note_vers_percentile(Note, Percentile),
    findall(Inst, (bareme_percentile(Inst, Min, Max), Percentile >= Min, Percentile =< Max), InstitutionsMatch),
    list_to_set(InstitutionsMatch, Institutions).


% ============================================================================
% NOUVEAU MODULE 2: SCORING MULTI-CRITERES AVANCE
% ============================================================================

% Poids des criteres dans le score global
poids_critere(bac_match, 0.40).
poids_critere(budget, 0.30).
poids_critere(localisation, 0.30).

% Calcul du score d'adequation du Budget (0-100)
score_budget(Inst, BudgetEtudiant, Score) :-
    (frais_scolarite(Inst, _, _) -> 
        (BudgetEtudiant > 30000 -> Score = 100 ;
         bourse_merite(Inst, _, _) -> Score = 80 ;
         Score = 20)
    ; Score = 100). % Si public/gratuit, budget parfait

% Calcul du score de Localisation (0-100)
score_localisation(Inst, VilleEtudiant, Score) :-
    (etablissement(Inst, VilleEtudiant, _, _, _) -> Score = 100 ;
     Score = 50). % Si hors de la ville de l'etudiant

% Helper pour récupérer le domaine de manière flexible (Arity 8)
get_inst_domaine(Inst, Domaine) :-
    (   institution(Inst, _, _, domaine(Domaine), _, _, _, _)
    ;   institution(_, nom(Inst), _, domaine(Domaine), _, _, _, _)
    ), !.

% Score Global d'Orientation (0-100) - Version 6 arguments (Expert)
% calculer_score_orientation(Bac, Note, Budget, Ville, Inst, ScoreFinal)
calculer_score_orientation(Bac, Note, BudgetEtudiant, VilleEtudiant, Inst, ScoreFinal) :-
    % 1. Score BAC (Basé sur la note et l'appartenance de l'institution aux choix possibles)
    (institutions_par_note(Note, InstsValides), member(Inst, InstsValides) -> ScoreBase = 100 ; ScoreBase = 40),
    
    % 2. Bonus de Compatibilité (BAC vs DOMAINE)
    (
        get_inst_domaine(Inst, Domaine),
        check_compatibilite(Bac, Domaine, Statut, _)
    -> 
        (Statut = excellent -> BonusComp = 1.2 ; 
         Statut = possible -> BonusComp = 1.0 ;
         Statut = difficile -> BonusComp = 0.5 ;
         BonusComp = 0.1)
    ; 
        BonusComp = 1.0 % Par défaut
    ),
    
    ScoreBac is ScoreBase * BonusComp,

    % 3. Score Budget
    score_budget(Inst, BudgetEtudiant, S_Budget),
    
    % 4. Score Localisation
    score_localisation(Inst, VilleEtudiant, S_Localisation),
    
    % Ponderation
    poids_critere(bac_match, P_Bac),
    poids_critere(budget, P_Budget),
    poids_critere(localisation, P_Loc),
    
    RawScore is (ScoreBac * P_Bac) + (S_Budget * P_Budget) + (S_Localisation * P_Loc),
    % Clamp score between 0 and 100
    ScoreFinal is min(100, max(0, RawScore)).


% ============================================================================
% NOUVEAU MODULE 4: BASE DE DONNEES DES BOURSES ET AIDES (SCHOLARSHIPS)
% ============================================================================

% detail_bourse(Nom, Institution, TauxCouverture, Criteres, LienOuInfos)
detail_bourse('Bourse d''Excellence UIR', 'UIR', '100%', 'Mention Tres Bien au BAC (Moyenne > 16/20). Entretien obligatoire.', 'Sur dossier lors de l''inscription').
detail_bourse('Bourse Sociale UIR', 'UIR', '50-100%', 'Revenu familial limite. Necessite une enquete sociale.', 'Demande de bourse a remplir sur le site').
detail_bourse('Bourse Fondation OCP', 'UM6P', '100%', 'Excellence academique et boursier Minhaty.', 'Dossier specifique UM6P').
detail_bourse('Bourse d''Encouragement EMSI', 'EMSI', '20%', 'Pour les etudiants majors de leur promotion academique.', 'Automatique en fin d''annee').
detail_bourse('Minhaty (Bourse Etat)', 'Public (FST, ENSA, Fac)', '1000-1900 DH/Trimestre', 'Revenu des parents modeste (Seuil fixe par le ministere).', 'Inscription sur minhaty.ma en juin').
detail_bourse('Bourse AMCI', 'Internationaux', '750 DH/Mois', 'Etudiants hors Maroc, traites par l''Agence', 'Dossier diplomatique').

% Trouver les bourses accessibles pour un etudiant
bourses_accessibles(NoteBac, TypeEcole, ListeBourses) :-
    findall(Nom, 
            (detail_bourse(Nom, Inst, _Taux, Condition, _Info),
             (TypeEcole = Inst ; Inst = 'Public (FST, ENSA, Fac)'),
             (NoteBac >= 16 -> true ; \+ sub_string(Condition, _, _, _, 'Moyenne > 16/20'))
            ), ListeBoursesUniques),
    list_to_set(ListeBoursesUniques, ListeBourses).



% ======================================================================
% NOUVELLE BASE DE DONNEES SUPER-STRUCTUREE (GENEREE PAR INJECTION)
% ======================================================================
:- discontiguous nouvel_etablissement/2.
:- discontiguous info_etablissement/3.

nouvel_etablissement('ARM', 'MILITAIRE ET SÉCURITÉ').
info_etablissement('ARM', 'Présentation et Spécialités', 'Armée de Terre : Infanterie (Benguérir), Artillerie (Fès), Blindés (Meknès), etc..').
info_etablissement('ARM', 'Présentation et Spécialités', 'Armée de l''Air (ERA) : Spécialités techniques aéronautiques à Marrakech.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Avantages : Les élèves bénéficient de l''internat complet (hébergement, restauration, habillement) et perçoivent une solde mensuelle pendant leurs études.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Ce cycle forme les cadres de maîtrise des FAR dans diverses spécialités techniques et administratives. Contrairement au cycle des officiers, celui-ci est plus court et axé sur l''opérationnel.').
info_etablissement('ARM', 'Présentation et Spécialités', 'D''après les documents fournis, voici les informations concernant le cycle des Sous-Officiers des Forces Armées Royales (FAR) pour les spécialités navales et aéronautiques (ERA et ERN) :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Elles interviennent également pour porter secours à la population en cas de fléaux ou de catastrophes naturelles.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Elles travaillent en coordination avec d''autres services de sécurité comme la Sûreté Nationale, la Gendarmerie Royale et les Forces Armées Royales.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Femmes : 1,67 m.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Hommes : 1,73 m.').
info_etablissement('ARM', 'Présentation et Spécialités', 'L''Académie Royale Militaire est le noyau principal pour la formation des officiers des Forces Armées Royales (FAR). Elle propose une formation double, académique et militaire, pour les officiers de l''armée de terre, de la Gendarmerie Royale et des Forces Auxiliaires.').
info_etablissement('ARM', 'Présentation et Spécialités', 'L''Artillerie.').
info_etablissement('ARM', 'Présentation et Spécialités', 'L''Infanterie.').
info_etablissement('ARM', 'Présentation et Spécialités', 'La Santé Militaire (Infirmiers).').
info_etablissement('ARM', 'Présentation et Spécialités', 'Langue et Littérature Anglaises.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Le Génie Militaire.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Le Matériel et l''Intendance.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Le centre de formation est situé à Casablanca.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Le centre de formation est situé à Marrakech.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Le recrutement pour ces deux grades suit un parcours rigoureux :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Les Forces Auxiliaires sont un appareil de sécurité au Maroc opérant sous l''autorité du Ministre de l''Intérieur.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Les Gardiens de la Paix font partie des cadres de la Sûreté Nationale (DGSN). Ils sont chargés du maintien de l''ordre public, de la circulation, de la protection des personnes et des biens, et assurent des missions de proximité sur le terrain.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Les Transmissions.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Les commissaires constituent le cadre supérieur de la hiérarchie de la Sûreté Nationale. Ils sont chargés de la direction, de la conception et de la supervision des services de police.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Les officiers de police assurent des missions de commandement opérationnel, d''enquête et d''encadrement des brigadiers et gardiens de la paix.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Leur rôle principal est de maintenir l''ordre et la sécurité sur tout le territoire national.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Lieu de formation : Institut Royal de Police à Kénitra ou dans ses centres de formation (Bouknadel, Ifrane, Oujda, etc.).').
info_etablissement('ARM', 'Présentation et Spécialités', 'Lieu de formation : La formation se déroule à l''École de Formation des Cadres des Forces Auxiliaires de Ben Slimane.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Objectifs : Assurer la formation initiale et continue des sous-officiers de la Marine Royale et de pays partenaires.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Objectifs : Former les sous-officiers dans diverses spécialités techniques et militaires de l''armée de l''air.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Pour postuler à ce cycle, le candidat doit remplir les critères suivants :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Pour postuler à ce grade, le candidat doit remplir les critères suivants :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Pour postuler à l''ERA ou à l''ERN, le candidat doit :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Pour postuler à l''un des centres de formation des sous-officiers, il faut :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Pour postuler, le candidat doit remplir les critères suivants au 31 décembre 2025 :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Régime : Internat complet (formation militaire et policière).').
info_etablissement('ARM', 'Présentation et Spécialités', 'Régime : Internat complet (logement, nourriture et habillement gratuits).').
info_etablissement('ARM', 'Présentation et Spécialités', 'Rémunération : Les élèves sous-officiers perçoivent une solde (salaire) mensuelle durant leur formation.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Sciences Juridiques.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Sciences et Techniques.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Selon le domaine de spécialité (Infanterie, Artillerie, Génie, Transmissions, Santé Militaire, etc.), les candidats sont affectés dans différents centres :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Selon le schéma de votre document, les sous-officiers sont formés dans différents centres spécialisés (CIB, CPT, CIT, etc.) couvrant des domaines comme :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Spécialités : Fusiliers Marins (Mouchat Al Bahriya) ou Personnel Naviguant.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Spécialités : Énergie ou Opérations.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Spécialités mentionnées : Contrôleur aérien (pour les garçons uniquement), anglais, cuisine.').
info_etablissement('ARM', 'Présentation et Spécialités', 'Toutes les candidatures se font exclusivement sur le portail numérique de la DGSN :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Toutes les candidatures se font exclusivement via le portail officiel des recrutements des FAR :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Voici les informations concernant le recrutement des Élèves Gardiens de la Paix (Sûreté Nationale / DGSN) extraites de votre dernière capture d''écran :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Voici les informations concernant les Écoles de Formation des Sous-Officiers des Forces Armées Royales (FAR), extraites de votre dernière capture d''écran :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Voici les informations détaillées concernant le cycle des Sous-Officiers des Forces Auxiliaires (FA), extraites de votre dernière capture d''écran :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Voici les informations détaillées concernant le recrutement des Élèves Officiers de Police et des Élèves Commissaires de Police (Sûreté Nationale / DGSN), extraites de votre dernière capture d''écran :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Voici les informations détaillées concernant les Écoles Royales de l''Air (ERA) et l''École Royale Navale (ERN), basées sur votre document :').
info_etablissement('ARM', 'Présentation et Spécialités', 'Être apte physiquement.').
info_etablissement('ARM', 'Présentation et Spécialités', '1. Sous-Officiers de la Marine Royale (ERN)').
info_etablissement('ARM', 'Présentation et Spécialités', '2. École Royale Navale (ERN) - Casablanca').
info_etablissement('ARM', 'Présentation et Spécialités', '1. École Royale de l''Air (ERA) - Marrakech').
info_etablissement('ARM', 'Présentation et Spécialités', '2. Sous-Officiers des Forces Royales Air (ERA)').
info_etablissement('ARM', 'Présentation et Spécialités', 'Présentation du Cycle Sous-Officier').
info_etablissement('ARM', 'Présentation et Spécialités', 'Présentation du Cycle Sous-Officier (SRE)').
info_etablissement('ARM', 'Présentation et Spécialités', '1. Élèves Commissaires de Police').
info_etablissement('ARM', 'Présentation et Spécialités', 'Présentation de l''ARM').
info_etablissement('ARM', 'Présentation et Spécialités', 'Présentation et Missions').
info_etablissement('ARM', 'Présentation et Spécialités', '2. Élèves Officiers de Police').
info_etablissement('ARM', 'Présentation et Spécialités', 'Présentation et Missions').
info_etablissement('ARM', 'Présentation et Spécialités', 'Centres de Formation Mentionnés').
info_etablissement('ARM', 'Présentation et Spécialités', 'Spécialités et Centres de Formation').
info_etablissement('ARM', 'Conditions d''Accès', 'Acuité visuelle : Au moins 15/20 pour les deux yeux (sans correction par lunettes ou lentilles).').
info_etablissement('ARM', 'Conditions d''Accès', 'Aptitude physique : Jouir d''une bonne santé physique.').
info_etablissement('ARM', 'Conditions d''Accès', 'Avoir un casier judiciaire vierge et être apte physiquement.').
info_etablissement('ARM', 'Conditions d''Accès', 'Avoir un casier judiciaire vierge.').
info_etablissement('ARM', 'Conditions d''Accès', 'Baccalauréat : Être titulaire du Baccalauréat (toutes séries selon la spécialité) de l''année en cours ou de l''année précédente.').
info_etablissement('ARM', 'Conditions d''Accès', 'Baccalauréat : Être titulaire du Baccalauréat (toutes séries) ou d''un diplôme équivalent.').
info_etablissement('ARM', 'Conditions d''Accès', 'Baccalauréat : Être titulaire du Baccalauréat de l''année en cours ou des deux années précédentes.').
info_etablissement('ARM', 'Conditions d''Accès', 'Baccalauréat : Être titulaire du Baccalauréat de l''année en cours.').
info_etablissement('ARM', 'Conditions d''Accès', 'Casier judiciaire : Ne pas avoir d''antécédents judiciaires.').
info_etablissement('ARM', 'Conditions d''Accès', 'Casier judiciaire : Être de bonne moralité et n''avoir aucun antécédent judiciaire.').
info_etablissement('ARM', 'Conditions d''Accès', 'Classement final : Les candidats admis sont classés en fonction de leur moyenne générale au Baccalauréat.').
info_etablissement('ARM', 'Conditions d''Accès', 'Conditions d''accès : Être de nationalité marocaine, avoir un casier judiciaire vierge, et être titulaire d''un Baccalauréat de l''année en cours ou des deux années précédentes.').
info_etablissement('ARM', 'Conditions d''Accès', 'Conditions physiques : Acuité visuelle de 15/20 minimum pour les deux yeux (sans verres ni lentilles) et une bonne audition.').
info_etablissement('ARM', 'Conditions d''Accès', 'Conditions physiques : Identiques à celles des commissaires (vision et audition).').
info_etablissement('ARM', 'Conditions d''Accès', 'Conditions spécifiques : En plus des conditions générales (célibataire, 18-23 ans, bachelier des deux dernières années), le candidat doit être apte au service en mer.').
info_etablissement('ARM', 'Conditions d''Accès', 'Cycle Ingénieur (Bac Sciences Mathématiques) :').
info_etablissement('ARM', 'Conditions d''Accès', 'Cycle Licence (Bac Sciences Mathématiques ou Physiques) :').
info_etablissement('ARM', 'Conditions d''Accès', 'Diplôme requis : Diplôme d''études universitaires générales (DEUG) ou équivalent (Bac+2).').
info_etablissement('ARM', 'Conditions d''Accès', 'L''ERA forme les officiers des Forces Royales Air. Elle propose deux types de cursus pour les bacheliers :').
info_etablissement('ARM', 'Conditions d''Accès', 'L''ERN forme les officiers de la Marine Royale. Elle est réservée aux bacheliers en Sciences Mathématiques.').
info_etablissement('ARM', 'Conditions d''Accès', 'Nationalité : Être de nationalité marocaine.').
info_etablissement('ARM', 'Conditions d''Accès', 'Note importante : La taille minimale est très strictement contrôlée lors de la visite médicale initiale.').
info_etablissement('ARM', 'Conditions d''Accès', 'Note importante : Les candidats admis sont classés en fonction de leur moyenne obtenue au Baccalauréat.').
info_etablissement('ARM', 'Conditions d''Accès', 'Présélection : Basée sur la moyenne générale du Baccalauréat.').
info_etablissement('ARM', 'Conditions d''Accès', 'Présélection : Basée sur la moyenne obtenue au Baccalauréat avec la mention "Assez Bien" minimum (session ordinaire).').
info_etablissement('ARM', 'Conditions d''Accès', 'Présélection : Elle est basée sur la moyenne générale obtenue au Baccalauréat.').
info_etablissement('ARM', 'Conditions d''Accès', 'Présélection : Elle est effectuée sur la base de la moyenne générale obtenue au Baccalauréat.').
info_etablissement('ARM', 'Conditions d''Accès', 'Présélection : Elle se base sur la moyenne générale du Baccalauréat.').
info_etablissement('ARM', 'Conditions d''Accès', 'Présélection : Elle se base sur la moyenne obtenue au Baccalauréat avec, au minimum, la mention "Assez Bien" en session ordinaire.').
info_etablissement('ARM', 'Conditions d''Accès', 'Santé : Jouir d''une bonne aptitude physique.').
info_etablissement('ARM', 'Conditions d''Accès', 'Taille minimale :').
info_etablissement('ARM', 'Conditions d''Accès', 'Taille minimale : 1,65 m pour les garçons et 1,60 m pour les filles.').
info_etablissement('ARM', 'Conditions d''Accès', 'Taille minimale : 1,70 m pour les garçons et 1,60 m pour les filles.').
info_etablissement('ARM', 'Conditions d''Accès', 'Taille minimale : 1,70 m pour les hommes et 1,67 m pour les femmes.').
info_etablissement('ARM', 'Conditions d''Accès', 'Taille minimale : Mesurer au moins 1,70 m.').
info_etablissement('ARM', 'Conditions d''Accès', 'Voici un récapitulatif complet des opportunités de formation et de recrutement dans les domaines de la construction et de la sécurité (Militaire et Sûreté Nationale), basé sur l''ensemble de vos documents pour l''année 2025/2026 :🏗️ I. Domaine de la Construction et de l''UrbanismeCe pôle regroupe les écoles d''architecture, d''urbanisme et les instituts techniques spécialisés.ÉtablissementDiplôme / DuréeConditions ClésSite Web d''inscriptionENA (Architecture)Architecte (6 ans)Bac Sci/Tech/Éco, < 22 ans, Moyenne > 12/20.concoursena.maINAU (Urbanisme)DINAU (5 ans)Bac Sci, SVT, Math, < 21 ans, Moyenne > 12/20.inau.ac.maIFTSAU (Technique)Technicien Spé. (2 ans)Bac Sci/Tech/Arts Appliqués, 17-25 ans.muat.gov.maITSGC (Génie Civil)Technicien Spé. (2 ans)Bac Sci/Tech/Éco, < 30 ans.emploi-public.ma🎖️ II. Domaine Militaire et ParamilitaireLes recrutements se divisent entre les cycles d''Officiers (Bac requis) et de Sous-Officiers (Bac requis, formation plus courte).1. Cycle des Officiers (Grandes Écoles)ARM (Meknès) : Formation de 4 ans (Licence). Taille min : 1,70m (H) / 1,60m (F).ERA (Marrakech) : Pilotes et ingénieurs de l''Air. Bac Math ou Physique requis.ERN (Casablanca) : Officiers de Marine. Bac Math requis. Taille min : 1,70m.FA (Ben Slimane) : Officiers des Forces Auxiliaires. Formation en 4 ans à l''ARM.2. Cycle des Sous-Officiers (Sergents)FAR / ERA / ERN : Formation de 3 ans. Grade de Sergent. Âge : 18-23 ans.Forces Auxiliaires (FA) : Formation de 2 ans à Ben Slimane. Âge : 18-24 ans. Taille min : 1,70m.Inscription unique : www.recrutement.far.ma (ou recrutement.fa.gov.ma pour les FA).👮 III. Sûreté Nationale (DGSN)Les conditions de taille et de vision sont ici particulièrement strictes.GradeDiplôme RequisÂge MaxTaille Min (H/F)Gardien de la PaixBaccalauréat30 ans1,73 m / 1,67 mOfficier de PoliceBac + 2 (DEUG)30 ans1,70 m / 1,67 mCommissaireMaster / Bac + 535 ans1,70 m / 1,67 mVision : Minimum 15/20 pour les deux yeux réunis, sans correction.Inscription : concours.dgsn.gov.ma💡 Points de vigilance communsCélibat : Obligatoire pour tous les concours militaires et paramilitaires.Casier judiciaire : Doit être totalement vierge.Présélection : Elle se fait presque toujours sur la base de la moyenne du Bac (souvent pondérée 75% National / 25% Régional).').
info_etablissement('ARM', 'Conditions d''Accès', 'Âge : Avoir au moins 18 ans et au plus 24 ans à la date du concours.').
info_etablissement('ARM', 'Conditions d''Accès', 'Âge : Avoir au moins 21 ans et au plus 30 ans à la date du concours.').
info_etablissement('ARM', 'Conditions d''Accès', 'Âge : Avoir entre 18 et 22 ans.').
info_etablissement('ARM', 'Conditions d''Accès', 'Âge : Avoir entre 18 et 23 ans.').
info_etablissement('ARM', 'Conditions d''Accès', 'Âge : Entre 21 et 30 ans au plus à la date du concours.').
info_etablissement('ARM', 'Conditions d''Accès', 'Âge : Entre 25 et 35 ans au plus à la date du concours.').
info_etablissement('ARM', 'Conditions d''Accès', 'État civil : Être célibataire.').
info_etablissement('ARM', 'Conditions d''Accès', 'Être de nationalité marocaine et célibataire.').
info_etablissement('ARM', 'Conditions d''Accès', 'Être titulaire du Baccalauréat (toutes séries) de l''année en cours ou de l''année précédente.').
info_etablissement('ARM', 'Conditions d''Accès', 'Être titulaire du Baccalauréat de l''année en cours dans la filière requise.').
info_etablissement('ARM', 'Conditions d''Accès', 'Conditions d''Admission').
info_etablissement('ARM', 'Conditions d''Accès', 'Conditions de Candidature').
info_etablissement('ARM', 'Conditions d''Accès', 'Conditions de Candidature (Communes)').
info_etablissement('ARM', 'Processus de Sélection', 'Avoir entre 18 et 22 ans au 31 décembre de l''année du concours.').
info_etablissement('ARM', 'Processus de Sélection', 'Avoir entre 18 et 23 ans au 16 août de l''année du concours.').
info_etablissement('ARM', 'Processus de Sélection', 'Concours : Les candidats convoqués passent des tests de santé, des tests physiques et psychotechniques, ainsi qu''une épreuve orale.').
info_etablissement('ARM', 'Processus de Sélection', 'Concours : Les candidats convoqués passent par :').
info_etablissement('ARM', 'Processus de Sélection', 'Contrôle approfondi de la moralité et des antécédents judiciaires.').
info_etablissement('ARM', 'Processus de Sélection', 'Convocation : Les candidats présélectionnés reçoivent une convocation par e-mail (e-mail) indiquant la date et le lieu des tests.').
info_etablissement('ARM', 'Processus de Sélection', 'Convocation : Les candidats retenus reçoivent une convocation par e-mail pour passer les tests.').
info_etablissement('ARM', 'Processus de Sélection', 'Des tests d''aptitude médicale.').
info_etablissement('ARM', 'Processus de Sélection', 'Des tests physiques (sport).').
info_etablissement('ARM', 'Processus de Sélection', 'Des tests physiques et psychotechniques.').
info_etablissement('ARM', 'Processus de Sélection', 'Des tests psychotechniques.').
info_etablissement('ARM', 'Processus de Sélection', 'Entretien devant un jury.').
info_etablissement('ARM', 'Processus de Sélection', 'Entretien psychotechnique et oral devant un jury.').
info_etablissement('ARM', 'Processus de Sélection', 'L''inscription se fait exclusivement via le portail officiel de la Sûreté Nationale pendant la période d''ouverture du concours :').
info_etablissement('ARM', 'Processus de Sélection', 'Organisation du Concours : Les candidats présélectionnés sont convoqués pour passer :').
info_etablissement('ARM', 'Processus de Sélection', 'Organisation du concours : Les candidats retenus doivent se présenter avec leurs effets personnels et de sport pour passer les tests d''aptitude médicale, physique et psychotechnique.').
info_etablissement('ARM', 'Processus de Sélection', 'Pour être éligible au concours des sous-officiers, le candidat doit remplir les critères suivants au 16 août 2025 :').
info_etablissement('ARM', 'Processus de Sélection', 'Présélection : Basée sur l''étude des dossiers.').
info_etablissement('ARM', 'Processus de Sélection', 'Présélection : Étude des dossiers basée sur le mérite académique.').
info_etablissement('ARM', 'Processus de Sélection', 'Test de sport (course de fond).').
info_etablissement('ARM', 'Processus de Sélection', 'Test de sport (course).').
info_etablissement('ARM', 'Processus de Sélection', 'Tests de sélection :').
info_etablissement('ARM', 'Processus de Sélection', 'Tests de sélection : Les candidats retenus passent une visite médicale, des tests physiques, des tests psychotechniques ainsi qu''un entretien oral.').
info_etablissement('ARM', 'Processus de Sélection', 'Tests physiques.').
info_etablissement('ARM', 'Processus de Sélection', 'Tests psychotechniques.').
info_etablissement('ARM', 'Processus de Sélection', 'Une visite médicale complète.').
info_etablissement('ARM', 'Processus de Sélection', 'Une épreuve orale (entretien).').
info_etablissement('ARM', 'Processus de Sélection', 'Une épreuve orale.').
info_etablissement('ARM', 'Processus de Sélection', 'Visite médicale approfondie et test psychotechnique.').
info_etablissement('ARM', 'Processus de Sélection', 'Visite médicale.').
info_etablissement('ARM', 'Processus de Sélection', 'Épreuve Écrite : Un QCM ou une épreuve portant sur des sujets d''ordre général et les missions de la DGSN.').
info_etablissement('ARM', 'Processus de Sélection', 'Épreuves Orales et Aptitudes :').
info_etablissement('ARM', 'Processus de Sélection', 'Épreuves Orales et Physiques :').
info_etablissement('ARM', 'Processus de Sélection', 'Épreuves Écrites : Dissertations ou QCM sur des sujets d''ordre général, juridique ou administratif.').
info_etablissement('ARM', 'Processus de Sélection', 'Épreuves écrites et entretien oral.').
info_etablissement('ARM', 'Processus de Sélection', 'concours.dgsn.gov.ma').
info_etablissement('ARM', 'Processus de Sélection', 'Processus de Sélection et Concours').
info_etablissement('ARM', 'Processus de Sélection', 'Procédure de sélection et inscription (Commune)').
info_etablissement('ARM', 'Processus de Sélection', 'Procédure de Sélection').
info_etablissement('ARM', 'Processus de Sélection', 'Procédure de Sélection et Concours').
info_etablissement('ARM', 'Durée et Diplôme', 'Ce cycle forme les cadres de maîtrise des FAR dans diverses spécialités techniques et administratives. La formation est dispensée dans des établissements militaires spécialisés et prépare les élèves à devenir des techniciens et des encadrants de terrain.').
info_etablissement('ARM', 'Durée et Diplôme', 'Cursus : Identique au cycle ingénieur, soit 5 ans d''études.').
info_etablissement('ARM', 'Durée et Diplôme', 'Diplôme : Officier Ingénieur d''État dans les spécialités Pilotage ou Systèmes Aéronautiques.').
info_etablissement('ARM', 'Durée et Diplôme', 'Diplôme : Officier Ingénieur d''État de la Marine Royale.').
info_etablissement('ARM', 'Durée et Diplôme', 'Diplôme : Officier de Licence dans les spécialités Pilotage, Contrôleur Aérien ou Télémécanicien.').
info_etablissement('ARM', 'Durée et Diplôme', 'Diplôme requis : Master, Master spécialisé ou diplôme équivalent.').
info_etablissement('ARM', 'Durée et Diplôme', 'Diplômes obtenus : Les élèves reçoivent un Diplôme de Qualification Professionnelle ou un Diplôme de Technicien dans leur spécialité, ainsi qu''un brevet militaire.').
info_etablissement('ARM', 'Durée et Diplôme', 'Durée : Le cycle de formation initiale pour les élèves Moussaâidine (Sous-Officiers) dure 2 ans.').
info_etablissement('ARM', 'Durée et Diplôme', 'Durée de la formation : Elle s''étale sur 3 ans.').
info_etablissement('ARM', 'Durée et Diplôme', 'Durée de la formation : Non spécifiée précisément sur cette fiche, mais elle est généralement de 2 ans.').
info_etablissement('ARM', 'Durée et Diplôme', 'Durée et diplôme : La formation dure 3 ans. Elle est sanctionnée par le grade de Sergent (sous-officier).').
info_etablissement('ARM', 'Durée et Diplôme', 'Durée et diplôme : La formation s''étale sur 3 ans. Le cursus débouche sur le grade de Sergent.').
info_etablissement('ARM', 'Durée et Diplôme', 'Formation : 4 ans (Licence en 3 ans + 1 an de formation militaire et professionnelle).').
info_etablissement('ARM', 'Durée et Diplôme', 'Formation : 5 ans (2 ans de classes préparatoires + 3 ans de cycle ingénieur).').
info_etablissement('ARM', 'Durée et Diplôme', 'Grade à la sortie : Le cursus est sanctionné par l''obtention du grade de Sergent.').
info_etablissement('ARM', 'Durée et Diplôme', 'La formation dure quatre ans. Après trois ans d''études, l''élève officier obtient une Licence dans l''un des parcours suivants :').
info_etablissement('ARM', 'Durée et Diplôme', 'Santé Militaire : Formation d''infirmiers et techniciens de santé à Rabat.').
info_etablissement('ARM', 'Durée et Diplôme', 'Voici les informations détaillées concernant le cycle des Sous-Officiers des Forces Armées Royales (FAR), basées sur vos documents pour l''année universitaire 2025/2026 :').
info_etablissement('ARM', 'Durée et Diplôme', 'À la fin de la quatrième année, il reçoit le diplôme d''études universitaires et militaires et est nommé au grade de Sous-Lieutenant.').
info_etablissement('ARM', 'Durée et Diplôme', 'Cursus et Diplômes').
info_etablissement('ARM', 'Durée et Diplôme', 'Cursus et Formation').
info_etablissement('ARM', 'Inscription, Contact et Divers', 'Inscription : Les candidatures doivent être déposées exclusivement sur le site : www.recrutement.far.ma.').
info_etablissement('ARM', 'Inscription, Contact et Divers', 'L''inscription se fait exclusivement en ligne sur le portail des recrutements des FAR :').
info_etablissement('ARM', 'Inscription, Contact et Divers', 'L''inscription se fait exclusivement sur le portail des recrutements des FAR :').
info_etablissement('ARM', 'Inscription, Contact et Divers', 'L''inscription se fait obligatoirement en ligne sur le portail dédié aux recrutements des Forces Auxiliaires :').
info_etablissement('ARM', 'Inscription, Contact et Divers', 'L''inscription se fait obligatoirement et exclusivement via le portail officiel des recrutements des FAR :').
info_etablissement('ARM', 'Inscription, Contact et Divers', 'www.recrutement.fa.gov.ma').
info_etablissement('ARM', 'Inscription, Contact et Divers', 'www.recrutement.far.ma').
info_etablissement('ARM', 'Inscription, Contact et Divers', 'Inscription').
info_etablissement('ARM', 'Inscription, Contact et Divers', 'Modalités d''Inscription').
nouvel_etablissement('Facultés de Médecine, de Pharmacie et de Médecine Dentaire (FMP', 'MILITAIRE ET SÉCURITÉ').
info_etablissement('Facultés de Médecine, de Pharmacie et de Médecine Dentaire (FMP', 'Conditions d''Accès', 'C''est noté. Voici l''extraction maximale des données concernant le domaine médical et paramédical à partir de tes dernières captures d''écran.🏛️ Présentation : Facultés de Médecine, de Pharmacie et de Médecine Dentaire (FMP - FMD)Ces établissements visent à former des cadres supérieurs dans le domaine de la santé pour répondre aux besoins nationaux en matière de services médicaux, curatifs et de prévention.🎓 Durée des Études et DiplômesLe cursus a été récemment harmonisé pour les trois filières majeures :Médecine Générale : 6 ans d''études → Diplôme de Docteur en Médecine.Pharmacie : 6 ans d''études → Diplôme de Docteur en Pharmacie.Médecine Dentaire : 6 ans d''études → Diplôme de Docteur en Médecine Dentaire.📝 Conditions d''Admission et SélectionL''accès est très sélectif et réservé aux bacheliers des filières scientifiques :Séries de Bac admises : Sciences Mathématiques (A et B), Sciences Physiques, SVT ou Sciences Agronomiques.Âge : Être inscrit en année de Bac ou titulaire du Bac de l''année précédente.Processus de sélection (en deux étapes) :Présélection : Basée sur la moyenne calculée à 75% National + 25% Régional.Concours Écrit Commun : Porte sur 4 matières (Coefficient 1 pour chaque matière, durée 2h par épreuve) :Sciences de la Vie et de la Terre (SVT).Physique.Chimie.Mathématiques.Note éliminatoire : Toute note inférieure à 05/20 dans l''une des matières est éliminatoire.📍 Répartition Géographique (Zone Orientale)Le document précise les facultés de rattachement selon ton lieu de résidence (sectorisation) :FilièreFaculté de rattachementZones concernées (Provinces)MédecineFMP OujdaPréfecture Oujda-Angad, Berkane, Taourirt, Jerada, Figuig, Nador, Driouch et Guercif.PharmacieFMP OujdaProvinces de la région de l''Oriental.Médecine DentaireFMD RabatProvinces de la région de l''Oriental.🏥 Autres Établissements mentionnésD''après le diagramme de synthèse, d''autres parcours de santé sont disponibles :ISPITS : Institut Supérieur des Professions Infirmières et Techniques de Santé (Formation d''infirmiers et techniciens spécialisés).I3S : Institut des Sciences de la Santé.📂 InscriptionPlateforme unique : www.cursussup.gov.maChoix : Le candidat doit classer ses vœux par priorité (Médecine, Pharmacie, Dentaire) lors de l''inscription.Conseil de préparation : Puisque le concours écrit approche, concentre-toi sur les programmes de 2ème année Bac en SVT et Physique-Chimie, car ce sont les piliers de l''examen d''entrée.').
info_etablissement('Facultés de Médecine, de Pharmacie et de Médecine Dentaire (FMP', 'Conditions d''Accès', 'Ce guide d''orientation pour l''année universitaire 2025/2026, publié par l''Académie Régionale d''Éducation et de Formation de l''Oriental, offre une vue d''ensemble complète des opportunités post-baccalauréat au Maroc. Voici une synthèse structurée des données extraites de l''ensemble des documents fournis :🏛️ 1. Panorama des Études SupérieuresLe système est structuré en plusieurs pôles pour orienter les bacheliers selon leurs compétences :Établissements Universitaires : Facultés classiques et à accès régulé.Grandes Écoles et Instituts : Ingénierie, commerce et technologies (ENSA, ENSAM, ENCG, ISCAE, etc.).Domaines Spécifiques : Santé (Médecine, Pharmacie, ISPITS), Architecture (ENA), et Numérique (ENIADB).💼 2. Commerce et GestionÉtablissementDuréeAdmission / SélectionENCG5 ansBac Économie, Gestion, Sciences ou Pro. Présélection (75% Nat/25% Rég) + Concours TAFEM.ISCAE3 ansBac Sciences ou Économie, âge < 21 ans. Écrit (Maths, Anglais, Culture G) + Oral.⚙️ 3. Ingénierie, Technologie et ArchitectureENSA & ENSAM : Formation d''ingénieur d''État en 5 ans. Admission via présélection et concours national commun sur www.cursussup.gov.ma.ENSCK (Chimie - Kénitra) : Formation de 5 ans spécialisée en chimie. Concours écrit incluant Maths, Physique, Chimie et Français.ENIADB (IA & Numérique - Berkane) : Spécialisation en IA et Robotique. Concours portant sur les Maths, l''Informatique et les Soft Skills.ENA (Architecture) : Cursus de 6 ans. Sélection par écrit (QCM : Culture, Art, Géométrie) et dessin, après présélection sur dossier. Inscription sur www.concoursena.ma.FST & EST : La FST propose un cycle Licence (3 ans) avec sélection sur dossier pondéré. L''EST prépare au DUT en 2 ans par présélection uniquement.🏥 4. Santé et ParamédicalFacultés de Médecine et Pharmacie (FMP/FMD) : Doctorat en 6 ans. Concours écrit commun (SVT, Physique, Chimie, Maths) avec note éliminatoire < 05/20.ISPITS : Licence en 3 ans dans diverses spécialités (Soins, Sage-femme, Techniques de santé). Sélection par écrit puis test d''aptitude oral.ISSS (Sciences de la Santé - Settat) : Offre des spécialités techniques comme la maintenance biomédicale ou la radiophysique. Sélection par écrit (Maths, Physique ou Chimie selon l''option).🔗 5. Plateformes d''Inscription ClésPour la majorité des établissements à accès régulé (ENCG, ENSA, ENSAM, FST, EST, Médecine), la candidature s''effectue sur le portail unique :👉 www.cursussup.gov.ma').
info_etablissement('Facultés de Médecine, de Pharmacie et de Médecine Dentaire (FMP', 'Conditions d''Accès', 'Ce guide d''orientation pour l''année universitaire 2025/2026, publié par l''Académie Régionale d''Éducation et de Formation de l''Oriental, offre une vue d''ensemble complète des opportunités post-baccalauréat au Maroc.Voici une synthèse structurée de toutes les données extraites des documents fournis :🏛️ 1. Panorama des Études SupérieuresLe système est divisé en plusieurs pôles majeurs pour orienter les bacheliers selon leurs compétences :Établissements Universitaires : Facultés classiques et à accès régulé.Grandes Écoles et Instituts : Ingénierie, commerce et technologies (ENSA, ENSAM, ENCG, ISCAE, etc.).Pôles d''Excellence : Classes Préparatoires (CPGE) et Brevet de Technicien Supérieur (BTS).Domaines Spécifiques : Enseignement (Écoles de formation), Formation Professionnelle (OFPPT), et secteurs Militaire/Paramilitaire.💼 2. Commerce, Gestion et AdministrationÉtablissementDurée des étudesConditions d''accèsSélectionENCG5 ans (10 semestres)Bac Économie, Gestion, Sciences ou Pro.Présélection (75% Nat/25% Rég) + Concours TAFEM.ISCAE3 ans (Licence)Bac Sciences ou Économie, < 21 ans.Dossier + Écrit (Maths, Anglais, Culture G) + Oral.⚙️ 3. Ingénierie et Sciences AppliquéesA. Écoles Généralistes (ENSA & ENSAM)Structure : 2 ans de cycle préparatoire intégré + 3 ans de cycle ingénieur (5 ans au total).Admission : Réservée aux bacheliers Sciences Mathématiques, Expérimentales, Techniques ou Professionnels industriels.Sites d''inscription : Via la plateforme nationale www.cursussup.gov.ma.B. Écoles SpécialiséesENSCK (Chimie - Kénitra) : Formation de 5 ans pour devenir ingénieur chimiste. Admission via présélection et concours écrit (Maths, Physique, Chimie, Français).ENIADB (IA & Numérique - Berkane) : Spécialisation en Intelligence Artificielle, Robotique et Cybersécurité. Concours incluant des épreuves de Mathématiques, Informatique et Soft Skills.🧪 4. Sciences, Technologies et SantéA. FST (Faculté des Sciences et Techniques)Système : LMD (Licence, Master, Doctorat).Parcours initiaux : MIP (Maths/Info/Physique), MIPC (Chimie en plus), BCG (Bio/Chimie/Géo), GE-GM (Génie Électrique/Mécanique).Sélection : Uniquement sur dossier (Moyenne pondérée 75% Nat/25% Rég).B. EST (École Supérieure de Technologie)Diplôme : DUT en 2 ans, avec possibilité de Licence Professionnelle en 1 an supplémentaire.Sélection : Présélection sans concours écrit, basée sur le mérite et la filière du bac.C. Domaine de la SantéFMP/FMD (Médecine & Dentaire) : 6 ans pour le doctorat. Concours écrit commun (SVT, Physique, Chimie, Maths) avec note éliminatoire < 05/20.ISPITS (Infirmiers & Paramédical) : Licence en 3 ans. Sélection par écrit (matière de spécialité + Français) puis test d''aptitude oral.ISSS (Sciences de la Santé - Settat) : Spécialités comme la maintenance biomédicale ou la radiophysique. Inscription sur www.isss.uh1.ac.ma.🔗 5. Plateformes d''Inscription ClésPour la majorité de ces établissements (ENCG, ENSA, ENSAM, FST, EST, Médecine), la candidature s''effectue sur le portail unique :👉 www.cursussup.gov.ma').
info_etablissement('Facultés de Médecine, de Pharmacie et de Médecine Dentaire (FMP', 'Conditions d''Accès', 'Excellente intuition ! Ta nouvelle capture d''écran concerne justement l''ISPITS (Institut Supérieur des Professions Infirmières et Techniques de Santé). C''est le pilier de la formation paramédicale au Maroc.Voici l''extraction complète des données pour cet établissement :🏛️ Présentation de l''ISPITSL''ISPITS est un réseau d''instituts nationaux qui forment des professionnels de santé dans divers domaines techniques et infirmiers. La formation est structurée selon le système LMD (Licence en 3 ans).🎓 Cursus et DiplômeDurée : 3 ans (6 semestres).Diplôme : Licence d''État en Sciences Infirmières et Techniques de Santé.Spécialités (Filières) :Soins Infirmiers : Polyvalent, Anesthésie-Réanimation, Santé Mentale, Soins Urgents et Intensifs, Santé Communautaire, Gériatrie, Néonatologie.Sage-femme : (Filière unique).Techniques de Santé : Laboratoire, Radiologie, Diététique, Santé et Environnement, Préparateur en Pharmacie, Statistiques Sanitaires.Rééducation et Réadaptation : Kinésithérapie, Orthophonie, Orthoptie, Psychomotricité.Assistance Sociale : Assistant social.📝 Conditions d''Admission et SélectionL''accès est ouvert aux bacheliers (année en cours ou précédente) des séries Sciences Expérimentales ou Sciences Mathématiques.Le processus se déroule en 3 étapes :Présélection : Basée sur la moyenne du Bac (75% National + 25% Régional).Examen Écrit (2 épreuves) :Épreuve 1 (1h30) : Matière selon la filière choisie (SVT, Physique, Chimie ou Maths) - Coefficient 2.Épreuve 2 (1h00) : Français (Culture générale) - Coefficient 1.Test d''Aptitude : Un entretien oral devant un jury pour valider la motivation et les capacités du candidat.📍 Carte des Spécialités (Zones Oujda/Oriental)Selon ton tableau, voici les options disponibles spécifiquement à Oujda et son annexe à Nador :LieuFilières Disponibles (Exemples)Matière ConcoursOujdaInfirmier Polyvalent, Anesthésie, Santé Mentale, Urgences, Sage-femme, Laboratoire, Radiologie.SVT (ou Physique/Chimie selon l''option)NadorInfirmier Polyvalent, Sage-femme.SVT📂 InscriptionPlateforme : ispits.sante.gov.maAffectation : Elle se fait automatiquement selon ta zone géographique (lieu d''obtention du Bac) et le classement par mérite.Point de vigilance : Contrairement à la médecine, les épreuves de l''ISPITS dépendent fortement de la filière choisie. Par exemple, si tu choisis "Radiologie", tu seras interrogé en Physique.').
info_etablissement('Facultés de Médecine, de Pharmacie et de Médecine Dentaire (FMP', 'Durée et Diplôme', 'Basée sur la dernière capture d''écran, voici les informations détaillées concernant l''École Nationale d’Architecture (ENA) pour l''année universitaire 2025/2026 :').
nouvel_etablissement('École Royale de Gendarmerie (ERG)', 'MILITAIRE ET SÉCURITÉ').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Aptitude : Être apte physiquement et n''avoir aucun antécédent judiciaire.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Audiovisuel et Communication :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Avoir une note minimale de 14/20 en Arabe, en Français et en deuxième langue étrangère.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Beaux-Arts et Design :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Bien reçu ! J''ai analysé la nouvelle série d''images que vous avez téléchargées. Conformément à vos instructions, je me concentre sur ces documents pour vous fournir une synthèse structurée des nouvelles informations concernant les domaines artistiques, touristiques et techniques, tout en complétant les détails sur les cycles militaires.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Centres de formation : En cas de réussite, l''incorporation se fait dans l''un des centres mentionnés (ex: Marrakech, Oujda, Casablanca, Agadir, etc.).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Contenu : Elle comprend une formation générale, militaire, juridique, professionnelle et technique, ainsi que de l''éducation physique et sportive.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'ENSAD : École Nationale Supérieure d''Art et de Design.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'ESBA : École Supérieure des Beaux-Arts (Casablanca).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'ESITH : École Supérieure des Industries du Textile et de l''Habillement (Casablanca).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'IFTSAU (Architecture & Urbanisme - Oujda) :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'INBA : Institut National des Beaux-Arts (Tétouan).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'INSAP : Institut National des Sciences de l''Archéologie et du Patrimoine (Rabat).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'ISIC : Institut Supérieur de l''Information et de la Communication (Rabat).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'ISIT : Institut Supérieur International de Tourisme (Tanger).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'ISMAC : Institut Supérieur des Métiers de l''Audiovisuel et du Cinéma (Rabat).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'ITSGC (Génie Civil & Finances Locales) :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Il existe deux sections de formation : une section Arabe et une section Française.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'L''ERG est l''institution chargée de la formation et du perfectionnement des élèves gendarmes, opérant sous un régime d''internat.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'L''ISIC a pour mission de préparer des cadres supérieurs spécialisés dans les techniques d''information et de communication pour les secteurs public et privé.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'L''image image_c3b04f.png présente les principaux établissements supérieurs pour ces secteurs :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'L''établissement est situé au Avenue Allal El Fassi, Madinat Al Irfane, B.P. 10000, Rabat.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Les candidats doivent remplir les critères suivants :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Mode et Textile :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Objectif : Former des gardiens de la paix, des officiers, des inspecteurs et des commissaires de police.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Patrimoine et Tourisme :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Pour postuler, le candidat doit remplir les critères suivants :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Régime : Externat.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Souhaitez-vous des précisions sur un autre établissement présent dans vos documents, comme l''ITSGC (Génie Civil) ?').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Sport : Une course de 1500 mètres (Coefficient : 1).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Spécialisation : Des matières supplémentaires peuvent être intégrées selon les directives du Commandant de la Gendarmerie Royale.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Type de formation : Enseignement technique professionnel comprenant des cours théoriques, des travaux pratiques et des stages sur le terrain.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Une copie de la Carte d''Identité Nationale (CIN).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Une demande manuscrite signée par le candidat précisant la filière choisie et ses coordonnées.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Une photo d''identité récente.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Une épreuve d''Anglais obligatoire pour toutes les spécialités (1h30).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Une épreuve de culture générale en Arabe ou en Français liée au domaine de l''audiovisuel et du cinéma (2 heures).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Une épreuve de spécialité consistant en l''analyse d''un texte en Français sur un sujet cinématographique ou audiovisuel (scientifique, technique ou artistique selon la filière) (2 heures).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Voici les informations extraites uniquement de la dernière capture (image_c3b0c6.png) concernant l''ISIC :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Être âgé entre 17 et 25 ans au maximum.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Système de Formation').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'III. Cycles des Sous-Officiers (Détails par Corps)').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Institut Supérieur de l''Information et de la Communication (ISIC)').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'I. Domaines des Arts, du Tourisme et de l''Audiovisuel').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'II. Urbanisme et Génie Civil (Détails Techniques)').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Présentation de l''IFTSAU Oujda').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'École Royale de Gendarmerie (ERG) - Marrakech').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Présentation et Formation').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Présentation et Spécialités', 'Rappels Importants issus des documents :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', '2. Conditions de Candidature :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Acuité visuelle : Avoir une force visuelle d''au moins 15/10 sans l''utilisation de lunettes ou de lentilles (minimum 10/10 pour chaque œil).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Aptitude physique : Être physiquement apte pour la fonction demandée.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Avoir une moyenne générale minimale de 14/20 au Baccalauréat.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Baccalauréat : Être titulaire du Baccalauréat (toutes séries) de l''année en cours ou de l''année précédente.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Conditions de Candidature').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Conditions de santé : Pour la Gendarmerie (image_c3ac15.png) et la Police (image_c3afd4.png), l''acuité visuelle est éliminatoire si elle est inférieure à 15/10 sans correction.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Corps / École	Spécialités mentionnées	Taille Min (H/F)	Inscription').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Diplôme : Être titulaire d''un baccalauréat pour l''année en cours ou la précédente.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Diplôme : Être titulaire du Baccalauréat ou d''un diplôme reconnu équivalent.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Les documents à télécharger incluent les relevés de notes du Bac (Régional et National), le diplôme du Bac et la CNI.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Les nouvelles captures détaillent les spécificités du grade de Sergent (Sous-officier) :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Nationalité : Être de nationalité marocaine.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'OU être titulaire d''un Diplôme de Technicien (dans la limite de 10 % des places disponibles) dans des spécialités similaires (Urbanisme, Architecture, Dessin de bâtiment, Génie Civil, etc.).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Pour les filières Image, Son, ou Montage et Post-production : Baccalauréat dans des spécialités scientifiques ou techniques avec une mention "Assez bien" au minimum.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Pour les filières Réalisation, Production, ou Écriture : Baccalauréat toutes options confondues avec une moyenne générale minimale de 14/20.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Présélection : Basée sur l''étude du dossier et les résultats du Baccalauréat.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Présélection : Basée sur la moyenne générale du baccalauréat et d''autres éléments du dossier.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Présélection : Basée sur les résultats obtenus au Baccalauréat.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Présélection : Une première étape de sélection est effectuée sur la base des moyennes obtenues au Baccalauréat.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Taille minimale : 1,70 m pour les garçons et 1,68 m pour les filles.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Taille minimale : Mesurer au moins 1,73 m pour les hommes et 1,67 m pour les femmes.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Une copie des relevés de notes des deux années du baccalauréat (Régional et National).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Une copie du diplôme du Baccalauréat.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Âge : Avoir entre 18 et 24 ans au plus à la date du 1er septembre de l''année du concours.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Âge : Avoir entre 21 ans au moins et 30 ans au plus à la date du concours.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Âge : Entre 17 et 25 ans au plus tard au 31 décembre de l''année du concours.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Âge : Ne pas dépasser 25 ans à la date du concours.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'État civil : Être de nationalité marocaine et célibataire.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat avec une moyenne générale supérieure ou égale à 12/20 dans les filières suivantes : Sciences Expérimentales, Sciences Mathématiques, Architecture, Arts Appliqués, Bâtiment et Travaux Publics (ou diplôme équivalent).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Être titulaire du Baccalauréat (toutes séries) de l''année en cours ou de l''année précédente.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Conditions d''Accès', 'Conditions de Candidature').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', '3. Procédure de Sélection et Concours :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Basé sur le document fourni (image_c399e5.png), voici les informations relatives au concours d''accès au Mairie de Formation des Techniciens Spécialisés en Architecture et Urbanisme (IFTSAU) de Oujda pour la session 2025/2026 :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Concours écrit : Mathématiques et Dessin (2h) + Analyse de texte en Français avec traduction vers l''Arabe (2h).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Convocation : Les candidats retenus sont convoqués par e-mail pour passer les tests dans les centres désignés.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Examen Oral : Entretien devant un jury portant sur la présentation d''un projet dans le domaine de l''audiovisuel ou du cinéma.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Examen Écrit :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Institution : Le concours est organisé par l''Institut Royal de Police (IRP) sous la tutelle de la Direction Générale de la Sûreté Nationale (DGSN).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'L''Institut Supérieur des Métiers de l''Audiovisuel et du Cinéma (ISMAC) a pour mission d''assurer la formation et d''offrir des services dans les domaines liés à l''audiovisuel et au cinéma. La formation dure trois ans, débouchant sur une Licence Fondamentale dans l''un des parcours suivants : Image, Son, Montage et Post-production, Production, Réalisation, ou Écriture.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Le concours se déroule en deux étapes :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Les images image_c399e5.png (IFTSAU) et image_c39a42.png (ITSGC) précisent les concours :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Les listes des candidats présélectionnés pour l''écrit seront publiées sur ce même portail.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Modalités de Sélection').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Oral : Entretien (Coefficient 2).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Oral : Épreuve de culture générale (Coefficient : 4, Durée : 15 min).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Organisation : Le concours inclut des examens médicaux, des tests psychotechniques et des épreuves sportives.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Présélection : Les candidats inscrits sont sélectionnés par une commission après étude de leurs dossiers.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Voici les détails du concours d''accès pour la saison 2025/2026 :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Écrit : QCM (Coefficient 3, 3h) portant sur les Mathématiques et les langues (Arabe/Français).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Écrit : Sujet d''ordre général (social, politique ou culturel) ou un QCM (Durée : 1h, Coefficient : 2).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Épreuve Orale : Un entretien devant un jury pour les candidats ayant réussi l''écrit.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Épreuve Écrite :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Épreuve Écrite : Traitement d''un sujet rédactionnel (3 heures) avec un résumé traduit dans la deuxième langue étrangère.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Épreuves du concours :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'concours.dgsn.gov.ma').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Procédure de Sélection (Concours)').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Processus de Sélection', 'Procédure de Sélection et Concours').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', '1. Système d''études et Diplôme :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'Adresse : Institut de Formation des Techniciens Spécialisés en Urbanisme et Architecture - Route Sidi Maafa, Oujda.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'Analyse de texte en Français avec traduction de certains passages vers l''Arabe (Durée : 2 heures).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'Diplôme délivré : Diplôme de Technicien Spécialisé.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'Diplôme requis :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'Dossier de candidature : Il comprend le formulaire d''inscription en ligne signé, une demande manuscrite, des copies certifiées des diplômes et des relevés de notes, ainsi qu''une copie de la CNI.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'Durée : La formation pour les élèves gendarmes dure 2 ans.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'Durée de formation : La formation dure 12 mois (un an) au sein des écoles régulières dépendant de l''Institut Royal de Police.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'Durée de la formation : 2 ans.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'L''institut a pour mission de former des techniciens spécialisés dans les domaines de l''urbanisme, de l''architecture, du bâtiment et du génie civil pour travailler dans les administrations publiques, les collectivités territoriales et le secteur privé.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'L''institut adopte le système LMD (Licence, Master, Doctorat).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'La formation pour la Licence dure 3 ans (6 semestres).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'Mathématiques et Dessin (Durée : 2 heures).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'À la fin de chaque année, l''étudiant effectue un stage de formation dans une institution médiatique.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Durée et Diplôme', 'Cursus et Formation').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', '4. Inscription :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'Air (ERA)	Contrôleur aérien, Anglais, Cuisine	1,70 m / 1,60 m	recrutement.far.ma').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'Auxiliaires (FA)	Maintien de l''ordre (2 ans)	1,70 m (H)	recrutement.fa.gov.ma').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'Documents à préparer : Pour la Gendarmerie, prévoyez une copie intégrale de l''acte de naissance et une photo 4x4 lors de l''inscription en ligne.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'Dossier de Candidature').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'Gendarmerie (ERG)	Formation générale et juridique (2 ans)	1,70 m / 1,68 m	recrutement.gr.ma').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'L''inscription doit être effectuée sur le portail électronique de la DGSN :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'L''inscription s''effectue obligatoirement en ligne sur le portail dédié :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'L''inscription se fait exclusivement en ligne via le portail : www.muat.gov.ma pendant la période fixée par l''administration.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'L''inscription se fait via la plateforme : preinscription.isic.ma.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'Le dossier doit être déposé via le site www.ismac.ac.ma et doit comprendre les pièces numérisées suivantes :').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'Le formulaire d''inscription en ligne dûment rempli et signé.').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'Lors de l''inscription, le candidat doit scanner et télécharger sa Carte d''Identité Nationale (recto-verso), un extrait d''acte de naissance et une photo d''identité (4x4).').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'Marine (ERN)	Fusiliers Marins, Personnel Naviguant	1,70 m / 1,60 m	recrutement.far.ma').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'Terre (FAR)	Infanterie, Cavalerie, Santé, Matériel, etc.	1,70 m / 1,60 m	recrutement.far.ma').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'recrutement.gr.ma').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'Modalités d''Inscription').
info_etablissement('École Royale de Gendarmerie (ERG)', 'Inscription, Contact et Divers', 'Contact').
nouvel_etablissement('École Royale de l''Air (ERA)', 'MILITAIRE ET SÉCURITÉ').
info_etablissement('École Royale de l''Air (ERA)', 'Présentation et Spécialités', 'L''école assure la formation initiale et continue des officiers des Forces Royales Air.').
info_etablissement('École Royale de l''Air (ERA)', 'Présentation et Spécialités', 'École Royale de l''Air (ERA) - Marrakech').
info_etablissement('École Royale de l''Air (ERA)', 'Conditions d''Accès', '2. Conditions d''admission :').
info_etablissement('École Royale de l''Air (ERA)', 'Conditions d''Accès', 'Avoir un casier judiciaire vierge.').
info_etablissement('École Royale de l''Air (ERA)', 'Conditions d''Accès', 'Baccalauréat : Doit être de l''année en cours (Sciences Mathématiques pour le cycle Ingénieur ; Sciences Mathématiques ou Physiques pour le cycle Licence).').
info_etablissement('École Royale de l''Air (ERA)', 'Conditions d''Accès', 'Présélection : Basée sur la moyenne du Baccalauréat avec mention "Assez Bien" minimum.').
info_etablissement('École Royale de l''Air (ERA)', 'Conditions d''Accès', 'Taille minimale : 1,65 m pour les garçons et 1,60 m pour les filles.').
info_etablissement('École Royale de l''Air (ERA)', 'Conditions d''Accès', 'Âge : Entre 18 et 20 ans au maximum au 31 décembre de l''année du concours.').
info_etablissement('École Royale de l''Air (ERA)', 'Conditions d''Accès', 'Être de nationalité marocaine et célibataire.').
info_etablissement('École Royale de l''Air (ERA)', 'Processus de Sélection', '3. Processus de sélection :').
info_etablissement('École Royale de l''Air (ERA)', 'Processus de Sélection', 'Tests : Visite médicale, tests physiques, tests psychotechniques et épreuve orale.').
info_etablissement('École Royale de l''Air (ERA)', 'Durée et Diplôme', '1. Les Cursus proposés :').
info_etablissement('École Royale de l''Air (ERA)', 'Durée et Diplôme', 'Cycle Ingénieur : Comprend 2 ans de classes préparatoires suivis de 3 ans de cycle ingénieur dans les filières "Pilotage" ou "Systèmes Aéronautiques".').
info_etablissement('École Royale de l''Air (ERA)', 'Durée et Diplôme', 'Cycle Licence (Pilotage) : Formation de 4 ans au total (3 ans de licence + 1 an de formation militaire et professionnelle).').
info_etablissement('École Royale de l''Air (ERA)', 'Inscription, Contact et Divers', '4. Inscription :').
info_etablissement('École Royale de l''Air (ERA)', 'Inscription, Contact et Divers', 'Se fait exclusivement en ligne sur le portail : www.recrutement.far.ma.').
nouvel_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'INGÉNIERIE, SCIENCES ET TECHNOLOGIE').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '1. Domaine : Biologie, Chimie et Géologie (BCG)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '1. Domaine : Sciences Humaines, Lettres et Arts').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '1. Information et Cinéma').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '1. Urbanisme et Génie Civil').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '1. École Royale de l''Air (ERA) - Marrakech').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '2. Beaux-Arts et Design').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '2. Domaine : Mathématiques, Informatique et Physique (MIP)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '2. Domaine : Sciences Juridiques, Économiques et de Gestion').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '2. Marine Royale (ERN) - Casablanca').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '2. Textile et Tourisme').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '3. Artisanat de Prestige').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '3. Domaine : Physique et Chimie (PC)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '3. Domaine : Sciences').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '3. Gendarmerie Royale (ERG)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '4. Domaine : Informatique Appliquée').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '4. Forces Auxiliaires (FA)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '4. Parcours d''Excellence et Sans Tronc Commun').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', '5. Sûreté Nationale (DGSN) - Gardiens de la Paix').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'AAT (Arts Traditionnels - Casablanca) : Spécialisation en calligraphie arabe pour les 18-30 ans. Les candidats doivent soumettre 3 modèles de leurs travaux artistiques.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Accès : Entre 17 et 24/25 ans.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Agences de voyages.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Agent technique de vente.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Agro-sciences et biotechnologie végétale.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Aide Éducateur en Préscolaire (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Ambulancier (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Analyses médicales (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Arts culinaires (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Arts culinaires.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Assistant Administratif (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Assistant Administratif.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Automatisation et instrumentation industrielle.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Autres parcours (S1-S6) : Philosophie, Études Hispaniques (Estudios Hispanicos), Géographie et Aménagement, Langue et Culture Amazighe.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Auxiliaire de Soins (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Biologie : sciences biomédicales.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Biologie et santé.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Biologie, Chimie et Géologie :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Boulanger Pâtisserie.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Bâtiment (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'CENTRE DE FORMATION ET D''INSERTION DES JEUNES AHL ANGAD OUJDA').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'CPGE (Classes Préparatoires) :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Ce pôle regroupe des instituts spécialisés dans les médias, les arts visuels et le cinéma.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Ce pôle regroupe des établissements spécialisés dans la communication, le cinéma et les arts visuels.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Ce secteur regroupe les Forces Armées Royales (FAR), la Gendarmerie Royale, les Forces Auxiliaires et la Sûreté Nationale.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Centre Mixte de Formation Professionnelle Oujda').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Centre de Formation dans les métiers de l''Automobile OUJDA').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Centres de Formation et Filières par Province').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Ces filières visent l''excellence académique ou une intégration technique rapide.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Ces formations sont conçues pour une insertion directe dans le marché du travail en fournissant des compétences pratiques et techniques spécialisées.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Ces établissements proposent des formations professionnalisantes avec des critères d''admission spécifiques.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Cet établissement dispose d''un internat et propose :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Cet établissement dispose d''un internat et propose les filières suivantes :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Cet établissement ne dispose pas d''internat et propose :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Chimie organique et produits naturels.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Cité des Métiers et des Compétences (CMC) Nador').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Classes Préparatoires (CPGE) :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Complexe de formation dans les métiers des nouvelles technologies de l''information de l''offshoring et l''électronique').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Cuisine.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Cycle des Sous-Officiers (Sergent) : Formation de 3 ans dans des spécialités telles que contrôleur aérien, anglais ou cuisine.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'D''après la dernière capture d''écran fournie (image_c47aa2.png), voici les informations spécifiques concernant cette section :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Design Graphique et Digital (التصميم الغرافيكي والرقمي).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Dessinateur de bâtiment.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Diagnostic en électronique embarquée.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Diagnostic et Electronique Embarquée Automobile (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Droit : Droit privé ou public, en Arabe ou en Français.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Droit en Arabe :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Développement Digital (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Développement digital.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Développement en Habillement (تطوير الألبسة).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'ENSAD (Art et Design - Mohammedia) :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'ESBA (Casablanca) : École Supérieure des Beaux-Arts. Formation de 4 ans en Design d''intérieur, Design publicitaire ou Arts plastiques.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Eau et assainissement.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Educateur Spécialisé dans la Petite Enfance (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Electromécanique des systèmes automatisés.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Exploitation (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'FPN (Nador)	Formation pluridisciplinaire : Management portuaire, Marketing analytique, Sciences.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'FSHLA (Lettres - Oujda)	Études islamiques, Langues (Arabe, Français, Anglais, Espagnol, Amazigh), Géographie.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'FSHLA (Lettres)	Études islamiques, Langues (Arabe, Français, Anglais, Espagnol, Amazigh), Géographie, Histoire, Philosophie.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'FSJESO (Droit/Éco - Oujda)	Droit (Français/Arabe), Économie, Marketing digital, Audit, Banque.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'FSJESO (Droit/Éco)	Droit (Français/Arabe), Économie régionale, Audit et contrôle, Marketing digital.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'FSO (Sciences - Oujda)	Biologie, Chimie, Physique, Mathématiques, Intelligence Artificielle, Data Science.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Filière : Assistant Administratif. Pas d''internat.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Filière : Gestion des Entreprises (1A). Pas d''internat.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Filière : Gestion des entreprises. Pas d''internat.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Filières : MPSI, PCSI (Ingénierie), TSI (Technique), ECT et ECS (Économie).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Formation : 2 ans dans des lycées techniques spécialisés (Maintenance, Audiovisuel, Gestion, etc.).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Formation : 2 ans dans diverses spécialités (Comptabilité, Électrotechnique, Audiovisuel, etc.).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Formation : 4 ans d''études en art et design.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Formation : 4 ans d''études.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Formation : Dure 3 ans et mène au grade de sergent dans des spécialités comme le personnel navigant ou les fusiliers marins.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Froid commercial et climatisation.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Gestion de la Chaîne Logistique (تدبير السلسلة اللوجستيكية).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Gestion de la Production en Habillement (تدبير إنتاج الألبسة).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Gestion de la Production en Textile (تدبير إنتاج النسيج).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Gestion des Achats et Sourcing (تدبير المشتريات والبحث عن الممونين).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Gestion des Entreprises (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Gestion des entreprises.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Génie Civil (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Génie Industriel (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Génie Mécanique (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Génie Thermique (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Génie civil.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Génie climatique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Génie des matériaux.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Génie des procédés industriels.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Génie informatique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Génie Énergétique (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Génie électrique (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Génie électrique et énergies renouvelables.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Géomètre topographe.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Géosciences et géosciences appliquées à l''exploration minière.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Hébergement : Possibilité d''accès à l''internat pour les étudiants hors Casablanca (selon les places disponibles).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'I. Communication, Arts et Design').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'I. Écoles Supérieures Spécialisées (Arts, Communication et Technique)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'II. Classes Préparatoires et Formations Techniques (CPGE & BTS)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'II. Patrimoine, Tourisme et Industries Spécialisées').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'III. Filières d''Excellence et Techniques (CPGE & BTS)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'III. Métiers de l''Enseignement (ESEF)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'INBA (Beaux-Arts - Tétouan) & ESBA (Casablanca) :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'INBA (Tétouan) : Institut National des Beaux-Arts. Propose des départements en Art, Design Publicitaire et Bande dessinée.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'INSTITUT DE TECHNOLOGIE APPLIQUEE EL AIOUN SIDI MELLOUK : Assistant Administratif (1A). Pas d''internat.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'INSTITUT DE TECHNOLOGIE APPLIQUÉE EL AIOUN SIDI MELLOUK').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'INSTITUT SPECIALISE DE TECHNOLOGIE APPLIQUEE DEBDOU : Assistant Administratif (1A). Pas d''internat.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'INSTITUT SPÉCIALISÉ DE TECHNOLOGIE APPLIQUÉE DEBDOU').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'ISIC (Information et Communication - Rabat) :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'ISMAC (Audiovisuel et Cinéma - Rabat) :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'ISMAC (Cinéma et Audiovisuel - Rabat) :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'ISTA Bouarfa (Avec internat) : Électricité de maintenance industrielle, Assistant Administratif (1A), Arts culinaires (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'ISTA Industrie Agro-Alimentaire et Oléiculture Berkane (Avec internat) : Techniques d''horticulture, Industrie Agroalimentaire (Options Machines ou Procédés), Agro-industrie (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'ISTA Saïdia (Pas d''internat) : Agent socio-éducatif.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'IV. Offre Universitaire (Université Mohammed Premier)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'IV. Universités (Exemple de l''Université Mohammed Premier - Oujda)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Infographie prépresse (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Infographie.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Informatique et intelligence artificielle.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Infrastructure Digitale (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Infrastructure digitale.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Installation et Maintenance Biomédicale (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé dans les Métiers de Transport Routier').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée (ISTA) Nador').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée Ain Beni Mathar : Assistant Administratif (1A), Électricité industrielle (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée BNINSAR').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée El Aounia Oujda').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée El Aounia Oujda : Bâtiment, Assistant Administratif.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée Koulouche Oujda').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée Koulouche Oujda : Réparation des engins à moteur (Option : automobiles), Électricité de maintenance industrielle.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée Lazaret Oujda').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée Lazaret Oujda : Assistant Administratif.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée Sidi Maafa Oujda').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée Sidi Maafa Oujda (avec internat) : Électricité de maintenance industrielle, Froid commercial et climatisation, Fabrication mécanique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée Taourirt').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée Taourirt : Électricité de maintenance industrielle, Assistant Administratif (1A). Pas d''internat.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de Technologie Appliquée Zaio').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de l''Hôtellerie et de la Restauration Omar Ben Omar Oujda').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut Spécialisé de l''Hôtellerie et de la Restauration Omar Ben Omar Oujda : Arts culinaires, Service de Restaurant ''Arts de table'' (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut de Formation dans les Métiers de la Santé et de l''Action Sociale Oujda').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut de Formation dans les Métiers de la Santé et de l''Action Sociale Oujda : Assistant en cabinet de rééducation réhabilitation, Opérateur de stérilisation (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut de Technologie Appliquée (ITA) Al Aaroui Nador').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut de Technologie Appliquée Figuig (Pas d''internat) : Assistant Administratif (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut de Technologie Appliquée Laârassi Nador').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut spécialisé de l''hôtellerie et de tourisme').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Institut spécialisée de l''hôtellerie et de tourisme : Art de table service de restauration.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'L'' ESEF (École Supérieure d''Éducation et de Formation) prépare les futurs enseignants du primaire et du secondaire.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'L''ENSAD, affiliée à l''Université Hassan II de Casablanca, a pour mission de former des cadres moyens et supérieurs dans les métiers des arts et du design.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'L''ERA forme les officiers et sous-officiers pour les Forces Royales Air.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'L''ERG assure une formation de 2 ans sous régime d''internat.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'L''admission se fait sur la base de :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'La formation se déroule à l''Institut Royal de Police (IRP).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'La plupart des centres ne disposent pas d''internat, à l''exception de l''ISTA Sidi Maafa.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Le centre de formation assure la formation initiale et continue des sous-officiers de la Marine Royale.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Les candidats doivent classer leurs choix de filières par ordre de préférence.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Les facultés proposent des parcours diversifiés en accès ouvert ou régulé.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Management Agricole (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Management Hôtelier.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Management Touristique (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Management Touristique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Management hôtelier (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Mathématiques et applications.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Mathématiques, Informatique et Physique :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Matière et rayonnement.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Matières clés : Les notes en Français et en Anglais sont déterminantes pour le classement.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Matériaux et applications.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Matériaux organiques et inorganiques.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Moyenne pondérée : 75% du National et 25% du Régional.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Mécanique énergétique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Mécatronique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Méthodes en fabrication mécanique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Métiers du Cinéma et de l''Audiovisuel (مسلك مهن السينما والسمعي البصري).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Officiers : Formation de 4 ans à l''Académie Royale Militaire (ARM) de Meknès.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Ondes, matériaux et énergie.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Parcours : Droit Privé (Droit de l''Argent et des Affaires), Droit Public (Études Politiques et Internationales).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Parcours : Informatique et Intelligence Artificielle, Mathématiques et Applications.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Parcours : Littérature, Linguistique et Analyse du Discours.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Parcours : Littérature, Sciences du Langage.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Parcours : Matériaux Organiques et Inorganiques, Génie des Matériaux, Physique Moderne, Génie Électrique et Énergies Renouvelables, Mécanique Énergétique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Parcours : Politiques Économiques, Comptabilité, Contrôle et Audit, Banque et Assurance, Comptabilité, Finance et Fiscalité.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Parcours : Science de l''Environnement, Biologie : Sciences Biomédicales, Science et Biotechnologie des Plantes.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Parcours : Études Coraniques et Hadith, Études de la pensée et de la croyance, Études de Jurisprudence et Principes de la Religion.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Parcours : Études Culturelles, Linguistique, Littérature.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Parcours sans tronc commun : Management Portuaire et Logistique, Management des PME-PMI.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Photographie (مسلك الفوتوغرافيا).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Physique et Chimie :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Physique moderne.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Production et Qualité en Automobile (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Province d''Oujda').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Province de Berkane').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Province de Driouch').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Province de Figuig').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Province de Jerrada').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Province de Taourirt').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Préparateur en pharmacie (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Public concerné : Étudiants de la Région de l''Oriental et de la province d''Al Hoceima.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Qualité Hygiène Sécurité Environnement (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Radiologie diagnostique (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Radiophysique médicale.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Responsable d''exploitation logistique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Réparation des engins à moteur : Option automobiles.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Science de l''environnement.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Science et biotechnologie des plantes.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Sciences des données.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Sciences Économiques et de Gestion :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Secrétaire Médicale (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Service de Restauration (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Souhaitez-vous que je vous aide à comparer les options d''hébergement ou les spécialités entre ces différents centres de la province ?').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Spécialités : Art, Design publicitaire, Bande dessinée (INBA) ; Design d''intérieur, Publicité, Arts plastiques (ESBA).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Spécialités : Design Graphique, Photographie et Audiovisuel.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Spécialités : Enseignement primaire (incluant l''Amazigh) et secondaire (Mathématiques, Physique-Chimie, Français, Anglais, etc.).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Spécialités : Image, Son, Montage, Réalisation et Production.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Séries acceptées : Scientifiques, Littéraires, Artistiques et Techniques.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Tous les établissements de cette province listés ci-dessous ne disposent pas d''internat.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Transformation et valorisation des plantes aromatiques et médicinales (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Une copie de la CNI.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Une fois le délai expiré, aucune modification ou ajout de choix n''est possible.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Une photo d''identité.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Écologie et environnement.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Économie et Gestion : Économie régionale, Économétrie, Audit, Marketing digital, Comptabilité, Banque et Assurance.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Éducateur Spécialisé en Petite Enfance.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Électricité de Maintenance industrielle.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Électricité de maintenance industrielle.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Électricité industrielle (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Électricité industrielle.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Électromécanique des systèmes automatisés.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Énergies renouvelables et efficacité énergétique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Établissement	Domaines de formation').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Établissement	Filières principales').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Études Anglaises :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Études Arabes :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Études Françaises :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Études Islamiques :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Pôle Universitaire (Facultés - FSJESO Oujda)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Pôle Technologie et Excellence (CPGE & BTS)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Filières proposées').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Secteur Militaire et Sécurité').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Arts, Communication et Design').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Pôle Information, Arts et Design').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'École Nationale Supérieure d''Art et de Design (ENSAD)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Secteurs Technique, Touristique et Artisanal').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Offre de formation à la Faculté Pluridisciplinaire de Nador (FPN)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Pôle Patrimoine, Tourisme et Technique').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Offre de formation à Nador').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Offre de formation à Oujda (Suite)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Offre de formation à Taourirt').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'École Supérieure des Industries du Textile et de l''Habillement (ESITH)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Informations complémentaires').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Le Taux de Formation Professionnelle').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Présentation et Spécialités', 'Offre de formation à la Faculté des Sciences d''Oujda (FSO)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'AAT (Arts Traditionnels - Casablanca) : Formation en calligraphie arabe à la Mosquée Hassan II pour les bacheliers âgés de 18 à 30 ans.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Académie des Arts Traditionnels (AAT) : Située à la Mosquée Hassan II de Casablanca. Elle propose notamment une formation en calligraphie arabe accessible sur concours pratique et écrit pour les bacheliers de 18 à 30 ans.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Accès : Baccalauréat (toutes séries) avec une moyenne ≥ 14/20 et au moins 14/20 dans les langues (arabe, français, anglais).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Accès : Moins de 21 ans au 31 décembre. Sélection basée sur la moyenne du Bac et les notes dans les matières spécifiques.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Accès : Moins de 25 ans. Baccalauréat scientifique/technique (mention Bien) ou autre série avec une moyenne ≥ 14/20.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Admission : Basée sur une présélection (75% de la note du Bac) et un entretien oral (25%).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Basé sur les documents fournis pour l''année universitaire 2025/2026, voici une synthèse des opportunités de formation supérieure au Maroc, classées par pôle d''enseignement.🎨 Pôle Arts, Design et CommunicationCe pôle regroupe des établissements spécialisés dans les arts visuels, le cinéma et la communication.ESBA (Beaux-Arts - Casablanca) : Formation de 4 ans en Design (intérieur, publicitaire) et Arts plastiques. Sélection sur concours écrit et entretien oral avec présentation d''un porte-folio (Porte-folio).ENSAD (Art et Design - Mohammedia) : Licences en Design graphique, Audiovisuel et Photographie. Sélection via www.cursussup.gov.ma (75% National / 25% Régional).AAT (Arts Traditionnels - Casablanca) : Formation en calligraphie arabe à la Mosquée Hassan II pour les bacheliers de 18 à 30 ans.ISMAC (Cinéma et Audiovisuel - Rabat) : Filières Image, Son et Réalisation accessibles aux bacheliers de moins de 25 ans ayant une moyenne $\\ge$ 14/20.🏛️ Pôle Patrimoine, Tourisme et ÉducationINSAP (Archéologie - Rabat) : Cycle de 3 ans en Archéologie ou Anthropologie. Sélection sur concours écrit (traduction, langues) et test psychotechnique.ISIT (Tourisme - Tanger) : Management hôtelier et touristique. Moyenne au Bac $\\ge$ 14/20 pour l''hôtellerie et $\\ge$ 12/20 pour le tourisme.ESITH (Textile et Logistique - Casablanca) : Licences professionnelles avec des frais de scolarité de 25 000 DH/an.ESEF (Éducation - Oujda) : Forme aux métiers de l''enseignement primaire et secondaire. Sélection basée à 75% sur le dossier et 25% sur l''entretien oral.⚙️ Filières d''Excellence et Techniques (CPGE & BTS)CPGE (Classes Préparatoires) : Cycle de 2 ans préparant aux concours des grandes écoles (CNC/CNAEM). Filières : MPSI, PCSI (Ingénierie), TSI (Technique), ECT et ECS (Économie).BTS (Brevet de Technicien Supérieur) : Formation technique de 2 ans dans diverses spécialités (Maintenance, Gestion, Audiovisuel). Candidature sur ebts.men.gov.ma pour les moins de 23 ans.🎓 Pôle Universitaire (Université Mohammed Premier - Oujda & Nador)Les facultés proposent des licences en accès ouvert ou des parcours d''excellence.ÉtablissementDomaines et Parcours clésFSJESO (Oujda)Droit (Français/Arabe), Audit, Marketing digital, Banque et Assurance.FSHLA (Oujda)Langues (Anglais, Espagnol, Amazigh), Études islamiques, Géographie.FSO (Oujda)Intelligence Artificielle, Sciences des données, Énergies renouvelables.FPN (Nador)Management portuaire, Marketing analytique, Biologie biomédicale.Souhaitez-vous que je vous aide à préparer la liste des documents requis pour le dossier de candidature de l''une de ces écoles ?').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Basé sur les documents fournis, voici un aperçu détaillé des opportunités d’études supérieures au Maroc pour l’année universitaire 2025/2026, classées par domaine et par type de formation.I. Pôle Arts, Médias et TourismeCe pôle regroupe des instituts spécialisés dans la communication, le cinéma, les beaux-arts et le patrimoine.Information et Communication (ISIC - Rabat) : Formation de 3 ans (LMD) préparant aux métiers du journalisme et de la communication. Admission sur concours après l’obtention d’un Bac avec une moyenne minimale de 14/20.Audiovisuel et Cinéma (ISMAC - Rabat) : Propose des licences en Image, Son, Montage, Réalisation et Écriture. Les candidats doivent avoir moins de 25 ans et une moyenne au Bac $\\ge$ 14/20 (ou mention "Assez Bien" pour les filières techniques).Beaux-Arts (INBA - Tétouan & ESBA - Casablanca) : Formations de 4 ans en arts plastiques et design. Sélection sur concours écrit, épreuves pratiques (dessin, peinture) et entretien avec présentation d’un portfolio.Art et Design (ENSAD - Mohammedia) : Spécialités en Design Graphique, Photographie et Audiovisuel. Inscription via la plateforme nationale "Tawjih".Tourisme (ISIT - Tanger) : Management hôtelier et touristique. Moyenne au Bac requise $\\ge$ 14/20 pour l’hôtellerie et $\\ge$ 12/20 pour le tourisme.Archéologie et Patrimoine (INSAP - Rabat) : Études en archéologie et anthropologie pour les bacheliers de moins de 25 ans.II. Pôle Textile, Artisanat et ArchitectureIndustrie Textile (ESITH - Casablanca) : Licences professionnelles en habillement, textile et logistique. Formation payante (25 000 DH/an).Arts Traditionnels (AAT - Casablanca) : Formation en calligraphie arabe à la Mosquée Hassan II pour les 18-30 ans.Architecture et Urbanisme (IFTSAU - Oujda) : Formation de 2 ans pour les bacheliers scientifiques/techniques avec une moyenne $\\ge$ 12/20.III. Pôle Technique et Excellence (CPGE & BTS)Ces filières préparent soit aux grandes écoles d''ingénieurs, soit à une insertion professionnelle rapide.Classes Préparatoires (CPGE) : Cycle de 2 ans préparant aux concours nationaux (CNC/CNAEM) et français. Filières : MPSI, PCSI (Ingénierie), TSI (Technique), ECT et ECS (Économie). Sélection rigoureuse basée sur les notes du Bac.Brevet de Technicien Supérieur (BTS) : Formation technique de 2 ans dans diverses spécialités (Comptabilité, Électrotechnique, Audiovisuel, etc.). Admission sur la base de la moyenne du Baccalauréat.IV. Universités et Écoles NormalesL''image finale mentionne également les structures rattachées à l''Université Mohammed Premier d''Oujda :Facultés (FSO, FSJESO, FLSHO, FPN) : Sciences, Droit, Lettres et filières pluridisciplinaires.Enseignement (ENS & ESEF) : Écoles Normales Supérieures et Écoles Supérieures d''Éducation et de Formation pour les futurs enseignants.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Basé sur les documents fournis, voici une synthèse détaillée des opportunités de formation et de recrutement au Maroc pour l''année académique 2025/2026.🎖️ Pôle Défense et SécuritéCe secteur propose des carrières d''officiers et de sous-officiers avec des critères physiques et académiques précis.1. École Royale de l''Air (ERA) - MarrakechCycle des Officiers :Ingénieur (5 ans) : Ouvert aux bacheliers Sciences Mathématiques (orientés MP).Licence en Pilotage (4 ans) : Ouvert aux bacheliers Sciences Mathématiques ou Physiques.Conditions : Nationalité marocaine, célibataire, casier judiciaire vierge, âgé de 18 à 20 ans.Taille minimale : 1,65 m pour les garçons et 1,60 m pour les filles.2. École Royale de Gendarmerie (ERG)Formation : 2 ans (formation générale, militaire, juridique et technique).Conditions : Bacheliers toutes séries (année en cours ou précédente), âgés de 18 à 24 ans.Taille minimale : 1,70 m pour les garçons et 1,68 m pour les filles.3. Sûreté Nationale (DGSN) - Gardiens de la PaixFormation : 12 mois à l''Institut Royal de Police.Conditions : Bacheliers âgés de 21 à 30 ans.Taille minimale : 1,73 m (H) / 1,67 m (F).Vision : 15/10 sans lunettes ou lentilles (minimum 10/10 par œil).🎨 Pôle Arts, Design et CommunicationCes instituts supérieurs offrent des formations spécialisées dans les domaines créatifs.ÉtablissementFilières principalesCritères d''admissionISIC (Journalisme)Presse écrite, Audiovisuel, ComBac toutes séries, Moyenne $\\ge$ 14/20.ISMAC (Cinéma)Image, Son, Montage, RéalisationBac (mention "Assez Bien") ou Moyenne $\\ge$ 14/20.INBA (Beaux-Arts)Art, Design Publicitaire, BDConcours pratique (dessin, peinture) + oral.ENSAD (Design)Design Graphique, Photo, VidéoPrésélection (75% National, 25% Régional).🏛️ Pôle Patrimoine, Tourisme et TechniqueINSAP (Rabat) : Formation en Archéologie et Anthropologie. Accessible avec le Bac toutes séries, < 25 ans.ISIT (Tanger) : Management touristique et hôtelier. Moyenne Bac $\\ge$ 14/20 pour l''hôtellerie ou $\\ge$ 12/20 pour le tourisme.ESITH (Casablanca) : Textile, Habillement et Logistique. Frais de scolarité de 25 000 DH par an.AAT (Casablanca) : Académie des Arts Traditionnels (Calligraphie). Accessible aux bacheliers de 18 à 30 ans.🎓 Classes Préparatoires (CPGE)Les CPGE préparent en 2 ans aux concours des Grandes Écoles (CNC/CNAEM).Filières : MPSI, PCSI (Ingénierie), TSI (Technique), ECT, ECS (Économie).Condition : Moins de 21 ans au 31 décembre de l''année du concours.Débouchés : Accès aux écoles prestigieuses comme l''EMI, l''EHTP, l''ISCAE ou l''ENCG.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Basée sur l''ensemble des documents fournis pour l''année universitaire 2025/2026, voici une synthèse détaillée des opportunités de formation supérieure au Maroc.📚 I. Pôle Éducation et Enseignement (ESEF & ENS)Ces établissements forment les futurs cadres de l''enseignement primaire et secondaire via des cycles de Licence en Éducation (3 ans).1. Écoles Supérieures d''Éducation et de Formation (ESEF)Filières : Enseignement primaire (arabe ou amazighe) et spécialités du secondaire (Mathématiques, Physique-Chimie, Français, Anglais, Philosophie, etc.).Conditions d''accès : Être âgé de moins de 21 ans au moment de la présélection.Sélection : Présélection basée à 75% sur la moyenne du Baccalauréat et un entretien oral comptant pour 25%.2. Écoles Normales Supérieures (ENS)Localisations : Fès, Meknès, Rabat, Casablanca, Tétouan.Spécialités : Offre similaire aux ESEF avec l''ajout de filières comme l''Éducation physique et sportive (Casablanca et Tétouan).📜 II. Pôle Études Islamiques et Sciences de la ReligionCes facultés et instituts se spécialisent dans la théologie, la Charia et les études coraniques.Dar El Hadith El Hassania (Rabat) : Requiert un Baccalauréat avec mention (moyenne $\\ge$ 12/20) et une note minimale de 12/20 dans trois langues (Arabe, Français et une troisième langue).Institut Mohammed VI des Lectures et Études Coraniques (Rabat) : Nécessite d''être âgé de moins de 30 ans et d''avoir mémorisé l''intégralité du Coran.Facultés de la Charia (Fès, Agadir, Smara) : Accessibles avec tous types de Baccalauréat, avec respect de la distribution géographique pour certaines.🏛️ III. Pôle Patrimoine, Arts et TechniqueINSAP (Archéologie - Rabat) : Formation en 3 ans (Archéologie ou Anthropologie) accessible sur concours aux moins de 25 ans.Concours : Traduction Arabe-Français (coeff 2), Langue étrangère (coeff 1), et test psychotechnique (coeff 2).BTS (Brevet de Technicien Supérieur) : Formation technique de 2 ans dans des spécialités comme la Maintenance automobile, l''Audiovisuel ou la Comptabilité.Sélection : Priorité de 75% aux filières techniques et professionnelles.⚙️ IV. Classes Préparatoires aux Grandes Écoles (CPGE)Le cycle préparatoire de 2 ans prépare aux concours d''accès aux grandes écoles d''ingénieurs (CNC) et de commerce (CNAEM).Filières principales :MPSI : Orientée Mathématiques et Physique.PCSI : Orientée Physique et Chimie.TSI : Orientée Sciences Industrielles.ECT / ECS : Orientées Économie et Commerce.Conditions : Âge inférieur à 21 ans au 31 décembre de l''année de candidature.Débouchés : Écoles prestigieuses comme l''EMI, l''EHTP, l''ISCAE ou les réseaux ENSA/ENSAM.🎓 V. Offre Universitaire de l''Oriental (Université Mohammed Premier)L''université propose des parcours diversifiés à Oujda (FSO, FSJESO, FSHLA) et Nador (FPN).Sciences (FSO) : Parcours en IA, Data Science, Énergies renouvelables et Biotechnologies.Droit et Économie (FSJESO) : Droit en français/arabe, Marketing digital et Audit.Pluridisciplinaire (FPN Nador) : Management portuaire, Marketing analytique et Sciences biomédicales.Modalité de pré-inscription : Pour toutes ces facultés, l''enregistrement se fait sur entissab.ump.ma.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Candidats concernés : Bacheliers de toutes les provinces et préfectures du Royaume.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Conditions : Baccalauréat (toutes séries) de l''année en cours ou précédente, âge de 18 à 24 ans, et taille minimale de 1,70 m pour les garçons et 1,68 m pour les filles.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Conditions : Baccalauréat scientifique de l''année en cours ou des deux années précédentes, âge entre 18 et 23 ans, et taille minimale de 1,70 m (hommes) / 1,60 m (femmes).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Conditions : Baccalauréat toutes séries (année en cours ou précédente), moyenne générale ≥ 14/20, et note ≥ 14/20 en langues (Arabe, Français et Anglais).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Conditions : Baccalauréat, âge entre 21 et 30 ans, et taille minimale de 1,73 m (hommes) / 1,67 m (femmes).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Conditions : Moins de 25 ans. Moyenne ≥ 14/20 pour les filières scientifiques et techniques, ou mention "Assez Bien" pour les autres.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Conditions : Être célibataire, de nationalité marocaine, et mesurer au minimum 1,65 m pour les garçons et 1,60 m pour les filles.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Conditions de candidature : Avoir au minimum le niveau de la deuxième année complète du cycle du Baccalauréat et être âgé de moins de 30 ans au début de la formation.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Conformément à votre règle de gestion du serveur, j''ai ignoré tout le contexte précédent pour me concentrer uniquement sur la dernière capture d''écran fournie (image_c41204.png).Voici les détails concernant les classes de préparation au Brevet de Technicien Supérieur (BTS) pour la session 2025/2026 :🎓 Présentation du BTSLe BTS est une formation de deux ans dispensée dans des lycées techniques sélectionnés. Elle vise à former des techniciens hautement qualifiés, opérationnels immédiatement sur le marché du travail dans divers secteurs économiques.📝 Conditions et Modalités de CandidatureÂge : Ne pas dépasser 23 ans au 30 septembre de l''année du concours.Diplôme : Être titulaire du Baccalauréat (ou diplôme équivalent) dans une filière adaptée à la spécialité choisie.Inscription : S''effectue en ligne via le portail ebts.men.gov.ma ou via l''espace Moutamadris.Dossier (après acceptation) : Nécessite une copie certifiée du Bac, une copie de la CNI, un extrait d''acte de naissance et une enveloppe timbrée.🧪 Critères de SélectionLa sélection se base sur l''ordre de mérite selon les critères suivants :75 % de la note pour les filières techniques et professionnelles.25 % pour les autres filières.La capacité d''accueil est généralement limitée à 30 étudiants par classe.🛠️ Spécialités et Centres (Exemples de la Région de l''Oriental)Le document liste les spécialités disponibles selon le type de Baccalauréat et le centre d''examen :SpécialitéCentres d''Examen (Exemples)Baccalauréat Requis (Exemples)Maintenance AutomobileLycée Moulay Ismaïl (Meknès)Bac Sciences Maths, Physique ou TechniqueAudiovisuelLycée Al Laimoun (Rabat)Bac Toutes séries (avec priorités spécifiques)ÉlectrotechniqueLycée Al Maghrib Al Arabi (Oujda)Bac Sciences Maths ou Sciences TechniquesGestion ComptableLycée Al Maghrib Al Arabi (Oujda)Bac Sciences Économiques ou GestionTourismeLycée Zineb En-Nefzaouia (Sidi Slimane)Bac Toutes séries').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Cycle des Officiers : Propose un cycle ingénieur (5 ans) et une licence en pilotage (4 ans). Les candidats doivent être bacheliers de l''année en cours en Sciences Mathématiques (Ingénieur) ou Sciences Math/Physiques (Licence).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'D''après les documents fournis, voici une synthèse détaillée des principales opportunités de formation et de recrutement au Maroc pour l''année 2025/2026 :🎖️ I. Secteur Militaire et ParamilitaireCe secteur propose des formations d''officiers et de sous-officiers avec des critères de sélection rigoureux.InstitutionSpécialités / GradesConditions ClésInscriptionÉcole Royale de l''Air (ERA)Officiers (Ingénieur/Pilote) & Sous-officiersBac (Math/Phys), 18-20 ans, Taille $\\ge$ 1,65m (H) / 1,60m (F)recrutement.far.maMarine Royale (ERN)Sous-officiers (Fusiliers, Navigants)Bac Sci, 18-23 ans, Taille $\\ge$ 1,70m (H) / 1,60m (F)recrutement.far.maGendarmerie Royale (ERG)Élève Gendarme (2 ans de formation)Bac toutes séries, 18-24 ans, Taille $\\ge$ 1,70m (H) / 1,68m (F)recrutement.gr.maPolice (DGSN)Gardiens de la Paix (12 mois)Bac, 21-30 ans, Taille $\\ge$ 1,73m (H) / 1,67m (F), Vision 15/10concours.dgsn.gov.ma🎨 II. Arts, Design et CommunicationCes instituts forment aux métiers créatifs, aux médias et au cinéma.ISIC (Information et Communication) : Formation de 3 ans (LMD). Accessible avec un Bac (toutes séries) et une moyenne $\\ge$ 14/20. Inscription sur preinscription.isic.ma.ISMAC (Audiovisuel et Cinéma) : Licences en Image, Son, Réalisation ou Montage. Sélection basée sur une épreuve de culture générale, une épreuve de spécialité et l''Anglais.ENSAD (Art et Design) : Formation en Design Graphique, Cinéma et Photographie. Inscription via la plateforme nationale cursussup.gov.ma.Écoles des Beaux-Arts :INBA (Tétouan) : Spécialités Art, Design Publicitaire et BD. Admission sur concours pratique (dessin, peinture).ESBA (Casablanca) : Formation en Design d''intérieur, Publicité et Arts plastiques. Requiert un portfolio artistique lors de l''oral.🏛️ III. Patrimoine, Tourisme et TechniqueINSAP (Archéologie et Patrimoine) : Formation de 3 ans en Archéologie ou Anthropologie. Sélection sur concours écrit (traduction, langues) et test psychotechnique.ISIT (Tourisme et Hôtellerie) : Filières de Gestion hôtelière ou Management touristique. Présélection basée sur 75% du National et 25% du Régional.ESITH (Textile et Logistique) : Licence Professionnelle en 3 ans. Frais de formation annuelle de 25 000 DH.AAT (Arts Traditionnels) : Formation en calligraphie arabe à la Mosquée Hassan II. Ouvert aux bacheliers âgés de 18 à 30 ans.🎓 IV. Classes Préparatoires (CPGE)Les CPGE préparent aux grandes écoles d''ingénieurs (CNC) ou de commerce.Filières : MPSI (Maths/Physique), PCSI (Physique/Chimie), TSI (Technique), ECT et ECS (Économie).Conditions : Être scolarisé en année terminale du Bac, avoir moins de 21 ans.Inscription : Sur www.cpge.ac.ma ou via l''espace massarservice.men.gov.ma.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Définition et Conditions d''Accès').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'ENSAD (Art et Design - Mohammedia) : Licences en Design graphique, Audiovisuel et Photographie. Inscription via www.cursussup.gov.ma avec une sélection basée sur la moyenne du Bac (75% National, 25% Régional).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'IFTSAU (Oujda) : Institut de Formation des Techniciens Spécialisés en Architecture et Urbanisme. Formation de 2 ans pour les bacheliers scientifiques/techniques avec une moyenne ≥ 12/20.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'INSAP (Archéologie - Rabat) : Cycle de 3 ans en Archéologie ou Anthropologie. Sélection par concours (traduction, langues) pour les bacheliers de moins de 25 ans.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'INSAP (Archéologie - Rabat) : Formation en Archéologie et Anthropologie pour les bacheliers de moins de 25 ans. Sélection par écrit (traduction, langues) et test psychotechnique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'INSAP (Archéologie - Rabat) : Formation en Archéologie et Anthropologie. Accessible avec le Bac (toutes séries) pour les moins de 25 ans. Sélection sur épreuves de traduction et test psychotechnique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'ISIC (Rabat) : Institut Supérieur de l''Information et de la Communication. Formation en 3 ans (Licence) accessible avec un baccalauréat (moyenne ≥ 14/20). Inscription sur preinscription.isic.ma.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'ISIT (Tourisme - Tanger) : Management hôtelier et touristique. Moyenne au Bac requise ≥ 14/20 (Filière opérationnelle) ou ≥ 12/20 (Gestion touristique).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'ISIT (Tourisme - Tanger) : Management hôtelier et touristique. Moyenne au Bac ≥ 14/20 pour la filière hôtelière et ≥ 12/20 pour la filière touristique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'ISIT (Tourisme - Tanger) : Management hôtelier et touristique. Moyenne minimale au Bac : 14/20 pour la filière opérationnelle et 12/20 pour le management touristique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Les documents fournis détaillent les conditions d''accès, les procédures de sélection et les programmes de formation pour divers établissements d''enseignement supérieur et de recrutement au Maroc pour l''année universitaire 2025/2026.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Note importante : Les bacheliers en Sciences Économiques et Gestion ne peuvent postuler que pour les filières "Gestion des Achats & Sourcing" et "Gestion de la Chaîne Logistique".').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'OU être titulaire du Baccalauréat de l''année précédente.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Pour les titulaires d''un Baccalauréat étranger, ils doivent télécharger une copie du diplôme, de l''équivalence et de la CNI sur la plateforme.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Présélection : Calculée selon le mérite sur la base de la moyenne pondérée du Baccalauréat (75% National et 25% Régional), avec application d''un coefficient spécifique à chaque filière de Bac.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Sous-Officiers : Formation de 2 ans à Ben Slimane pour les bacheliers âgés de 18 à 24 ans.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Sur la base des documents fournis, voici un récapitulatif complet des opportunités de formation supérieure au Maroc pour l''année universitaire 2025/2026, incluant les conditions d''accès et les modalités d''inscription.🎨 Arts, Design et CommunicationCe pôle regroupe des établissements spécialisés dans les arts visuels, le design et les médias.ESBA (Beaux-Arts - Casablanca) :Formation : 4 ans d''études divisés en deux cycles, spécialités : Design d''intérieur, Design publicitaire, Arts plastiques.Conditions : Baccalauréat (toutes séries), âge entre 17 et 25 ans.Sélection : Phase 1 (Tests écrits en culture générale, dessin et arts plastiques) ; Phase 2 (Entretien oral de 10-20 min avec présentation d''un porte-folio).ENSAD (Art et Design - Mohammedia) :Filières : Design graphique et numérique, Cinéma et audiovisuel, Photographie.Sélection : Basée sur la moyenne du Bac (75% National, 25% Régional) via la plateforme www.cursussup.gov.ma.AAT (Arts Traditionnels - Casablanca) :Spécialité : Art de la calligraphie arabe.Conditions : Nationalité marocaine, âge de 18 à 30 ans, bacheliers ayant validé au moins deux années d''études supérieures.Dossier : Doit inclure 3 modèles de calligraphie ou d''ornementation réalisés par le candidat.🏛️ Patrimoine, Tourisme et Industries SpécialiséesINSAP (Archéologie - Rabat) :Formation : Tronc commun de 2 ans suivi d''une année de spécialisation en Archéologie ou Anthropologie.Sélection : Concours écrit incluant une traduction (Arabe vers Français), un test de langue étrangère (Anglais ou Espagnol) et un test psychotechnique.ISIT (Tourisme - Tanger) :Filières : Management opérationnel de l''hôtellerie et de la restauration (Moyenne Bac $\\ge$ 14/20) ; Management touristique (Moyenne Bac $\\ge$ 12/20).Conditions : Moins de 25 ans au moment du concours.ESITH (Textile et Logistique - Casablanca) :Licence Professionnelle : Filières en développement textile, habillement, et gestion de la chaîne logistique.Frais : Contribution aux frais de formation de 25 000 DH/an, payable en deux tranches.⚙️ Filières d''Excellence et Techniques (CPGE & BTS)CPGE (Classes Préparatoires) :Filières : MPSI, PCSI (Ingénierie) ; TSI (Technique) ; ECT, ECS (Économie).Débouchés : Préparation aux concours nationaux (CNC) et aux concours des écoles de commerce (CNAEM).Inscription : Via www.cpge.ac.ma ou l''espace Moutamadris.BTS (Brevet de Technicien Supérieur) :Formation : 2 ans dans diverses spécialités (Maintenance, Électrotechnique, Gestion, Tourisme, etc.).Candidature : En ligne sur ebts.men.gov.ma. Sélection basée à 75% sur les filières techniques et professionnelles.🎓 Pôle Universitaire (Université Mohammed Premier - Oujda)Les facultés proposent des licences en accès ouvert ou des parcours d''excellence.FacultéFilières de Licence (Exemples)FSJESO (Droit/Éco)Droit des affaires, Audit et contrôle de gestion, Marketing digital, Banque et assurance.FSO (Sciences)Intelligence artificielle, Sciences des données, Énergies renouvelables, Génie informatique.FSHLA (Lettres)Études islamiques, Langues (Anglais, Espagnol, Amazigh), Médiation culturelle.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Sélection : Baccalauréat requis (priorité de 75% aux filières techniques/professionnelles). Inscription sur ebts.men.gov.ma.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Sélection : Basée sur la moyenne du Bac avec une priorité de 75% pour les filières techniques et professionnelles.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Taille minimale : 1,70 m pour les hommes.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Un certificat de scolarité de la 2ème année du Bac.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Voici un aperçu des opportunités de formation et de recrutement pour l''année 2025/2026 au Maroc, basé sur les documents fournis :🎖️ Secteur Militaire et ParamilitaireCe secteur propose des formations de Sous-officiers (Sergent) d''une durée de 2 à 3 ans et des formations d''Officiers de 4 à 5 ans.ÉtablissementGrade / DuréeConditions ClésInscriptionÉcole Royale de l''Air (ERA)Sergent (3 ans) / Officier (4-5 ans)Bac, 18-23 ans, Taille $\\ge$ 1.65m (H) / 1.60m (F)recrutement.far.maMarine Royale (ERN)Sergent (3 ans)Bac Sci, 18-23 ans, Taille $\\ge$ 1.70m (H) / 1.60m (F)recrutement.far.maForces Auxiliaires (FA)Sergent (2 ans) / Officier (4 ans)Bac, 18-23/24 ans, Taille $\\ge$ 1.70m (H)recrutement.fa.gov.maGendarmerie Royale (ERG)Élève Gendarme (2 ans)Bac, 18-24 ans, Taille $\\ge$ 1.70m (H) / 1.68m (F)recrutement.gr.ma👮 Sûreté Nationale (DGSN)La formation pour les Gardiens de la Paix dure 12 mois à l''Institut Royal de Police.Conditions : Baccalauréat, âge entre 21 et 30 ans.Physique : Taille min 1.73m (H) / 1.67m (F) et vision 15/10 sans correction.Inscription : concours.dgsn.gov.ma.🎨 Arts, Audiovisuel et CommunicationCes instituts supérieurs proposent des licences en 3 ou 4 ans.ISIC (Information & Com.) : Admission avec Bac (toutes séries), moyenne $\\ge$ 14/20. Inscription sur preinscription.isic.ma.ISMAC (Cinéma) : Filières techniques (Bac Sci/Tech) ou artistiques (Bac toutes séries, moy $\\ge$ 14/20). Site : ismac.ac.ma.INBA (Beaux-Arts Tétouan) : Admission sur concours écrit (français/arabe), pratique (dessin/peinture) et entretien. Inscription par courrier.ESBA (Beaux-Arts Casa) : Formation en 4 ans (Design intérieur, publicitaire, Arts plastiques).ENSAD (Art & Design) : Inscription via la plateforme cursussup.gov.ma.🏗️ Architecture, Textile et ArtisanatIFTSAU (Urbanisme & Architecture) : Formation de 2 ans à Oujda. Bac Sci/Tech requis avec moyenne $\\ge$ 12/20. Site : muat.gov.ma.ESITH (Textile & Logistique) : Licence pro (3 ans). Bac Sci ou Éco. Frais de scolarité : 25 000 DH/an. Site : esith.ac.ma.Académie des Arts Traditionnels (AAT) : Située à la Mosquée Hassan II (Casa). Formation en Calligraphie arabe. Âge entre 18 et 30 ans. Inscription sur aat.ac.ma.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Voici un récapitulatif complet et organisé de toutes les opportunités de formation et de recrutement présentées dans vos documents pour l''année 2025/2026.🎖️ I. Pôle Défense et Sécurité (FAR, Gendarmerie, Police)Ce secteur se divise en deux parcours : les Officiers (encadrement, formation longue) et les Sous-officiers (technique, formation courte).1. École Royale de l''Air (ERA) - MarrakechOfficiers : Cycle Ingénieur (5 ans) ou Licence Pilote (4 ans). Bac Math/Physique requis.Sous-officiers (Sergent) : Formation de 3 ans (Contrôleur aérien, Anglais, etc.).Conditions : Célibataire, taille min 1,65m (H) / 1,60m (F).Lien : recrutement.far.ma2. Gendarmerie Royale (ERG)Formation : 2 ans (internat).Conditions : Bac toutes séries, 18-24 ans. Taille min : 1,70m (H) / 1,68m (F).Lien : recrutement.gr.ma3. Sûreté Nationale (DGSN - Gardiens de la Paix)Formation : 12 mois à l''Institut Royal de Police.Conditions : Bac, 21-30 ans. Taille : 1,73m (H) / 1,67m (F).Santé : Vision de 15/10 cumulée sans correction.Lien : concours.dgsn.gov.ma🎨 II. Pôle Arts, Design et CommunicationCes instituts forment aux métiers créatifs et aux médias.InstitutSpécialitésConditionsISICJournalisme, CommunicationBac toutes séries, moyenne $\\ge$ 14/20.ISMACCinéma, Son, Image, RéalisationBac Sci/Tech ou moyenne $\\ge$ 14/20.INBABeaux-Arts, Design, BDConcours écrit + épreuves de dessin/peinture.ESBADesign d''intérieur, Publicité, ArtsConcours + entretien avec Portfolio.ENSADDesign Graphique, PhotographiePrésélection (75% National / 25% Régional).🏛️ III. Pôle Patrimoine, Tourisme et TechniqueINSAP (Rabat) : Archéologie et Patrimoine. Bac toutes séries, < 25 ans. Épreuves : Traduction, Langue et test psycho-technique.ISIT (Tanger) : Management hôtelier et touristique. Sélection sur moyenne du Bac et écrit (Anglais/Français/Culture).ESITH (Casablanca) : Textile, Habillement et Logistique. Licence Pro (3 ans). Frais : 25 000 DH/an.AAT (Casablanca) : Arts Traditionnels (Calligraphie). 18-30 ans. Test pratique de calligraphie/ornementation.🎓 IV. Classes Préparatoires et BTSL''image image_c40e44.png rappelle l''existence des filières :CPGE : Classes Préparatoires aux Grandes Écoles (2 ans pour préparer les concours d''ingénieurs).BTS : Brevet de Technicien Supérieur (2 ans pour une insertion professionnelle rapide).💡 Points de vigilance pour vos dossiers :Dates : La plupart des inscriptions ferment entre mai et juillet.Moyenne : Pour les écoles de design et communication (ISIC, ISMAC), une moyenne de 14/20 est souvent le seuil minimal de présélection.Santé : Pour le militaire et la police, vérifiez votre vision et votre taille avant de postuler pour éviter une élimination directe.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Voici une synthèse complète et structurée de toutes les opportunités de formation et de recrutement présentées dans vos documents pour l''année 2025/2026.🎖️ I. Pôle Défense et Sécurité (FAR, Gendarmerie, Police)Ce secteur est divisé en deux niveaux : les Officiers (formation longue, encadrement) et les Sous-officiers (formation technique, terrain).1. Armée et Gendarmerie (FAR / ERG)École Royale de l''Air (ERA) :Officiers : Cycle Ingénieur (5 ans) ou Licence Pilote (4 ans). Bac Math/Physique requis.Sous-officiers : 3 ans de formation. Taille min : 1,65m (H) / 1,60m (F).Gendarmerie Royale (ERG) : Formation de 2 ans. Bac toutes séries. Taille min : 1,70m (H) / 1,68m (F). Inscription sur recrutement.gr.ma.Marine Royale (ERN) : Formation de 3 ans (Sergent). Bac Scientifique requis.2. Sûreté Nationale (DGSN)Gardiens de la Paix : Formation de 12 mois.Conditions : Bac, 21-30 ans. Taille : 1,73m (H) / 1,67m (F).Aptitude : Vision de 15/10 sans correction.🎨 II. Pôle Arts, Communication et DesignCes instituts exigent souvent un fort bagage culturel et artistique.InstitutSpécialitésConditions d''accèsISICJournalisme, CommunicationBac toutes séries, moyenne $\\ge$ 14/20.ISMACImage, Son, Réalisation, MontageBac Sci/Tech ou moyenne $\\ge$ 14/20.INBABeaux-Arts, Design, Bande dessinéeConcours écrit + pratique (dessin/peinture).ESBADesign d''intérieur, Publicité, ArtsConcours + présentation du portfolio.ENSADDesign Graphique, PhotographiePrésélection (75% National / 25% Régional).🏛️ III. Pôle Patrimoine, Tourisme et TechniqueINSAP (Archéologie) : Formation de 3 ans. Bac toutes séries, < 25 ans. Épreuves : Traduction (Fr/Ar), Langue étrangère et test psycho-technique.ISIT (Tourisme) : Gestion hôtelière et touristique. Moyenne Bac $\\ge$ 14/20 (Filière hôtelière) ou $\\ge$ 12/20 (Filière touristique).ESITH (Textile & Logistique) : Licence Pro (3 ans). Bac Sci/Éco. Frais : 25 000 DH/an.AAT (Arts Traditionnels) : Formation en Calligraphie arabe à la Mosquée Hassan II (Casa). 18-30 ans.💡 Synthèse des Liens d''InscriptionMilitaire : recrutement.far.maGendarmerie : recrutement.gr.maSûreté Nationale : concours.dgsn.gov.maDesign/Art (ENSAD) : cursussup.gov.maVoulez-vous que je vous aide à préparer une "Demande').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Être inscrit en année terminale du Baccalauréat pour l''année en cours.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat Scientifique ou Économique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'I. Sciences Humaines, Éducation et Études IslamiquesCe pôle regroupe les établissements formant aux métiers de l''enseignement, du droit et de la théologie.1. Éducation et Enseignement (ESEF)Les Écoles Supérieures d’Éducation et de Formation préparent aux métiers de l''enseignement primaire et secondaire.Spécialités : Enseignement primaire (langue arabe ou amazighe) et secondaire (Maths, Physique-Chimie, SVT, Informatique, Français, Anglais, Histoire-Géo, etc.).Admission : Moins de 21 ans au moment de la présélection. Sélection basée sur une présélection sur dossier (75%) et un entretien oral (25%).2. Études Islamiques et Sciences de la ReligionÉtablissements : Facultés d''Oul Al-Dine (Tétouan), des Sciences de la Charia (Smara), de la Charia (Fès/Agadir), Dar El Hadith El Hassania, et l''Institut Mohammed VI des Lectures et Études Coraniques.Conditions spécifiques (Dar El Hadith El Hassania) : Avoir le Bac avec une moyenne $\\ge$ 12/20 et une note $\\ge$ 12/20 en langues (Arabe, Français, Anglais/Espagnol). Un test de mémorisation du Coran est requis pour certaines institutions.🎨 II. Patrimoine, Arts et TourismeDes établissements spécialisés pour les carrières dans la conservation et la création.INSAP (Rabat) : Institut National des Sciences de l’Archéologie et du Patrimoine.Formation : Cycle de 3 ans (Tronc commun de 2 ans + 1 an de spécialisation en Archéologie ou Anthropologie).Concours : Traduction Arabe-Français (coeff 2), Langue étrangère (coeff 1), et test psychotechnique (coeff 2). Moins de 25 ans à la clôture des inscriptions.Arts Traditionnels (AAT Casablanca) : Formation en calligraphie arabe à la Mosquée Hassan II. Ouvert aux bacheliers de 18 à 30 ans sur présentation de 3 modèles de travaux personnels.⚙️ III. Excellence Technique et Professionnelle (CPGE & BTS)Ces filières constituent des passerelles vers les grandes écoles d''ingénieurs ou une insertion rapide.1. Classes Préparatoires (CPGE)Objectif : Préparation aux concours nationaux (CNC) et français pour les grandes écoles.Filières : MPSI (Maths-Physique), PCSI (Physique-Chimie), TSI (Technique), ECT (Économie-Commerce option technologique), et ECS (option scientifique).Débouchés : Accès aux écoles prestigieuses (EMI, EHTP, ERA, ERN, ENSA, ISCAE, ENCG, etc.).Inscription : Sur www.cpge.ac.ma ou l''espace Moutamadris. Âge maximum : 21 ans au 31 décembre.2. Brevet de Technicien Supérieur (BTS)Formation : 2 ans dans des lycées techniques spécialisés (Maintenance automobile, Audiovisuel, Gestion comptable, Tourisme, Électrotechnique, etc.).Admission : Bacheliers de moins de 23 ans au 30 septembre. Sélection basée sur la moyenne du Bac (75% pour les filières techniques et professionnelles).🎓 IV. Offre Universitaire (Région de l''Oriental)L''Université Mohammed Premier propose des parcours diversifiés à Oujda et Nador.ÉtablissementDomaines et Parcours de LicenceFSJESO (Oujda)Droit (Public/Privé en Arabe et Français), Économie régionale, Marketing digital, Audit, Banque.FSHLA (Oujda)Études Islamiques, Langues (Arabe, Français, Anglais, Espagnol, Amazigh), Géographie, Histoire, Philosophie.FSO (Oujda)Agro-sciences, Biotechnologie, IA, Data Science, Énergies renouvelables, Radiophysique médicale.FPN (Nador)Management portuaire, Marketing analytique, Biologie biomédicale, Gestion des PME.Modalité de pré-inscription : Pour toutes ces facultés, le pré-enregistrement s''effectue obligatoirement sur le site http://entissab.ump.ma.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Centres de Formation et Filières (Technicien Spécialisé)Le document détaille les établissements par province, la disponibilité d''un internat et les filières proposées :ProvinceÉtablissementInternatFilières proposéesBerkaneISTA* AhfirNONGestion des entreprises, Développement Digital.ISTA BerkaneOUIÉlectromécanique, Éducateur spécialisé en petite enfance, Gestion des entreprises, Techniques de développement informatique, Secrétariat de direction, Commerce, Réseaux informatiques.ISTA Industrie Agro-Alimentaire (Berkane)OUIFabrication agroalimentaire, Hygiène et Qualité, Emballage et Conditionnement, Technologie des Aliments.ISTA SaïdiaNONÉducateur spécialisé en petite enfance.DriouchISTA MidarNONGestion des entreprises.FiguigISTA BouarfaOUIGestion des entreprises, Infrastructure Digitale.GuercifISTA Guercif / TaddartOUI/NONGestion des entreprises.JerradaISTA JerradaNONGestion des entreprises, Éducateur spécialisé, Électromécanique, Génie topographique.ISTA Ain Beni MatharNONGestion des entreprises.*ISTA : Institut Spécialisé de Technologie Appliquée📝 Points clés à retenir :Hébergement : Les centres de Berkane (partiellement), Bouarfa et Guercif disposent d''un internat, ce qui est crucial pour les étudiants venant de zones éloignées.Diversité des filières : La province de Berkane offre la plus grande variété, incluant des spécialisations uniques en Agro-industrie.Digital : Les filières "Développement Digital" et "Infrastructure Digitale" sont présentes pour répondre aux besoins technologiques actuels.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Conditions d''Accès', 'Conditions de Candidature').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'CPGE (Classes Préparatoires) : Cycle de 2 ans préparant aux concours nationaux (CNC) pour les grandes écoles d''ingénieurs (ex: EMI, EHTP) et de commerce (CNAEM). Filières : MPSI, PCSI, TSI, ECT, ECS.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Ce pôle prépare aux concours des grandes écoles ou à une insertion professionnelle technique rapide.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Classement : Les candidats sont classés par ordre de mérite pour l''accès aux épreuves suivantes du concours.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Débouchés : Accès aux grandes écoles marocaines (EMI, EHTP, ENSA, ISCAE, ENCG) via les concours CNC ou CNAEM.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Débouchés : Concours CNC (Écoles d''ingénieurs comme EMI, EHTP) ou CNAEM (Écoles de commerce comme ENCG, ISCAE).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'ESBA (Beaux-Arts - Casablanca) : Formation de 4 ans en Design et Arts Plastiques. Admission pour les 17-25 ans après un concours écrit et un entretien avec présentation d''un porte-folio (Porte-folio).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Filières : Image, Son, Montage, Réalisation et Écriture.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'ISIT (Tanger) : Institut Supérieur International de Tourisme. Forme aux métiers de l''hôtellerie, de la restauration et du management touristique. Inscription sur www.concours.isit.ma.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'ISMAC (Rabat) : Institut Supérieur des Métiers de l''Audiovisuel et du Cinéma. Propose des licences en Image, Son, Montage, Réalisation, etc. Sélection sur écrit (culture générale, spécialité, anglais) et oral.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'ISTA Berkane (Avec internat) : Électricité de maintenance industrielle, Assistant administratif, Technicien Comptable d''Entreprises, Technicien en réparation des engins à moteur (Option automobiles), Froid industriel, Agent technique de vente, Agent d''entretien en froid et génie thermique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'L''admission se fait par voie de concours après une phase de présélection :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Souhaitez-vous que je vous explique comment fonctionne le coefficient de pondération (75%/25%) pour maximiser vos chances de présélection ?').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Sélection : Présélection sur dossier, examen écrit (sujet d''actualité) et entretien oral.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Sélection : Présélection sur dossier, épreuve écrite (3h) et entretien oral.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Sélection : Présélection, écrit (culture générale, spécialité, anglais) et oral (projet professionnel).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Sélection : Via la plateforme cursussup.gov.ma (75% National / 25% Régional).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Sélection : Épreuves écrites (langues), pratiques (dessin, peinture) et entretien avec présentation d''un portfolio artistique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Sélection : Étude de dossier, tests médicaux, psychotechniques et épreuves sportives.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Épreuves : Écrit (QCM ou sujet général), oral et une course de 1 500 m.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Épreuves : Écrit (langues), pratique (dessin et peinture) et entretien avec présentation d''un portfolio artistique (Porte-folio).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Processus de Sélection', 'Procédure de Sélection').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'BTS (Brevet de Technicien Supérieur) :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'BTS (Brevet de Technicien Supérieur) : Formation technique de 2 ans dans des spécialités telles que la maintenance, l''électrotechnique ou l''audiovisuel. Inscription sur ebts.men.gov.ma pour les moins de 23 ans.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Basé sur les documents fournis, voici une synthèse détaillée des opportunités d’études supérieures au Maroc pour l’année universitaire 2025/2026.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Centre de Formation dans les métiers de l''Automobile OUJDA : Technicien en Peinture Automobile, Technicien en Réparation des Engins à Moteur (Option : Automobile).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Ces parcours sont destinés aux étudiants visant une spécialisation poussée ou l''accès aux grandes écoles d''ingénieurs et de commerce.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Cette section se concentre sur les parcours menant aux diplômes techniques professionnels.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'D''après la dernière capture d''écran fournie (image_c47f22.png), voici les informations concernant les centres de formation et les filières pour le diplôme de Technicien Spécialisé dans la province d''Oujda pour l''année 2025/2026. Tous les établissements listés ci-dessous ne disposent pas d''internat.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'D''après les documents fournis, voici les informations concernant le diplôme de Technicien (1/3) pour la région de l''Oriental (saison 2025/2026).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Diplôme du Technicien (DT).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Diplôme du Technicien Spécialisé (DTS).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Diplômes préparés :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Durée : La formation est sanctionnée par un diplôme de Technicien après deux ans d''études.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'ENSAD (Mohammedia) : École Nationale Supérieure d''Art et de Design. Filières en Design Graphique, Cinéma/Audiovisuel et Photographie. Inscription via www.cursussup.gov.ma.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'ESITH (Casablanca) : École Supérieure des Industries du Textile et de l''Habillement. Propose des licences professionnelles en habillement, textile et logistique. Frais de formation : 25 000 DH/an.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'ESITH (Textile et Logistique - Casablanca) : Licence professionnelle (3 ans). Frais de scolarité : 25 000 DH/an.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'ESITH (Textile et Logistique - Casablanca) : Licence professionnelle (3 ans). Frais de scolarité de 25 000 DH/an.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'ESITH (Textile et Logistique - Casablanca) : Propose des licences professionnelles en développement textile et habillement. La formation est payante à hauteur de 25 000 DH par an.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Filières : Technicien Comptable d''Entreprises, Assistant Administratif. Pas d''internat.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Formation : Cycle LMD (3 ans) débouchant sur une licence en Information et Communication.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Formation : Cycle LMD (3 ans) pour un diplôme en journalisme ou communication.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'ISTA Ahfir (Pas d''internat) : Technicien Comptable d''Entreprises, Assistant administratif.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'ISTA Midar (Pas d''internat) : Technicien Comptable d''Entreprises, Assistant administratif.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'ITSGC : Institut de Formation des Techniciens Spécialisés en Génie Civil. Admission sur QCM de mathématiques et langues.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Institut Spécialisé dans les Métiers de Transport Routier (avec internat) : Moniteur auto-école, Technicien en Réparation des Engins à Moteur (Option : Poids Lourds et Autocars).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Institut Spécialisé de Technologie Appliquée Jerrada : Technicien Comptable d''Entreprises, Électricité de maintenance industrielle, Assistant Administratif (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Institut de Technologie Appliquée de Transformation des Dattes Figuig (Avec internat) : Technicien en valorisation des dattes.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'L''ESITH forme des cadres destinés aux secteurs du textile, de l''habillement et de la logistique. La formation débouche sur un diplôme de Licence Professionnelle après 3 ans d''études.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'L''enseignement est organisé par domaines, avec des Troncs Communs (S1-S4) menant à diverses spécialités de Licence (S5-S6).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'L''enseignement est structuré en Troncs Communs (S1-S4) suivis de parcours de Licence (S5-S6).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'L''offre de formation supérieure au Maroc pour l''année universitaire 2025/2026 est diversifiée, couvrant les domaines des arts, de l''ingénierie, de l''éducation et des sciences universitaires. Voici une synthèse structurée basée sur les documents fournis.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'La faculté propose des licences dans les domaines juridiques et économiques.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Le cursus de formation s''étale sur 4 semestres (2 ans) d''études fondamentales, suivis d''une spécialisation pour l''obtention du diplôme dans l''une des filières suivantes :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Le cycle Licence Professionnelle propose les spécialités suivantes :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Les facultés proposent des licences en accès ouvert ou des parcours d''excellence.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Les relevés de notes des 3 années du lycée (Contrôle continu et Régional).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Licence d''Excellence : Marketing et Gestion de l''Analyse de Données (Marketing et Data Analytics Gestion).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Objectif : Les établissements de formation professionnelle visent à former des ouvriers spécialisés et des techniciens qualifiés grâce à des cours théoriques et pratiques pour faciliter leur intégration dans divers secteurs économiques (industrie, commerce, agriculture, social).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Parcours de Licence :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Parcours de Licence : Développement informatique.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Sur la base des documents fournis, voici les données détaillées extraites de la dernière capture d''écran (image_c41cae.png) concernant la Faculté Pluridisciplinaire de Nador (FPN) pour l''année universitaire 2024/2023 :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Technicien (2/3) dans la province de Nador pour l''année 2025/2026 :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Technicien (3/3) dans les provinces de Jerrada, Oujda et Taourirt pour l''année 2025/2026 :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Technicien Comptable d''Entreprises.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Technicien Spécialisé Géomètre Topographe (1A).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Technicien Spécialisé dans les provinces d''Oujda et Taourirt pour l''année 2025/2026 :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Technicien en réparation des engins à moteur : Option automobiles.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Technicien spécialisé d''exploitation en transport.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Technicien spécialisé en Diagnostic et Electronique Embarquée.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Voici les données extraites de la dernière capture d''écran (image_c47e89.png) concernant les centres de formation et les filières de Technicien Spécialisé dans la province de Nador pour 2025/2026 :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'le M Institut de Formation dans le Domaine de la Santé (IFPS) d''Oujda pour l''année 2025 :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Cursus et Filières').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Offre de formation par province (Niveau Technicien)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Offre de formation à Nador (Niveau Technicien)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'Offre de formation à Oujda (Technicien Spécialisé)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Durée et Diplôme', 'www.cursussup.gov.ma').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'AAT (Arts Traditionnels - Casablanca) : Formation en calligraphie arabe à la Mosquée Hassan II pour les 18-30 ans. Inscription incluant la soumission de 3 modèles de calligraphie ou d''ornementation.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Adresse : Avenue Hassan II, BP 150 Mohammedia (Siège de la présidence de l''Université Hassan II).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'C''est un dossier extrêmement complet que vous avez là ! En suivant votre règle, je me concentre sur la dernière capture d''écran (image_c40a23.png) concernant l''École Supérieure des Industries du Textile et de l''Habillement (ESITH) de Casablanca.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Coût : Une contribution aux frais de formation de 25 000 DH par an est demandée (payable en deux tranches).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Frais de dossier : 500 DH à verser sur le compte de l''ESITH (le reçu doit être conservé).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Inscription : La pré-inscription se fait via la plateforme électronique http://entissab.ump.ma.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Inscription : Les candidatures s''effectuent sur le site www.inscription.ofppt.ma durant la période fixée.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Inscription : Via www.cpge.ac.ma ou l''espace Moutamadris.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'L''inscription se fait en ligne via le lien : http://urlz.fr/iib5. Le dossier doit comprendre :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'L''inscription se fait obligatoirement en ligne via la plateforme nationale de gestion des accès (Tawjih) :').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'L''étude du dossier scolaire (Projet professionnel et motivations).').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Plateforme d''inscription : Le pré-enregistrement s''effectue sur le site http://entissab.ump.ma.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Site Web : www.ensad.ma').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Souhaitez-vous que je vous aide à trouver les dates de début des inscriptions pour ces centres de formation professionnelle ?').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Technico-Commercial en Vente de Véhicules et Pièces de Rechange.').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Voulez-vous que je vous aide à préparer le dossier de candidature ou la lettre de motivation pour l''un de ces établissements ?').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Frais de scolarité et Avantages').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Modalités d''Inscription').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Modalités d''Inscription (Procédure numérique)').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Contact').
info_etablissement('École Nationale Supérieure d''Art et de Design (ENSAD)', 'Inscription, Contact et Divers', 'Modalités d''Inscription').
nouvel_etablissement('ISSS', 'SANTÉ ET PARAMÉDICAL').
info_etablissement('ISSS', 'Présentation et Spécialités', 'L''institut propose plusieurs spécialités de santé très demandées sur le marché de l''emploi :').
info_etablissement('ISSS', 'Présentation et Spécialités', 'Le processus de recrutement est rigoureux et comprend trois étapes :').
info_etablissement('ISSS', 'Présentation et Spécialités', 'Sage-femme.').
info_etablissement('ISSS', 'Présentation et Spécialités', 'Santé et Environnement.').
info_etablissement('ISSS', 'Présentation et Spécialités', 'Sciences Infirmières (Polyvalent).').
info_etablissement('ISSS', 'Présentation et Spécialités', 'Synthèse de vos options :').
info_etablissement('ISSS', 'Présentation et Spécialités', 'Technologue de Laboratoire Biomédical.').
info_etablissement('ISSS', 'Présentation et Spécialités', 'Technologue en Instrumentation et Maintenance Biomédicale.').
info_etablissement('ISSS', 'Présentation et Spécialités', 'Technologue en Radiophysique, Radiobiologie et Radioprotection.').
info_etablissement('ISSS', 'Présentation et Spécialités', 'Vous disposez maintenant d''un panorama complet incluant le Sport (IRFCJS), l''Agriculture (IAV/ENAM), la Logistique (IFTL), le BTP (IFMBTP) et désormais la Santé (ISSS).').
info_etablissement('ISSS', 'Présentation et Spécialités', 'Présentation de l''ISSS').
info_etablissement('ISSS', 'Conditions d''Accès', 'Avoir une moyenne de Baccalauréat permettant de franchir le seuil de présélection.').
info_etablissement('ISSS', 'Conditions d''Accès', 'Merci pour ces nouveaux documents. Nous avons maintenant une vision complète des opportunités dans le domaine des sciences du sport au Maroc pour l''année universitaire 2025/2026.Voici une synthèse organisée des trois établissements majeurs que vous avez téléchargés, afin de vous aider à comparer leurs offres et modalités :1. Institut des Sciences du Sport (ISS) - SettatRattaché à l''Université Hassan 1er, cet institut se concentre sur la gestion et la technologie sportive.Filières (Licence 3 ans) : Management du sport, Entraînement sportif, Technologie du sport.Conditions : Baccalauréat de l''année en cours ou précédente (Sciences Physiques, SVT, Maths, Économie selon la filière).Sélection :Présélection sur dossier (60%).Examen écrit (20%) : Culture générale, sport et langues.Entretien oral (20%).Inscription : http://preinscription.uh1.ac.ma/preinscription/iss.html.2. Institut des Sciences du Sport (ISSF) - FèsRattaché à l''Université Sidi Mohamed Ben Abdellah, il offre une approche pédagogique et compétitive.Filières (Licence 3 ans) : Éducation physique et sciences des activités sportives, Management du sport, Entraînement sportif.Conditions : Ouvert aux baccalauréats scientifiques, littéraires et économiques.Sélection :Examen écrit.Tests physiques : Athlétisme, gymnastique et sports collectifs.Inscription : Plateforme www.fsdm.usmba.ac.ma.3. Institut des Métiers du Sport (IMSK) - KénitraCet institut se distingue par ses spécialités de niche comme le journalisme sportif ou l''entrepreneuriat numérique.Filières (Licence 3 ans) :Administration des affaires et gestion des organisations sportives.Animation et journalisme du sport.Entrepreneuriat numérique dans le sport (Digital sport entrepreneurship).Métiers du parasport (sport pour personnes en situation de handicap).Conditions : Baccalauréat toutes séries (selon la spécialité).Particularité : Pas d''internat sur place, mais possibilité de logement universitaire.Inscription : http://ims.uit.ac.ma/pre-inscrip.💡 Synthèse Comparative RapideAspectISS SettatISSF FèsIMSK KénitraProfil dominantManagement & TechnoPédagogie & PerformanceBusiness, Média & SocialTests PhysiquesNon (Dossier + Écrit/Oral)Oui (Obligatoires)Non spécifié sur l''afficheSpécialité uniqueTechnologie du sportÉducation PhysiqueParasport / JournalismeConseil pour votre candidature :Le domaine du sport au Maroc devient très compétitif. Pour ISSF Fès, préparez dès maintenant votre condition physique, tandis que pour ISS Settat, assurez-vous d''avoir une bonne culture générale sportive pour l''écrit.').
info_etablissement('ISSS', 'Conditions d''Accès', 'Présélection : Basée sur la moyenne du Baccalauréat (généralement calculée à hauteur de 75% pour le National et 25% pour le Régional).').
info_etablissement('ISSS', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat Scientifique (Sciences Physiques, SVT, Sciences Mathématiques ou Sciences Agronomiques).').
info_etablissement('ISSS', 'Conditions d''Accès', 'Conditions de Candidature').
info_etablissement('ISSS', 'Processus de Sélection', 'Concours Écrit : Les candidats retenus passent des épreuves dans les matières scientifiques (Mathématiques, Physique-Chimie, SVT) et en Français.').
info_etablissement('ISSS', 'Processus de Sélection', 'Entretien Oral : Pour évaluer les motivations et les aptitudes du candidat à exercer dans le domaine de la santé.').
info_etablissement('ISSS', 'Processus de Sélection', 'Modalités de Sélection et Admission').
info_etablissement('ISSS', 'Durée et Diplôme', 'L''ISSS est un établissement rattaché à l''Université Hassan 1er de Settat. Il propose des formations de haut niveau en sciences de la santé, structurées selon le système LMD (Licence, Master, Doctorat).').
info_etablissement('ISSS', 'Durée et Diplôme', 'L''accès en première année est ouvert aux candidats remplissant les critères suivants :').
info_etablissement('ISSS', 'Durée et Diplôme', 'Filières de Licence Professionnelle (3 ans)').
info_etablissement('ISSS', 'Inscription, Contact et Divers', 'Adresse : Complexe Universitaire, B.P. 555, Settat.').
info_etablissement('ISSS', 'Inscription, Contact et Divers', 'Inscription en ligne : Les pré-candidatures s''effectuent sur la plateforme numérique de l''université généralement entre juin et juillet.').
info_etablissement('ISSS', 'Inscription, Contact et Divers', 'Site Web : www.isss.uh1.ac.ma.').
info_etablissement('ISSS', 'Inscription, Contact et Divers', 'Localisation et Contact').
nouvel_etablissement('ENA', 'ARCHITECTURE, URBANISME ET AMÉNAGEMENT').
info_etablissement('ENA', 'Présentation et Spécialités', 'Centres de formation : En plus du siège à Rabat, l''école dispose de plusieurs centres à Fès, Tétouan, Marrakech, Agadir et Oujda. L''affectation se fait selon une répartition géographique spécifique.').
info_etablissement('ENA', 'Présentation et Spécialités', 'L''ENA est une institution publique à accès régulé dont l''objectif est de former des cadres supérieurs (Architectes d''État) spécialisés dans le domaine de l''architecture.').
info_etablissement('ENA', 'Présentation et Spécialités', 'Pour postuler, le candidat doit remplir les critères suivants :').
info_etablissement('ENA', 'Présentation et Spécialités', 'QCM (50 min) : Portant sur la Culture & Société, l''Art & Architecture, la Géométrie & Perception, et la Langue & compréhension.').
info_etablissement('ENA', 'Présentation et Spécialités', 'Épreuve de Dessin et Expression Artistique (60 min).').
info_etablissement('ENA', 'Présentation et Spécialités', 'Présentation de l''ENA').
info_etablissement('ENA', 'Conditions d''Accès', 'Baccalauréat : Être titulaire d''un Baccalauréat Scientifique, Technique ou Économique (ou diplôme équivalent).').
info_etablissement('ENA', 'Conditions d''Accès', 'Moyenne : Avoir une note supérieure ou égale à 12/20 à l''examen régional (pour le Bac marocain) et une moyenne générale supérieure ou égale à 12/20.').
info_etablissement('ENA', 'Conditions d''Accès', 'Nationalité : Être de nationalité marocaine.').
info_etablissement('ENA', 'Conditions d''Accès', 'Âge : Avoir moins de 22 ans à la date du concours.').
info_etablissement('ENA', 'Conditions d''Accès', 'Conditions d''Admission').
info_etablissement('ENA', 'Processus de Sélection', 'Concours Écrit : Il comprend deux épreuves :').
info_etablissement('ENA', 'Processus de Sélection', 'Dossier : Une copie du formulaire d''inscription et le reçu de paiement doivent être conservés pour le jour du concours.').
info_etablissement('ENA', 'Processus de Sélection', 'Plateforme unique : L''inscription se fait obligatoirement en ligne sur le site www.concoursena.ma.').
info_etablissement('ENA', 'Processus de Sélection', 'Présélection : Elle est basée sur une moyenne calculée à 75% de la note du National et 25% de la note du Régional.').
info_etablissement('ENA', 'Processus de Sélection', 'Processus de Sélection (en 2 étapes)').
info_etablissement('ENA', 'Durée et Diplôme', 'Diplôme : Diplôme d''Architecte (Ingénieur d''État en Architecture).').
info_etablissement('ENA', 'Durée et Diplôme', 'Durée des études : 6 ans, organisés en 3 cycles.').
info_etablissement('ENA', 'Durée et Diplôme', 'Voici les informations détaillées concernant l''Institut National d''Aménagement et d''Urbanisme (INAU) pour l''année universitaire 2025/2026, d''après votre document :').
info_etablissement('ENA', 'Durée et Diplôme', 'Cursus et Diplôme').
info_etablissement('ENA', 'Inscription, Contact et Divers', 'Frais de dossier : Le règlement des frais (100 MAD) doit être effectué selon les modalités indiquées sur le portail.').
info_etablissement('ENA', 'Inscription, Contact et Divers', 'Modalités d''Inscription').
nouvel_etablissement('INAU', 'ARCHITECTURE, URBANISME ET AMÉNAGEMENT').
info_etablissement('INAU', 'Présentation et Spécialités', 'L''INAU est un établissement public à accès régulé situé à Rabat. Il a pour mission de former des cadres supérieurs spécialisés dans l''aménagement du territoire, l''urbanisme et la gestion urbaine.').
info_etablissement('INAU', 'Présentation et Spécialités', 'L''institut est situé à Rabat, Avenue Allal El Fassi, Madinat Al Irfane.').
info_etablissement('INAU', 'Présentation et Spécialités', 'Une épreuve d''analyse de données statistiques et/ou graphiques (1 heure).').
info_etablissement('INAU', 'Présentation et Spécialités', 'Une épreuve de dissertation analytique (1 heure).').
info_etablissement('INAU', 'Présentation et Spécialités', 'Voici l''extraction des données concernant l''ISIC (Institut Supérieur de l''Information et de la Communication) à partir de ta dernière capture d''écran :').
info_etablissement('INAU', 'Présentation et Spécialités', 'Présentation de l''INAU').
info_etablissement('INAU', 'Présentation et Spécialités', 'Localisation').
info_etablissement('INAU', 'Conditions d''Accès', 'Avoir une note de baccalauréat supérieure ou égale à 12/20 (moyenne calculée entre le National et le Régional).').
info_etablissement('INAU', 'Conditions d''Accès', 'Durée des études : La formation dure 5 ans après le Baccalauréat.').
info_etablissement('INAU', 'Conditions d''Accès', 'Être de nationalité marocaine.').
info_etablissement('INAU', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat dans l''une des filières suivantes : Sciences Physiques, Sciences de la Vie et de la Terre (SVT), Sciences Mathématiques, Sciences Agronomiques ou Sciences Appliquées.').
info_etablissement('INAU', 'Conditions d''Accès', 'Conditions d''Admission').
info_etablissement('INAU', 'Processus de Sélection', 'Avoir moins de 21 ans à la date du concours.').
info_etablissement('INAU', 'Processus de Sélection', 'Concours Écrit : Les candidats retenus passent deux épreuves :').
info_etablissement('INAU', 'Processus de Sélection', 'Entretien Oral : Les candidats ayant réussi l''écrit sont convoqués pour un entretien de motivation devant un jury.').
info_etablissement('INAU', 'Processus de Sélection', 'Frais de dossier : Le paiement des frais de participation au concours doit être effectué selon les modalités précisées sur le portail.').
info_etablissement('INAU', 'Processus de Sélection', 'Pour participer au concours, le candidat doit répondre aux critères suivants :').
info_etablissement('INAU', 'Processus de Sélection', 'Présélection (Intikae) : Elle est basée sur une moyenne calculée à 50% de la note du National et 50% de la note du Régional.').
info_etablissement('INAU', 'Processus de Sélection', 'Procédure de Sélection (3 étapes)').
info_etablissement('INAU', 'Durée et Diplôme', 'Diplôme : Les lauréats obtiennent le Diplôme de l''Institut National d''Aménagement et d''Urbanisme (DINAU).').
info_etablissement('INAU', 'Durée et Diplôme', 'Cursus et Diplôme').
info_etablissement('INAU', 'Inscription, Contact et Divers', 'Inscription en ligne : Les candidats doivent s''inscrire via le site officiel de l''institut : www.inau.ac.ma.').
info_etablissement('INAU', 'Inscription, Contact et Divers', 'Modalités d''Inscription').
nouvel_etablissement('ISIC', 'BÂTIMENT, TRANSPORT, LOGISTIQUE ET DIVERS').
info_etablissement('ISIC', 'Présentation et Spécialités', 'Finances Locales.').
info_etablissement('ISIC', 'Présentation et Spécialités', 'Génie Civil (Travaux des Collectivités Territoriales).').
info_etablissement('ISIC', 'Présentation et Spécialités', 'L''ISIC est l''unique établissement public au Maroc spécialisé dans la formation des professionnels du journalisme et de la communication. Situé à Rabat, il forme des cadres hautement qualifiés pour les médias et les départements de communication.').
info_etablissement('ISIC', 'Présentation et Spécialités', 'L''institut est situé à Rabat, Avenue Allal El Fassi, Madinat Al Irfane.').
info_etablissement('ISIC', 'Présentation et Spécialités', 'La formation est structurée selon le système LMD :').
info_etablissement('ISIC', 'Présentation et Spécialités', 'Selon le diagramme de synthèse de vos documents, voici les établissements rattachés au domaine de la construction et de l''aménagement :').
info_etablissement('ISIC', 'Présentation et Spécialités', 'Spécialisation : À partir du 4ème semestre.').
info_etablissement('ISIC', 'Présentation et Spécialités', 'Spécialités mentionnées :').
info_etablissement('ISIC', 'Présentation et Spécialités', 'Tronc commun : Les trois premiers semestres.').
info_etablissement('ISIC', 'Présentation et Spécialités', 'Voici les informations détaillées concernant les instituts spécialisés en Génie Civil, Travaux Publics et Finance Locale basées sur vos documents :').
info_etablissement('ISIC', 'Présentation et Spécialités', 'Présentation de l''ISIC').
info_etablissement('ISIC', 'Présentation et Spécialités', 'Localisation').
info_etablissement('ISIC', 'Conditions d''Accès', 'Avoir une note minimale de 14/20 à l''examen du Baccalauréat (moyenne générale).').
info_etablissement('ISIC', 'Conditions d''Accès', 'Baccalauréat : Séries Scientifiques, Techniques ou Économiques (ou diplôme de technicien équivalent).').
info_etablissement('ISIC', 'Conditions d''Accès', 'Baccalauréat : Séries Scientifiques, Techniques, Architecture, Arts Appliqués, Bâtiment et Travaux Publics, avec une moyenne générale supérieure ou égale à 12/20.').
info_etablissement('ISIC', 'Conditions d''Accès', 'Conditions d''accès :').
info_etablissement('ISIC', 'Conditions d''Accès', 'Ne pas dépasser l''âge de 25 ans au 31 décembre de l''année du concours.').
info_etablissement('ISIC', 'Conditions d''Accès', 'Présélection : Basée sur le dossier du candidat (notes du Bac).').
info_etablissement('ISIC', 'Conditions d''Accès', 'Âge : Entre 17 et 25 ans au 31 décembre de l''année du concours.').
info_etablissement('ISIC', 'Conditions d''Accès', 'Âge : Ouvert aux candidats jusqu''à 30 ans maximum au jour du concours.').
info_etablissement('ISIC', 'Conditions d''Accès', 'Être titulaire du Baccalauréat (toutes séries confondues) ou d''un diplôme équivalent, pour l''année en cours ou l''année précédente.').
info_etablissement('ISIC', 'Conditions d''Accès', 'Conditions d''Admission').
info_etablissement('ISIC', 'Processus de Sélection', 'Concours :').
info_etablissement('ISIC', 'Processus de Sélection', 'ENA (Architecture) : www.concoursena.ma.').
info_etablissement('ISIC', 'Processus de Sélection', 'Le Concours (Écrit et Oral) :').
info_etablissement('ISIC', 'Processus de Sélection', 'Oral : Entretien avec un jury pour évaluer la culture générale, la curiosité intellectuelle et le projet professionnel.').
info_etablissement('ISIC', 'Processus de Sélection', 'Oral : Un entretien (coefficient 2) devant une commission.').
info_etablissement('ISIC', 'Processus de Sélection', 'Pour être éligible au concours, le candidat doit :').
info_etablissement('ISIC', 'Processus de Sélection', 'Sélection :').
info_etablissement('ISIC', 'Processus de Sélection', 'Écrit : Un QCM (coefficient 3, durée 3h) portant sur les Mathématiques et les langues (Arabe ou Français).').
info_etablissement('ISIC', 'Processus de Sélection', 'Écrit : Épreuves de Mathématiques et Dessin (2h), ainsi qu''une épreuve d''analyse de texte en français et sa traduction vers l''arabe (2h).').
info_etablissement('ISIC', 'Processus de Sélection', 'Écrit : Épreuves de culture générale, d''actualité et de langues (Arabe, Français et Anglais).').
info_etablissement('ISIC', 'Processus de Sélection', 'Processus de Sélection (en 2 étapes)').
info_etablissement('ISIC', 'Durée et Diplôme', 'Basée sur vos documents, voici les informations essentielles concernant l''Académie Royale Militaire (ARM) de Meknès pour l''année universitaire 2025/2026 :').
info_etablissement('ISIC', 'Durée et Diplôme', 'Ces instituts dépendent du Ministère de l''Intérieur et forment des techniciens spécialisés en Génie Civil et en Finance Locale.').
info_etablissement('ISIC', 'Durée et Diplôme', 'Ces instituts forment des techniciens spécialisés pour travailler dans les administrations publiques et le secteur privé.').
info_etablissement('ISIC', 'Durée et Diplôme', 'Cursus : La formation dure 2 ans et débouche sur un diplôme de Technicien Spécialisé.').
info_etablissement('ISIC', 'Durée et Diplôme', 'Cycle Licence (3 ans / 6 semestres) :').
info_etablissement('ISIC', 'Durée et Diplôme', 'Diplôme délivré : Licence d''Études Fondamentales en Information et Communication.').
info_etablissement('ISIC', 'Durée et Diplôme', 'IFTSAU (Techniciens Urbanisme) : www.muat.gov.ma.').
info_etablissement('ISIC', 'Durée et Diplôme', 'Cursus et Diplômes').
info_etablissement('ISIC', 'Durée et Diplôme', '1. Instituts de Formation des Techniciens en Architecture et Urbanisme (IFTSAU) - Oujda').
info_etablissement('ISIC', 'Durée et Diplôme', '2. Instituts de Formation des Techniciens Spécialisés (ITSGC) - Oujda').
info_etablissement('ISIC', 'Inscription, Contact et Divers', 'Choix de langue : Le candidat doit choisir dès l''inscription la section dans laquelle il souhaite étudier (Section Arabe ou Section Française).').
info_etablissement('ISIC', 'Inscription, Contact et Divers', 'INAU (Urbanisme) : www.inau.ac.ma.').
info_etablissement('ISIC', 'Inscription, Contact et Divers', 'ITSGC (Génie Civil/Finances) : www.emploi-public.ma.').
info_etablissement('ISIC', 'Inscription, Contact et Divers', 'Inscription : En ligne sur le site http://depot.emploi-public.ma.').
info_etablissement('ISIC', 'Inscription, Contact et Divers', 'Inscription : Via le portail www.muat.gov.ma.').
info_etablissement('ISIC', 'Inscription, Contact et Divers', 'Plateforme : L''inscription se fait via le site officiel : www.isic.ac.ma.').
info_etablissement('ISIC', 'Inscription, Contact et Divers', '3. Récapitulatif des plateformes par domaine').
info_etablissement('ISIC', 'Inscription, Contact et Divers', 'Modalités d''Inscription').
nouvel_etablissement('Institut (IFPS Oujda)', 'BÂTIMENT, TRANSPORT, LOGISTIQUE ET DIVERS').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Agent de maintenance des véhicules de transport routier.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Agent(e) d''exploitation logistique.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Agent(e) d''exploitation transport.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Agent(e) en diagnostic électronique embarqué.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Agent(e) en maintenance des véhicules poids lourds.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Agronomie.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Aide en orientation et accueil aux urgences.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Aide-soignant en bloc opératoire.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Aptitudes Physiques :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Aquaculture (Élevage des organismes aquatiques).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Arboriculture fruitière, Oléiculture et Viticulture.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Autres spécialités : 5 ans d''études.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Avantages : Les élèves bénéficient d''une bourse d''études.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Avoir moins de 30 ans au début de la formation.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Berkane :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Bonne constitution physique.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Bouknadel / Salé :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'C''est un plaisir de t''accompagner dans l''exploration de ces opportunités de formation. À travers les documents que tu as partagés, nous avons couvert un large éventail de domaines allant de l''agriculture au transport, en passant par le cinéma et le textile.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'CHA : Complexe Horticole d''Agadir.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Capacités auditives spécifiques (entendre un chuchotement à 50 cm et une voix normale à 5 m).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Conducteur en transport routier.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Contrôleur logistique.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Cycle Préparatoire : dure 2 ans.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'D''après la dernière capture d''écran (image_c4916f.png), voici les informations concernant les établissements du domaine de l''agriculture (Secteur Agricole) au Maroc.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Dessin de bâtiment.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'E-Commerce et entrepreneuriat.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'ENAM : École Nationale d''Agriculture de Meknès.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Gestion et Maîtrise de l''Eau (GME).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Gestionnaire de stock (Magasinier).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Gros Œuvres (Maçonnerie).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Génie Rural : Gestion et aménagement de l''espace rural.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Génie Rural.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Génie Topographique.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Horticulture / Protection des Végétaux / Aménagement des Espaces Verts.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Horticulture, Paysagisme et Espaces Verts.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Hydraulique Rurale et Irrigation : Maîtrise des systèmes d''arrosage et des ressources en eau.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'IAV : Institut Agronomique et Vétérinaire Hassan II.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'ITSA : Institut de Technologie Spécialisée en Agriculture.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Industrie Agricole et Alimentaire.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Informations complémentaires : Disponibles sur le portail de formation agricole.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Ingénierie Rurale et Économie.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Ingénierie du Développement.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Internat : Possibilité d''hébergement pour les étudiants ne résidant pas à Casablanca, dans la limite des places disponibles.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'L''ENAM est un établissement public d''enseignement supérieur spécialisé dans le domaine agricole, le développement rural et la recherche scientifique. La formation dure 5 ans et est structurée en deux cycles :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'L''IFTL Nouaceur a pour objectif de préparer des cadres moyens à travers des formations de deux ans, incluant des stages en entreprise, pour répondre aux besoins des sociétés de transport et de logistique.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'L''IRTSEF de Salé est un institut spécialisé dans la formation de cadres hautement qualifiés destinés à travailler dans le secteur des eaux, des forêts et de la vie sauvage.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'L''IRTSEF est un institut de formation qui prépare des cadres techniques hautement qualifiés pour intervenir dans le secteur des eaux, des forêts et de la protection de la biodiversité.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'L''accès à l''institut se fait en plusieurs étapes :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'L''admission se déroule en plusieurs étapes :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'L''admission se fait en plusieurs étapes :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'L''institut IFMBTP de Fès propose des formations qualifiantes adaptées aux besoins du marché de l''emploi dans le secteur du bâtiment. L''objectif est de favoriser l''insertion des jeunes en leur apportant des compétences techniques et comportementales (soft skills).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'L''offre de formation est répartie entre plusieurs types d''institutions spécialisées :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'L''établissement propose les parcours suivants :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'La formation est soumise à un régime d''internat obligatoire.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'La note de Français à l''examen régional.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Laboratoire BTP.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Le document liste de nombreux instituts à travers le Maroc, proposant diverses spécialisations :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Le document présente une structure en nid d''abeille regroupant les principaux instituts de formation supérieure et technique dans ce secteur.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Le recrutement s''effectue selon les étapes suivantes :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Les notes des matières scientifiques à l''examen national (Mathématiques, Physique-Chimie et SVT).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Les étudiants peuvent se spécialiser dans les domaines suivants :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Les étudiants sont formés à la fois aux techniques forestières (sylviculture, aménagement) et reçoivent une formation de base en discipline para-militaire.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Marketing des produits horticoles.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Marrakech (Souihla) :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Matières clés : Une attention particulière est portée aux résultats en matières scientifiques (Français et Anglais inclus).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Meknès :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Menuiserie Aluminium et Inox.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Menuiserie Bois.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Médecine Vétérinaire : 6 ans d''études.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Médecine Vétérinaire.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Niveau Qualification (Spécialisation) :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Opérateur en transport routier.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Organisateur(trice) des flux en logistique de production.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Organisateur(trice) des services maritimes et opérations portuaires.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Organisateur(trice) du transport multimodal.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Particularité : Le programme se distingue par un mélange de formation civile et militaire.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Peinture et Étanchéité.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Plantes Aromatiques et Médicinales : Culture, transformation et valorisation de ces plantes.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Pour les candidats aux filières de transport et secours sanitaire, une copie du permis de conduire de catégorie "B" ou "C" est également requise.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Pour postuler à l''IRTSEF, le candidat doit remplir les critères suivants :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Production Animale et Halieutique.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Profil recherché : Responsabilité, flexibilité, capacité à travailler sous pression et bon sens de la communication.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Protection des plantes et de l''environnement.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Routes et Travaux Publics.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Régime : Les étudiants bénéficient d''un régime d''internat obligatoire, incluant une bourse d''études, avec une formation combinant des aspects civils et militaires.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Régime : Les étudiants suivent un régime d''internat obligatoire.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Sciences Agronomiques.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Sciences Expérimentales (SVT, Physique-Chimie, Sciences Agronomiques).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Sciences Expérimentales : Sciences de la Vie et de la Terre (SVT), Sciences Physiques, Sciences Agronomiques.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Sciences Mathématiques (A ou B).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Sciences Mathématiques (A).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Sciences Physiques ou Sciences de la Vie et de la Terre (SVT).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Sciences et Techniques des Productions Végétales.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Sciences et Technologies Mécaniques : Fabrication Mécanique, Maintenance Industrielle, Construction Mécanique.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Sciences et Technologies Électriques : Génie Électrique, Électricité Industrielle.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Sciences et Technologies Électriques ou Mécaniques.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Souhaitez-vous que je vous aide à localiser l''institut sur une carte ou à préparer votre lettre de motivation pour l''une de ces filières ?').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Souhaitez-vous que je vous aide à trouver les date').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Suivi des résultats : Via drafm.net/itsh ou itsh.drafm.net.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Sur place ou par courrier : Au bureau d''ordre de l''institut IFMBTP à Fès.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Taourirt :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Techniques de Laboratoire : Analyse et contrôle de la qualité dans le domaine agricole.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Topographie (Métré).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Topographie (TOPO).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Topographie.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Une copie de la Carte d''Identité Nationale Électronique (CNIE).').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Voici les informations clés concernant les derniers établissements et domaines identifiés :').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Électricité et Domotique.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Électromécanique : Maintenance et gestion des équipements motorisés et automatisés.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Électromécanique et systèmes automatisés.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Être âgé d''au moins 17 ans.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Être âgé de 30 ans au maximum au début de la formation.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Être âgé de 30 ans au maximum à la date de la rentrée scolaire.').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Spécialités proposées (après l''APESA)').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Système de formation').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Système et Filières de Formation').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Système de formation').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Objectifs et Système de Formation').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Présentation et Objectifs').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Système et Filières de Formation').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Système de formation').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Présentation de la formation').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Principaux Établissements et Instituts Agricoles').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Régime de formation').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Régime de l''établissement').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Présentation de l''Institut (IFPS Oujda)').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Exemples d''établissements et spécialités (par ville)').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Présentation de l''institut').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Modalités d''admission').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Modalités de candidature').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Objectifs et Filières de Formation').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Système de formation').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Filières disponibles (9 spécialités)').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Filières et Niveaux de formation').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Spécialités proposées').
info_etablissement('Institut (IFPS Oujda)', 'Présentation et Spécialités', 'Présentation de l''établissement').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Acuité visuelle d''au moins 7/10 sans correction.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Aptitude physique : Avoir une acuité visuelle d''au moins 7/10 sans correction, mesurer au minimum 1,70 m, posséder une structure physique saine, et avoir une capacité auditive permettant d''entendre un chuchotement à 50 cm et une voix normale à 5 m.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Avoir au minimum le niveau de la deuxième année complète du Baccalauréat (Scientifique ou Technique) ou être titulaire d''un diplôme de Qualification Professionnelle dans un domaine lié.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Avoir au minimum le niveau de la deuxième année complète du cycle du Baccalauréat, ou être titulaire d''un diplôme de qualification professionnelle (ou équivalent).').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Avoir une acuité visuelle minimale de 15/20 pour les deux yeux sans correction.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Avoir une taille minimale de 1,70 m pour les garçons et 1,65 m pour les filles.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Baccalauréat Professionnel (Agricole, Maintenance ou Électricité).').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Baccalauréat Professionnel Agricole.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Calcul de la note : Basé sur la moyenne du Baccalauréat National (75 %) et du Baccalauréat Régional (25 %).').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Conditionnement et Valorisation des produits agricoles.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Diplôme : Être titulaire d''un Baccalauréat dans l''une des filières suivantes : Sciences Physiques, Sciences de la Vie et de la Terre (SVT), Sciences Agronomiques, Sciences Mathématiques (A ou B) ou un Baccalauréat Professionnel Agricole.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Documents requis : Copie de la CNIE, relevé de notes global (National et Régional), copie du Baccalauréat et un certificat médical attestant du respect des critères physiques cités plus haut.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Entretien : Les candidats présélectionnés passent des tests oraux pour évaluer leur motivation et leurs aptitudes. Les titulaires d''un Baccalauréat Sciences Agronomiques ou Professionnel Agricole ne sont pas soumis à la présélection et passent directement l''entretien.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'L''inscription aux différents instituts pour les cycles de Technicien et Technicien Spécialisé s''effectue via le portail électronique : http://fpa-concours.agriculture.gov.ma. Les conditions communes sont les suivantes :').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Le concours est ouvert aux candidats titulaires d''un Baccalauréat dans les filières scientifiques ou techniques suivantes :').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Le dossier de candidature (comprenant la copie de la CNIE, les relevés de notes du Baccalauréat et le diplôme) peut être soumis de trois manières :').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Nationalité : Être de nationalité marocaine.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Ne pas dépasser l''âge de 23 ans à la date du concours.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Ne pas dépasser l''âge de 30 ans au début de la formation.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Ne pas dépasser l''âge de 30 ans à la date du concours.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Note : Les titulaires d''un Baccalauréat Professionnel Agricole ou Sciences Agronomiques ne sont pas soumis à cette présélection par plateforme, sous réserve de leur inscription sur le site.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Note : Les titulaires d''un Baccalauréat Sciences Agronomiques ou d''un Baccalauréat Professionnel Agricole sont dispensés de la présélection et passent directement à l''entretien.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Note importante : Les titulaires d''un Baccalauréat Sciences Agronomiques ou Professionnel Agricole ne sont pas soumis à la présélection s''ils s''inscrivent sur la plateforme.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Pour le niveau Technicien : Avoir le niveau de la deuxième année complète du Baccalauréat et ne pas dépasser l''âge de 25 ans.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Pour le niveau Technicien : Être en deuxième année complète du cycle du Baccalauréat (filières scientifiques, techniques ou agricoles) ou être titulaire d''un diplôme de qualification agricole.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Pour le niveau Technicien Spécialisé : Être titulaire d''un Baccalauréat (filières scientifiques, techniques ou agricoles) ou d''un diplôme de Technicien dans une spécialité correspondante.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Pour le niveau Technicien Spécialisé : Être titulaire d''un Baccalauréat et ne pas dépasser l''âge de 30 ans.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Pour les bacheliers : Remplir le formulaire de candidature en ligne via le portail www.imt.ac.ma avant la date limite. Tout dossier contenant des informations incorrectes sera annulé.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Présélection : Basée sur l''étude des dossiers et le classement selon les notes de l''Examen National Unifié des matières scientifiques. Un quota est alloué par académie et par type de Baccalauréat.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Présélection : Basée sur la moyenne des notes du Baccalauréat (National et Régional).').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Présélection : Basée sur la moyenne des notes obtenues au Baccalauréat dans les matières clés : Mathématiques, Physique-Chimie, SVT (National) et la note de Français (Régional).').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Présélection : Basée sur les notes du Baccalauréat National (Mathématiques, Physique-Chimie et SVT) et de la note de Français à l''examen régional.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Présélection : Basée sur les notes obtenues au Baccalauréat (National et Régional).').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Présélection : Elle s''effectue sur dossier, en se basant sur les notes obtenues au Baccalauréat (Moyenne générale).').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Présélection : Elle se base sur la moyenne de l''Examen National du Baccalauréat, en tenant compte de la capacité d''accueil de l''école.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Sélection : Elle s''effectue par une présélection basée sur les notes du Baccalauréat (National et Régional), suivie d''un entretien oral pour les candidats sélectionnés.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Taille minimale de 1,70 m.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Technicien : Avoir le niveau de la deuxième année complète du Baccalauréat et avoir moins de 30 ans.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Technicien : Avoir le niveau de la deuxième année complète du Baccalauréat, ne pas dépasser 30 ans et réussir les tests d''aptitude (connaissances générales, tests psychotechniques et entretien).').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Technicien Spécialisé : La sélection se fait sur la base de la moyenne du Baccalauréat.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Technicien Spécialisé : Être titulaire d''un Baccalauréat (selon la filière demandée), ne pas dépasser 30 ans et réussir la sélection basée sur les notes du Baccalauréat.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Technicien Spécialisé : Être titulaire du Baccalauréat et avoir moins de 30 ans au début de la formation.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Un certificat scolaire original prouvant le niveau de la deuxième année du Baccalauréat (visé par l''académie ou la délégation pour les candidats du privé) ou une copie du diplôme de qualification professionnelle.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Un test d''aptitude physique.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Une copie du relevé de notes de la deuxième année du Baccalauréat ou du diplôme de qualification.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Âge : Avoir au maximum 30 ans à la date du concours.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Âge : Ne pas dépasser 30 ans au début de la formation.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Être de nationalité marocaine.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat (Scientifique ou Technique) ou être titulaire d''un diplôme de Technicien dans une spécialité liée à la filière choisie.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat Scientifique ou Technique (ou un diplôme de Technicien équivalent dans la spécialité demandée).').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat dans l''une des filières suivantes :').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat dans l''une des filières suivantes : Sciences Expérimentales (SVT, Physique-Chimie, Sciences Agronomiques), Sciences Mathématiques (A ou B), ou un Baccalauréat Professionnel (Mécanique, Électricité, Agricole).').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat dans l''une des filières suivantes : Sciences Mathématiques (A ou B), Sciences Physiques, Sciences de la Vie et de la Terre (SVT), Sciences Agronomiques, ou un Baccalauréat Professionnel Agricole.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat dans l''une des filières suivantes : Sciences Physiques, Sciences de la Vie et de la Terre (SVT), Sciences Agronomiques, Sciences Mathématiques (A ou B) ou un Baccalauréat Professionnel Agricole.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat de l''année en cours dans l''une des filières : Sciences Mathématiques (A ou B), Sciences Physiques, Sciences de la Vie et de la Terre (SVT), Sciences Agronomiques, ou un Baccalauréat Professionnel (filière Gestion d''Exploitation Agricole).').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat de l''année en cours dans l''une des filières suivantes : Sciences Mathématiques (A ou B), Sciences Physiques, Sciences de la Vie et de la Terre (SVT), ou Sciences Agronomiques.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat de l''année en cours ou de l''année précédente dans les filières : Sciences Mathématiques (A), Sciences Physiques, Sciences de la Vie et de la Terre (SVT), Sciences Agronomiques, ou Sciences et Technologies Électriques/Mécaniques.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Être titulaire d''un Baccalauréat scientifique, technique ou agricole (pour le niveau Technicien Spécialisé) ou avoir le niveau de la 2ème année du Bac (pour le niveau Technicien).').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Être titulaires d''un Baccalauréat Scientifique ou Technique.').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Système et conditions d''inscription').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Rappel des conditions générales (selon les documents précédents)').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Conditions d''accès par cycle').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Conditions de Candidature').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Conditions de Candidature à l''APESA').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Conditions de candidature').
info_etablissement('Institut (IFPS Oujda)', 'Conditions d''Accès', 'Conditions et Modalités de Candidature').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Concours : Les candidats présélectionnés passent des tests physiques, un test écrit et un entretien oral. L''échec à l''une de ces étapes est éliminatoire.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Concours : Les candidats présélectionnés sont convoqués pour passer des épreuves comprenant :').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Concours : Les candidats présélectionnés sont convoqués pour passer un test écrit (Test d''Aptitude).').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Concours : Les candidats retenus passent un test physique, un test écrit et un entretien oral. Tout échec à l''une de ces épreuves est éliminatoire.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Concours : Les frais de dossier pour le concours s''élèvent à 500 DH.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Concours écrit : Les candidats présélectionnés passent un examen écrit portant sur les Mathématiques, la Physique-Chimie et les Sciences de la Vie et de la Terre.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Email pour le concours : Concours-oujda@ifmeree.ac.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Entretien : Les candidats présélectionnés passent un entretien oral pour valider leur projet professionnel et leur motivation.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Entretien : Les candidats retenus après présélection passent un entretien oral pour évaluer leur motivation.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Entretien : Les candidats retenus après présélection sont convoqués par email pour un entretien oral.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Inscription : Elle s''effectue exclusivement en ligne sur le portail https://concours.fpa-agriculture.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Inscription : Elle s''effectue exclusivement en ligne sur le portail www.iav.ac.ma. Les frais de dossier pour le test s''élèvent à 150 DH (non remboursables).').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Inscription : Elle se fait via le portail du ministère de l''agriculture : http://fpa-concours.agriculture.gov.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Inscription en ligne : Elle s''effectue exclusivement sur le portail https://fpa-concours.agriculture.gov.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Inscription en ligne : Elle s''effectue sur le portail unique https://concours.fpa-agriculture.ma. Il est impératif de suivre les instructions et de remplir le formulaire sur le site.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Inscription en ligne : Obligatoire via le portail du ministère de l''agriculture : https://fpa-concours.agriculture.gov.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Inscription en ligne : Obligatoire via le portail https://fpa-concours.agriculture.gov.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Inscription en ligne : Se fait exclusivement via le portail https://concours.fpa-agriculture.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'L''admission se fait par voie de sélection basée sur les critères suivants :').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'L''admission se fait via un processus de sélection rigoureux :').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Le concours est ouvert aux candidats remplissant les critères suivants :').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Pour les titulaires d''un diplôme de Technicien : Un CV, une copie du diplôme (ou attestation de réussite) et les relevés de notes doivent être envoyés par email à imt.institut@gmail.com en précisant l''objet "Passerelles".').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Pour participer au concours d''accès en première année, les candidats doivent :').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Présélection : Basée sur les notes de l''Examen National (Mathématiques, Physique, Chimie et SVT) et de la note de Français à l''Examen Régional.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Présélection : Basée sur une formule combinant :').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Réussir le concours d''accès (tests écrit et oral).').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Réussir le concours d''accès.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Sélection : L''accès en première année se fait par voie de sélection. Une passerelle permet également aux titulaires d''un diplôme de Technicien d''accéder à la formation dans la limite de 10 % des places pédagogiques, après étude de dossier et réussite d''un test écrit ou oral.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Sélection : Présélection sur dossier suivie d''un test écrit et d''un entretien oral.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Technicien : La sélection repose sur une présélection suivie d''un concours (entretien ou test).').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Un entretien oral.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Un test écrit (Mathématiques, Sciences ou Français selon l''année).').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Une inscription via le portail officiel : http://fpa-concours.agriculture.gov.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Être âgé de 30 ans au maximum lors de l''année du concours.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Être âgé de 30 ans au maximum à la date du concours.').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Modalités de Sélection et Admission').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Modalités de Sélection et Inscription').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Modalités de Sélection et d''Inscription').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Modalités de candidature et sélection').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Modalités de sélection et d''admission').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Modalités de sélection et d''inscription').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Modalités de sélection et inscription').
info_etablissement('Institut (IFPS Oujda)', 'Processus de Sélection', 'Processus de Sélection et Inscription').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Après avoir réussi l''année préparatoire, les étudiants peuvent s''orienter vers :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Basé sur la capture d''écran fournie (image_c491cb.png), voici les informations détaillées concernant l''Institut Agronomique et Vétérinaire Hassan II (IAV) pour l''année universitaire 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Basé sur la dernière capture d''écran fournie (image_c489e7.png), voici les informations détaillées concernant l''Institut de Formation aux Métiers des Énergies Renouvelables et de l''Efficacité Énergétique (IFMEREE) d''Oujda pour l''année universitaire 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Cycle Ingénieur : dure 3 ans, aboutissant au diplôme d''Ingénieur Agronome dans l''une des spécialités proposées.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'D''après la capture d''écran fournie (image_c495c6.png), voici les informations détaillées concernant l''Institut Royal des Techniciens Spécialisés des Eaux et Forêts (IRTSEF) de Salé pour l''année universitaire 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'D''après la dernière capture d''écran (image_c48969.png), voici les informations détaillées concernant l''Institut des Mines de Touissit (IMT) pour l''année universitaire 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'D''après la dernière capture d''écran (image_c49909.png), voici les informations détaillées concernant l''Institut des Techniciens Spécialisés en Génie Rural et Topographie (ITSGRT) de Meknès pour l''année universitaire 2024/2025 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'D''après la dernière capture d''écran (image_c49c4c.png), voici les informations détaillées concernant l''Institut des Techniciens Spécialisés en Agriculture (ITSAT) de Tétouan pour l''année universitaire 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'D''après la dernière capture d''écran fournie (image_c48d29.png), voici les informations détaillées concernant l''Institut de Formation dans les Métiers du Bâtiment et des Travaux Publics (IFMBTP) de Fès pour l''année 2025 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'D''après la dernière capture d''écran fournie (image_c48de4.png), voici les informations détaillées concernant les instituts de formation dans le domaine de l''agriculture pour l''année 2025 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'D''après la dernière capture d''écran fournie (image_c48e29.png), voici les informations détaillées concernant le cycle de Technicien Spécialisé à l''École Supérieure des Industries du Textile et de l''Habillement (ESITH) de Casablanca pour l''année 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'D''après la dernière capture d''écran fournie (image_c494b2.png), voici les informations détaillées concernant l''École Nationale d''Agriculture de Meknès (ENAM) pour l''année universitaire 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'D''après la dernière capture d''écran fournie (image_c4956a.png), voici les informations détaillées concernant le Complexe Horticole d''Agadir (CHA) pour l''année universitaire 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'D''après la dernière capture d''écran fournie (image_c495c6.png), voici les informations détaillées concernant l''Institut Royal des Techniciens Spécialisés des Eaux et Forêts (IRTSEF) de Salé pour l''année universitaire 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'D''autres centres comme ceux de Fquih Ben Salah, Tiflet, Settat, ou Errachidia proposent des formations de Technicien en élevage ou en cultures variées (grandes cultures, cultures oasiennes).').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Dossier : Comprend une copie de la carte d''identité (CNIE), deux copies certifiées du diplôme ou certificat de scolarité, deux copies certifiées du relevé de notes, deux photos d''identité et le dossier d''orientation à retirer auprès de l''administration.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Dossier : Une copie de la CNIE, une copie du diplôme (ou certificat scolaire) et les relevés de notes sont nécessaires.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Dossier requis : Photo d''identité, CV, copie de la CNIE, copie du diplôme ou certificat scolaire, et relevé de notes.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Durée : La formation dure deux ans.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Durée : La formation s''étale sur deux ans.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'IRTSEF : Institut Royal des Techniciens Spécialisés des Eaux et Forêts.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'ITSAT : Institut Technicien Spécialisé en Agriculture en Territoire (ou similaire selon la spécialité régionale).').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'ITSGRT : Institut Technicien Spécialisé en Génie Rural et Topographie.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'ITSHM : Institut Technicien Spécialisé en Horticulture (ou Maintenance/Machinisme selon le contexte spécifique).').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'ITSMAER : Institut Technicien Spécialisé en Mécanique Agricole et Équipement Rural.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'L''ESITH est une institution publique d''enseignement supérieur non rattachée à l''université. Elle vise à former des cadres moyens capables d''assumer des responsabilités de production dans le secteur du textile et de l''habillement. La formation dure deux ans et débouche sur un diplôme de Technicien Spécialisé dans la filière Méthodes de Fabrication.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'L''IAV est un institut d''enseignement supérieur de haut niveau visant à former des cadres spécialisés dans les domaines liés à l''agriculture, au développement rural et à la médecine vétérinaire. La durée des études varie selon la spécialité :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'L''ITSGRT de Meknès forme des techniciens spécialisés capables de gérer les ressources en eau et de réaliser des travaux topographiques. La formation dure deux ans et propose deux filières principales :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'L''institut a pour mission de former des cadres techniques spécialisés dans la protection et la gestion durable des ressources forestières et de la faune sauvage. La formation dure deux ans et débouche sur le diplôme de Technicien Spécialisé des Eaux et Forêts.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'L''institut a pour objectif de former des techniciens dans le domaine de la santé capables de s''intégrer rapidement sur le marché du travail dans le secteur médical. La formation dure deux ans et débouche sur un diplôme de Technicien dans l''une des spécialités suivantes :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'L''institut a pour objectif de préparer des techniciens et techniciens spécialisés dans les métiers du transport et de la logistique à travers les spécialités suivantes :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'L''institut de Tétouan prépare des techniciens spécialisés pour le secteur agricole et forestier. La formation dure deux ans et propose deux spécialités distinctes :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'L''institut dispose d''un internat pour accueillir les étudiants durant leur cursus.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'L''institut forme des experts techniques pour accompagner la modernisation du secteur agricole. La durée de la formation est de deux ans, débouchant sur un diplôme de Technicien Spécialisé dans l''une des trois filières suivantes :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'L''institut forme des techniciens et des techniciens spécialisés dans les domaines de l''énergie et de l''efficacité énergétique. La formation dure deux ans et propose les spécialités suivantes :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'L''institut vise à former des techniciens et techniciens spécialisés dans le domaine de l''audiovisuel et du cinéma. La formation dure deux ans et propose les spécialisations suivantes :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'L''institut vise à former des techniciens spécialisés dans le domaine de l''énergie et des mines pour le marché du travail dans les secteurs industriel et topographique. La durée des études est de deux ans, après quoi l''étudiant obtient un diplôme de Technicien Spécialisé dans l''une des spécialités suivantes :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'La première année est une Année Préparatoire aux Études Supérieures en Agriculture (APESA), à l''issue de laquelle les étudiants choisissent leur spécialité (sans redoublement possible en APESA).').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Le Complexe Horticole d''Agadir (Aït Melloul), rattaché à l''Institut Agronomique et Vétérinaire Hassan II, propose une formation technique, théorique et pratique. La durée des études est de deux ans et débouche sur un diplôme de Technicien Spécialisé dans l''une des filières suivantes :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Niveau Technicien :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Niveau Technicien : Image, Montage, Habillage et Maquillage Cinéma.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Niveau Technicien Spécialisé :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Niveau Technicien Spécialisé : Audiovisuel, Effets Spéciaux, Décor et Accessoires, Régie et Gestion de Production.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Pour le cycle Technicien :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Pour le cycle Technicien Spécialisé :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Pour le cycle de Technicien, le dossier doit comprendre :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Pour rappel, l''accès à ces établissements (niveaux Technicien et Technicien Spécialisé) nécessite généralement :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Pour être admis à l''année préparatoire, le candidat doit :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Qualification : Avoir le niveau de la troisième année de l''enseignement secondaire collégial et avoir moins de 30 ans.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien : Aviculture, Horticulture, Production animale.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien : Conducteur de transport de marchandises.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien : Conducteur de transport de personnes.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien : Enseignement de la conduite (Moniteur).').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien : Installation des Systèmes Photovoltaïques.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien : Production animale, Production végétale, Arboriculture, Élevage des ruminants.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien : Production et valorisation des amandes.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien : Réparation des véhicules de poids lourd.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien : Visite technique des véhicules.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien Spécialisé : Exploitation du transport et de la logistique.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien Spécialisé : Gestion des intrants agricoles.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien Spécialisé : Horticulture, Topographie, Gestion de l''eau.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien Spécialisé : Hydraulique rurale et irrigation, Gestion des exploitations agricoles.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien Spécialisé : Hydraulique rurale et irrigation, Électromécanique, Équipements agricoles.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien Spécialisé : Systèmes Éoliens, Systèmes Solaires, Efficacité Énergétique.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Technicien en traitement et stérilisation du matériel médical.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'l''Institut Royal des Techniciens Spécialisés des Eaux et Forêts (IRTSEF) de Salé pour l''année 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'l''Institut Spécialisé dans les Métiers du Cinéma (ISMC) de Ouarzazate pour l''année universitaire 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'l''Institut Spécialisé dans les Métiers du Transport Routier et de la Logistique (ISMTL) de Taourirt pour l''année universitaire 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'l''Institut de Formation dans les Métiers du Transport et de la Logistique (IFTL) de Nouaceur (Casablanca) pour l''année 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'l''Institut des Techniciens Spécialisés en Mécanique Agricole et Équipement Rural (ITSMAER) de Bouknadel (Salé) pour l''année universitaire 2025/2026 :').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Être âgé de 23 ans au maximum au 31 décembre de l''année de candidature.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Être âgé de 26 ans au maximum au début de l''année scolaire (ou 30 ans pour les titulaires d''une Licence).').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Être âgé de moins de 23 ans au 1er septembre de l''année de candidature.').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Système et Durée de formation').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Objectifs et Durée de Formation').
info_etablissement('Institut (IFPS Oujda)', 'Durée et Diplôme', 'Système et Durée de formation').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : Avenue Moulay Abdellah, Route de Debdou, Taourirt, Code Postal 60800.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : Avenue Sidi Mohamed Ben Abdellah, Tabriquet, B.P. 201, Salé.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : B.P. 121, Aït Melloul, Agadir, 80150.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : B.P. 184, Avenue Al-Qods, Tabriquet, Salé.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : B.P. 184, Rue Al-Qods, Tabriquet, Salé.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : B.P. 4003, Bouknadel, Salé (Route de Kénitra).').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : B.P. 4003, Km 10, Route de Chefchaouen, B.P. 20 Ben Karrich, Tétouan.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : B.P. 4003, Meknès.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : B.P. 6202, Cité de l''Irrigation, Avenue Allal El Fassi, Madinat Al Irfane, Rabat.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : Institut Spécialisé dans les Métiers du Cinéma, Rue Ennasr, B.P. 43, Ouarzazate.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : Institut de Formation aux Métiers des Énergies Renouvelables et de l''Efficacité Énergétique, Technopole Med-Est, Commune Ahl Angad, Oujda.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : Institut de Formation dans le Domaine de la Santé, Route de Jerada, Centre de Santé Oued En-Nachef, Oujda.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : Institut des Mines de Touissit, Touissit / Province d''Oujda, Code Postal 64850.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : Pôle Urbain de Nouaceur - Lot P 41, Nouaceur.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : Route de Haj Kaddour, B.P. S/40, Meknès.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : Route de Meknès, Route Nationale 6, Fès, 30000.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Adresse : École Supérieure des Industries du Textile et de l''Habillement, Route d''El Jadida, Km 8, B.P. 7731, Oulfa, Casablanca.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Email : IFMBTP@GMAIL.COM.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Email : formation.cha@gmail.com.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Email : ismc.direction@ofppt.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'En ligne : Via le lien d''inscription mentionné sur le portail.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Frais de dossier : Le montant est de 60 DH, à payer sur le compte ouvert au nom de l''ENAM auprès de Poste Maroc.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Frais de formation : Après admission définitive, l''étudiant doit s''acquitter d''une contribution aux frais de formation de 15 000 DH par an, payable en deux tranches (12 500 DH à l''inscription et le reste en janvier).').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Inscription : Elle s''effectue exclusivement en ligne via le site www.enameknes.ac.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Inscription : Elle se fait en ligne via le lien http://inscription.ifmeree.ac.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Inscription : Elle se fait via le portail www.iftl.ma/candidature.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Inscription : S''effectue en ligne via le portail http://takwine.ofppt.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Inscription en ligne : https://konosys.esith.ac.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'L''inscription doit se faire obligatoirement sur la plateforme électronique ifps.sante.gov.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Le candidat doit remplir les critères suivants au moment de l''inscription :').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Par Email : En envoyant les documents à inscriptionifmbtp@gmail.com.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Site Web : www.IRTSEF.net.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Site Web : www.eauxetforets.gov.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Site Web : www.enameknes.ac.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Site Web : www.esith.ac.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Site Web : www.iav.ac.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Site Web : www.iavcha.ac.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Site Web : www.ifmeree.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Site Web : www.iftl.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Site Web : www.imt.ac.ma.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Site Web : www.itsmaer.com.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Site Web : www.tsgrt.drafm.net.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Souhaitez-vous que je vous aide à préparer la liste des documents requis pour le dossier de candidature en ligne à l''ESITH ?').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Téléphone : 0522078705 / 0659645761.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Téléphone : 0535631766.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Téléphone : 0536654003.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Téléphone : 0536694640 / 0536679241.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Téléphone : 0668682865.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Étude du dossier : Analyse du parcours scolaire, des motivations et du projet professionnel du candidat.').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Frais et hébergement').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Dossier de Candidature').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Dossier de candidature').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Modalités de dépôt du dossier').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Contact').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Contact et Localisation').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Contact et adresse').
info_etablissement('Institut (IFPS Oujda)', 'Inscription, Contact et Divers', 'Localisation et Contact').
nouvel_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'BÂTIMENT, TRANSPORT, LOGISTIQUE ET DIVERS').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Présentation et Spécialités', 'Cet institut prépare aux métiers stratégiques du transport et de la logistique.').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Présentation et Spécialités', 'IMSK : Institut de Management du Sport (Kénitra).').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Présentation et Spécialités', 'IRFCJS : Institut Royal de Formation des Cadres de la Jeunesse et des Sports.').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Présentation et Spécialités', 'ISSF : Institut Supérieur des Sciences de la Formation.').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Présentation et Spécialités', 'ISSS : Institut Supérieur des Sciences de la Santé.').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Présentation et Spécialités', 'L''institut de Fès propose des formations qualifiantes pour intégrer le secteur dynamique du BTP.').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Présentation et Spécialités', 'L''un de tes documents mentionne les principaux instituts spécialisés dans ce secteur au Maroc :').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Présentation et Spécialités', 'Spécialités : Topographie, Dessin de bâtiment, Électricité de bâtiment, Menuiserie aluminium, et bien d''autres (9 filières au total).').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Présentation et Spécialités', 'Domaine de la Jeunesse et des Sports').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Présentation et Spécialités', 'Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP) - Fès').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Présentation et Spécialités', 'Institut Spécialisé des Métiers du Transport Routier et de la Logistique (ISMTL) - Taourirt').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Conditions d''Accès', 'Basé sur les documents fournis, voici une synthèse détaillée des opportunités de formation pour l''année universitaire 2025/2026 dans les domaines du sport et de l''agriculture au Maroc.🏟️ Domaine de la Jeunesse et des SportsCe secteur propose des licences professionnelles axées sur l''entraînement, la gestion et l''éducation spécialisée.Institut Royal de Formation des Cadres (IRFCJS)Filières proposées : Entraînement sportif, Protection de l''enfance et soutien de la famille, et Éducation de la petite enfance.Durée : 3 ans pour l''obtention d''une licence professionnelle.Conditions d''accès : Ouvert aux titulaires d''un baccalauréat (scientifique de préférence pour le sport).Sélection : Présélection sur dossier, tests physiques (pour le sport), épreuves écrites et entretien oral.Inscription : Exclusivement en ligne sur http://irfc.men.gov.ma.Institut des Sciences du Sport (ISS) - SettatFilières : Management du sport, Entraînement sportif et Technologie du sport.Admission : Basée sur la qualité du dossier (60%), un test écrit (20%) et un entretien oral (20%).Inscription : Préinscription sur http://preinscription.uh1.ac.ma/preinscription/iss.html.🚜 Domaine du Secteur AgricoleLe réseau des établissements agricoles offre des formations allant du technicien à l''ingénieur agronome.Établissements d''Enseignement Supérieur (Ingénierie)IAV Hassan II (Rabat) : Formation de 5 à 6 ans en médecine vétérinaire, agronomie, topographie ou génie rural. Sélection via l''Année Préparatoire aux Études Supérieures en Agriculture (APESA).ENAM (Meknès) : Formation d''Ingénieur Agronome sur 5 ans avec des spécialités comme l''arboriculture, la protection des plantes ou l''économie rurale. Inscription sur www.enameknes.ac.ma.Instituts de Techniciens Spécialisés (Bac + 2)Le portail unique d''inscription pour ces instituts est : https://fpa-concours.agriculture.gov.ma.InstitutSpécialités ClésConditions / ParticularitésIRTSEF SaléEaux et Forêts.Taille min: 1,70m, régime d''internat militaire, bourse incluse.ITSGRT MeknèsTopographie et Maîtrise de l''eau.Âge max : 26 ans au début de la formation.ITSMAER BouknadelÉlectromécanique et Hydraulique rurale.Ouvert aux bacs scientifiques, techniques et pro.CHA AgadirHorticulture, Paysagisme et Aquaculture.Sélection : Notes de français (régional) + matières scientifiques (national).ITSHM MeknèsGestion d''entreprises agricoles.Formation par alternance entre l''institut et l''entreprise.ITSAT TétouanPlantes aromatiques et médécinales.Inscription sur concours.fpa-agriculture.ma.🏗️ Autres Secteurs ClésBâtiment (IFMBTP Fès) : 9 filières dont la topographie et l''électricité de bâtiment. Inscription par email à inscriptionifmbtp@gmail.com.Logistique (IFTL Nouaceur) : Formations en gestion des flux, maintenance de poids lourds et transport multimodal. Inscription sur www.iftl.ma/candidature.Cinéma (ISMC Ouarzazate) : Métiers de l''audiovisuel (décor, image, régie). Inscription via http://takwine.ofppt.ma.Textile (ESITH Casablanca) : Spécialité en production textile. Préinscription sur https://konosys.esith.ac.ma.').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Conditions d''Accès', 'Conditions : Être âgé d''au moins 17 ans, posséder un Baccalauréat ou un diplôme de technicien, et réussir le concours (écrit et oral).').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Conditions d''Accès', 'D''après les documents fournis, voici les détails concernant l''Institut Royal de Formation des Cadres de la Jeunesse et des Sports (IRFCJS) et d''autres opportunités de formation pour l''année universitaire 2025/2026 :🏟️ Institut Royal de Formation des Cadres (IRFCJS)L''IRFCJS est une institution sous la tutelle du Ministère de la Jeunesse et des Sports, visant à former des cadres spécialisés dans le sport, la jeunesse et la petite enfance.Filières et Conditions d''accès :Filière Entraînement Sportif :Public : Titulaires d''un Baccalauréat scientifique pour la 1ère année, ou Baccalauréat toutes séries pour les sportifs de haut niveau.Sélection : Présélection sur dossier, tests physiques, épreuves écrites (français et connaissances sportives) et entretien oral.Filière Protection de l''Enfance et Soutien de la Famille / Éducation de la Petite Enfance :Public : Titulaires d''un Baccalauréat toutes séries.Sélection : Présélection sur dossier, épreuve écrite et entretien oral.Modalités d''inscription :L''inscription se fait exclusivement en ligne via le portail : http://irfc.men.gov.ma.La formation dure 3 ans et débouche sur une Licence Professionnelle.🚜 Formations Spécialisées en Agriculture (Détails complémentaires)En complément des instituts déjà cités, d''autres centres proposent des spécialités pointues :InstitutSpécialités proposéesConditions spécifiquesITSGRT MeknèsTopographie (TOPO) et Gestion et Maîtrise de l''Eau (GME).Bac scientifique ou technique, âge max 26 ans (30 ans pour licenciés).ITSMAER BouknadelÉlectromécanique, Hydraulique Rurale et Irrigation.Bac scientifique, technique ou professionnel agricole, max 30 ans.ITSHM MeknèsCommercialisation des intrants agricoles et Gestion des entreprises.Formation par alternance, Bac scientifique ou économique requis.ITSAT TétouanPlantes Aromatiques et Médicinales, Techniques de Laboratoire.Sélection sur notes (Maths, Physique, SVT, Français) + Entretien.🏗️ Secteur du Bâtiment (IFMBTP Fès)L''Institut de Formation aux Métiers du Bâtiment et des Travaux Publics de Fès propose 9 filières de formation initiale et continue.Filières : Topographie, Électricité de bâtiment, Dessin de bâtiment, Menuiserie Aluminium, etc.Admission : Être titulaire d''un Baccalauréat, avoir au moins 17 ans et réussir le concours d''entrée.Inscription : Via le lien électronique de l''institut ou par email à inscriptionifmbtp@gmail.com.Rappel important pour toutes ces formations : Les inscriptions pour la session 2025/2026 sont généralement ouvertes entre mai et juillet 2025.').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Conditions d''Accès', 'Niveau Technicien : Réparation des véhicules poids lourds, Conduite de transport de marchandises ou de personnes (Niveau 2ème année Bac requis, max 25 ans).').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Conditions d''Accès', 'Niveau Technicien Spécialisé : Exploitation en transport et logistique (Bac requis, max 30 ans).').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Processus de Sélection', 'Agriculture : https://fpa-concours.agriculture.gov.ma.').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Processus de Sélection', 'Sélection : Pour le niveau TS, sélection sur dossier ; pour le niveau Technicien, sélection plus concours.').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Durée et Diplôme', 'l''Institut Supérieur des Sciences de la Santé (ISSS) de Settat pour l''année universitaire 2025/2026 :').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Inscription, Contact et Divers', 'Cinéma (OFPPT) : http://takwine.ofppt.ma.').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Inscription, Contact et Divers', 'Inscription : En ligne via l''adresse inscriptionifmbtp@gmail.com ou directement au siège à Fès.').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Inscription, Contact et Divers', 'Résumé des Portails d''Inscription Clés :').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Inscription, Contact et Divers', 'Textile (ESITH) : https://konosys.esith.ac.ma.').
info_etablissement('Institut de Formation aux Métiers du Bâtiment et des Travaux Publics (IFMBTP)', 'Inscription, Contact et Divers', 'Transport (IFTL) : www.iftl.ma/candidature.').
nouvel_etablissement('Institut des Techniciens Spécialisés en Horticulture (ITSHM)', 'BÂTIMENT, TRANSPORT, LOGISTIQUE ET DIVERS').
info_etablissement('Institut des Techniciens Spécialisés en Horticulture (ITSHM)', 'Présentation et Spécialités', 'Cet institut est dédié à la formation d''experts en horticulture, en phase avec les besoins du marché marocain.').
info_etablissement('Institut des Techniciens Spécialisés en Horticulture (ITSHM)', 'Présentation et Spécialités', 'Filières : Commercialisation des intrants agricoles et Gestion des entreprises agricoles.').
info_etablissement('Institut des Techniciens Spécialisés en Horticulture (ITSHM)', 'Conditions d''Accès', 'Conditions : Être de nationalité marocaine, avoir au maximum 30 ans et être titulaire d''un Baccalauréat scientifique ou technique.').
info_etablissement('Institut des Techniciens Spécialisés en Horticulture (ITSHM)', 'Conditions d''Accès', 'Sélection : Présélection basée sur les notes du Baccalauréat (National et Régional), suivie d''un entretien oral.').
info_etablissement('Institut des Techniciens Spécialisés en Horticulture (ITSHM)', 'Durée et Diplôme', 'Institut des Techniciens Spécialisés en Horticulture (ITSHM) - Meknès').
nouvel_etablissement('Généralités', 'AUTRES ÉTABLISSEMENTS').
info_etablissement('Généralités', 'Présentation et Spécialités', '1. Contexte Institutionnel').
info_etablissement('Généralités', 'Présentation et Spécialités', '2. Panorama des Études Supérieures (7 Catégories)').
info_etablissement('Généralités', 'Présentation et Spécialités', '3. Répertoire des Écoles Identifiées').
info_etablissement('Généralités', 'Présentation et Spécialités', '4. Fiche Technique Détaillée : ENCG').
info_etablissement('Généralités', 'Présentation et Spécialités', '5. Annuaire des Sites Web (Réseau ENCG)').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Autorité : Académie Régionale de l''Éducation et de la Formation (AREF) - Région de l''Oriental.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'C''est entendu. Je vais procéder à une extraction exhaustive et structurée de l''ensemble des données présentes dans les quatre images que tu as partagées.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'C''est l''établissement le plus documenté dans tes captures.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'ENCG : École Nationale de Commerce et de Gestion.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'ENIADB : École Nationale de l''Industrie Alimentaire et de Biotechnologie.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'ENSA : École Nationale des Sciences Appliquées.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'ENSAM : École Nationale Supérieure d''Arts et Métiers.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'ENSCK : École Nationale Supérieure de Chimie de Kénitra.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'EST : École Supérieure de Technologie.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'FST : Faculté des Sciences et Techniques.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'ISCAE : Institut Supérieur de Commerce et d''Administration des Entreprises.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Les établissements mentionnés par leurs acronymes dans le diagramme sont :').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Ma''ahid wa Madaris ''Ulya : Instituts et Grandes Écoles (Ingénierie, Commerce, etc.).').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Madaris at-Tarbiya wa at-Takwin : Écoles normales supérieures pour les métiers de l''enseignement.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Mousasat Jami''iya : Facultés et établissements universitaires classiques.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Mousasat at-Takwin al-Mihni : Centres de formation professionnelle (OFPPT).').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Objectif de formation : Cadres hautement qualifiés en commerce, gestion et management, avec une forte composante en langues et communication.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Responsable : Mounia Mouzouri (Directrice de l''AREF de l''Oriental).').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Semestre 10 : Stage de fin d''études et Projet de Fin d''Études (PFE).').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Semestres 1 à 4 : Tronc commun (Bases de l''économie et gestion).').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Semestres 5 & 6 : Phase de détermination et choix d''orientation.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Semestres 7 à 9 : Spécialisation approfondie.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Source : Ministère de l''Éducation Nationale, du Préscolaire et des Sports.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Takwin al-''Askari wa Chibh al-''Askari : Écoles militaires et paramilitaires.').
info_etablissement('Généralités', 'Présentation et Spécialités', 'Voici la base de données complète consolidée :').
info_etablissement('Généralités', 'Conditions d''Accès', 'Baccalauréat Professionnel : Commerce, Comptabilité, Logistique, Administration.').
info_etablissement('Généralités', 'Conditions d''Accès', 'Baccalauréat en : Économie, Gestion, Sciences Mathématiques, Sciences Expérimentales.').
info_etablissement('Généralités', 'Conditions d''Accès', 'Conditions d''accès :').
info_etablissement('Généralités', 'Conditions d''Accès', 'Document : Guide "Le Guide de l''Orientation Post-Baccalauréat" - 5ème Édition.').
info_etablissement('Généralités', 'Conditions d''Accès', 'Le guide classe les opportunités après le bac en sept grands pôles :').
info_etablissement('Généralités', 'Conditions d''Accès', 'Présélection : Calculée sur la base de la note du Bac (75% National + 25% Régional).').
info_etablissement('Généralités', 'Conditions d''Accès', 'Voici l''extraction complète des données concernant l''ENIADB (École Nationale de l''Intelligence Artificielle et de la Numérisation - Berkane) à partir de ta capture d''écran.🏛️ Présentation de l''ENIADBSituée à Berkane, cette école est spécialisée dans les domaines de pointe du numérique. Elle forme des ingénieurs capables de répondre aux besoins croissants du marché de l''emploi en technologies de l''information.Spécialités principales :Intelligence Artificielle (IA)RobotiqueRéseaux et CybersécuritéGénie Informatique🎓 Cursus et DiplômeLa formation à l''ENIADB suit le modèle classique des écoles d''ingénieurs :Cycle Préparatoire (2 ans / 4 semestres) : Formation de base.Cycle Ingénieur (3 ans) : Spécialisation approfondie incluant des stages en entreprise, des travaux pratiques en laboratoires et des projets de fin d''études.Diplôme : Ingénieur d''État.📝 Conditions d''accèsL''accès est ouvert selon deux niveaux :En 1ère année du Cycle Préparatoire :Ouvert aux bacheliers en Sciences Mathématiques, Sciences Expérimentales (PC, SVT) et Sciences & Technologies (Électrique/Mécanique).En 1ère année du Cycle Ingénieur (Passerelles) :Ouvert aux titulaires d''un DEUG, DUT, DEUST, DEUP ou d''une Licence dans les filières SMI, SMA, SMP (sous réserve de réussite sur dossier et/ou concours).Processus de Sélection :Présélection : Basée sur les notes du Baccalauréat.Examen écrit : Porte sur les Mathématiques, l''Informatique et les Soft Skills.Entretien oral : Une étape de validation devant un jury.📍 Informations PratiquesDétailInformation extraiteUniversitéUniversité Mohammed Ier – OujdaLocalisationBerkaneSite d''inscriptionscolarite-eniadb.ump.ma/online_studentsContact Emailcontact@ump.ac.maTéléphone0536500614💡 Le petit "plus" de l''ENIADBC''est l''une des écoles les plus récentes et les plus modernes du réseau. Elle est idéale si tu es passionné par la Data Science et le Machine Learning, car son programme est spécifiquement construit autour de l''intelligence artificielle, contrairement aux écoles d''ingénieurs plus généralistes.Note importante : N''oublie pas de préparer tes pièces justificatives (CIN, relevés de notes, photo) en format numérique pour l''inscription sur leur plateforme spécifique.').
info_etablissement('Généralités', 'Conditions d''Accès', 'Voici l''extraction complète des données concernant l''ENSCK (École Nationale Supérieure de Chimie de Kénitra) à partir de ta capture d''écran.🏛️ Présentation de l''ENSCKL''ENSCK est une école d''ingénieurs spécialisée dans la formation d''Ingénieurs Chimistes de haut niveau, capables d''intervenir dans la production, la recherche, et la gestion au sein de secteurs industriels variés (chimie fine, matériaux, environnement, développement durable).🎓 Structure de la FormationLe cursus s''étale sur 5 ans (10 semestres) pour l''obtention du diplôme d''Ingénieur d''État :Cycle Préparatoire Intégré (2 ans) : Focus sur le domaine scientifique fondamental, les techniques d''expression et l''informatique.Cycle Ingénieur (3 ans) : Spécialisation technique en chimie, gestion de projets, langues et communication.Pédagogie : Inclut des stages de terrain, des travaux en laboratoires et des visites d''entreprises.📝 Conditions d''accès et InscriptionL''accès est ouvert aux bacheliers (année en cours ou précédente) des filières suivantes :Sciences Mathématiques (A et B).Sciences Expérimentales : Filières Physique-Chimie (PC) et Sciences de la Vie et de la Terre (SVT).Processus de Sélection :Présélection : Basée sur la moyenne calculée à 75% National + 25% Régional.Examen écrit : Un concours portant sur les matières suivantes :MathématiquesPhysiqueChimieLangue française (programme de la filière Sciences Physiques).Plateforme d''inscription : [lien suspect supprimé] (Site de l''Université Ibn Tofail).📍 Informations de ContactL''école est unique et située à Kénitra :DétailInformation extraiteÉtablissementÉcole Nationale Supérieure de Chimie de KénitraUniversitéUniversité Ibn Tofail – KénitraAdresseB.P. 242 – KénitraTéléphone0537329201Site Web[lien suspect supprimé]💡 Points clés à retenirSpécificité : Contrairement à l''ENSA ou l''ENSAM qui sont généralistes, l''ENSCK est ultra-spécialisée dans le domaine de la chimie et de l''ingénierie des procédés.Concours écrit : Attention, le français fait partie des épreuves du concours écrit pour cette école.').
info_etablissement('Généralités', 'Conditions d''Accès', 'Voici l''extraction exhaustive des données concernant l''ISCAE (Institut Supérieur de Commerce et d''Administration des Entreprises) à partir de ta capture d''écran.🏛️ Présentation de l''ISCAEL''ISCAE est la première institution publique d''enseignement supérieur de gestion au Maroc. Elle forme des cadres supérieurs pour les secteurs public et privé dans les domaines de l''administration, du commerce, de la comptabilité et de l''économie appliquée.🎓 Cursus et Diplôme (Licence)La formation en Cycle Licence dure 3 ans. Les spécialités disponibles après l''obtention du diplôme de Licence sont :Commerce InternationalMarketing / VenteBourse et Marchés FinanciersFinance et ComptabilitéGestion Bancaire📝 Conditions d''accèsPour postuler en 1ère année de Licence, le candidat doit remplir les critères suivants :Baccalauréat : Être titulaire d''un Bac en filières Scientifiques ou Économiques.Âge : Ne pas dépasser 21 ans au 31 décembre de l''année du concours.🧪 Processus de Sélection (3 Étapes)Le système d''admission de l''ISCAE est l''un des plus rigoureux :Présélection : Basée sur les notes obtenues au Baccalauréat.Épreuves Écrites :AnglaisCulture Générale en FrançaisMathématiquesÉpreuve Orale (Entretien) :Entretien individuel en Français.Entretien individuel en Anglais.📂 Procédure d''Inscription (Candidature en ligne)L''inscription se fait via le site : www.groupeiscae.ma.Dossier PDF : Les candidats présélectionnés doivent envoyer un dossier complet par e-mail (copie de la fiche de candidature, copie de la CIN, reçu des frais de concours).Frais de concours : Le paiement doit être effectué par virement bancaire sur le compte de l''Institut auprès de la Trésorerie Générale du Royaume.📍 Localisation des CentresL''ISCAE dispose de deux campus principaux :VilleAdresse préciseCasablancaKm 9.5 Route de Nouaceur, B.P. 8114 Oasis.Rabat28 Avenue Annakhil, Secteur 10, Hay Riad.Note Importante : Contrairement à l''ENCG (5 ans), l''ISCAE propose un cycle Licence de 3 ans, souvent suivi d''un Cycle Grande École (Master) pour les étudiants souhaitant approfondir leur expertise.').
info_etablissement('Généralités', 'Conditions d''Accès', 'Voici l''extraction exhaustive des données concernant la FST (Faculté des Sciences et Techniques) à partir de ta dernière capture d''écran.🏛️ Présentation de la FSTLa FST est un établissement universitaire à accès régulé qui adopte le système LMD (Licence, Master, Doctorat). Elle propose des formations alliant sciences théoriques et applications techniques pour répondre aux besoins des secteurs industriels et technologiques.🎓 Cursus et SpécialitésLa formation initiale se fait dans le cadre du Cycle Licence (3 ans / 6 semestres).Les deux premières années (4 semestres) constituent un tronc commun appelé DEUST (Diplôme d''Études Universitaires Scientifiques et Techniques) avant la spécialisation en Licence.Les 4 Troncs communs (Parcours) proposés :MIP : Mathématiques, Informatique, Physique.MIPC : Mathématiques, Informatique, Physique, Chimie.BCG : Biologie, Chimie, Géologie.GE-GM : Génie Électrique, Génie Mécanique.📝 Conditions d''accès et InscriptionL''accès est ouvert aux bacheliers des filières suivantes :Sciences Mathématiques (A et B).Sciences Expérimentales (PC, SVT, Agro).Sciences et Technologies (Électrique et Mécanique).Bac Professionnel : Filières techniques (Maintenance, Aéronautique, Électronique, Construction, etc.).Processus de Sélection :Sélection sur dossier : Pas de concours écrit. La sélection se base sur un classement par mérite via une moyenne calculée (75% National + 25% Régional) avec l''application de coefficients de pondération spécifiques à chaque tronc commun.Plateforme : Inscription obligatoire sur www.cursussup.gov.ma. L''élève peut formuler jusqu''à 5 choix de parcours.📍 Réseau des Facultés (8 Centres)VilleUniversité de rattachementSite WebAl HoceimaUniversité Mohammed Ierwww.fsth.ump.maFèsUniv. Sidi Mohamed Ben Abdellahwww.fst-usmba.ac.maTangerUniv. Abdelmalek Essaâdiwww.fstt.ac.maMohammediaUniv. Hassan IIwww.fstm.ac.maSettatUniv. Hassan Ierwww.fsts.ac.maBeni MellalUniv. Sultan Moulay Slimanewww.fstbm.ac.maMarrakechUniv. Cadi Ayyadwww.fstg-marrakech.ac.maErrachidiaUniv. Moulay Ismaïlwww.fste.umi.ac.ma💡 Ce qu''il faut retenirFlexibilité : Le diplôme DEUST (après 2 ans) permet de postuler aux concours d''entrée des Grandes Écoles d''Ingénieurs (ENSA, ENSAM, etc.) ou de continuer en Licence.Diversité : C''est l''établissement qui offre le spectre le plus large de spécialités scientifiques (de la biologie au génie mécanique).').
info_etablissement('Généralités', 'Conditions d''Accès', 'Voici l''extraction exhaustive des données concernant les EST (Écoles Supérieures de Technologie) à partir de ta dernière capture d''écran.🏛️ Présentation de l''ESTLes EST sont des établissements universitaires à accès régulé qui forment des techniciens supérieurs hautement qualifiés. L''objectif est de fournir des compétences théoriques et pratiques permettant une insertion rapide dans les secteurs économiques, industriels et commerciaux.🎓 Cursus et DiplômesLa formation initiale à l''EST se déroule principalement en deux étapes :DUT (Diplôme Universitaire de Technologie) : Formation de 2 ans (4 semestres).Licence Professionnelle : Après le DUT, les étudiants peuvent postuler pour une année supplémentaire (1 an) pour obtenir une Licence.📝 Conditions d''accès et InscriptionL''accès est ouvert aux bacheliers des filières suivantes :Sciences : Mathématiques (A et B), Expérimentales (PC, SVT, Agro).Économie : Sciences Économiques, Gestion Comptable.Technique : Électrique et Mécanique.Bac Professionnel : Maintenance, Électronique, Logistique, Énergies Renouvelables, Bâtiment, Comptabilité, Commerce, etc.Processus de Sélection :Présélection uniquement : Il n''y a pas de concours écrit. La sélection se fait sur la base de la moyenne du Bac (75% National + 25% Régional) avec des coefficients de pondération selon la filière du Bac et la spécialité demandée.Plateforme : Inscription sur www.cursussup.gov.ma. L''élève peut choisir jusqu''à 10 choix (combinaisons filières/villes).📍 Réseau des Écoles (18 Centres)Le réseau des EST est l''un des plus vastes au Maroc :VilleSite WebVilleSite WebOujdawww.esto.ump.maBeni Mellalwww.estbm.usms.ac.maNadorwww.estn.ump.maKhénifrawww.estk.ac.maFèswww.est.usmba.ac.maFquih Ben Salahwww.est.usms.ac.maCasablancawww.est-uh2c.ac.maSafiwww.est.uca.maSaléwww.ests.um5.ac.maEssaouirawww.este.uca.maSidi Bennourhttp://www.estsb.ucd.ac.maEl Kelaâ des Sraghnawww.uca.ma/eskaKénitrawww.est.uit.ac.maAgadirwww.esta.ac.maMeknèswww.est-umi.ac.maGuelmimwww.estg.ac.maLaâyounewww.estl.ac.maDakhlawww.estd.uiz.ac.ma💡 Différence CléContrairement aux écoles d''ingénieurs (ENSA/ENSAM) qui demandent 5 ans d''études, l''EST permet d''obtenir un diplôme professionnel en 2 ans seulement, idéal pour ceux qui veulent entrer rapidement sur le marché du travail ou poursuivre en licence professionnelle ensuite.').
info_etablissement('Généralités', 'Conditions d''Accès', 'Présentation de l''ENSAL''ENSA est un réseau d''écoles d''ingénieurs marocaines rattachées aux universités publiques. Elle vise à former des Ingénieurs d''État hautement qualifiés sur les plans théorique et pratique.🎓 Structure de la FormationLa formation dure 5 ans (10 semestres) et se décompose en deux cycles :Cycle Préparatoire Intégré (2 ans) : Focus sur les sciences fondamentales (Maths, Physique, Chimie) et les techniques de base.Cycle Ingénieur (3 ans) : Spécialisation technique, gestion de projets, entrepreneuriat, langues et communication.Diplôme délivré : Diplôme d''Ingénieur d''État.📝 Conditions et Procédures d''AccèsL''accès est ouvert aux titulaires d''un Baccalauréat (année en cours ou année précédente) dans les filières suivantes :Type de BaccalauréatFilières admisesSciencesSciences Mathématiques (A et B), Sciences Expérimentales (SVT, PC, Agro).TechniqueSciences et Technologies Électriques / Mécaniques.ProfessionnelAéronautique, Systèmes Électroniques, Maintenance Industrielle, Énergies Renouvelables (Solaire), Logistique, Construction Bâtiment, etc.Processus de Sélection :Présélection : Basée sur la moyenne du Bac (75% National + 25% Régional) avec application de coefficients de pondération selon la filière.Concours Écrit : Un examen national commun pour les candidats retenus après la présélection.Inscription : Obligatoirement sur la plateforme www.cursussup.gov.ma.📍 Réseau des Écoles (Villes et Universités)L''ENSA est présente dans de nombreuses villes à travers le Maroc :VilleUniversité de rattachementSite WebOujdaMohammed Ierwww.ensao.ump.maAgadirIbn Zohrwww.ensa-agadir.ac.maTangerAbdelmalek Essaâdiwww.ensat.ac.maTétouanAbdelmalek Essaâdiwww.ensa.tetouan.uae.ac.maAl HoceimaAbdelmalek Essaâdiwww.ensah.maFèsSidi Mohamed Ben Abdellahwww.ensaf.ac.maKénitraIbn Tofailwww.ensa.uit.ac.maMarrakechCadi Ayyadwww.ensa.ac.maSafiCadi Ayyadwww.ensas.uca.maEl JadidaChouaib Doukkaliwww.ensaj.ucd.ac.maBeni MellalSultan Moulay Slimaneensabm.usms.ac.maKhouribgaSultan Moulay Slimaneensak.usms.ac.maBerrechidHassan Ierwww.ensab.ac.maInformation Clé : Lors de ta candidature en ligne, tu dois obligatoirement classer toutes les écoles par ordre de préférence. Une fois la période d''inscription terminée, aucune modification de tes choix n''est possible.Souhaites-tu que je t''explique comment sont calculés les coefficients de pondération pour la présélection ou que l''on passe à une autre école ?').
info_etablissement('Généralités', 'Conditions d''Accès', 'Présentation de l''ENSAML''ENSAM forme des Ingénieurs d''État spécialisés dans les domaines des arts, des métiers et de l''ingénierie industrielle (conception, fabrication, montage, qualité et maintenance).🎓 Structure de la FormationLe cursus s''étale sur 5 ans (10 semestres) :Cycle Préparatoire Intégré (2 ans) : Formation scientifique et technique de base.Cycle Ingénieur (3 ans) : Spécialisation approfondie, gestion de projets, entrepreneuriat et communication.Pédagogie : Accent mis sur les stages de terrain, les travaux pratiques en atelier et le contact direct avec le milieu industriel.📝 Conditions d''accès et InscriptionL''accès est ouvert aux bacheliers (année actuelle ou précédente) des filières suivantes :Type de BacFilières admisesSciencesSciences Mathématiques (A et B), Sciences Expérimentales (SVT, PC).TechniqueSciences et Technologies Électriques / Mécaniques.ProfessionnelAéronautique, Systèmes Électroniques, Maintenance Industrielle, Énergies Renouvelables, Construction Bâtiment, Logistique, etc.Processus de Sélection :Présélection : Calculée sur la base de la moyenne du Bac (75% National + 25% Régional).Examen écrit : Un concours national commun pour les candidats sélectionnés.Plateforme : Inscription obligatoire sur www.cursussup.gov.ma.📍 Localisation des Établissements (Réseau ENSAM)Le document identifie trois établissements majeurs au Maroc :VilleUniversité de rattachementSite Web OfficielMeknèsUniversité Moulay Ismaïlwww.ensam-umi.ac.maCasablancaUniversité Hassan IIwww.ensam-casa.maRabatUniversité Mohammed Vwww.ensam.um5.ac.ma💡 Points Importants à retenirOrdre de préférence : Lors de l''inscription en ligne, l''étudiant doit classer les trois écoles (Meknès, Casablanca, Rabat). Ce choix est définitif après la clôture des inscriptions.Objectif Pro : L''ENSAM est particulièrement reconnue pour sa proximité avec le secteur de la production et de l''industrie lourde.').
info_etablissement('Généralités', 'Conditions d''Accès', 'Informations GénéralesDocument : Guide d''orientation "Après le Baccalauréat" (5ème édition).Source : Académie Régionale de l''Éducation et de la Formation (AREF) - Région de l''Oriental.Objectif : Accompagner les élèves dans la construction de leur projet personnel et professionnel en offrant des informations précises sur les parcours disponibles.🏛️ Types d''Établissements et ParcoursL''image liste les grandes catégories d''études accessibles après le bac :CatégorieTypes d''institutions / FormationsUniversitaireÉtablissements universitaires (Facultés, etc.)Grandes ÉcolesInstituts et Écoles Supérieures (Ingénierie, Commerce, etc.)Classes PréparatoiresCPGE (Classes Préparatoires aux Grandes Écoles)Technique CourtBTS (Brevet de Technicien Supérieur)ÉducationÉcoles de l''Éducation et de la Formation (Métiers de l''enseignement)ProfessionnelÉtablissements de Formation ProfessionnelleMilitaireÉtablissements de formation Militaire et Para-militaire').
info_etablissement('Généralités', 'Processus de Sélection', 'Examen écrit : Le concours TAFEM (Test d''Admissibilité à la Formation en Management).').
info_etablissement('Généralités', 'Processus de Sélection', 'J''ai extrait ici l''intégralité des textes, chiffres et liens visibles. Souhaites-tu une analyse comparative entre deux de ces écoles ou plus d''infos sur le concours TAFEM ?').
info_etablissement('Généralités', 'Processus de Sélection', 'Processus de sélection :').
info_etablissement('Généralités', 'Durée et Diplôme', 'Aqsam Tahdiriya (CPGE) : Classes préparatoires aux grandes écoles d''ingénieurs.').
info_etablissement('Généralités', 'Durée et Diplôme', 'BTS (Brevet de Technicien Supérieur) : Sections de préparation au diplôme de technicien supérieur.').
info_etablissement('Généralités', 'Durée et Diplôme', 'Diplôme : Diplôme des Écoles Nationales de Commerce et de Gestion.').
info_etablissement('Généralités', 'Durée et Diplôme', 'Durée des études : 5 ans (10 semestres).').
info_etablissement('Généralités', 'Durée et Diplôme', 'Organisation du cursus :').
info_etablissement('Généralités', 'Durée et Diplôme', 'Plateforme de candidature : www.cursussup.gov.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Agadir	www.encg-agadir.ac.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Beni Mellal	www.encgbm.usms.ac.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Casablanca	www.encgcasa.ac.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Dakhla	www.encg-dakhla.ac.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'El Jadida	www.encgj.ucd.ac.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Fès	www.encgf.usmba.ac.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Kénitra	www.encg.uit.ac.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Marrakech	www.encg.u-cam.ac.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Meknès	www.encg.umi.ac.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Oujda	www.encgo.ump.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Settat	www.encg-settat.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Tanger	www.encgt.ma').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Ville	Site Web Officiel').
info_etablissement('Généralités', 'Inscription, Contact et Divers', 'Voici la liste complète des adresses électroniques extraite de la table :').
nouvel_etablissement('École Supérieure des Beaux', 'AUTRES ÉTABLISSEMENTS').
info_etablissement('École Supérieure des Beaux', 'Présentation et Spécialités', 'Design (ENSAD).').
info_etablissement('École Supérieure des Beaux', 'Conditions d''Accès', 'Conformément à la règle que nous avons établie, je me concentre uniquement sur les informations contenues dans la toute dernière capture d''écran (image_c406c7.png) concernant l''École Supérieure des Beaux-Arts (ESBA) de Casablanca.🎨 École Supérieure des Beaux-Arts (ESBA) - CasablancaL''ESBA est un établissement d''enseignement supérieur public qui forme des cadres de haut niveau dans les métiers des arts plastiques et du design.🎓 Cursus et SpécialitésLa formation dure 4 ans au total (divisée en deux cycles de 2 ans) et débouche sur le Diplôme du Cycle National Supérieur des Beaux-Arts dans l''une des filières suivantes :Design d''intérieur (التصميم الداخلي).Design publicitaire (التصميم الإشهاري).Arts plastiques (الفنون التشكيلية).📝 Conditions de CandidaturePour être éligible au concours 2025/2026, le candidat doit :Être titulaire du Baccalauréat (toutes séries ou diplôme équivalent).Être âgé entre 17 et 25 ans au maximum à la date du concours.📂 Dossier de CandidatureLe dossier doit être envoyé par courrier postal ordinaire à l''adresse de l''école et comprend :Une demande manuscrite incluant l''adresse, le numéro de téléphone et l''e-mail, accompagnée d''une lettre de motivation.Une copie certifiée conforme de la Carte d''Identité Nationale (CNI).Une enveloppe timbrée portant le nom et l''adresse du candidat.Deux photos d''identité récentes avec le nom au verso.Une copie du diplôme du Baccalauréat (ou certificat de scolarité pour les élèves en année terminale du Bac).🧪 Procédure de Sélection (Concours)Le concours d''accès se déroule en deux étapes majeures :1. Phase de Présélection InitialeÉcrit : Un examen de culture générale en langue arabe ou française.Pratique : Une épreuve de dessin et une épreuve de modelage (arts plastiques).Les candidats ayant obtenu une moyenne $\\ge 12/20$ aux épreuves précédentes (comptant pour 60% de la note) passent à l''étape finale.2. Phase de Sélection FinaleEntretien oral : Un entretien sur la culture générale et la vie quotidienne (durée de 10 à 20 minutes).Présentation du Portfolio : Le candidat doit présenter son dossier artistique personnel (Porte-folio).📍 Contact et InscriptionAdresse : École Supérieure des Beaux-Arts, 10 Rue Rachidi, 20070 Casablanca.E-mail : esba.casablanca@gmail.com').


% ==============================================================================
% 🛠️ NOUVELLES FONCTIONNALITES AVANCEES (INTELLIGENCE DE DIAGNOSTIC)
% ==============================================================================

% ---------------------------------------------------------
% 1. MOTEUR DE RECHERCHE NLP (Mots-Clés)
% ---------------------------------------------------------
% Permet de chercher un mot précis dans toutes les descriptions des écoles.
% Exemple: recherche_ecole_par_mot('internat', Ecole, Categorie, Phrase).
recherche_ecole_par_mot(MotCle, Ecole, Categorie, Phrase) :-
    info_etablissement(Ecole, Categorie, Phrase),
    sub_string(Phrase, _, _, _, MotCle).

% ---------------------------------------------------------
% 2. CALCULATEUR DE SEUIL DYNAMIQUE (75% National / 25% Régional)
% ---------------------------------------------------------
% Calcule la note de présélection exacte pour les écoles marocaines.
calculer_note_preselection(NoteNationale, NoteRegionale, ScoreFinal) :-
    ScoreFinal is (NoteNationale * 0.75) + (NoteRegionale * 0.25).

% Règle de diagnostic direct pour certaines écoles très demandées (Exemple)
% diagnostic_preselection('ENSA', 16, 14, Resultat).
diagnostic_preselection(Ecole, NoteNationale, NoteRegionale, Resultat) :-
    calculer_note_preselection(NoteNationale, NoteRegionale, Score),
    (   Ecole = 'ENSA', Score >= 14.0 -> 
        string_concat('✅ Excellent, ton score est de ', Score, T1),
        string_concat(T1, ' / 20. Tu as de très fortes chances d''être présélectionné pour l''ENSA.', Resultat)
    ;   Ecole = 'ENSA', Score < 14.0 -> 
        string_concat('⚠️ Attention, ton score de ', Score, T1),
        string_concat(T1, ' / 20 est peut-être juste pour l''ENSA cette année. Regarde aussi les FST.', Resultat)
    ;   (Ecole = 'FMP' ; Ecole = 'MEDECINE'), Score >= 14.5 -> 
        string_concat('✅ Excellent, ton score est de ', Score, T1),
        string_concat(T1, ' / 20. C''est un bon score pour le concours commun de Médecine.', Resultat)
    ;   string_concat('Score calculé : ', Score, Resultat) % Par défaut
    ).

% ---------------------------------------------------------
% 4. UTILITAIRES DE RECHERCHE AVANCÉE (NLP BRIDGE)
% ---------------------------------------------------------

% expert_respond(Message, Reponse)
% Cherche une réponse intelligente dans toute la base.
expert_respond(Input, Reponse) :-
    string_lower(Input, Msg),
    (   % 1. Recherche d'une école/institution
        (sub_string(Msg, _, _, _, 'ensa') -> etablissement('ENSA', Ville, Dipl, Dur, _), atomic_list_concat(['L\'ENSA (', Ville, ') propose un ', Dipl, ' en ', Dur, ' ans.'], Reponse))
    ;   (sub_string(Msg, _, _, _, 'encg') -> etablissement('ENCG', Ville, Dipl, Dur, _), atomic_list_concat(['L\'ENCG (', Ville, ') propose un ', Dipl, ' en ', Dur, ' ans.'], Reponse))
    ;   (sub_string(Msg, _, _, _, 'medecine') ; sub_string(Msg, _, _, _, 'fmp')) -> etablissement('FMP', Ville, Dipl, Dur, _), atomic_list_concat(['La Faculté de Médecine (', Ville, ') prépare au ', Dipl, ' en ', Dur, ' ans.'], Reponse)
    ;   (sub_string(Msg, _, _, _, 'cpge') ; sub_string(Msg, _, _, _, 'prepa')) -> Reponse = 'Les CPGE (Classes Préparatoires) sont accessibles en 2 ans après le Bac pour intégrer les grandes écoles d\'ingénieurs ou de commerce.'
    ;   (sub_string(Msg, _, _, _, 'bts') ; sub_string(Msg, _, _, _, 'dut')) -> Reponse = 'Le BTS et le DUT sont des formations courtes de 2 ans très prisées pour une insertion professionnelle rapide.'
    
    ;   % 2. Recherche par type de Bac
        (sub_string(Msg, _, _, _, 'svt') -> debouche('SVT', Dom, Ec, Cons), atomic_list_concat(['Avec un Bac SVT, tu peux viser : ', Dom, ' (', Ec, '). ', Cons], Reponse))
    ;   (sub_string(Msg, _, _, _, 'pc') ; sub_string(Msg, _, _, _, 'physique')) -> debouche('PC', Dom, Ec, Cons), atomic_list_concat(['Avec un Bac PC, tu peux viser : ', Dom, ' (', Ec, '). ', Cons], Reponse)
    ;   (sub_string(Msg, _, _, _, 'sm') ; sub_string(Msg, _, _, _, 'math')) -> debouche('SM', Dom, Ec, Cons), atomic_list_concat(['Avec un Bac SM, tu peux viser : ', Dom, ' (', Ec, '). ', Cons], Reponse)
    
    ;   % 3. Définitions générales
        definition(Terme, Def), sub_string(Msg, _, _, _, Terme) -> Reponse = Def
        
    ;   % 4. Fallback vers l'ancienne méthode de mots-clés
        trouver_ecole_par_mot_cle(Msg, Reponse)
    ).

% Helper: Recherche par mot-clé (Backup)
trouver_ecole_par_mot_cle(Message, Resultat) :-
    (   (sub_string(Message, _, _, _, 'ensa') ; sub_string(Message, _, _, _, 'ingénieur')) ->
        Resultat = 'L\'ENSA (École Nationale des Sciences Appliquées) est accessible après le Bac. Elle propose un cycle préparatoire de 2 ans et un cycle d\'ingénieur de 3 ans.'
    ;   (sub_string(Message, _, _, _, 'encg') ; sub_string(Message, _, _, _, 'commerce')) ->
        Resultat = 'L\'ENCG (École Nationale de Commerce et de Gestion) est spécialisée dans le management, l\'audit et le marketing (durée 5 ans).'
    ;   (sub_string(Message, _, _, _, 'médecine') ; sub_string(Message, _, _, _, 'fmp')) ->
        Resultat = 'Pour la Médecine (FMP), l\'admission se fait par concours commun national après présélection sur dossier.'
    ;   (sub_string(Message, _, _, _, 'fst') ; sub_string(Message, _, _, _, 'technique')) ->
        Resultat = 'La FST (Faculté des Sciences et Techniques) propose des licences professionnelles et des masters dans divers domaines techniques.'
    ;   (sub_string(Message, _, _, _, 'svt') ; sub_string(Message, _, _, _, 'sciences de la vie')) ->
        Resultat = 'Avec un Bac SVT, tu peux postuler en Médecine, à l\'ENSA, à la FST, ou faire une licence en biologie à la Faculté des Sciences.'
    ;   Resultat = 'Je n\'ai pas trouvé de réponse précise pour ce mot-clé, mais je suis expert en orientation post-bac au Maroc. Peux-tu préciser ta question ?'
    ).

% ---------------------------------------------------------
% 3. CHATBOT INTERACTIF EN LIGNE DE COMMANDE (Le "Start")
% ---------------------------------------------------------
% Lance le système de recommandation via la commande : start.
start :-
    writeln('==============================================================='),
    writeln('🤖 BIENVENUE DANS YAFI : Le Conseiller d''Orientation IA'),
    writeln('==============================================================='),
    writeln('Quel est ton domaine favori ?'),
    writeln('1. MILITAIRE ET SÉCURITÉ'),
    writeln('2. INGÉNIERIE, SCIENCES ET TECHNOLOGIE'),
    writeln('Tapez le nom exact entre quotes (ex: ''MILITAIRE ET SÉCURITÉ''.).'),
    read(Domaine),
    writeln(''),
    writeln('➡️ Voici les grandes écoles dans ce domaine :'),
    afficher_ecoles_domaine(Domaine),
    writeln('==============================================================='),
    writeln('Pour voir les détails d''une école, utilise la requête :'),
    writeln('?- info_etablissement(''NomEcole'', Categorie, Info).').

% Règle d'affichage (itère et échoue proprement)
afficher_ecoles_domaine(Domaine) :-
    nouvel_etablissement(Ecole, Domaine),
    write(' 🏫 - '), writeln(Ecole),
    fail.
afficher_ecoles_domaine(_).

% ---------------------------------------------------------
% 4. FONCTION UTILITAIRE : LISTER TOUTES LES CATEGORIES D'INFO
% ---------------------------------------------------------
% Exemple : lister_categories('ARM').
lister_categories(Ecole) :-
    writeln('Catégories d''informations disponibles pour cette école :'),
    setof(Cat, Info^(info_etablissement(Ecole, Cat, Info)), ListeCats),
    afficher_liste(ListeCats).

afficher_liste([]).
afficher_liste([H|T]) :-
    write(' 📌 '), writeln(H),
    afficher_liste(T).
