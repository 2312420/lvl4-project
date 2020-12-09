# Contains predictions models
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
from sklearn import preprocessing
import pandas as pd
from datetime import datetime


# Linear regression model
def linear_regression(df, split, target_feature):
    train = df[:split].copy()
    valid = df[split:].copy()

    x_train = train.drop(target_feature, axis=1)
    y_train = train[target_feature]
    x_valid = valid.drop(target_feature, axis=1)
    y_valid = valid[target_feature]

    model = LinearRegression()
    model.fit(x_train, y_train)

    preds = model.predict(x_valid)
    return preds, train, valid


def date_to_time(x):
    return x.toordinal()


def expand_time(df):
    df["day_year"] = df["time"].dt.year
    df["day_month"] = df["time"].dt.month
    df["day_week"] = df["time"].dt.week
    df["day"] = df["time"].dt.day
    df["day_hour"] = df["time"].dt.hour
    df["day_minute"] = df["time"].dt.minute
    df["day_dayofweek"] = df["time"].dt.dayofweek
    return df

def linear_regression_2(df, split, target_feature):
    train = df[:split].copy()
    valid = df[split:].copy()

    train = expand_time(train)
    valid = expand_time(valid)

    x_train = train[['sentiment', 'day_year', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_train = train[target_feature]

    x_valid = valid[['sentiment', 'day_year', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_valid = valid[target_feature]

    print(x_train)

    model = LinearRegression()
    model.fit(x_train, y_train)

    preds = model.predict(x_valid)
    return preds, train, valid


def sentiment_regression(df):
    train = df.copy()

    x_train = train.drop(["sentiment", "time"], axis=1)

    print(x_train.columns)
    y_train = train['sentiment']

    model = LinearRegression()
    model.fit(x_train, y_train)

    return model
