import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from server_optimized import app

client = app.test_client()

response = client.post('/api/evaluate', json={
    "bac": "PC",
    "budget": 30000,
    "ville": "Rabat",
    "ecole": "ENSA"
})

print("Status Code:", response.status_code)
print("Response:", response.get_json())
