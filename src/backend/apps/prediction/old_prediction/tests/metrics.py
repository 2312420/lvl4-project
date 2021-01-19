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
import csv

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

        # Get mean squared error for full all predictions
        times = []
        prices = []
        for point in predictions:
            times.append(point[0])
            prices.append(point[1])

        true = []
        pred = []
        for index, point in stock_df.iterrows():
            if index.__str__() in times:
                pos = times.index(index.__str__())
                true.append(point['Close'])
                pred.append(prices[pos])

        total_mean_squared_loss = mean_squared_error(true, pred)

        # Get mean squared error for past thirty days
        past_30_days = end_point - timedelta(days=30)
        true = []
        pred = []
        for index, point in stock_df[past_30_days:].iterrows():
            if index.__str__() in times:
                pos = times.index(index.__str__())
                true.append(point['Close'])
                pred.append(prices[pos])

        past_30_days_loss = mean_squared_error(true, pred)

        return total_mean_squared_loss, past_30_days_loss
    else:
        return None, None


def get_sentence_amount(company):
    stock_code = company['stock_code']
    url = base_url + '/company/' + stock_code + '/sentences'
    r = requests.get(url)
    if r.status_code == 200:
        content = r.json()
        return len(content)


if __name__ == '__main__':
    record_current_predictions()
    now = datetime.now().strftime(("%d-%m-%Y, %H-%M"))
    file_name = "results/squared_error/results " + now + ".csv"
    with open(file_name, "x") as f:
        fieldnames = ['stock_code', 'short_hand', 'sentences', 'articles', 'total_mean', '30_days_mean']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for company in get_companies():
            total, past_30 = squared_loss(company)
            if total:
                sentences = get_sentence_amount(company)
                writer.writerow({'stock_code': company['stock_code'], 'short_hand': company['short_hand'],
                                 'sentences': sentences, 'total_mean': total,
                                 '30_days_mean': past_30})
