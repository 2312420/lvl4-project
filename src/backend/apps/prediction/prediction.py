#from sklearn.preprocessing import PolynomialFeatures
#
#import pandas as pd
#import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
import stock_data
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


# Given points squish down into single points for each date
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
            sentiment.append(point['sentiment'])
            pass
        else:
            to_add['sentiment'] = np.mean(sentiment)
            output.append(to_add)
            cur_date = point['time']
            to_add = point

    return output


# Plot sentiment
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
def format_df(points_array):
    df = pd.DataFrame(points_array)

    # set time as index
    df['time'] = pd.to_datetime(df.time, format="%Y-%m-%d %H:%M:%S")
    df.index = df['time']

    # Use fastai to create new coloumns
    #fastai_code.add_datepart(df, "time")

    # Drop useless fields
    df.drop('company_id', axis=1, inplace=True)
    df.drop('sentence_id', axis=1, inplace=True)
    df.drop('id', axis=1, inplace=True)
    df.drop('time', axis=1, inplace=True)
    return df.sort_index(ascending=True, axis=0)


def squish_sentiment2(df):
    pass

if __name__ == '__main__':
    data = squish_sentiment(filter_points(get_points("FB", "2 month")))
    df = format_df(data)

    train = df[:32].copy()
    valid = df[32:].copy()

    x_train = train.drop('close', axis=1)
    y_train = train['close']
    x_valid = valid.drop('close', axis=1)
    y_valid = valid['close']

    model = LinearRegression()
    model.fit(x_train, y_train)

    preds = model.predict(x_valid)

    print(preds)

    # plot
    valid['predictions'] = 0
    valid['predictions'] = preds

    valid.index = df[32:].index
    train.index = df[:32].index

    plt.plot(train['close'])
    plt.plot(valid[['close', 'predictions']], )

    plt.show()
