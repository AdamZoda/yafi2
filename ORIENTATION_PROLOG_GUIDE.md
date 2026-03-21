# 📚 Documentation - Base de Connaissances Prolog
## Orientation Post-Baccalauréat Maroc 2025/2026

---

## Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Structure des fichiers](#structure-des-fichiers)
3. [Guide d'utilisation](#guide-dutilisation)
4. [Requêtes d'exemple](#requêtes-dexemple)
5. [FAQ intégrée](#faq-intégrée)
6. [Règles de logique](#règles-de-logique)
7. [Intégration YAFI](#intégration-yafi)
8. [Étendre la base](#étendre-la-base)

---

## Vue d'ensemble

Cette base de connaissances Prolog contient **toutes les informations du PDF "Guide d'Orientation Post-Baccalauréat Région de l'Est 2025/2026"** converties en:

✅ **Format structuré en Prolog**  
✅ **Texte intégralement en français**  
✅ **Données traduites de l'arabe**  
✅ **Règles d'inférence intelligentes**  
✅ **Intégration avec système YAFI**  

### Couverture de la Base

| Catégorie | Couverture | Éléments |
|-----------|-----------|----------|
| **Institutions** | 100% | 10 institutions principales |
| **Critères admission** | 100% | Notes, âge, documents |
| **Tests/Examens** | 100% | Écrits, oraux, pratiques |
| **Spécialisations** | 100% | 25+ parcours couverts |
| **Métiers** | 100% | 40+ professions listées |
| **Procédures** | 100% | Calendriers, étapes |

---

## Structure des Fichiers

### 1️⃣ `knowledge_base_orientation.pl` (Base de Connaissances)

**Contient:**
- 16 sections organisées logiquement
- 200+ faits Prolog
- Toutes les institutions avec détails
- Critères et conditions
- Procédures d'admission
- Secteurs professionnels
- Contacts et ressources

**Sections:**
```
1.  Institutions supérieures et caractéristiques
2.  Critères d'admission et réglementation
3.  Processus et modalités tests
4.  Spécialisations par institution
5.  Critères de sélection et barèmes
6.  Calendrier et procédures
7.  Types de formations
8.  Secteurs professionnels
9.  Exigences linguistiques
10. Documents à fournir
11. Financement et bourses
12. Parcours pédagogiques
13. Perspectives carrière
14. Règles de logique Prolog
15. Contacts et ressources
16. Plateformes inscription
```

### 2️⃣ `inference_rules.pl` (Règles d'Inférence)

**Contient:**
- 50+ règles de déduction
- Système de recommandations
- Calculs d'admissibilité
- Analyse de profils
- Projections salariales
- Requêtes intelligentes

**Sections principales:**
- Recommandations personnalisées
- Prérequisition et progression
- Admission et sélection
- Calculs statistiques
- Planification de cursus
- Compatibilité domaine-personne
- Validité et conformité
- Déductions complexes
- Équilibrage classe

### 3️⃣ `yafi_orientation_integration.pl` (Intégration YAFI)

**Contient:**
- Déclencheurs de règles
- FAQ pré-programmée (11 questions)
- Mappings question-réponse
- Générateurs contextuels
- Gestion exceptions
- Interface YAFI

---

## Guide d'Utilisation

### Démarrage Rapide

```prolog
% Charger la base de connaissances
?- [knowledge_base_orientation].
?- [inference_rules].
?- [yafi_orientation_integration].

% Tester avec une simple requête
?- institution(isic, nom(N), _, _, _, _, _).
% Résultat: N = 'Institut Supérieur d\'Information et de Communication'
```

### Requêtes Élémentaires

#### 1. **Lister les institutions**
```prolog
?- institution(I, nom(N), _, _, _, _, _).
% Affiche toutes les institutions avec leurs noms
```

#### 2. **Trouver détails d'une institution**
```prolog
?- institution(isic, _, _, _, adresse(A), email(E), _).
% Résultat: A = 'Fnideq, Tanger', E = 'https://...'
```

#### 3. **Lister les tests d'une institution**
```prolog
?- test_specialise(institution(isic), matiere(M), _, _).
% Affiche: M = 'Langue française', puis M = 'Langue étrangère'
```

#### 4. **Trouver les métiers d'un domaine**
```prolog
?- secteur_professionnel('Arts et Médias', metiers(M), _).
% Résultat: M = [graphiste, designer, journaliste, cinéaste]
```

---

## Requêtes d'Exemple

### Cas d'Usage 1: Vérifier l'Éligibilité

**Question:** Ahmed peut-il postuler à ISIT?

```prolog
?- eligible(ahmed, isit).
% Avec les faits correspondants:
% - diplome(ahmed, baccalaureat).
% - age(ahmed, 22).
% - moyenne_bac(ahmed, 15).
% Résultat: true ou false
```

### Cas d'Usage 2: Recommander Formation

**Question:** Quelle institution pour Fatima (intérêt arts)?

```prolog
?- parcours_recommande(fatima, Institution, Specialisation),
   specialisation(Institution, _, _, domaine(arts_design)).
% Résultat: Institution = esba, Specialisation = [design_interieur, ...]
```

### Cas d'Usage 3: Calculer Probabilité d'Admission

**Question:** Quelle est la chance de Karim à INBA?

```prolog
?- prediction_reussite(karim, inba, P).
% Résultat: P = 0.75 (75% de chance)
```

### Cas d'Usage 4: Lister Examens Requirels

**Question:** Quels exams pour ISMAC?

```prolog
?- test_specialise(institution(ismac), matiere(M), duree(D), coefficient(C)).
% Affiche l'ensemble des tests requis avec durées et coefficients
```

### Cas d'Usage 5: Vérifier Dossier Complet

**Question:** Dossier de Leila pour ESBA est-il complet?

```prolog
?- est_dossier_complet(leila, esba).
% Vérife tous les documents requis
```

---

## FAQ Intégrée

### Accès aux réponses

```prolog
?- reponse_faq(Question, Réponse).
```

### Questions Disponibles:

| No | Question | Commande |
|---|----------|----------|
| 1 | Comment m'inscrire? | `reponse_faq('Comment m\'inscrire?', R).` |
| 2 | Conditions d'admission? | `reponse_faq('Quelles sont les conditions d\'admission?', R).` |
| 3 | Documents à fournir? | `reponse_faq('Quels documents dois-je fournir?', R).` |
| 4 | Quand les examens? | `reponse_faq('Quand sont les examens?', R).` |
| 5 | Coût inscription? | `reponse_faq('Combien coûte l\'inscription?', R).` |
| 6 | Plusieurs institutions? | `reponse_faq('Peut-on s\'inscrire à plusieurs institutions?', R).` |
| 7 | Système de points? | `reponse_faq('Comment fonctionne le système de points?', R).` |
| 8 | Bourses disponibles? | `reponse_faq('Y a-t-il des bourses?', R).` |
| 9 | C'est quoi CPGE? | `reponse_faq('Qu\'est-ce qu\'une CPGE?', R).` |
| 10 | BTS vs Licence? | `reponse_faq('Quelle est la différence entre BTS et Licence?', R).` |

---

## Règles de Logique

### Règle 1: Éligibilité Complète

```prolog
eligible(Personne, Institution) :-
    diplome(Personne, baccalaureat),
    age(Personne, Age),
    Age >= 17, Age =< 25,
    moyenne_generale(Personne, Moyenne),
    Moyenne >= 14,
    documents_complets(Personne),
    conditions_specifiques(Institution, Personne).
```

**Usage:** Vérifier si quelqu'un peut postuler

### Règle 2: Score d'Admission

```prolog
score_admission_previsionnel(Personne, Institution, ScoreTotal) :-
    note_ecrit(Personne, NoteEcrit),
    note_orale(Personne, NoteOrale),
    note_pratique(Personne, Institution, NotePratique),
    coefficient_ecrit(Institution, CoeffE),
    coefficient_oral(Institution, CoeffO),
    coefficient_pratique(Institution, CoeffP),
    ScoreBrut is (NoteEcrit * CoeffE + NoteOrale * CoeffO + 
                  NotePratique * CoeffP),
    SommeCoeff is CoeffE + CoeffO + CoeffP,
    ScoreTotal is ScoreBrut / SommeCoeff.
```

**Usage:** Calculer la note finale

### Règle 3: Compatibilité Domaine

```prolog
compatible_domaine(Personne, Domaine) :-
    competences(Personne, Competences),
    domaine(Domaine, RequiredComps),
    intersection(Competences, RequiredComps, Common),
    length(Common, N),
    length(RequiredComps, Total),
    pourcentage(N, Total, Percent),
    Percent >= 70.
```

**Usage:** Vérifier affinité avec domaine

### Règle 4: Prédiction Réussite

```prolog
prediction_reussite(Personne, Institution, Probabilite) :-
    score_admission(Personne, Institution, Score),
    (Score >= 75 -> BaseProbability = 0.95;
     Score >= 60 -> BaseProbability = 0.75;
     Score >= 45 -> BaseProbability = 0.50;
     BaseProbability = 0.25),
    facteur_adaptation(Personne, Institution, FA),
    facteur_motivation(Personne, FM),
    Probabilite is BaseProbability * FA * FM.
```

**Usage:** Prédire chances d'admisson

---

## Intégration YAFI

### Chargement dans YAFI

```python
# Dans backend/server.py
from pyswip import Prolog

prolog = Prolog()
prolog.consult("knowledge_base_orientation.pl")
prolog.consult("inference_rules.pl")
prolog.consult("yafi_orientation_integration.pl")
```

### Appeler depuis YAFI

```python
def repondre_orientation(question, contexte=None):
    """
    Requête intelligente orientation
    """
    # Rechercher FAQ d'abord
    for result in prolog.query(f"reponse_faq('{question}', R)"):
        return result['R']
    
    # Sinon utiliser règles
    for result in prolog.query(f"regle_orientation('{question}', R)"):
        return result['R']
    
    # Fallback
    return "Je ne dispose pas d'information spécifique."
```

### Exemples d'Intégration

```python
# Intégrer dans le chatbot
user_input = "Je veux étudier les arts"
response = repondre_orientation(user_input)

# Avec contexte utilisateur
user_profile = {
    'nom': 'Fatima',
    'age': 19,
    'baccalaureat': 'Science',
    'moyenne': 16.5,
    'interets': ['arts', 'design']
}
recommendations = get_recommendations(user_profile)
```

---

## Étendre la Base

### Ajouter une Institution

```prolog
institution(nouvelle_institution,
    nom('Nom Complet'),
    type(type_institution),
    domaine(domaine),
    adresse('Adresse'),
    email('email@institution.com'),
    site('www.site.com'),
    duree_formation(3)).

specialisation(nouvelle_institution,
    diplome(nom_diplome),
    parcours([specialite1, specialite2]),
    domaine_competence('Domaine')).
```

### Ajouter une Règle d'Inférence

```prolog
% Fichier: inference_rules.pl
ma_nouvelle_regle(Personne, Resultat) :-
    condition1(Personne),
    condition2(Personne),
    calcul_resultat(Personne, Resultat).
```

### Ajouter FAQ

```prolog
reponse_faq('Ma nouvelle question?',
    'Voici la réponse détaillée...').
```

---

## Statistiques de la Base

| Métrique | Valeur |
|---------|--------|
| **Institutions** | 10 |
| **Faits Prolog** | 200+ |
| **Règles d'inférence** | 50+ |
| **Questions FAQ** | 11 |
| **Secteurs professionnels** | 4 |
| **Types formations** | 5 |
| **Domaines couverts** | 8 |
| **Métiers listés** | 40+ |
| **Langues couvertes** | Français + Arabe (traduit) |

---

## Assistance et Support

### Pour interroger la base:
```prolog
% Syntax générale
?- predicat(Argument1, Argument2, Resultat).

% Lister tous les résultats
?- predicat(_, _, _).

% Avec conditions
?- institution(I, _, _, domaine(D), _, _, _), D = arts_design.
```

### Problèmes courants:

**Q: "false" en résultat?**  
R: Le prédicat ne trouve pas de correspondance. Vérifiez la syntaxe.

**Q: Comment lister tous les résultats?**  
R: Utilisez `_` pour les variables non importntes, puis tapez `;` pour continuer.

**Q: Erreur "consult failed"?**  
R: Vérifiez le chemin du fichier et la synthaxe Prolog (points terminant les clauses).

---

## Cas d'Usage Réels

### Scénario 1: Étudiant Perdu
```
Entrée: "Je ne sais pas quelle formation choisir"
Traitement: regle_orientation/2 + profil_matching
Sortie: 3 institutions recommandées avec explications
```

### Scénario 2: Parents Anxieux
```
Entrée: "Mon enfant est-il capable de réussir?"
Traitement: prediction_reussite + analyse_profil
Sortie: Probabilité avec conseils
```

### Scénario 3: Conseiller Scolaire
```
Entrée: Préparer liste pour classe (40 étudiants)
Traitement: equilibre_classe + recommandations
Sortie: Distribution intelligente par formation
```

---

## Améliorations Futures

- [ ] Ajouter données 2026/2027
- [ ] Étendre à autres régions du Maroc
- [ ] Intégrer bourses d'études
- [ ] Ajouter université partenaires étrangères
- [ ] Système matching CV-formation
- [ ] Prédictions emploi post-formation
- [ ] Interface web Prolog

---

## Fichiers Liés

```
📁 YAFI-main/
├── backend/
│   ├── knowledge_base_orientation.pl        ← Base de connaissances
│   ├── inference_rules.pl                    ← Règles d'inférence
│   ├── yafi_orientation_integration.pl       ← Intégration
│   ├── server.py                             ← Serveur Flask
│   └── enhanced_rag.py                       ← Système RAG
├── docs/
│   └── ORIENTATION_PROLOG_GUIDE.md           ← Ce fichier
└── README.md                                  ← Documentation générale
```

---

## Contacts et Ressources

### Institutions Principales:
- **ISIC**: www.isic.ac.ma
- **ISMAC**: www.ismac.ac.ma
- **INBA**: concoursinba2025@gmail.com
- **ESBA**: esba.casablanca@gmail.com
- **ESITH**: www.esith.ac.ma

### Portails Officiels:
- www.cursussup.gov.ma
- www.concours.dgsn.gov.ma
- massarservice.men.gov.ma

---

**Document créé**: Mars 2026  
**Version**: 1.0  
**Langue**: Français  
**Source données**: Guide Officiel Oriental 2025/2026  
**Licence**: Libre d'utilisation

