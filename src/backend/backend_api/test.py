import requests
import json
url = "http://127.0.0.1:5000/sentence"
payload = {"text": "this is a test sentence", "article_id": "test"}
r = requests.post(url, json=payload)

print(r.text)
