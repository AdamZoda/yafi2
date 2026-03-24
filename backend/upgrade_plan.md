# 🚀 Plan d'Amélioration : Vers un YAFI 2.0 Plus Intelligent et Humain

Voici une série d'idées concrètes pour faire évoluer l'intelligence, le naturel et les capacités de résolution de problèmes complexes de l'assistant YAFI.

## Axe 1 : Améliorer le "Naturel" et l'Empathie (Humanisation)

Actuellement, les réponses (notamment celles de Prolog) sont souvent très structurées et informatives, mais peuvent manquer de chaleur.


### 1.2. Gestion Émotionnelle des Notes
*   **Idée** : Améliorer le conseiller d'orientation dans `server.py`. Si l'utilisateur donne une note très basse (ex: 9/20), le bot devrait exprimer de l'empathie, dédramatiser la situation, et se focaliser immédiatement sur les solutions alternatives (OFPPT, rattrapage, ou filières sans seuil) plutôt que de juste lister froidement les options.
*   **Implémentation** : Revoir la fonction `strategie_profil` dans `knowledge.pl` pour y inclure des "tags d'humeur" que Python interprétera pour choisir une introduction réconfortante ou félicitante.

### 1.3. Réponses Progressives (Streaming)
*   **Idée** : Au lieu de bloquer l'interface pendant 0.5s à 1s puis d'afficher un pavé de texte d'un coup, faire en sorte que le texte s'affiche lettre par lettre (streaming), comme ChatGPT ou Claude.
*   **Bénéfice** : L'interface paraîtra beaucoup plus fluide et "vivante", simulant un humain en train de taper.

---

## Axe 2 : Scénarios Complexes et Multi-Variables

Les étudiants posent souvent des questions croisées complexes : *"Je veux faire médecine, mais je n'aime pas le sang, j'hésite avec dentaire, et mes parents n'ont pas d'argent pour le privé. J'ai 16."*

### 2.1. L'Entretien Guidé (Mode "Consultation")
*   **Idée** : Si la demande est trop floue (ex: *"Je ne sais pas quoi faire"*), le bot ne doit pas essayer de deviner. Il doit initier une **série de questions dynamiques** :
    1. *"D'accord, procédons par élimination. Tu es plutôt plutôt chiffres, lettres, ou sciences du vivant ?"*
    2. *"Super, tu préfères des études longues (5+ ans) ou courtes pour travailler vite ?"*
    3. *"As-tu une contrainte géographique ?"*
*   **Implémentation** : Utiliser `conversation_manager.py` pour stocker un "état" (ex: `status: "in_vocational_quiz"`). Si ce statut est actif, les prochaines entrées utilisateur ne sont pas cherchées dans la base RAG, mais servent à remplir les variables du quiz.

### 2.2. Outil de Super-Comparaison
*   **Idée** : Que l'utilisateur puisse dire explicitement *"Compare ENSA et FST"*.
*   **Implémentation dans Prolog** : Créer une règle Prolog `comparer(EcoleA, EcoleB, ComparaisonOut)` qui va chercher les points communs (gratuit/public, ingénierie) et les différences (Parcours intégré vs Cycle Licence+Master, Localisations) et les présenter sous forme d'un petit tableau Markdown généré dynamiquement.

---

## Axe 3 : Enrichir la Base de Connaissances Initiale (Prolog & RAG)

La base est actuellement bonne, mais elle peut être étendue avec des données hyper-spécifiques.

### 3.1. Base de Données "Métiers du Futur" et Salaries
*   **Ajout** : Ne plus seulement parler d'**écoles**, mais parler de **métiers**.
*   **Nouvelles données dans `knowledge_chunks.json`** :
    *   *Data Scientist* : Salaire junior (~15k MAD), compétences requises, écoles menant à ce métier (INPT, ENSIAS, etc.).
    *   *Architecte Cloud* : Demande très forte, profils recherchés...
*   **Nouveau Flux** : L'utilisateur cherche *"Comment devenir développeur ?"* -> Le système trouve le chunk métier -> Lie ce chunk aux écoles formant à ce métier.

### 3.2. Intégration de Témoignages
*   **Idée** : Ajouter un fichier RAG spécifique contenant des mini-témoignages anonymisés d'anciens étudiants.
*   **Exemple** : *"Yassine, 23 ans : L'ENCG demande beaucoup de travail de groupe, il faut être très sociable."*
*   **Bénéfice** : Lorsqu'un étudiant demande "C'est difficile l'ENCG ?", le bot peut répondre avec les statistiques d'admission ET citer un "avis d'ancien" qualitatif, ce qui humanise drastiquement le retour.

### 3.3. Gestion Fine des Bourses (Minhaty, Bourses Privées)
*   **Idée** : Les aspects financiers sont cruciaux. Il faut enrichir la base sur les *Bourses d'Excellence*.
*   **Ajouts Prolog** : Connaître les écoles privées (UIR, UM6P, EMSI) qui offrent des bourses de mérite si l'étudiant a +16 ou +17 au Bac. Le bot pourra dire : *"L'UIR est chère (70 000 DH), mais avec ton 17/20, tu es quasi assuré d'avoir la bourse excellence à 100% !"*

---

## Axe 4 : Améliorations Techniques du RAG

### 4.1. Hybrid Search (BM25 + Dense Vectors)
*   **Le problème** : La recherche vectorielle pure est excellente pour le concept global, mais parfois mauvaise pour les acronymes ou les mots très spécifiques (ex: si l'utilisateur demande exactement le sigle obscur "ISCAE" mal épelé "ISCA").
*   **Amélioration (`vector_knowledge.py`)** : Combiner FAISS avec un algorithme BM25 (recherche par mots-clés exacts) et fusionner les scores. Cela permet d'avoir la compréhension conceptuelle des vecteurs ET la précision chirurgicale des mots-clés.

### 4.2. "Intent Classification" avant le Traitement
<<<<<<< HEAD
*   **Le problème** : Actuellement, `server.py` utilise une longue série de `if/elif` pour déterminer si on est dans un calcul de note, une recherche d'école, ou une salutation. Si les requêtes deviennent très complexes en langage naturel, ces `if` vont casser.
=======
*- [ ] **EST Integration** : Ajouter les informations sur l'École Supérieure de Technologie (Safi, Casa, GI, TM).
    - [x] Ajouter les faits Prolog (ESTS Safi: GI, TM, GIM, GESA, Mécatronique, etc.).
    - [x] Mettre à jour `KNOWN_ENTITIES` et handlers dans le backend.
    - [/] Vérifier les requêtes "EST à Safi" et "Score EST".
nt très complexes en langage naturel, ces `if` vont casser.
>>>>>>> 3257fc1 (final)
*   **Amélioration** : Utiliser un petit modèle d'Intelligence Artificielle de classification d'intentions rapide (ex: `scikit-learn` ou un mini modèle LLM local) directement au début de la route `/chat`. Le modèle catégorise le message entrant en une classe claire : `["CALCULATE_SCORE", "COMPARE_SCHOOLS", "QUIZ", "GENERAL_CHAT"]`. Le code python pourra ensuite router l'action avec une précision parfaite.

---

## Conclusion : État des Lieux et Prochaine Étape
**Le Serveur Backend tel qu'il est aujourd'hui est très solide technologiquement (RAG vectoriel complet).** 
La prochaine grande évolution n'est pas structurelle, mais qualitative :
1.  **Déléguer la mise en forme linguistique à un vrai modèle de langage connecté (OpenAI API ou Groq/Llama3 pour la rapidité)** en lui fournissant les données brutes (Prolog+Faiss) comme "vérité absolue".
2.  Ajouter des "scripts de conversation" pour faire de l'entretien actif (où l'IA pose des questions à l'étudiant).
