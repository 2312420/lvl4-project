# Used for turning sentences in HotOrNot databse into data points in time series database
import json
import requests
import stock_data

baseurl = "http://127.0.0.1:5000"


# Get all sentences that need to be transformed into points
def get_sentences():
    url = baseurl + "/sentence/findByStatus"
    payload = {"status": "PRED"}
    r = requests.get(url, json=payload)
    if r.status_code == 200:
        return r.json()
    else:
        return None


# Get all points in db
def get_points():
    url = baseurl + "/points"
    r = requests.get(url)
    return r.json()


# Given a sentence turn it into a point
def sentence_to_point(sentence_json):
    url = baseurl + "/points"
    date_time = sentence_json['date'] + " " + sentence_json['time']
    payload = {"time": date_time,
               "company_id": sentence_json['context'],
               "sentiment": sentence_json['sentiment'],
               "sentence_id": sentence_json['id']}
    r = requests.post(url, json=payload)


def update_price(point_id):
    pass


if __name__ == '__main__':
    get_points()

    #while(True):
    #    for sentence in get_sentences():
    #        sentence_to_point(sentence)
    #        print("point created")

