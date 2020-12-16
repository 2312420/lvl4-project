# Used for testing predictions

# Imports
import requests
import json
import yfinance as yf
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

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
        stock_data = yf.Ticker(company['stock_code'])
        start_point = datetime.strptime(predictions[0][0], "%Y-%m-%d %H:%M:%S")
        end_point = datetime.strptime(predictions[-1][0], "%Y-%m-%d %H:%M:%S")
        stock_df = stock_data.history(start=start_point, end=end_point)

        predictions_df = pd.DataFrame(predictions)
        past_30_days = end_point - timedelta(days=30)

        times = []
        prices = []
        for point in predictions:
            times.append(point[0])
            prices.append(point[1])

        n = 0
        y = 0
        for index, point in stock_df.iterrows():
            if index.__str__() in times:
                n += 1
                pos = times.index(index.__str__())
                y += (point['Close'] - prices[pos])

        total_mean_squared_loss = ( np.square(y) ) / n

        #n = 0
        #y = 0
        true = []
        pred = []
        for index, point in stock_df[past_30_days:].iterrows():
            if index.__str__() in times:
                pos = times.index(index.__str__())
                true.append(point['Close'])
                pred.append(prices[pos])

        past_30_days_loss = mean_squared_error(true,pred)

        print(company['short_hand'])
        print(past_30_days_loss)

        return total_mean_squared_loss


if __name__ == '__main__':
    i = 0
    for company in get_companies():
        squared_loss(company)
        #i += 1
        #if i == 3:
        #    break

