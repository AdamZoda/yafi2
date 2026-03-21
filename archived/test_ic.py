from intent_classifier import IntentClassifier

ic = IntentClassifier()

print("\n--- Test 1 ---")
r1 = ic.classify("prix de emsi", threshold=0.55)
print(f"Intent 1: {r1}")

print("\n--- Test 2 ---")
r2 = ic.classify("et pour uir ?", threshold=0.55)
print(f"Intent 2: {r2}")

print("\n--- Test 3 ---")
r3 = ic.classify("quelle est la duree des etudes a ensa ?", threshold=0.55)
print(f"Intent 3: {r3}")
