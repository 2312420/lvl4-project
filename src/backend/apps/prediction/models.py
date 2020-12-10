# Contains predictions models
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


# Take time feature and expand it into multiple features
def expand_time(df):
    df["day_year"] = df["time"].dt.year
    df["day_month"] = df["time"].dt.month
    df["day_week"] = df["time"].dt.isocalendar().week
    df["day"] = df["time"].dt.day
    df["day_hour"] = df["time"].dt.hour
    df["day_minute"] = df["time"].dt.minute
    df["day_dayofweek"] = df["time"].dt.dayofweek
    return df


# Used to make actual predictions
def linear_regression(df):
    data = df.copy()

    x_train = data[['sentiment', 'day_year', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_train = data['close']

    pipe = make_pipeline(StandardScaler(),)

# Used for testing data on self
def test_model(df, split, target_feature):
    train = df[:split].copy()
    valid = df[split:].copy()

    train = expand_time(train)
    valid = expand_time(valid)

    x_train = train[['sentiment', 'day_year', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_train = train['close']

    x_valid = valid[['sentiment', 'day_year', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_valid = valid['close']

    pipe = make_pipeline(StandardScaler(), LinearRegression())
    pipe.fit(x_train, y_train)

    preds = pipe.predict(x_valid)

    valid['predictions'] = 0
    valid['predictions'] = preds

    valid.index = df[split:].index
    train.index = df[:split].index

    plt.plot(train['close'])
    plt.plot(valid[['close', 'predictions']])
    plt.xticks(fontsize=5)
    plt.show()


def sentiment_regression(df):
    train = df.copy()
    x_train = train.drop(["sentiment", "time"], axis=1)
    y_train = train['sentiment']
    model = LinearRegression()
    model.fit(x_train, y_train)
    return model
