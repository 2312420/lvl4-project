# Imports
import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Python files
import stock_data
import models

# Variables
baseurl = "http://127.0.0.1:5000"


# Get all companies from db
def get_companies():
    url = baseurl + "/company"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None


# Get data points from db given a stock code and time frame
def get_points(stock_code, interval):
    url = baseurl + "/points/" + stock_code + "/" + interval
    r = requests.get(url)
    return r.json()


# Filter points that are missing data
def filter_points(points):
    output = []
    for point in points:
        if point['high']:
            output.append(point)
    return output


# Updates verdict of company in database
def update_verdict(stock_code, verdict):
    url = baseurl + '/company/verdict'
    payload = {'stock_code': stock_code, 'verdict': verdict}
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        return "verdict updated"
    else:
        return "something went wrong"


# Given ordered data set of points combine points with common time into single point
def squish_sentiment(points):
    output = []
    sentiment = []
    cur_date = None

    for point in points:
        if cur_date == None:
            cur_date = point['time']
            to_add = point
            sentiment.append(point['sentiment'])
        elif cur_date == point['time']:
            # Common point
            sentiment.append(point['sentiment'])
        else:
            # Not common point
            to_add['sentiment'] = np.mean(sentiment)
            output.append(to_add)
            cur_date = point['time']
            to_add = point
        if output == []:
            # All data points are from same time
            to_add['sentiment'] = np.mean(sentiment)
            output.append(to_add)

    return output


# Takes an array of points and turns it into workable dataset
def format_df(points_array, stock_code):
    df = pd.DataFrame(points_array)

    # Drop undesired fields
    df.drop('company_id', axis=1, inplace=True)
    df.drop('sentence_id', axis=1, inplace=True)
    df.drop('id', axis=1, inplace=True)

    # Set time to datetieme
    df['time'] = pd.to_datetime(df.time, format="%Y-%m-%d %H:%M:%S")

    # Add missing days to data frame
    df = add_stock_data(df, stock_code, 2)

    # Set time as index
    df.index = df['time']

    #df.drop('time', axis=1, inplace=True)
    return df.sort_index(ascending=True, axis=0)


# Takes dataframe with stock data and adds any missing data
def add_stock_data(df, stock_code, start_month):

    # Build model for predicting sentiment
    model = models.past_sentiment_regression(df)

    # Reading in stock data
    start = datetime.now() - relativedelta(month=start_month)
    data = stock_data.get_stock_data(stock_code, start, datetime.now(), "1d")
    dates = []

    for index, item in df.iterrows():
        dates.append(item["time"].date())

    for index, item in data.iterrows():
        if index.date() not in dates:
            pred = model.predict([item[["Open","High","Low","Close","Volume"]]])
            df = df.append({
                "sentiment": pred[0],
                "time": index,
                "open": item["Open"],
                "high": item["High"],
                "low": item["Low"],
                "close": item["Close"],
                "volume": item["Volume"]
                }, ignore_index=True)

    return df


if __name__ == '__main__':
    companies = get_companies()
    while True:
        for company in companies:
            stock_code = company['stock_code']
            points = get_points(stock_code, "3 month")
            if points == []:
                print("No data")
                update_verdict(stock_code, "NO-DATA")
            else:
                if(points[0]['close'] == None):
                    update_verdict(stock_code, "NO-DATA")
                else:
                    data = squish_sentiment(filter_points(points))
                    df = format_df(data, stock_code)

                    days_into_future = 10
                    prediction_df = models.linear_regression(df, "close", days_into_future)

                    if prediction_df['predictions'][-(days_into_future-1)] < prediction_df['predictions'][-1]:
                        print(update_verdict(stock_code, "HOT"))
                    else:
                        print(update_verdict(stock_code, "NOT"))
