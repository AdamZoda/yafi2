import sys
import os

# Add backend to path
backend_path = os.path.join(os.getcwd(), 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

import user_memory

def test_memory():
    session_id = "test_bot_session"
    
    print(f"--- Testing Memory for {session_id} ---")
    
    # 1. Load (should be default)
    profile = user_memory.load(session_id)
    print(f"Initial profile: {profile.get('bac')}, {profile.get('moyenne')}")
    
    # 2. Update
    print("Updating profile with Bac PC and 15.5...")
    user_memory.update(session_id, {"bac": "PC", "moyenne": 15.5, "ville": "Rabat"})
    
    # 3. Reload
    profile2 = user_memory.load(session_id)
    print(f"Reloaded profile: {profile2.get('bac')}, {profile2.get('moyenne')}, {profile2.get('ville')}")
    
    # 4. Add message
    user_memory.add_message(session_id, "user", "Hello, I have a Bac PC")
    profile3 = user_memory.load(session_id)
    print(f"History length: {len(profile3.get('history', []))}")
    
    if profile2.get('bac') == "PC" and profile2.get('moyenne') == 15.5:
        print("\n✅ TEST PASSED: Memory logic is working.")
    else:
        print("\n❌ TEST FAILED: Memory mismatch.")

if __name__ == "__main__":
    test_memory()
