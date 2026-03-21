% ============================================================================
% Règles d'Inférence Avancées - Base Orientation Post-Baccalauréat
% Fichier complémentaire: inference_rules.pl
% ============================================================================

% ============================================================================
% SECTION 1: RÈGLES DE RECOMMANDATION PERSONNALISÉE
% ============================================================================

% Recommander une institution basée sur le profil
recommander_institution(Profil, Institution, Score) :-
    evaluator_profil(Profil, Scores),
    institution(Institution, _, _, _, _, _, _),
    calculate_match_score(Profil, Institution, Score),
    Score > 65.

% Évaluer les compétences du profil
evaluator_profil(profil(Domaine, Langues, Competences), Scores) :-
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
    matiere_bac(Personne, Matiere, Note, Coefficient),
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
    profil(Personne, Profil),
    objectif(Personne, Objectif),
    institution_cible(Objectif, InstCible),
    findall(Cours, cours_pertinent(Objectif, Cours), ListeCours),
    ordonner_par_prerequis(ListeCours, CheminProgressif).

% Plan de préparation personnalisé
plan_preparation(Personne, Institution, Schedule) :-
    examens_requis(Institution, Exams),
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
             competences(Etudiant, Comp),
             moyenne_generale(Etudiant, Moy)),
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
    profil(Personne, Profil),
    interet_principal(Personne, Domaine),
    institution(Institution, _, _, domaine(Domaine), _, _, _),
    specialisation(Institution, _, Specialisation, _),
    compatible_domaine(Personne, Domaine).

% Requête: Quels sont les examens à passer?
examens_concernant(Personne, Institution, ListeExamens) :-
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
