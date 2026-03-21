% ============================================================================
% Fichier d'Intégration - YAFI avec Base Orientation Post-Bac
% Mode d'emploi et mappings question-réponse
% ============================================================================

% ============================================================================
% SECTION 1: CHARGEMENT DES BASES DE CONNAISSANCE
% ============================================================================

% Charger les fichier basis Prolog
:- consult('knowledge_base_orientation.pl').
:- consult('inference_rules.pl').

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
    (Score >= 75 -> Verdict = 'Très bon potentiel';
     Score >= 60 -> Verdict = 'Bon potentiel';
     Score >= 45 -> Verdict = 'Potentiel acceptable';
     Verdict = 'Révision recommandée').

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
    competences(Personne, Comps),
    interets(Personne, Interets),
    
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

action_step(Personne, Institution, 'Préparer les documents') :-
    documents_obligatoires(Institution, _).

action_step(Personne, Institution, 'S\'entraîner aux examens') :-
    examens_requis(Institution, _).

action_step(Personne, Institution, 'Pratiquer l\'interview') :-
    test_oral_requis(Institution).

% ============================================================================
% SECTION 6: TRAITEMENT DES EXCEPTIONS
% ============================================================================

% Gestion des cas limites d'admission
cas_special_admission(Personne, Institution, ManipulationSpeciale) :-
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
    institution(Inst, nom(Nom), _, _, _, _, _),
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
