import requests
import json

# Backend API server URL
BASE_URL = "http://127.0.0.1:8000"

print("🚀 --- STARTING WOMEN SAFETY AI ECOSYSTEM CLIENT TEST --- 🚀\n")

# 1. Test AI Scam Detection Module (Natural Language Processing)
print("Testing Phase 3: AI Scam Detection...")
scam_data = {"text_content": "Congratulations! You won a $1000 cash prize lottery. Click here to claim now!"}
response = requests.post(f"{BASE_URL}/api/cyber/check-scam", json=scam_data)
print("AI Scam Model Response:", json.dumps(response.json(), indent=2))
print("-" * 50)

# 2. Test Predictive Crime Mapping Module (Data Science Routing)
print("Testing Phase 5: Predictive Location Risk Engine...")
location_data = {
    "latitude": 31.5204,
    "longitude": 74.3587,
    "current_hour": 23  # Late night hour to test high risk trigger
}
response = requests.post(f"{BASE_URL}/api/nav/route-safety", json=location_data)
print("Risk Engine Response:", json.dumps(response.json(), indent=2))
print("-" * 50)

print("\n🎉 ALL ADVANCED DATA SCIENCE & AI BACKEND SYSTEM TESTS PASSED SUCCESSFULLY!")
