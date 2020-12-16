# Used for testing predictions

# Imports
import requests
import json
import yfinance as yf
from datetime import datetime

# Urls
prediction_url = "http://127.0.0.1:5004"
base_url = "http://127.0.0.1:5000"


# Get all companies from db
def get_companies():
    url = base_url + "/company"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None


def run_predictions():
    url = prediction_url + '/predictions'
    for company in get_companies():
        r = requests.get(url, json=company)


def record_current_predictions():
    now = datetime.now().strftime(("%d-%m-%Y, %H-%M-%S"))
    file_name = "results/historic_predictions/predictions " + now + ".txt"
    with open(file_name, "x") as f:
        for company in get_companies():
            f.write(json.dumps(company))


def squared_loss(company):

    predictions = json.loads(company['predictions'])
    if predictions != "[]":
        pass

if __name__ == '__main__':
    i = 0
    record_current_predictions()

    #for company in get_companies():
    #    print(company['short_hand'])
    #    squared_loss(company)


        #i += 1
        #if i == 5:
        #    break