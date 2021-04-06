# Used for getting data for given company given a certain time frame

# Imports
from datetime import date, datetime
import requests
import numpy as np
import pandas as pd

# Python files
from modules import stock_data
from models import sentiment_model

baseurl = "http://backend-api:5000"


# Get data points from db given a stock code and time frame
def get_points(stock_code, start_date):
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    interval = date.today() - start
    url = baseurl + "/points/" + stock_code + "/" + str(interval.days) + " day"
    r = requests.get(url)

    return r.json()


# Gets historical stock price
def stock_points(stock_code, start_date, end_date):
    data = stock_data.get_stock_data(stock_code, start_date, end_date,"1d")
    return data


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


# Combine actual datafframes
def combine_data(df, stock_data):
    model = sentiment_model.past_sentiment_regression(df)
    dates = []
    for index, item in df.iterrows():
        dates.append(item["time"].date())

    for index, item in stock_data.iterrows():
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


# create new dataframe from sentiment and historical data
def create_df(sentiment, historical):
    new_sentiment = squish_sentiment(sentiment)

    df = pd.DataFrame(new_sentiment)
    df.drop('company_id', axis=1, inplace=True)
    df.drop('sentence_id', axis=1, inplace=True)
    df.drop('id', axis=1, inplace=True)

    # Set time to datetieme
    df['time'] = pd.to_datetime(df.time, format="%Y-%m-%d %H:%M:%S")

    try:
        df = combine_data(df, historical)
    except ValueError:
        print("Value error encountered")
        return pd.DataFrame

    # Set time as index
    df.index = df['time']

    return df.sort_index(ascending=True, axis=0)


# Main function for getting finished dataframe for comapny
def get_data(stock_code, start_date, end_date):
    sentiment_data = get_points(stock_code, start_date)
    historical_data = stock_points(stock_code, start_date, end_date)

    if sentiment_data == [] or historical_data.empty == True:
        return pd.DataFrame()
    else:
        combined = create_df(sentiment_data, historical_data)
        return combined

