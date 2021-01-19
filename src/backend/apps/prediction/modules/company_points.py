# Used for getting data for given company given a certain time frame
from modules import stock_data
from datetime import date, datetime
import requests
import numpy as np

baseurl = "http://127.0.0.1:5000"


# Get data points from db given a stock code and time frame
def get_points(stock_code, start_date):
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    interval = date.today() - start
    url = baseurl + "/points/" + stock_code + "/" + str(interval.days) + " day"
    r = requests.get(url)
    return r.json()


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


def combine_data(sentiment, historical):
    new_sentiment = squish_sentiment(sentiment)
    print(new_sentiment)

    return None


def get_data(stock_code, start_date, end_date):
    sentiment_data = get_points(stock_code, start_date)
    historical_data = stock_points(stock_code, start_date, end_date)

    combined = combine_data(sentiment_data, historical_data)


