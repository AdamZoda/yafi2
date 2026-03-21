# YAFI Backend - Moteur d'Orientation Scolaire

Ce dossier contient le cœur de l'intelligence artificielle de YAFI, un assistant virtuel conçu pour guider les étudiants marocains dans leur orientation post-bac.

## 🧠 Architecture du Système

Le backend fonctionne en combinant deux moteurs d'intelligence artificielle :

1. **Le Moteur Logique (Prolog)** : Gère les règles strictes, les calculs de notes, les seuils d'admission et les conditions pour chaque école. C'est le cerveau formel.
2. **Le Moteur RAG Vectoriel (Python/FAISS)** : Comprend le langage naturel, effectue des recherches sémantiques ultra-rapides dans une base de données de connaissances et génère des réponses textuelles via un LLM (sans hallucinations).

### 📂 Fichiers Principaux

* **`server.py`** : Le point d'entrée principal. C'est un serveur web (Flask) qui reçoit les questions des utilisateurs, décide quel moteur utiliser (Prolog ou RAG), et retourne la réponse.
* **`knowledge.pl`** : La base de connaissances brute. Contient la liste des écoles, les villes, les types de bac et les règles d'admission.
* **`vector_knowledge.py`** : Le gestionnaire du système de recherche vectorielle (RAG Professionnel).
* **`embedding_service.py`** : Transforme le texte en vecteurs mathématiques pour permettre à l'IA de comprendre le "sens" des questions.
* **`conversation_manager.py`** : Sauvegarde l'historique de la conversation de chaque utilisateur pour que YAFI se souvienne du contexte (ex: si vous posez une question de suivi).
* **`prompt_engine.py`** : Gère les instructions dictées à l'IA pour garantir des réponses sûres, précises et sans invention.

### 🗄️ Base de Données Vectorielle (FAISS)

* **`build_vector_index.py`** : Script à lancer si vous modifiez/ajoutez de nouvelles connaissances. Il découpera le texte et recréera la base de données de recherche.
* **`knowledge_chunks.json`** et **`yafi_vector_index.faiss`** : Les fichiers générés par le script ci-dessus, utilisés par le moteur RAG pour trouver les informations instantanément.

## 🚀 Comment Lancer le Serveur

1. Assurez-vous d'avoir Python installé avec toutes les dépendances requises :
   ```bash
   pip install flask flask-cors pyswip sentence-transformers faiss-cpu numpy python-dotenv supabase
   ```
2. Lancez le serveur principal :
   ```bash
   python server.py
   ```
   *Le serveur démarrera sur le port 5000 (http://localhost:5000).*

## ⚙️ Maintenance & Mise à Jour

Si vous mettez à jour les informations d'orientation (nouveaux seuils, nouvelles écoles) dans le fichier de contexte (`yafi_knowledge_context.json`) :

1. Ouvrez votre terminal dans ce dossier `backend`.
2. Exécutez le script de reconstruction :
   ```bash
   python build_vector_index.py
   ```
3. Redémarrez `server.py` pour qu'il charge la nouvelle base de données.
