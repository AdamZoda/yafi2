
import os
import datetime

filepath = r'c:\Users\PC\Downloads\YAFI\yafi2-main\backend\server.py'
log_path = r'c:\Users\PC\Downloads\YAFI\yafi2-main\backend\debug_chat.log'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'def chat():' in line:
        new_lines.append(line)
        new_lines.append(f'    with open(r"{log_path}", "a", encoding="utf-8") as lf:\n')
        new_lines.append('        lf.write(f"\\n--- [{{datetime.datetime.now()}}] NEW REQUEST ---\\n")\n')
        continue
    
    if 'detected_intent = intent_classifier.classify' in line:
        new_lines.append(line)
        new_lines.append(f'    with open(r"{log_path}", "a", encoding="utf-8") as lf:\n')
        new_lines.append('        lf.write(f"Message: {{user_message_normalized}}\\n")\n')
        new_lines.append('        lf.write(f"Detected Intent: {{detected_intent}}\\n")\n')
        new_lines.append('        lf.write(f"Current Entity: {{current_entity}}\\n")\n')
        continue

    if 'if not detected_intent and USE_VECTOR_SEARCH' in line:
        new_lines.append(f'    with open(r"{log_path}", "a", encoding="utf-8") as lf:\n')
        new_lines.append('        lf.write(f"Entering RAG Block: {{not detected_intent}}\\n")\n')
        new_lines.append(line)
        continue

    new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Diagnostic logging added to server.py.")
