from sklearn.linear_model import LinearRegression
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

    return output


# Plot sentiment graph
def plot_sentiment(df):
    points = []
    y = []
    for i in range(len(df)):
        points.append(df.iloc[i].at['sentiment'])
        y.append(i)

    start_date = df.iloc[0].at['time']
    end_date = df.iloc[-1].at['time']
    plt.title("Sentiment for " + df.iloc[0].at["company_id"])
    plt.xlabel(start_date + " to " + end_date)
    plt.ylabel("sentiment")
    plt.plot(y, points)
    plt.show()


# Takes an array of points and turns it into workable dataset
def format_df(points_array, stock_code):
    df = pd.DataFrame(points_array)

    # Drop undesired fields
    df.drop('company_id', axis=1, inplace=True)
    df.drop('sentence_id', axis=1, inplace=True)
    df.drop('id', axis=1, inplace=True)

    # Set time to datetiem
    df['time'] = pd.to_datetime(df.time, format="%Y-%m-%d %H:%M:%S")

    # Add missing days to data frame
    df = add_stock_data(df, stock_code, 8)

    # Set time as index
    df.index = df['time']

    #df.drop('time', axis=1, inplace=True)
    return df.sort_index(ascending=True, axis=0)


# Takes dataframe with stock data and adds any missing data
def add_stock_data(df, stock_code, start_month,):

    # Build model for predicting sentiment
    model = models.sentiment_regression(df)

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

    stock_code = "FB"

    data = squish_sentiment(filter_points(get_points(stock_code, "2 month")))
    df = format_df(data, stock_code)

    print(df)

    split = 105

    preds, train, valid = models.linear_regression_2(df, split, "close")

    # plot
    valid['predictions'] = 0
    valid['predictions'] = preds

    valid.index = df[split:].index
    train.index = df[:split].index

    plt.plot(train['close'])
    plt.plot(valid[['close', 'predictions']])
    plt.xticks(fontsize=5)
    plt.show()



