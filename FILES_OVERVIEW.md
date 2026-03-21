# Vue d'ensemble des fichiers du projet

Ce document explique **à quoi sert chaque fichier/élément principal** du projet YAFI (backend + frontend). Il sert de référence rapide pour comprendre la structure et le rôle de chaque composant.

---

## 🧩 Racine du projet

### `README.md`
- Documentation principale du projet (comment démarrer, architecture, fonctionnement).

### `package.json` / `vite.config.ts` / `tsconfig.json` / `tailwind.config.js`
- Configuration du frontend React (dépendances, build, TypeScript, TailwindCSS).

### `requirements.txt`
- Liste des dépendances Python nécessaires pour le backend.

### `.env`
- Fichier de configuration (variables d'environnement) partagé entre backend et frontend.

---

## 🧠 Backend (dossier `backend/`)

### Serveurs Web
- `server.py`
  - Serveur Flask principal. Expose l’API `/chat` et orchestre le pipeline (Prolog + LLM + RAG).

- `server_optimized.py`
  - Variante avec quelques optimisations (gestion de temps d’attente, logging). (Ancienne version)

- `server_optimized_v3.py`
  - Version itérative avec améliorations de performance et de tolérance d’erreurs.

- `server_optimized_v4.py`
  - Version actuelle optimisée (limite de timeout pour Ollama, fallback rapide, multithreading possible).

- `server_integration_example.py`
  - Exemple simple montrant comment consommer l’API `/chat` depuis un script externe.


### Gestion de la conversation
- `conversation_manager.py`
  - Gère l’historique de conversation (sessions, résumés, états de quiz/interactions).


### LLM / génération de texte
- `llm_engine.py`
  - Envoie des prompts à Ollama (via HTTP) et récupère des réponses.

- `prompt_engine.py`
  - Construction de prompts avancés pour le LLM (ajoute contexte, instructions, formatage).

- `response_builder.py`
  - Assemble la réponse finale (fusionne Prolog/RAG + LLM, ajoute métadonnées, source).


### Recherche vectorielle / connaissances
- `knowledge_base_orientation`
  - Base Prolog (règles métiers, correspondances Bac/filières, scoring).

- `vector_knowledge.py`
  - Gestion de la recherche par similarité (FAISS + embeddings).

- `build_vector_index.py`
  - Script pour transformer `yafi_knowledge_context.json` en un index FAISS (`yafi_vector_index.faiss`).

- `yafi_knowledge_context.json`
  - Données de connaissances (Q&A) utilisées pour la recherche vectorielle.

- `yafi_vector_index.faiss`
  - Index FAISS préconstruit utilisé par `vector_knowledge.py`.

- `knowledge_chunks.json`
  - Fichier de chunks texte produits par `build_vector_index.py`.


### Analyse & diagnostic
- `diagnose_data_issues.py`
  - Scripts utilitaires pour trouver des problèmes dans les données (format, encoding, etc.).

- `diagnose_response_source.py`
  - Vérifie si les réponses proviennent bien de la bonne source (Prolog vs LLM).

- `compare_ollama_responses.py`
  - Compare des réponses "avant/après" pour valider les améliorations d’Ollama.

- `trace_llm_detailed.py`
  - Trace détaillée des échanges avec Ollama (logs, prompts envoyés, temps). 


### Évaluation / tests
- `evaluate_huge.py`, `evaluate_logic.py`
  - Scripts de benchmarking/évaluation automatique des réponses avec des jeux de questions.

- `test_ollama_integration.py`, `test_ollama_permissions.py`, `test_ic.py`, `test_llm.py`, `test_server.py`, `test_complete_system.py`
  - Batteries de tests unitaires / d’intégration pour valider le fonctionnement du pipeline.

- `run_automated_tests.py`
  - Lance plusieurs tests en séquence et produit des résultats.


### Divers / utilitaires
- `intent_classifier.py`
  - Classifie la requête de l’utilisateur (type d’intention).

- `user_memory.py` + `user_memory.json`
  - Persistance d’une mémoire utilisateur (stockage de sessions et préférences) via Supabase ou fichier.

- `prompt_*`, `response_*` (divers scripts)
  - Scripts de prototypage / expérimentations autour de prompts et réponses.

- `ollama_advanced_config.py`
  - Fichier de configuration avancée pour l’intégration Ollama (modèles, paramètres, permissions).

- `upgrade_plan.md`
  - Plan de montée en version / roadmap pour améliorer le backend.

- `results.txt` / `results_final.txt` / `eval_results*.txt` / `huge_results*.txt`
  - Sorties de tests / évaluations (générées automatiquement).

---

---

## ✨ Frontend (dossier `src/`)

### Structure générale
- `src/components/`
  - Composants UI (chat, sidebar, header, modals, etc.).

- `src/lib/`
  - Utilitaires réutilisables : API client, thèmes, gestion de Supabase, etc.

- `src/hooks/` / `src/contexts/`
  - Hooks et contextes React pour l’état global (user, thème, session de chat).

- `src/types/`
  - Définitions TypeScript (interfaces, types de données pour API et réponses).


### Entrée principale
- `src/main.tsx` (ou équivalent)
  - Point d’entrée de l’application React.

- `src/App.tsx`
  - Composant racine qui orchestre les routes et l’UI globale.

---

## 🧩 Fichiers statiques

- `public/`
  - Images, modèles 3D, icônes statiques et ressources servies directement par le frontend.

---

## 🧪 Autres fichiers utiles (logs / tests)

- `test_out.txt` (ou autres fichiers de logs temporaires)
  - Fichiers de sortie de tests; peuvent être supprimés si vous voulez nettoyer le repo.

---

## ✅ Recommandation
Pour garder le projet clair, conserve uniquement :
- `README.md` (documentation principale)
- Fichiers source (backend + frontend)
- Fichiers de configuration (package.json, requirements.txt, tsconfig, etc.)

Tout fichier temporaire ou script de test peut être supprimé si tu ne l’utilises plus.
