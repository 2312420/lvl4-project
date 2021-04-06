import json
import requests
from datetime import datetime

baseurl = "http://127.0.0.1:5000/"
source_ids = {
    "WSJ_Markest": 95,
    "WSJ_Technology": 96,
    "WSJ_US_business": 97,
    "TIME_business": 98,
    "BBC_business": 99,
    "CNBC": 100,
    "FinancialTimes": 101,
    "FortuneRssFeed": 102,
    "Economic_Times": 103,
}

add_url = baseurl + "/article_with_date"
with open('../raw/articles(15-12-2020).txt') as f:
    for line in f:
        line = json.loads(line)
        items = line[list(line.keys())[0]]
        title = items[0][0]
        transcript = items[0][1]
        source = source_ids[items[1]]
        datetime = items[2]
        payload = {"title": title, "transcript": transcript, "source_id": source, "date-time": datetime}
        r = requests.post(add_url, json=payload)
        print("article added")


