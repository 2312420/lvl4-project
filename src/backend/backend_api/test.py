import requests
import json
url = "http://127.0.0.1:5000/company"
payload = {"stock_code": "AAPL", "short_hand": "Apple"}
r = requests.post(url, json=payload)

print(r.text)
