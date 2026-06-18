import requests
import json

url = "http://localhost:8000/api/v1/chat"
payload = {
    "message": "How do I apply for Aadhaar?",
    "history": [],
    "language": "en"
}
response = requests.post(url, json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
