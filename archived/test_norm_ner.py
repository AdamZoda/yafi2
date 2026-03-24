
import unicodedata
import difflib

def normalize_text(text):
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    replacements = {
        'faculte': 'fac', 'universite': 'fac', 'univ': 'fac',
        'medecine': 'medecine', 'medcine': 'medecine', 'medcin': 'medecine',
        'ingenierie': 'ingenierie', 'ingenieur': 'ingenierie',
        'ensias': 'ensias', 'uir': 'uir', 'um6p': 'um6p', 'emsi': 'emsi',
        'engc': 'encg', 'engam': 'encg',
        'ecole': 'ecole', 'ecoles': 'ecole',
        'vs': 'versus',
    }
    text = text.replace("l'", " ").replace("d'", " ").replace("s'", " ").replace("j'", " ")
    words = text.split()
    normalized_words = [replacements.get(w, w) for w in words]
    return ' '.join(normalized_words)

KNOWN_ENTITIES = [
    "emsi", "uir", "um6p", "ensa", "encg", "fst", "ensias", "iscae", "uic", "fmp",
    "ensam", "enam", "iav", "ena", "casablanca", "rabat"
]

def extract_entity(text):
    words = text.split()
    for w in words:
        if len(w) > 2:
            matches = difflib.get_close_matches(w, KNOWN_ENTITIES, n=1, cutoff=0.7)
            if matches: return matches[0]
    matches = difflib.get_close_matches(text, KNOWN_ENTITIES, n=1, cutoff=0.6)
    if matches: return matches[0]
    return None

test_msg = "Différence entre ENSA et ENAM ?"
norm = normalize_text(test_msg.lower())
entity = extract_entity(norm)

print(f"Original: {test_msg}")
print(f"Normalized: {norm}")
print(f"Extracted Entity: {entity}")
