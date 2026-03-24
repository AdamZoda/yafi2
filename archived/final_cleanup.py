
import os

filepath = r'c:\Users\PC\Downloads\YAFI\yafi2-main\backend\server.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
skipping = False

# We want to remove the redundant part that starts at 1939 
# and ends right before the final return of the chat function.

for i, line in enumerate(lines):
    # The redundant part starts after PLATEFORMES usually or with a specific comment
    if i + 1 == 1939: 
        skipping = True
        print(f"Starting skip at line {i+1}")
    
    # The chat function end return
    if "return jsonify({" in line and skipping and i + 1 > 2200:
        skipping = False
        print(f"Stopping skip at line {i+1}")
    
    if not skipping:
        output_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"Final cleanup complete.")
