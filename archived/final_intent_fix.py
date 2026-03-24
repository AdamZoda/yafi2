
import os

filepath = r'c:\Users\PC\Downloads\YAFI\yafi2-main\backend\server.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # 1. Lower the threshold
    if 'threshold=0.60' in line:
        line = line.replace('threshold=0.60', 'threshold=0.40')
    
    # 2. Add Brute Force Comparison Detection
    if 'detected_intent = intent_classifier.classify' in line:
        new_lines.append(line)
        new_lines.append('\n        # --- BRUTE FORCE FALLBACK FOR COMPARISONS ---\n')
        new_lines.append('        if detected_intent is None:\n')
        new_lines.append('            msg_low = user_message.lower()\n')
        new_lines.append('            if any(w in msg_low for w in ["comparer", "difference", " vs ", " entre "]):\n')
        new_lines.append('                schools_found = [ent for ent in KNOWN_ENTITIES if ent in msg_low]\n')
        new_lines.append('                if len(schools_found) >= 2:\n')
        new_lines.append('                    detected_intent = "COMPARE_SCHOOLS"\n')
        new_lines.append('                    print(f"🔥 BRUTE FORCE MATCH: {detected_intent}")\n')
        continue

    # 3. Strictly isolate RAG block
    if 'if USE_VECTOR_SEARCH and len(user_message_normalized) > 2:' in line:
        line = line.replace('if USE_VECTOR_SEARCH and len(user_message_normalized) > 2:', 
                            'if not detected_intent and USE_VECTOR_SEARCH and len(user_message_normalized) > 2:')
    
    new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Intent priority and brute force fallback applied.")
