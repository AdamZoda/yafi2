"""
user_memory.py — Mémoire persistante par utilisateur (Session + Profil)
Priorité: Supabase → Fallback JSON local
"""
import json
import os
import time
<<<<<<< HEAD
=======
import threading
>>>>>>> 3257fc1 (final)
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG & INITIALIZATION
# ─────────────────────────────────────────────────────────────────────────────
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "user_memory.json")
_local_cache: dict = {}  # cache en RAM pour la session courante

# Supabase Initialization
_supabase = None
try:
    from supabase import create_client
    url = os.getenv("VITE_SUPABASE_URL")
    key = os.getenv("VITE_SUPABASE_ANON_KEY")
    if url and key:
        _supabase = create_client(url, key)
<<<<<<< HEAD
        # Only print once during startup if possible, but for now:
        # print("✅ Supabase Memory initialized.")
except ImportError:
    print("⚠️ Supabase library not installed. Using local memory only.")
except Exception as e:
    print(f"⚠️ Supabase initialization failed: {e}")
=======
except ImportError:
    pass
except Exception:
    pass
>>>>>>> 3257fc1 (final)


def _load_file() -> dict:
    """Charge le fichier JSON local."""
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save_file(data: dict):
    """Sauvegarde le fichier JSON local."""
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[UserMemory] Erreur sauvegarde local: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# API PRINCIPALE
# ─────────────────────────────────────────────────────────────────────────────

def _default_profile() -> dict:
    return {
        "bac": None,           # "PC", "SVT", "ECO"...
        "moyenne": None,       # float ex: 14.5
        "ville": None,         # "Casablanca", "Rabat"...
        "budget": None,        # Budget annuel
<<<<<<< HEAD
        "ecole": None,         # Dernière école mentionnée
=======
        "ecole": None,         # Last school ID (deprecated)
        "entities": [],        # ["ENSA", "ENCG"] - Multi-entity support
>>>>>>> 3257fc1 (final)
        "interets": [],        # ["informatique", "medecine"]
        "last_topic": None,    # dernier sujet abordé
        "last_intent": None,   # dernier intent NLU
        "history": [],         # [(role, text), ...]  — 10 derniers messages
        "last_seen": None,
        "created_at": None,
    }


def load(session_id: str) -> dict:
    """
    Charge le profil utilisateur.
    1. Cache RAM
    2. Supabase table user_profiles
    3. JSON local (fallback)
    """
    if session_id in _local_cache:
        return _local_cache[session_id]

    profile = None

    # Supabase - essaie user_profiles
    if _supabase:
        try:
            res = _supabase.table("user_profiles").select("*").eq("session_id", session_id).execute()
            if res.data:
                raw = res.data[0]
                profile = {
                    "bac": raw.get("bac_type"),
                    "moyenne": raw.get("average"),
                    "ville": raw.get("city"),
<<<<<<< HEAD
                    "budget": raw.get("budget"), # Now included
                    "ecole": raw.get("last_entity"),
=======
                    "budget": raw.get("budget"), 
                    "ecole": raw.get("last_entity"),
                    "entities": raw.get("entities") or ([raw.get("last_entity")] if raw.get("last_entity") else []),
>>>>>>> 3257fc1 (final)
                    "interets": raw.get("interests") or [],
                    "last_topic": raw.get("last_topic"),
                    "last_intent": raw.get("last_intent"),
                    "history": raw.get("history") or [],
                    "last_seen": raw.get("last_seen"),
                    "created_at": raw.get("created_at"),
                }
<<<<<<< HEAD
        except Exception as e:
            # Table pas encore créée -> on continue silencieusement vers le local
=======
        except Exception:
>>>>>>> 3257fc1 (final)
            pass

    # JSON local fallback
    if profile is None:
        file_data = _load_file()
        profile = file_data.get(session_id)

    if profile is None:
        profile = _default_profile()
        profile["created_at"] = datetime.utcnow().isoformat()
<<<<<<< HEAD
=======
    else:
        # Ensure entities key exists for legacy migrations
        if "entities" not in profile:
            profile["entities"] = [profile.get("ecole")] if profile.get("ecole") else []
>>>>>>> 3257fc1 (final)

    _local_cache[session_id] = profile
    return profile


<<<<<<< HEAD
def save(session_id: str, profile: dict):
    """Sauvegarde le profil (RAM + JSON + Supabase si dispo)."""
    profile["last_seen"] = datetime.utcnow().isoformat()
    _local_cache[session_id] = profile

    # JSON local
=======
def _save_to_supabase_async(upsert_data: dict):
    """Worker function to save to Supabase in the background."""
    if _supabase:
        try:
            _supabase.table("user_profiles").upsert(upsert_data).execute()
        except:
            pass

def save(session_id: str, profile: dict):
    """Sauvegarde le profil (RAM + JSON + Supabase asynchrone)."""
    profile["last_seen"] = datetime.utcnow().isoformat()
    _local_cache[session_id] = profile

    # JSON local (fast)
>>>>>>> 3257fc1 (final)
    file_data = _load_file()
    file_data[session_id] = profile
    _save_file(file_data)

<<<<<<< HEAD
    # Supabase
    if _supabase:
        try:
            upsert_data = {
                "session_id": session_id,
                "bac_type": profile.get("bac"),
                "average": profile.get("moyenne"),
                "city": profile.get("ville"),
                "budget": profile.get("budget"),
                "interests": profile.get("interets", []),
                "last_topic": profile.get("last_topic"),
                "last_entity": profile.get("ecole"),
                "last_intent": profile.get("last_intent"),
                "history": profile.get("history", [])[-20:], # 20 derniers messages
                "last_seen": profile["last_seen"],
            }
            _supabase.table("user_profiles").upsert(upsert_data).execute()
        except Exception as e:
            print(f"[UserMemory] Supabase save error: {e}")
=======
    # Supabase (Asynchronous fire-and-forget)
    if _supabase:
        upsert_data = {
            "session_id": session_id,
            "bac_type": profile.get("bac"),
            "average": profile.get("moyenne"),
            "city": profile.get("ville"),
            "budget": profile.get("budget"),
            "interests": profile.get("interets", []),
            "last_topic": profile.get("last_topic"),
            "last_entity": profile.get("ecole"),
            "last_intent": profile.get("last_intent"),
            "history": profile.get("history", [])[-20:], 
            "last_seen": profile["last_seen"],
        }
        # Start a background thread to prevent blocking
        threading.Thread(target=_save_to_supabase_async, args=(upsert_data,), daemon=True).start()
>>>>>>> 3257fc1 (final)


def update(session_id: str, updates: dict):
    """Met à jour des champs précis et sauvegarde."""
    profile = load(session_id)
    # Filtre les None pour ne pas écraser une valeur existante par du vide
    actual_updates = {k: v for k, v in updates.items() if v is not None}
<<<<<<< HEAD
=======
    
    # Special handling for entities (adding to list instead of overwriting)
    if "ecole" in actual_updates:
        new_ecole = actual_updates["ecole"]
        if new_ecole not in profile.get("entities", []):
            profile.setdefault("entities", []).append(new_ecole)
            # Keep only last 3 entities for focus
            profile["entities"] = profile["entities"][-3:]
    
>>>>>>> 3257fc1 (final)
    profile.update(actual_updates)
    save(session_id, profile)
    return profile


def add_message(session_id: str, role: str, content: str):
<<<<<<< HEAD
    """Ajoute un message à l'historique (max 10) pour cohérence avec ConversationManager."""
=======
    """Ajoute un message à l'historique."""
>>>>>>> 3257fc1 (final)
    profile = load(session_id)
    history = profile.get("history", [])
    history.append({"role": role, "content": content[:500], "ts": time.time()})
    profile["history"] = history[-10:]
    _local_cache[session_id] = profile
<<<<<<< HEAD
    # Optionnel: sauvegarder après chaque message ou attendre la fin du tour
=======
>>>>>>> 3257fc1 (final)
    save(session_id, profile)


def get_history(session_id: str, n: int = 5) -> list:
<<<<<<< HEAD
    """Retourne les n derniers messages pour le contexte LLM."""
=======
    """Retourne les n derniers messages."""
>>>>>>> 3257fc1 (final)
    profile = load(session_id)
    return profile.get("history", [])[-n:]
