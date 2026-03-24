
import os
import re

filepath = r'c:\Users\PC\Downloads\YAFI\yafi2-main\backend\server.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_until = None

for i, line in enumerate(lines):
    # Fix School Normalization
    if '"ispits": "ispits", "isss": "isss"' in line:
        line = line.replace('"ispits": "ispits", "isss": "isss"', '"ispits": "ispits", "isss": "isss", "enam": "enam", "iav": "iav"')
    
    # Fix COMPARE_SCHOOLS missing return
    if 'response_text = f"⚖️ **Comparaison** : {s1.upper()} vs {s2.upper()}\\n- Salaire: {data1[\'salary\']} vs {data2[\'salary\']}\\n- Insertion: {data1[\'rate\']} vs {data2[\'rate\']}"' in line:
        new_lines.append(line)
        new_lines.append('                  return jsonify({"response": response_text})\n')
        continue

    if 'response_text = "⚖️ **Comparaison** : Indiquez deux écoles (ex: \'Compare EMSI et UIR\') pour voir leurs statistiques côte à côte."' in line:
        new_lines.append(line)
        new_lines.append('                  return jsonify({"response": response_text})\n')
        continue

    # Fix SCHOOL_FEES missing returns
    if 'response_text += "\\n*Note : Ces écoles respectent tes critères de coût et de salaire à la sortie.*"' in line:
        new_lines.append(line)
        new_lines.append('                          return jsonify({"response": response_text})\n')
        continue
    
    if 'response_text = f"Désolé, je n\'ai pas trouvé d\'école d {domain} correspondant exactement à un budget de {budget} DH. Voulez-vous essayer avec un budget plus large ?"' in line:
        new_lines.append(line)
        new_lines.append('                          return jsonify({"response": response_text})\n')
        continue
        
    if 'response_text = "Désolé, une erreur technique est survenue lors de la recherche par budget."' in line:
        new_lines.append(line)
        new_lines.append('                      return jsonify({"response": response_text})\n')
        continue

    if 'response_text += "\\n💡 *Les prix varient selon les filières. Est-ce qu\'une école en particulier t\'intéresse ?*"' in line:
        new_lines.append(line)
        new_lines.append('                          return jsonify({"response": response_text})\n')
        continue

    if 'response_text = "Je n\'ai pas trouvé d\'informations sur les frais pour le moment."' in line:
        new_lines.append(line)
        new_lines.append('                          return jsonify({"response": response_text})\n')
        continue

    # Fix the final return of the chat function (and the indented code before it)
    if 'return jsonify({' in line and i > 1900:
        # Correctly indent the final return
        new_lines.append('    return jsonify({\n')
        continue
    
    if '"response": response_text' in line and i > 1900:
        new_lines.append('        "response": response_text\n')
        continue
    
    if '})' in line and i > 1900 and i < 1945:
        new_lines.append('    })\n')
        continue

    new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Alignment and returns fixed.")
