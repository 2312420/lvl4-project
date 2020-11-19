import requests
import json
url = "http://127.0.0.1:5000/article"
payload = {"id": "A1 test tile", "data": "content"}
r = requests.post(url, json=payload)

print(r.text)
