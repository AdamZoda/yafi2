import sys
import os
from pyswip import Prolog

prolog = Prolog()
base_dir = os.path.dirname(os.path.abspath(__file__))

print("Loading primary KB...")
try:
    prolog.consult(os.path.join(base_dir, "backend", "full_orientation_system.pl").replace('\\', '/'))
    print("✓ Primary KB OK")
except Exception as e:
    print(f"Error primary: {e}")

print("Loading secondary KB...")
try:
    prolog.consult(os.path.join(base_dir, "knowledge_base_orientation.pl").replace('\\', '/'))
    print("✓ Secondary KB OK")
except Exception as e:
    print(f"Error secondary: {e}")

print("Testing a query from primary...")
try:
    res = list(prolog.query("get_avis_ecole('ENSA', Note, Positif, Negatif)"))
    print("Avis ENSA:", res)
except Exception as e:
    print(f"Error querying primary: {e}")

print("Testing a query from secondary...")
try:
    res = list(prolog.query("institution(isic, Nom, Type, Domaine, Adresse, Email, Site, Duree)"))
    print("ISIC info:", res)
except Exception as e:
    print(f"Error querying secondary: {e}")

print("Done.")
