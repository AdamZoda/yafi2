
import os

filepath = r'c:\Users\PC\Downloads\YAFI\yafi2-main\backend\server.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
skipping = False
kept_lines = 0

for line in lines:
    # Mark the start of the buggy/redundant section
    if "# --- 6.96 NEW KNOWLEDGE: SALARIES ---" in line:
        skipping = True
        print(f"Starting skip at line: {line.strip()}")
        continue
    
    # Mark the end of the skip - we want to keep the final return and other routes
    if "# --- GLOBAL FALLBACK ---" in line or "return jsonify({" in line and skipping:
        skipping = False
        print(f"Stopping skip at line: {line.strip()}")
    
    if not skipping:
        output_lines.append(line)
        kept_lines += 1

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Cleanup complete. Kept {kept_lines} lines.")
