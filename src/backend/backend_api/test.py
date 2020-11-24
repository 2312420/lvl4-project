import requests
import json
url = "http://127.0.0.1:5000/article/1/status"
payload = {"id": "test", "title": "new test title", "transcript": "This is a test article", "source_id": "1", "status": "oof"}
r = requests.put(url, json=payload)

print(r.text)
