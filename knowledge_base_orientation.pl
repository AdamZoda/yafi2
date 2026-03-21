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
    examen_national: 75,
    examen_regional: 25
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
peut_postuler(Personne, Institution) :-
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
