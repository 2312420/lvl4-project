import requests
import json

baseurl = "http://127.0.0.1:5000"
url = baseurl + "/points/test"

r = requests.get(url)
print(r.json())
