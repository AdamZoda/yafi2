-- Script SQL pour créer la table de profil utilisateur dans Supabase (YAFI)
-- A exécuter dans l'éditeur SQL de Supabase

CREATE TABLE IF NOT EXISTS public.user_profiles (
    session_id TEXT PRIMARY KEY,           -- Identifiant de session unique (uuid ou string)
    bac_type TEXT,                         -- Type de Bac (PC, SVT, etc.)
    average FLOAT8,                        -- Moyenne (0-20)
    city TEXT,                             -- Ville de résidence
    interests JSONB DEFAULT '[]'::jsonb,   -- Liste des intérêts (ex: ["informatique"])
    last_topic TEXT,                       -- Dernier sujet abordé
    last_entity TEXT,                      -- Dernière école ou institution mentionnée
    last_intent TEXT,                      -- Dernier intent détecté
    history JSONB DEFAULT '[]'::jsonb,     -- Historique récent des messages
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Index pour accélérer les recherches par session
CREATE INDEX IF NOT EXISTS idx_user_profiles_session ON public.user_profiles (session_id);

-- Activer RLS (Row Level Security) - Optionnel mais recommandé
-- ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
-- Créer une policy pour autoriser l'accès anonyme (si applicable) ou via service_role
-- CREATE POLICY "Allow all for now" ON public.user_profiles FOR ALL USING (true);
