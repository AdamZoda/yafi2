# YAFI — Your AI for Intelligence (Orientation Chatbot)

Ce projet est un **chatbot d'orientation post-bac** conçu pour aider les étudiants marocains à choisir une filière, une école et une stratégie d'admission en fonction de leur profil (moyenne, spécialité, objectifs, contraintes, etc.).

## 🧠 Concept central

YAFI combine deux sources de "connaissance" pour répondre :

1. **Une base de connaissances logique (Prolog)**
   - Implémentée dans `backend/knowledge_base_orientation`
   - Contient des règles métier, des correspondances filière/bac, des critères d'admission
   - Permet de raisonner par règles (ex : "si bac SM et moyenne >= 14 alors ...")

2. **Un modèle de génération de texte (LLM / Ollama)**
   - Utilisé pour produire des réponses naturelles et détaillées
   - Intégré via `backend/llm_engine.py` (appel HTTP vers Ollama)
   - Le système combine les résultats Prolog + réponses LLM pour produire une réponse cohérente.

Cette architecture est un **système RAG (Retrieval-Augmented Generation)** : on récupère d'abord des faits/critères précis (Prolog + recherche vectorielle), puis on génère une réponse LLM enrichie.

## 🧩 Architecture simplifiée

```
Frontend (React + Vite)  <--->  Backend Flask (Python)  <--->  Ollama LLM
                                       |
                                       +--> Prolog (PySwip)
                                       +--> Recherche vectorielle (FAISS + embeddings)
                                       +--> Supabase (Optionnel pour mémoire utilisateur)
```

## 🏗️ Structure du projet

- `backend/`
  - `server.py` : serveur Flask principal (point d'entrée API)
  - `server_optimized_v4.py` : variante optimisée côté backend
  - `llm_engine.py` : couche d'abstraction pour interroger Ollama
  - `knowledge_base_orientation` : base de règles Prolog
  - `vector_knowledge.py` : recherche vectorielle / index FAISS
  - `user_memory.py` : stockage de mémoire utilisateur (Supabase)

- `src/` (frontend React + TypeScript)
  - `components/` : UI (chat, thèmes, sidebar, etc.)
  - `lib/` : utils, API, thèmes
  - `hooks/`, `contexts/` : état global

- `public/` : assets statiques (images, modèles 3D)

## 🚀 Comment lancer le projet (mode développement)

### 1) Démarrer l'API Backend

```bash
cd backend
pip install -r ../requirements.txt
python server.py
```

Le backend écoute normalement sur **http://localhost:5000**.

### 2) Démarrer le Frontend

```bash
npm install
npm run dev
```

Le frontend s'ouvre sur **http://localhost:5173**.

### 3) Lancer Ollama (LLM)

Ollama doit être en cours d'exécution pour que le chatbot génère des réponses intelligentes.

```bash
ollama serve
```

Par défaut, Ollama écoute sur **http://localhost:11435**.

## ✅ Comment ça marche (flux de requête)

1. L'utilisateur envoie une question depuis l'interface (ex : "Que faire avec un bac PC ?").
2. Le frontend envoie une requête POST à `/chat` sur le backend.
3. Le backend :
   - Analyse l'intention / extrait les paramètres (moyenne, bac, etc.)
   - Interroge Prolog pour obtenir des règles et des recommandations
   - (Optionnel) Utilise la recherche vectorielle (FAISS) pour retrouver des extraits de connaissances
   - Compose un prompt et envoie la demande à Ollama via l'API
   - Retourne un objet JSON contenant la réponse et la source (Prolog, LLM, etc.)

## 🔍 Comment tester rapidement

### Vérifier les services
- Backend : `python backend/server.py`
- Ollama : `ollama serve`

### Envoyer une requête de test

```bash
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{"message":"Bonjour","session_id":"test"}'
```

## 📌 Notes importantes

- Si Ollama n'est pas disponible, le serveur peut tomber en mode dégradé (réponses basées uniquement sur Prolog).
- Le dossier `backend/` contient plusieurs versions de serveur (optimisé / non optimisé). Le plus stable actuellement est `server.py`.

---

Ce fichier est le point unique de documentation pour comprendre le projet et savoir quoi exécuter. Pour toute modification, relancer les services (backend + Ollama) et vérifier les logs de `backend/server.py`.
