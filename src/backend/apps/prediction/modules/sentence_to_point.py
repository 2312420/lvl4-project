# Used for turning sentences in HotOrNot databse into data points in time series database
import requests
from modules import stock_data

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
    data = stock_data.data_at_date(sentence_json['context'], sentence_json['date'] + " " + sentence_json['time'])
    if data.empty:
        print("Blocked")
        payload = {"sentence_id": sentence_json['id'], "close": None}
        r = requests.post(url, json=payload)
    else:
        print("Point")
        payload = {"time": date_time,
                   "company_id": sentence_json['context'],
                   "sentiment": sentence_json['sentiment'],
                   "sentence_id": sentence_json['id'],
                   "open": data['Open'],
                   "high": data['High'],
                   "low": data['Low'],
                   "close": data['Close'],
                   "volume": data['Volume'], }
        r = requests.post(url, json=payload)


# Update stock data of point
def update_price(point):
    url = baseurl + "/points/price"
    data = stock_data.date_at_date(point['stock_code'], point['date_time'])
    if data.empty:
        print("Something wrong with stock code: " + point['stock_code'])
    else:
        payload = {"id": point['id'],
                   "open": data['Open'],
                   "high": data['High'],
                   "low": data['Low'],
                   "close": data['Close'],
                   "volume": data['Volume'], }
        r = requests.put(url, json=payload)
        print("point updated")


def update_points():
    for point in get_points():
        if point['open'] == None:
            update_price(point)
            print("Point updated")


def redo_points():
    url = "http://127.0.0.1:5000/sentence/findByStatus"
    payload = {"status": "DONE"}
    r = requests.get(url, json=payload)

    points = r.json()
    todo = len(points)

    for sentence in points:
        sentence_to_point(sentence)
        todo -= 1
        print(todo)


redo_points()
#def sentence_to_point(sentence):

#if __name__ == '__main__':
#     #If need to updated existing point data
#     for point in get_points():
#        if point['open'] == None:
#            update_price(point)
#            print("Point updated")

    #while(True):
    #    for sentence in get_sentences():
    #        sentence_to_point(sentence)
    #        print("Point created")





