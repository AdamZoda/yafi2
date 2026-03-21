import re

files = [
    r"c:\Users\user\Documents\chat\YAFI-main\knowledge_base_orientation.pl",
    r"c:\Users\user\Documents\chat\YAFI-main\backend\knowledge.pl",
    r"c:\Users\user\Documents\chat\YAFI-main\backend\full_orientation_system.pl"
]

def extract_predicates(filepath):
    preds = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('%') or line.startswith(':-'):
                    continue
                # Match start of line until an open parenthesis or a colon-dash
                m = re.match(r"^([a-zA-Z_]\w*)\b", line)
                if m:
                    preds.add(m.group(1))
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return preds

for f in files:
    print(f"\n--- {f.split(chr(92))[-1]} ---")
    preds = extract_predicates(f)
    print(", ".join(sorted(preds)))
