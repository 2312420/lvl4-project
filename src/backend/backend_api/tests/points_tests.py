import requests
import json
from datetime import datetime

baseurl = "http://127.0.0.1:5000"


# Test get api call
def test_get():
    url = baseurl + "/points/test"
    r = requests.get(url)
    print(r.json())


# Test post api call
def test_post():
    payload = {
        "time" : "2020-12-03 10:38:22",
        "sentiment": "0.4"
    }
    url = baseurl + "/points/" + "test"
    r = requests.post(url, json=payload)
    return r


def test_get_interval():
    url = baseurl + "/points/" + "test/" + "12 hours"
    r = requests.get(url)
    print(r.json())


if __name__ == '__main__':
    test_get_interval()
