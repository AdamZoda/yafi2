import re

filepath = r"c:\Users\user\Documents\chat\YAFI-main\backend\full_orientation_system.pl"
target_preds = ["probabilite_admission", "evaluer_admissibilite_avec_profil", "calculer_score_orientation", "prediction_reussite"]

with open(filepath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        for p in target_preds:
            if line.startswith(p + "("):
                print(f"Line {i+1}: {line.strip()}")
