# Flux de traitement d’un message utilisateur

Ce document décrit **en détail** comment une question envoyée par l’utilisateur est traitée, depuis l’envoi dans le frontend jusqu’à la **réponse renvoyée** au client.

---

## 1) L’utilisateur envoie un message (Frontend)

1. L’utilisateur tape une question dans l’interface de chat.
2. Le frontend React construit une requête POST vers l’API backend.
3. Exemple de requête envoyée au backend :

```json
POST /chat
{
  "message": "Je veux faire ingénierie, que dois-je faire ?",
  "session_id": "session-123"
}
```

---

## 2) Réception côté Backend (Flask)

- Le backend écoute sur `/chat` (route définie dans `backend/server.py`).
- Dès réception de la requête, le backend :
  1. Récupère `message` + `session_id`.
  2. Met à jour l’historique de conversation via `ConversationManager`.
  3. Appelle les composants qui vont calculer une réponse.

### Fichier principal (pipeline)
- `backend/server.py` (ou `server_optimized_v4.py` selon le serveur utilisé)
  - Valide la requête
  - Récupère le contexte de session
  - Appelle `prompt_engine`, `vector_knowledge`, `llm_engine`, `knowledge_base_orientation`, etc.

---

## 3) Historique & contexte (ConversationManager)

- `backend/conversation_manager.py` maintient l’historique des messages par `session_id`.
- Il permet de :
  - Garder les derniers échanges (pour contexte multi-tour)
  - Fournir un résumé de contexte à injecter dans le prompt
  - Maintenir un état (ex : quiz, formulaire, étapes)

Exemple d’utilisation :
```python
conversation_manager.add_message(session_id, 'user', message)
context = conversation_manager.get_context_summary(session_id)
```

---

## 4) Extraction d’intentions (NLU)

- `backend/intent_classifier.py` peut être utilisé pour analyser la question et déterminer :
  - le type de demande (orientation, info école, débouché, etc.)
  - les entités (bac, moyenne, école, ville)

Ceci aide à guider le pipeline (quelle base de connaissances utiliser, quel prompt construire, etc.).

---

## 5) Recherche dans les données (RAG)

Deux sources principales de connaissances :

### 5.1 Prolog (Raisonnement logique)
- Fichier : `backend/knowledge_base_orientation`
- Ce fichier contient des règles métier (bac → filières, conditions, scoring).
- Il est interrogé via PySwip (bindings Python pour SWI-Prolog).

Exemple de requête simple :
- "Si j’ai Bac PC et 14 de moyenne, quelles filières sont recommandées ?"

### 5.2 Recherche vectorielle (FAISS)
- Fichier : `backend/vector_knowledge.py`
- Il utilise l’index FAISS (`yafi_vector_index.faiss`) et les embeddings générés par `EmbeddingService`.
- Permet de retrouver des passages pertinents dans `yafi_knowledge_context.json`.

Flux de création de l’index :
1. `build_vector_index.py` transforme le JSON en chunks (`knowledge_chunks.json`).
2. Ces chunks sont encodés en vecteurs (via `EmbeddingService`).
3. FAISS permet de rechercher les passages proches de la question.

---

## 6) Construction du prompt (Prompt Engineering)

- `backend/prompt_engine.py` assemble :
  - Contexte (conversation, historique, résumé)
  - Résultats Prolog / vector index
  - Instructions / règles de style
  - Format de sortie attendu (ex : JSON, sections)

Ce prompt est envoyé au LLM pour générer une réponse naturelle.

---

## 7) Appel au LLM (Ollama)

- `backend/llm_engine.py` fait la requête HTTP vers Ollama (par défaut `http://localhost:11435`).
- Il envoie :
  - le prompt construit
  - les paramètres (température, max tokens, etc.)

Si Ollama n’est pas disponible ou si le temps dépasse un seuil, le backend peut :
- revenir à une réponse basée uniquement sur Prolog
- renvoyer un message d’erreur / fallback

---

## 8) Construction de la réponse finale

- `backend/response_builder.py` fusionne les éléments :
  - Résultats Prolog (logiques)
  - Résultats RAG (passages similaires)
  - Réponse générée par Ollama

Il produit un objet JSON renvoyé au frontend, avec :
- `response` (texte final)
- `source` (LLM, Prolog, RAG)
- `metadata` (scores, temps de traitement, etc.)

### Exemple de réponse JSON
```json
{
  "response": "Pour un bac PC avec 14 de moyenne, tu peux viser les filières suivantes...",
  "source": "LLM+Prolog",
  "time_ms": 932
}
```

---

## 9) Frontend : affichage et continuité

- Le frontend affiche le texte renvoyé par l’API.
- Il peut proposer des suggestions, boutons rapides ou questions de suivi.
- En cas de dialogue multi-tour, le backend réutilise l’historique de la session pour améliorer la cohérence.

---

## 🛠️ Notes d’exécution (comment tester)

1) Démarrer Ollama :
```bash
ollama serve
```

2) Démarrer le backend :
```bash
cd backend
python server.py
```

3) Envoyer une requête de test :
```bash
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{"message":"Quelle école pour un bac PC?","session_id":"test"}'
```

---

Ce document explique **tout le pipeline**, de l’envoi du message jusqu’à la réponse finale, en couvrant les étapes de traitement internes. N’hésite pas à demander si tu veux qu’on ajoute un diagramme visuel ou un exemple de log détaillé.