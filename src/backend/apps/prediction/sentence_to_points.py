# Used for turning sentences in HotOrNot databse into data points in time series database

import json
import requests

baseurl = "http://127.0.0.1:5000"

def get_sentences():
    url = baseurl + "/sentence/findByStatus"
    payload = {"status": "DONE"}
    r = requests.get(url, json=payload)
    if r.status_code == 200:
        return r.json()
    else:
        return None


def sentence_to_point(sentence_json):
    url = baseurl + "/points"
    date_time = sentence_json['date'] + " " + sentence_json['time']
    payload = {"time": date_time,
               "company_id": sentence_json['context'],
               "sentiment": sentence_json['sentiment'],
               "sentence_id": sentence_json['id']}
    r = requests.post(url, json=payload)
    print(r.status_code)

#id
#text
#sentiment
#stats
#date '11/11/2020'
#time '15:10:59'
#article_id
#Context

for sentence in get_sentences():
    url = baseurl + ""

    #print(sentence)
    #sentence_to_point(sentence)
    #break