"""
user_memory.py — Mémoire persistante par utilisateur (Session + Profil)
Priorité: Supabase → Fallback JSON local
"""
import json
import os
import time
import threading
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
except ImportError:
    pass
except Exception:
    pass


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
        "ecole": None,         # Last school ID (deprecated)
        "entities": [],        # ["ENSA", "ENCG"] - Multi-entity support
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
                    "budget": raw.get("budget"), 
                    "ecole": raw.get("last_entity"),
                    "entities": raw.get("entities") or ([raw.get("last_entity")] if raw.get("last_entity") else []),
                    "interets": raw.get("interests") or [],
                    "last_topic": raw.get("last_topic"),
                    "last_intent": raw.get("last_intent"),
                    "history": raw.get("history") or [],
                    "last_seen": raw.get("last_seen"),
                    "created_at": raw.get("created_at"),
                }
        except Exception:
            pass

    # JSON local fallback
    if profile is None:
        file_data = _load_file()
        profile = file_data.get(session_id)

    if profile is None:
        profile = _default_profile()
        profile["created_at"] = datetime.utcnow().isoformat()
    else:
        # Ensure entities key exists for legacy migrations
        if "entities" not in profile:
            profile["entities"] = [profile.get("ecole")] if profile.get("ecole") else []

    _local_cache[session_id] = profile
    return profile


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
    file_data = _load_file()
    file_data[session_id] = profile
    _save_file(file_data)

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


def update(session_id: str, updates: dict):
    """Met à jour des champs précis et sauvegarde."""
    profile = load(session_id)
    # Filtre les None pour ne pas écraser une valeur existante par du vide
    actual_updates = {k: v for k, v in updates.items() if v is not None}
    
    # Special handling for entities (adding to list instead of overwriting)
    if "ecole" in actual_updates:
        new_ecole = actual_updates["ecole"]
        if new_ecole not in profile.get("entities", []):
            profile.setdefault("entities", []).append(new_ecole)
            # Keep only last 3 entities for focus
            profile["entities"] = profile["entities"][-3:]
    
    profile.update(actual_updates)
    save(session_id, profile)
    return profile


def add_message(session_id: str, role: str, content: str):
    """Ajoute un message à l'historique."""
    profile = load(session_id)
    history = profile.get("history", [])
    history.append({"role": role, "content": content[:500], "ts": time.time()})
    profile["history"] = history[-10:]
    _local_cache[session_id] = profile
    save(session_id, profile)


def get_history(session_id: str, n: int = 5) -> list:
    """Retourne les n derniers messages."""
    profile = load(session_id)
    return profile.get("history", [])[-n:]
