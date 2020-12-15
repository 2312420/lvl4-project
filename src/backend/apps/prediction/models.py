# Contains predictions models
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from datetime import timedelta


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
def linear_regression(df, target_feature, future_days):
    data = expand_time(df.copy())

    x_train = data[['sentiment', 'day', 'day_year', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_train = data[target_feature]

    x_future = future_sentiment_regression(x_train, future_days)
    x_future = x_future[['sentiment', 'day', 'day_year', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]

    x_future = pd.concat([x_train, x_future])

    model = LinearRegression().fit(x_train, y_train)
    preds = model.predict(x_future)
    x_future['predictions'] = preds

    # Plot graph (for testing)
    #plt.plot(data['close'])
    #plt.plot(x_future['predictions'], color='green', alpha=0.4)
    #plt.xticks(fontsize=5)
    #plt.show()

    return x_future


# Used to fill in missing sentiment data
def past_sentiment_regression(df):
    train = df.copy()
    x_train = train.drop(["sentiment", "time"], axis=1)
    y_train = train['sentiment']
    model = LinearRegression()
    model.fit(x_train, y_train)
    return model


# Used to predict future sentiment
def future_sentiment_regression(df, future_days):
    # Create future dataframe
    now = datetime.now().replace(microsecond=0, minute=0, hour=0, second=0)

    data = df.copy()
    x_train = data[['day', 'day_year', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_train = data['sentiment']

    model = LinearRegression()
    model.fit(x_train[-future_days:], y_train[-future_days:])

    recent_sent = df['sentiment'][-1]
    future_df = pd.DataFrame({'time': [now], })#'sentiment': recent_sent})

    for i in range(1, future_days - 1):
        future_df = future_df.append({'time': now + timedelta(days=i)}, ignore_index=True)

    future_df = expand_time(future_df)
    future_df.index = future_df['time']
    future_df = future_df.drop(['time'], axis=1)
    future_df = future_df[['day', 'day_year', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]

    preds = model.predict(future_df)
    future_df['sentiment'] = preds

    return future_df


# Used for testing data on self
def test_model(df, split, target_feature):
    train = df[:split].copy()
    valid = df[split:].copy()

    train = expand_time(train)
    valid = expand_time(valid)

    x_train = train[['sentiment', 'day', 'day_year', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_train = train['close']

    x_valid = valid[['sentiment', 'day', 'day_year', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_valid = valid['close']

    pipe = make_pipeline(LinearRegression())
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