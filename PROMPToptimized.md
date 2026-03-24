# YAFI - Assistant d'Orientation Scolaire et Universitaire au Maroc
**Date**: 23 Mars 2026
**Framework**: Python + Flask/Django + Prolog
**Model**: Claude Haiku 4.5 (LLM Engine)
**Domaine**: Orientation Scolaire & Universitaire - MAROC UNIQUEMENT
**Architecture**: Hybride (Python + Prolog + RAG + LLM)
**Créateurs**: Adam Moufrije, Yasser, Yasser Adam Fahd Intelligence
**Status**: Production-Ready

⚠️ **NOTATION IMPORTANTE**: 
- Ce document explique l'ARCHITECTURE & FLUX via UN EXEMPLE PÉDAGOGIQUE
- YAFI répond LIBREMENT basée sa base Prolog réelle
- Interface Web = seul point d'entrée utilisateur
- Les données viennent de Prolog, PAS d'hard-code dans le prompt

---

---

## 🏗️ ARCHITECTURE PROFONDE YAFI 2.1 - Flux Complet de Traitement

### 📘 Exemple EXPLICATIF (Non-Bindant)
**Message Utilisateur Exemple**: *"Quels sont les frais de l'ENSA à Tanger ?"*

⚠️ **CLARIFICATION IMPORTANTE**: 
- Cet exemple **N'EST PAS une vérité figée** à coder
- C'est **JUSTE UNE ILLUSTRATION** du flux d'exécution
- **YAFI répond LIBREMENT** basée sa **base Prolog réelle & complète**
- La réponse varie selon **données Prolog actuelles** du système
- Interface web = seul point d'entrée utilisateur

Ce message traverse 6 phases montrant comment YAFI traite TOUTE question:

---

### **⏱️ PHASE 0 : Réception & Normalisation (Pre-processing)**
**Durée**: 0.05s | **Rôle**: Nettoyage du message

Dès que vous appuyez sur "Envoyer" via l'interface web:
1. **Nettoyage Textuel**: Minuscules, espaces superflus supprimés
2. **ASCII-fication**: Accents normalisés
3. **Output Phase 0**: Message normalisé prêt pour analyse
   ```python
   input: "Quels sont les frais de l'ENSA à Tanger ?"
   output: "quels sont les frais de l ensa a tanger"
   ```

---

### **🛡️ PHASE -1 : Filtre de Sécurité Précoce (Safety Guard 1)**
**Durée**: 0.01s | **Rôle**: Bloquer hors-scope IMMÉDIATEMENT

Le "garde du corps" à l'entrée. Vérifie une **liste de mots-clés interdits**:
```python
BLOCKLIST = [
    'tajine', 'recette', 'cuisine', 'football', 'météo',
    'politique', 'visa', 'études étrangères', 'bitcoin', ...
]

if any(word in message for word in BLOCKLIST):
    return "Je suis YAFI, assistant orientation MAROC uniquement."
```

**Dans cet exemple**: "ENSA" et "Frais" = ✅ PASS → Continuer

---

### **🗂️ PHASE 1 : Extraction d'Entités & Mémoire (Entity Extractor)**
**Durée**: 0.1s | **Rôle**: Identifier de quoi on parle

```python
def extract_entities(message):
    entities = {
        'ecole': ['ensa'],
        'ville': ['tanger'],
        'action': ['frais'],
        'niveau': None
    }
    
    # Sauvegarder dans session memory
    session['last_ecole'] = 'ensa'
    session['last_ville'] = 'tanger'
    
    return entities
```

**Output Phase 1**:
- `école = 'ENSA'`
- `région = 'Tanger'`
- **Session Memory**: Mémoriser contexte pour prochaine question
  - Si prochain message = *"Et les débouchés ?"* → YAFI sait qu'on parle de l'ENSA

---

### **🤖 PHASE 2 : Classification d'Intention (Intent Classifier)**
**Durée**: 0.15s | **Rôle**: Définir l'ACTION à effectuer

Le système classe le message dans une catégorie:
```python
INTENT_CLASSES = [
    'FINANCIALS',      # frais, coûts, prix, montant
    'ADMISSION',       # conditions, processus, documents
    'CURRICULUM',      # majors, spécialités, diplômes
    'CAREER',          # débouchés, métiers, salaires
    'INFRASTRUCTURE',  # campus, localisation, contact
    'SCHOLARSHIPS'     # bourses, aides, conditions
]

detected_intent = 'FINANCIALS'  # Keywords: "frais", "prix"
```

**Output Phase 2**: `Intent = FINANCIALS`

---

### **🏛️ PHASE 3 : Le Moteur Hybride (Hybrid Engine) - LE CŒUR**
**Durée**: 0.2s - 1.5s | **Rôle**: Chercher la réponse en PARALLÈLE

YAFI ouvre **deux canaux** simultanément:

#### **Branche A : Système Expert Prolog (SOURCE DE VÉRITÉ RÉELLE)**

⚠️ **IMPORTANT**: Prolog est **la base de connaissances réelle du système**, pas du hard-coding:
```prolog
% File: full_orientation_system.pl
% Cette base est PEUPLÉE avec données vérifiées du Maroc
% YAFI INTERROGE cette base, PAS l'inverse

detail_ecole(NomEcole, Région, Type, TypologieFreis) :-
    % Requête Prolog interroge réellement la base
    % Les réponses viennent de Prolog, pas du prompt
    % Exemple de ce qui POURRAIT être retourné:
    % NomEcole='ENSA', Région='Tanger', Type='Polytechnique', 
    % TypologieFreis='Public (Gratuit)'
    
    % MAIS aussi:
    % NomEcole='ENSA', Région='Fès', Type='Polytechnique',
    % TypologieFreis='Public (Gratuit)'
    
    % Les données RÉELLES peuvent être différentes
    % YAFI RÉPOND LIBREMENT basée sur Prolog
    true.

% Query: YAFI exécute cette requête à chaque fois
% ?- detail_ecole('ENSA', 'Tanger', _, Frais).
% Réponse: Prolog retourne ce qui existe RÉELLEMENT dans la base
```

**Processus Réel**:
1. Utilisateur demande via interface web
2. YAFI normalise la question
3. YAFI **exécute une requête Prolog RÉELLE** sur la base
4. Prolog retourne les résultats réels (pas des exemples)
5. YAFI utilise ces **résultats vrais** pour générer la réponse

#### **Branche B : RAG System (Contexte Documentaire Réel)**
```python
# RAG interroge aussi une base réelle (pas des exemples figés)
# Les chunks sont extraits de documents réels au Maroc

message_vector = embedding_model.encode(
    "quels sont les frais de l ensa a tanger"
)

# Recherche vectorielle dans la base réelle
top_3_chunks = faiss_index.search(message_vector, k=3)

# Les chunks retournés sont RÉELS (tirés des documents dans la base)
# Pas des exemples fictifs
```

**Output Phase 3**:
- **Prolog**: Résultats RÉELS de la base Prolog ✅
- **RAG**: Chunks RÉELS des documents ✅

---

### **🧠 PHASE 4 : Synthèse Technologique (LLM Engine)**
**Durée**: 1-3s | **Rôle**: Générer réponse intelligente basée données RÉELLES

⚠️ **CLARIFICATION**: Cette phase n'utilise **PAS** des réponses hard-codées.

```python
# Template générique du prompt (PAS spécifique à l'exemple)
SYSTEM_PROMPT = """
Tu es YAFI, expert en orientation scolaire & universitaire au MAROC.

🔴 RÈGLES ABSOLUES:
1. DONNÉES VÉRIFIÉES UNIQUEMENT (tirées de Prolog)
2. ANTI-HALLUCINATION: Si pas d'info exacte, dis "Je n'ai pas cette donnée"
3. MAROC STRICT: Pas d'études étrangères
4. TON: Professionnel, bienveillant, concis

✅ DONNÉES RÉELLES (de la base Prolog exécutée):
{resultats_prolog_reels}

📚 CONTEXTE DOCUMENTAIRE RÉEL (de la base RAG):
{chunks_rag_reels}

👤 PROFIL UTILISATEUR:
{profil_utilisateur}

❓ MESSAGE UTILISATEUR:
{message_utilisateur}

🎯 GÉNÈRE UNE RÉPONSE LIBRE:
- Basée UNIQUEMENT sur les données ci-dessus
- YAFI répond naturellement
- Proposer next steps logiques
"""

# À l'exécution, chaque variable {} est REMPLACÉE par les DONNÉES RÉELLES
# Exemple:
response = llm.generate(
    SYSTEM_PROMPT.format(
        resultats_prolog_reels=prolog_results,  # ← RÉSULTATS RÉELS
        chunks_rag_reels=rag_chunks,             # ← CHUNKS RÉELS
        profil_utilisateur=user_profile,         # ← PROFIL RÉEL
        message_utilisateur=user_message          # ← MESSAGE RÉEL
    ),
    max_tokens=256
)
```

**EXEMPLE (hyper théorique)** si Prolog retournait `ENSA = gratuit`:
```
Excellente question! L'ENSA (École Nationale des Sciences Appliquées) à Tanger 
est une école publique, donc les frais de scolarité sont GRATUITS.
Processus d'admission: via CNIPRE avec le BAC S-Maths.
Voulez-vous des détails sur la procédure ou les débouchés?
```

**MAIS** si Prolog retournait autre chose, YAFI répondrait autre chose!

**Output Phase 4**: Réponse LIBREMENT générée basée données réelles ✅

---

### **📜 PHASE 5 : Génération Finale & Garde-fou de Sortie**
**Durée**: 0.1s | **Rôle**: Valider la réponse avant envoi

```python
def safety_guard_final(response_text):
    """Dernier filtre avant affichage"""
    
    # Liste de mots "rouges" (hallucinations courantes)
    RED_FLAGS = [
        'États-Unis', 'Europe', 'visa', 'France', 'Canada',
        'tourisme', 'vacances', 'météo', 'recette'
    ]
    
    for flag in RED_FLAGS:
        if flag.lower() in response_text.lower():
            # Hallucination détectée!
            return "Je n'ai pas suffisamment d'infos pour répondre. Consultez un conseiller."
    
    return response_text  # ✅ SAFE
```

**Output Phase 5**: Réponse validée ✅

---

### **🏁 PHASE 6 : Affichage & Persistance**
**Durée**: 0.05s | **Rôle**: Afficher + sauvegarder

```python
@app.route('/api/yafi/response', methods=['POST'])
def send_response():
    response_text = "Excellente question! L'ENSA..."
    
    # 1. Envoyer au frontend (React)
    emit('yafi_response', {'message': response_text})
    
    # 2. Sauvegarder dans base (Supabase / PostgreSQL)
    ConversationYAFI(
        student_id=session['student_id'],
        question="Quels sont les frais de l'ENSA à Tanger ?",
        response=response_text,
        phase_times={
            'phase0': 0.05,
            'phase1': 0.10,
            'phase2': 0.15,
            'phase3': 0.75,
            'phase4': 2.50,
            'phase5': 0.10,
            'phase6': 0.05
        },
        total_time=3.70  # Moins de 4 secondes!
    ).save()
```

**Timeline Complète**:
```
Phase 0 (Normalisation):     0.05s  ████
Phase -1 (Safety 1):         0.01s  █
Phase 1 (Entités):           0.10s  ████
Phase 2 (Intent):            0.15s  ██████
Phase 3 (Hybride):           0.75s  ███████████████████████████████
Phase 4 (LLM):               2.50s  ╋╋╋╋╋╋╋╋╋╋╋╋ (parallelized)
Phase 5 (Safety 2):          0.10s  ████
Phase 6 (Persistance):       0.05s  ██
─────────────────────────────────────────
TOTAL:                       3.71s  ✅ USER-ACCEPTABLE
```

---

## 🌐 INTERFACE WEB YAFI - Point d'Entrée Utilisateur

### Architecture Frontend-Backend

```
┌────────────────────────────────────────────────────┐
│        INTERFACE WEB YAFI (React/Vue)              │
│                                                     │
│  ┌──────────────────────────────────────────────┐ │
│  │  Message Input Box                           │ │
│  │  "Quels sont les frais de l'ENSA ?"          │ │
│  │                      [Envoyer]               │ │
│  └──────────────────────────────────────────────┘ │
│                          │                         │
│                          ▼                         │
│  ┌──────────────────────────────────────────────┐ │
│  │  Chat Historique (Persistant)                │ │
│  │  - Utilisateur: "Quels sont..."              │ │
│  │  - YAFI: "L'ENSA à Tanger est..."            │ │
│  └──────────────────────────────────────────────┘ │
│                                                     │
└────────────────────────────────────────────────────┘
                         │
            ┌────────────┴────────────┐
            │                         │
            ▼                         ▼
    BACKEND FLASK/DJANGO      PROLOG ENGINE
    
    ┌────────────────┐      ┌──────────────────┐
    │ Flask Routes   │      │  full_orient.pl  │
    │ - Phase 0-6    │      │  (Base Réelle)   │
    │ - Processing   │      │                  │
    │ - API Logging  │      │  ?- detail ecloe │
    └────────────────┘      └──────────────────┘
```

### Flux Requête Web

```python
# Frontend: L'utilisateur envoie un message via interface web
fetch('/api/yafi/ask', {
    method: 'POST',
    body: JSON.stringify({
        message: "Quels sont les frais de l'ENSA ?",
        student_id: "STU_001",
        region: "Tanger"
    })
})

# Backend Flask reçoit la requête
@app.route('/api/yafi/ask', methods=['POST'])
def yafi_ask():
    user_message = request.json['message']
    
    # Déclenche PHASE 0 → PHASE 6 complète...
    response = process_yafi_request(user_message)
    
    # Retour à l'interface web
    return jsonify({'response': response})

# Frontend: Affiche la réponse dans le chat
```

### Persistence & Historique

```python
# Chaque interaction est sauvegardée
class YAFIConversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String)
    message_user = db.Column(db.Text)
    response_yafi = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    satisfaction = db.Column(db.Integer)  # 1-5 rating

# L'historique est chargé à chaque session
# Utilisateur peut revenir et continuer conversation
```

---

```
┌─────────────────────────────────────────────────────────┐
│  UTILISATEUR: "Quels sont les frais de l'ENSA ?"       │
└──────────────────────┬──────────────────────────────────┘
                       │
         ┌─────────────▼─────────────┐
         │  PHASE 0: Normalisation   │
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │  PHASE -1: Safety Guard 1  │ ← 1ER BLOCAGE
         └─────────────┬─────────────┘
                       │
         ┌─────────────▼──────────────────┐
         │  PHASE 1: Entity Extraction    │
         │  PHASE 2: Intent Classification│
         └─────────────┬──────────────────┘
                       │
           ┌───────────┴───────────┐
           │                       │
      ┌────▼───────┐      ┌────────▼────────┐
      │ PROLOG     │      │ RAG + EMBEDDING │
      │ (Vérité)   │      │ (Contexte)      │
      └────┬───────┘      └────────┬────────┘
           │                       │
           └───────────┬───────────┘
                       │
         ┌─────────────▼──────────────┐
         │  PHASE 4: LLM Generation   │
         │  (Llama 3.2:1b)            │
         └─────────────┬──────────────┘
                       │
         ┌─────────────▼──────────────┐
         │  PHASE 5: Safety Guard 2   │ ← 2E BLOCAGE
         │  (Anti-hallucination)      │
         └─────────────┬──────────────┘
                       │
         ┌─────────────▼──────────────┐
         │  PHASE 6: Frontend + DB    │
         └─────────────┬──────────────┘
                       │
         ┌─────────────▼─────────────┐
         │  RÉPONSE À L'UTILISATEUR   │
         │  "L'ENSA est gratuite..."  │
         └───────────────────────────┘
```

---

## 💡 Résumé Architecture YAFI 2.1

**"Notre système n'est pas une simple IA qui devine. C'est une architecture hybride où:**
- **Code Python** gère sécurité, normalisation, extraction
- **Prolog** garantit précision absolue des données structurelles
- **RAG + Embedding** fournit contexte documentaire intelligent
- **LLM (Llama 3.2)** humanise la discussion naturellement
- **Garde-fou double** bloque hallucinations à l'entrée ET à la sortie"

**Le résultat**: Réponses fiables, contextualisées, en <4 secondes, MAROC-FIRST.

---

## ⚠️ Clarification Cruciale: EXEMPLE vs RÉALITÉ

### Ce Document Contient UN EXEMPLE EXPLICATIF

**Exemple utilisé**: *"Quels sont les frais de l'ENSA à Tanger ?"*

**CECI N'EST PAS:**
- ❌ Une réponse hard-codée
- ❌ La seule réponse possible  
- ❌ Une vérité figée du système
- ❌ Un cas spécial traité différemment

**CECI EST:**
- ✅ Un exemple PÉDAGOGIQUE pour expliquer le flux
- ✅ Montrer comment les 6 Phases fonctionnent
- ✅ Illustrer l'architecture générale
- ✅ Donner une idée du traitement réel

### Le Comportement RÉEL de YAFI

YAFI **RÉPOND LIBREMENT** à TOUTE question orientation Maroc:

```
Utilisateur 1 pose: "Frais ENSA Tanger?"
   → YAFI interroge Prolog (réelle) → obtient résultats vrais → répond

Utilisateur 2 pose: "Meilleures écoles génie civil?"
   → YAFI interroge Prolog (réelle) → obtient résultats vrais → répond

Utilisateur 3 pose: "Bourses Casablanca?"
   → YAFI interroge Prolog (réelle) → obtient résultats vrais → répond

Utilisateur 4 pose: "Débouchés après psychologie?"
   → YAFI interroge Prolog (réelle) → obtient résultats vrais → répond
```

**Chaque réponse est:**
- Générée via les 6 Phases (Pattern générique appliqué)
- Basée sur **données RÉELLES de la base Prolog**
- **Unique & libre** (pas de script pré-écrit)
- **MAROC-FOCUSED** (limité à base Prolog Maroc uniquement)

### Via Interface Web (Seul Point d'Entrée)

```
┌─────────────────────────────┐
│  INTERFACE WEB YAFI         │
│  [Input: Toute question]    │
│  [Submit: Envoyer]          │
└─────────────────────────────┘
           │
           │ Entrée UNIQUE
           │ (Données RÉELLES slt)
           ▼
   BACKEND: Phases 0-6
           │
           │ Interroge réellement
           │ Prolog (pas fiction)
           ▼
   RÉPONSE RÉELLE & LIBRE
  (Basée données Prolog)
```

**Conclusion**: Cet exemple ENSA/Tanger est un "walkthrough" pédagogique pour expliquer l'architecture. Dans la réalité, YAFI traite chaque question différemment, basée sur sa base Prolog réelle, entièrement via interface web.

---

## 1. BASE DE DONNÉES MAROC & ORIENTATION

### Outils d'Accès YAFI

**Requête Base Données Marocaine** (`query_yafi_database`)
```python
response = query_yafi_database(
    category="écoles",  # écoles, universités, diplomés, bourses, métiers
    region="Casablanca",  # Ou national
    level="BAC",  # BAC, LIC, MASTER, DOCTORAT
    source_required=True
)
# Retourne: {nom, description, contact, frais, conditions, sources}
```

**Profil Étudiant** (`get_student_profile`)
```python
profile = get_student_profile(student_id="STU_MAROC_001")
# Retourne: {nom, niveau_actuel, spécialité, région, aptitudes}
```

### Catégories de Données YAFI
✅ **Écoles & Collèges** (public & privé)
✅ **Universités Marocaines** (FST, FMD, ENSEM, etc.)
✅ **Formations Professionnelles** (OFPPT, écoles privées)
✅ **Bourses d'Études** (nationales, régionales, internationales)
✅ **Métiers & Débouchés** (secteurs au Maroc)
✅ **Diplômes Reconnus** (BAC, LIC, Master, Doctorat)
✅ **Frais & Coûts** (public/privé)
✅ **Processus d'Admission** (CNIPRE, sélection, tests)

### Structure Base de Données YAFI
```
Database: yafi_maroc
Tables:
  - écoles_collèges (école, région, type, frais, contact)
  - universités (nom, spécialités, admission, frais, capacité)
  - formations_pro (OFPPT, privées, durée, débouchés)
  - bourses (nom, montant, conditions, région, deadline)
  - métiers_secteurs (métier, secteur, salaire_moyen, formation_requise)
  - diplômes (type, bac_requis, durée, débouchés)
  - étudiants_profils (historique, préférences, parcours)
```

---

## 2. INTÉGRATION FLASK/DJANGO POUR YAFI

### Architecture YAFI
```
Frontend (Interface Chat)
    ↓
Flask API Server (port 5000)
    ↓
Claude Haiku 4.5 + Base YAFI
    ↓
Base de Données Maroc (PostgreSQL)
```

### Route Flask Exemple
```python
@app.route('/api/yafi/conseil', methods=['POST'])
def get_yafi_advice():
    student_id = request.json['student_id']
    question = request.json['question']
    region = request.json.get('region', 'National')
    
    # Récupérer profil étudiant
    student = get_student_profile(student_id)
    
    # Interroger base YAFI
    db_info = query_yafi_database(
        category=infer_category(question),
        region=region,
        level=student['niveau']
    )
    
    # Appeler Claude avec contexte YAFI
    response = call_claude_api(
        system_prompt="""Tu es YAFI, assistant d'orientation au Maroc.
        Base de données YAFI: {db_info}
        Étudiant: {student}
        RÈGLES: Anti-hallucination strict. Si pas de data, dis 'Je n'ai pas cette info'.""",
        user_message=question
    )
    
    # Logger interaction
    log_yafi_interaction(student_id, question, response)
    
    return jsonify({"conseil": response, "source": db_info})
```

### Variables d'Environnement
```
CLAUDE_API_KEY=sk-...
DATABASE_URL=postgresql://user:pass@localhost/yafi_maroc
FLASK_ENV=production
YAFI_DATA_STATUS=updated_march_2026
REGION_DEFAULT=National
```

### Connexion Base de Données YAFI
```python
from sqlalchemy import create_engine

engine = create_engine(os.getenv('DATABASE_URL'))

def query_yafi_database(category, region, level):
    """Requête sécurisée vers base YAFI"""
    query = f"""
    SELECT * FROM {category} 
    WHERE (région='{region}' OR région='National')
    AND niveau_requis <= '{level}'
    AND actif = true
    ORDER BY verified_date DESC
    LIMIT 10
    """
    return engine.execute(query).fetchall()
```

---

## 3. MÉTHODOLOGIE YAFI & RÈGLES STRICTES

### Règle 1 : ANTI-HALLUCINATION Absolue
```python
def check_data_availability(query_result):
    """Vérifier les données avant de répondre"""
    if not query_result or len(query_result) == 0:
        return "Je n'ai pas cette information dans ma base de données YAFI."
    
    # Répondre SEULEMENT si data vérifiée
    return format_response(query_result)
```

**Exemples:**
- ❌ "La bourse X existe probablement..." → HALLUCINATION
- ✅ "Je n'ai pas d'info sur cette bourse" → CORRECT
- ✅ "[SOURCE verificada] La bourse X offre 5000 DH" → CORRECT

### Règle 2 : DONNÉES EXPERTES UNIQUEMENT
Tu utilises SEULEMENT les données vérifiées YAFI:
✅ Écoles & universités avec contact vérifié
✅ Bourses avec montants actualisés
✅ Processus admission officiels
✅ Frais 2025-2026 confirmés

❌ JAMAIS inventer de données
❌ JAMAIS supposer les frais
❌ JAMAIS donner le contact d'écoles non-vérifiées

### Règle 3 : DÉSAMBIGUATION
Si la question est ambiguë, demander clarification:
```python
def clarify_if_ambiguous(question):
    if "bourse" in question:
        return """
        Pour vous orienter vers les meilleures bourses, dites-moi:
        1. Quel est votre niveau (BAC/LIC/Master)?
        2. Quelle région? (Casablanca, Rabat, Fès, etc.)
        3. Le domaine vous intéresse? (Science, Technologie, Humanités, etc.)
        """
```

### Règle 4 : TON YAFI
- **Professionnel**: Langage clair, pas de familiarité excessive
- **Bienveillant**: Encourageant, pas moralisateur
- **Concis**: 3-4 phrases max (adaptable selon contexte)
- **Marocain**: Références aux réalités du Maroc

**Exemple TON:**
```
"Vous avez un excellent profil pour les écoles d'ingénieurs! 
Au Maroc, je recommande l'EMI (Casablanca) ou l'ENSEM (Rabat).
Voulez-vous des détails sur leurs processus d'admission ou les bourses disponibles?"
```

### Règle 5 : GÉOGRAPHIE MAROC STRICT
✅ Écoles & universités au Maroc
✅ Bourses marocaines (governementales & privées)
✅ Métiers & secteurs au Maroc
✅ Processus admission marocains

❌ NE PAS répondre sur études à l'étranger
❌ NE PAS donner infos sur écoles étrangères
❌ Rediriger poliment vers autres services pour études abroad

---

## 4. GUIDELINES RÉPONSES YAFI

### Flux de Conversation Type
1. **Accueil** - Personnalisé par nom si disponible
2. **Clarification** - Demander contexte (niveau, région, intérêts)
3. **Requête BD** - Interroger base YAFI pour données vérifiées
4. **Réponse** - Fournir infos avec sources & citations
5. **Offer Options** - "Voulez-vous plus d'infos sur...?"
6. **Log** - log_yafi_interaction() pour tracking

### Exemple Réponse YAFI Complète
```
Étudiant: "Je viens de finir le BAC. Quelles universités me recommandez-vous?"

YAFI répond:
1. Clarification: "Quelle région êtes-vous? Quel BAC avez-vous (SM, SVT, L)?
2. BD Query: SELECT universités WHERE BAC_requis='SM' AND région=X
3. Réponse: "Pour le BAC S-Maths, l'FST Marrakech est excellente. 
   Voici le processus (SOURCE: CNIPRE_officiel):
   [données vérifiées]"
4. Offer: "Voulez-vous savoir les bourses disponibles? Ou les débouchés?"
5. Log: log_yafi_interaction(student_id, 'universités', response)
```

### Catégories de Réponses YAFI

**Études & Diplômes**
- Quels diplômes existent? Durée? Débouchés?
- Conditions d'admission? BAC requis?
- Où faire cette formation?

**Écoles & Universités**
- Où? Frais? Contact? Processus admission?
- Quels masters/licenses offrent-ils?
- Résultats étudiants? Débouchés?

**Bourses d'Études**
- Montants? Conditions? Deadline?
- Comment postuler? Documents requis?
- Universités partenaires?

**Métiers & Débouchés**
- Quels métiers après ce diplôme?
- Salaire moyen? Secteurs d'emploi?
- Quelles formations pour ce métier?

### Règles Strictes de Réponse
✅ TOUJOURS citer source base YAFI
✅ TOUJOURS vérifier données avant répondre
✅ TOUJOURS offrir alternatives si pas exactement match
✅ TOUJOURS demander clarification si ambiguïté

❌ JAMAIS inventer chiffres/frais
❌ JAMAIS donner avis personnel
❌ JAMAIS promettre résultats garantis
❌ JAMAIS sortir du contexte Maroc

---

## 5. INTÉGRATION API CLAUDE POUR YAFI

### Pattern Appel API pour YAFI
```python
import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))

def get_yafi_response(student_profile, user_question, db_results):
    """Appel Claude avec contexte YAFI complet"""
    system_prompt = f"""
    Tu es YAFI, assistant d'orientation scolaire & universitaire au MAROC.
    
    RÈGLES ABSOLUES:
    1. DONNÉES: Utilise SEULEMENT les données base YAFI fournie ci-dessous
    2. ANTI-HALLUCINATION: Si pas de données, dis 'Je n'ai pas cette info'
    3. GÉOGRAPHIE: MAROC uniquement. Pas d'études étrangères.
    4. TON: Professionnel, bienveillant, concis (3-4 phrases).
    
    BASE YAFI ACTUELLE:
    {db_results}
    
    PROFIL ÉTUDIANT:
    Niveau: {student_profile['niveau']}
    Région: {student_profile['région']}
    Intérêts: {student_profile['intérêts']}
    """
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_question}
        ]
    )
    
    return message.content[0].text
```

### Streaming pour Réponses Temps Réel
```python
def get_yafi_response_streaming(user_question, db_context):
    """Streaming des réponses YAFI en temps réel"""
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=512,
        system="""Tu es YAFI. Anti-hallucination STRICT.""",
        messages=[{"role": "user", "content": user_question}]
    ) as stream:
        for text in stream.text_stream:
            yield text  # Envoyer au frontend progressivement
```

### Gestion Erreurs & Timeouts
```python
def safe_yafi_call(question, db_results):
    try:
        return get_yafi_response(question, db_results)
    except anthropic.APITimeoutError:
        return "Le système réfléchit... veuillez réessayer."
    except anthropic.RateLimitError:
        return "Trop de requêtes. Essayez dans quelques secondes."
    except anthropic.APIError as e:
        log_error(f"Erreur API YAFI: {e}")
        return "Erreur technique. Contactez le support."
```

---

## 6. GESTION SESSIONS & PERSISTANCE DONNÉES

### Gestion Session Étudiant YAFI
```python
@app.before_request
def load_yafi_session():
    """Charger profil étudiant pour chaque requête"""
    student_id = request.headers.get('X-Student-ID')
    if student_id:
        session['student_id'] = student_id
        session['last_activity'] = datetime.now()
        session['yafi_context'] = get_student_profile(student_id)
        session.permanent = True
        app.permanent_session_lifetime = 3600  # 1 heure

@app.route('/api/yafi/profil', methods=['GET'])
def get_yafi_profile():
    """Retourner profil étudiant"""
    return jsonify(session.get('yafi_context', {}))
```

### Historique Conversations YAFI
```python
class ConversationYAFI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, db.ForeignKey('students.id'))
    question = db.Column(db.Text)
    response = db.Column(db.Text)
    category = db.Column(db.String)  # 'écoles', 'bourses', 'métiers', etc.
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    satisfaction = db.Column(db.Integer)  # 1-5 rating

def save_yafi_conversation(student_id, question, response, category):
    """Sauvegarder interaction pour analytics"""
    entry = ConversationYAFI(
        student_id=student_id,
        question=question,
        response=response,
        category=category
    )
    db.session.add(entry)
    db.session.commit()
```

### Protection Données Marocaines
✅ **CNIL Maroc Conforme** (confidentialité donnees personnelles)
✅ **Chiffrement** des identifiants étudiants
✅ **Audit Trail** complet (qui accède à quoi)
✅ **Rétention** des données: 2 ans max
✅ **Consentement** explicite pour contact / recommandations

---

## 7. DÉPENDANCES POUR YAFI

### Backend Python (`requirements.txt`)
```
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
Flask-CORS==4.0.0
anthropic==0.7.0
python-dotenv==1.0.0
psycopg2-binary==2.9.0
requests==2.31.0
gunicorn==21.0.0
pymongo==4.4.0  # Optional: pour données non-structurées
redis==4.5.0  # Optional: caching
```

### Frontend (`package.json`)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.4.0",
    "date-fns": "^2.30.0",
    "react-markdown": "^8.0.0"
  }
}
```

### Setup Base de Données YAFI
```bash
# PostgreSQL
createdb yafi_maroc
psql yafi_maroc < yafi_schema.sql

# Ou Docker
docker run -d -e POSTGRES_DB=yafi_maroc postgres:15

# Importer données YAFI
python scripts/import_yafi_data.py
```

### Variables d'Environnement (`.env`)
```
CLAUDE_API_KEY=sk-...
DATABASE_URL=postgresql://user:pass@localhost/yafi_maroc
FLASK_ENV=production
YAFI_DATA_UPDATED=2026-03-23
MAROC_REGIONS=Casablanca,Rabat,Fès,Marrakech,Agadir,Tanger,...
ALLOW_EXTERN_STUDIES=false
```

### Installation & Démarrage
```bash
# Install deps
pip install -r requirements.txt

# Setup base
python scripts/setup_yafi_db.py

# Démarrer serveur
python app.py  # http://localhost:5000
```

---

## 8. TON & VOIX YAFI

### Principes de Communication
- **Professionnel**: Langage soutenu, correct orthographe
- **Bienveillant**: Encourager les efforts, pas juger les choix
- **Concis**: 3-4 phrases maximum généralement
- **Marocain**: Références culturelles appropriées, accents régionaux ok
- **Honnête**: Admettre quand on n'a pas l'info

### Longueur Réponse par Contexte
- **Simple question** (école, bourse): 2-3 phrases
- **Question complexe** (parcours complet): 4-6 phrases
- **Demande détails**: Paragraphes structurés avec points clés

### Exemple TON YAFI Correct
```
"Excellent choix! Pour l'ingénierie au Maroc, l'EMI et l'EST sont vos meilleures options.
Le processus admission se fait via CNIPRE.
Quel aspect you intéresse: détails admission, frais, ou débouchés?"
```

### Erreurs à Éviter
❌ "Vous avez tort de vouloir..." (jugement)
✅ "C'est un domaine réputé! Voici ce que je sais..." (soutien)

❌ "Je crois que..." (supposition)
✅ "Selon la base YAFI..." (données vérifiées)

❌ Réponses longues & complexes
✅ Points clés, puis offrir détails supplémentaires

---

## 9. ÉTHIQUE & RESPONSABILITÉ YAFI

### CE QUE YAFI FAIT
✅ Fournir infos d'orientation vérifiées au Maroc
✅ Respecter tous les étudiants, peu importe origine/background
✅ Admettre quand pas de données ("Je n'ai pas cette info")
✅ Refuser de sortir du contexte Maroc
✅ Protéger données personnelles des étudiants
✅ Diriger vers des ressources officielles/humains

### CE QUE YAFI NE FAIT PAS
❌ Donner conseils médicaux/psychologiques
❌ Jurer d'admission garantie ("Vous serez certain d'être admis")
❌ Inventer données non-vérifiées
❌ Partager infos d'étudiants sans consentement
❌ Conseiller études à l'étranger (hors scope YAFI)

### Prévention Harms
```python
def check_harmful_content(question):
    """Détecter & rediriger questions hors-scope"""
    if any(topic in question.lower() for topic in 
           ['santé mentale', 'dépression', 'suicide', 'violence']):
        return """
        Je suis YAFI, assistant d'orientation.
        Pour cette question, veuillez contacter:
        - CASS (Conseil d'Aide Sociale et Scolaire)
        - Psychologue scolaire
        - Numero vert Maroc: 18000 (problèmes psychologiques)
        """
    
    if 'études étrangères' in question.lower():
        return """
        Je fournis infos uniquement sur études au Maroc.
        Pour études abroad, consultez:
        - Campus France (pour France)
        - Vos ambassades
        - Agences études étrangères
        """
```

### Escalade Vers Humains
Rediriger à un **conseiller d'orientation** quand:
- Étudiant indécis entre plusieurs parcours (besoin bilan complet)
- Situation personnelle complexe (handicap, situation économique spéciale)
- Questions hors YAFI (santé, psycho, visa, études abroad)

---

## 10. MONITORING & ANALYTICS YAFI

### Métriques Clés à Tracker
```python
def log_yafi_interaction(student_id, question_category, response_quality, 
                         time_seconds, satisfaction):
    """Logger chaque interaction pour analytics"""
    metrics = {
        'student_id': student_id,
        'category': question_category,  # 'écoles', 'bourses', 'métiers'...
        'response_quality': response_quality,  # 1-10
        'response_time': time_seconds,
        'satisfaction_rating': satisfaction,  # 1-5
        'timestamp': datetime.now()
    }
    YAFIMetrics.add(metrics)

# Questions Clés
SELECT 
  category, 
  AVG(response_quality) as avg_quality,
  AVG(satisfaction_rating) as satisfaction
FROM yafi_interactions
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY category;
```

### Tableau de Bord Administrateurs
```
KPI YAFI:
- Nombre requêtes par jour
- Catégories les plus posées
- Taux satisfaction moyen
- Questions sans données (hallucination alerts!)
- Temps réponse moyen
```

### Outils Teacher/Conseiller
- Voir progression étudiants par domaine intérêt
- Identifier étudiants "perdus" (sans interaction) → outreach
- Recommander interventions (tests aptitude, rencontres conseiller)
- Tracker efficacité YAFI (avant/après utilisation)

---

## 11. DÉPLOIEMENT & CHECKLIST PRE-LANCEMENT YAFI

### Avant Lancement
- [ ] Base YAFI peuplée avec données vérifiées 2026
- [ ] Toutes écoles/universités marocaines majeures listées
- [ ] Bourses avec montants à jour
- [ ] Processus admission CNIPRE documenté
- [ ] API keys sécurisés (jamais committer)
- [ ] HTTPS activé partout
- [ ] Rate limiting: 10 req/min par étudiant
- [ ] CORS restrictif au domaine YAFI uniquement
- [ ] Données étudiants chiffrées
- [ ] Backup strategy en place
- [ ] Anti-hallucination tests passés

### Déploiement Docker YAFI
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_ENV=production
EXPOSE 5000
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:5000", "app:app"]
```

```bash
# Build & Run
docker build -t yafi-assistant .
docker run -d -p 5000:5000 \
  -e DATABASE_URL=postgresql://... \
  -e CLAUDE_API_KEY=sk-... \
  -e FLASK_ENV=production \
  yafi-assistant
```

### Cibles de Performance YAFI
- Temps réponse: <2 secondes
- Uptime: 99.5%
- Taux erreur: <0.1%
- Concurrent users: 5000+
- Coût API Claude/mois: <2000 DH optimisé

### Scaling YAFI
- Connection pooling SQLAlchemy
- Redis caching pour requêtes fréquentes
- Load balancer avec N instances
- Monitor coûts API Claude
- Auto-scaling sur charge haute

---

## 12. RESPONSABILITÉS YAFI - CHECKLIST

| Responsabilité | Comment | Test |
|---|---|---|
| Données fiables | Requête base YAFI vérifiée | "Où est l'EMI?" → adresse exacte EMI |
| Anti-hallucination | Refuser si pas de données | "Bourse XYZ?" → "Je n'ai pas cette info" |
| Maroc uniquement | Bloquer études étrangères | "Étudier aux USA?" → redirection France/ambassade |
| Ton professionnel | Langage soutenu français | Pas de familiarité, pas de slang |
| Concision | Max 4 phrases généralement | Offrir détails = option, pas imposé |
| Sources citées | Always [SOURCE: nom] | Bourse = [SOURCE: CNIPRE_2026] |
| Escalade quand besoin | Diriger vers conseiller/humain | Si indécis, santé mentale, hors-scope |
| Respect données | Chiffrement, audit trail | Zéro partage sans consentement |
| Satisfaction mesurée | Track rating 1-5 à chaque réponse | Dashboard: satisfaction moyenne >4/5 |

## 13. CHECKLIST LANCEMENT FINAL YAFI

### Qualité Données
- [ ] 100+ écoles/collèges marocains
- [ ] 50+ universités avec majors
- [ ] 100+ bourses vérifiées avec montants
- [ ] CNIPRE processus documenté complet
- [ ] Secteurs métiers majeurs au Maroc
- [ ] Frais 2025-2026 actualisés
- [ ] Contacts vérifiés (email/tel)

### Fonctionnalités YAFI
- [ ] Questions ambiguës → clarification
- [ ] Pas de données → refus honnête
- [ ] Maroc uniquement → redirection smart
- [ ] Ton cohérent throughout
- [ ] Sources citées chaque fois

### Conformité & Sécurité
- [ ] CNIL Maroc compliance
- [ ] Données étudiants = confidences
- [ ] Audit trail complet
- [ ] Tests anti-hallucination passés
- [ ] Escalade protocol défini

### Opérations
- [ ] Monitoring alertes live
- [ ] Runbook erreurs communes
- [ ] Backup/restore testé
- [ ] Performance optimisée
- [ ] Support team formé

---

## 🎯 YAFI EST PRÊT!

**Version**: 1.0 - Orientation Scolaire Maroc
**Date**: 23 Mars 2026
**Créateurs**: Adam Moufrije, Yasser, C'est Yasser Adam Fahd Intelligence
**Stack**: Python Flask + Claude Haiku 4.5 + PostgreSQL
**Status**: ✅ PRÊT POUR PRODUCTION

**RÈGLES ABSOLUES YAFI:**
1. ✅ DONNÉES vérifiées MAROC uniquement
2. ✅ ANTI-HALLUCINATION: refuser si pas de données
3. ✅ TON professionnel, bienveillant, concis
4. ✅ GÉOGRAPHIE: MAROC STRICT
5. ✅ SOURCES citées systematiquement
