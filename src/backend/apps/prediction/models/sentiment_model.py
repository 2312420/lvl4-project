# Sentiment prediction model to fill in missing sentiemnt data
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from datetime import timedelta

from models import common

from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import SGDRegressor

from sklearn.tree import DecisionTreeRegressor

# Used to fill in missing sentiment data
def past_sentiment_regression(df):
    train = df.copy()
    x_train = train.drop(["sentiment", "time"], axis=1)
    y_train = train['sentiment']
    model = make_pipeline(StandardScaler(), BayesianRidge())
    model.fit(x_train, y_train)
    return model


# Used to predict future sentiment
def future_sentiment_regression(df, future_days, end_date=-1):
    # Create future dataframe
    if end_date != -1:
    # End date beings set manually
        now = datetime.strptime(end_date, "%Y-%m-%d")
    else:
        now = datetime.now().replace(microsecond=0, minute=0, hour=0, second=0)

    data = df.copy()
    x_train = data[['day', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_train = data['sentiment']

    model = make_pipeline(StandardScaler(), BayesianRidge()) #BayesianRidge()
    model.fit(x_train[-future_days:], y_train[-future_days:])

    recent_sent = df['sentiment'][-1]
    future_df = pd.DataFrame({'time': [now], })#'sentiment': recent_sent})

    for i in range(1, future_days - 1):
        future_df = future_df.append({'time': now + timedelta(days=i)}, ignore_index=True)

    future_df = common.expand_time(future_df)
    future_df.index = future_df['time']
    future_df = future_df.drop(['time'], axis=1)
    future_df = future_df[['day', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]

    preds = model.predict(future_df)
    future_df['sentiment'] = preds

    return future_df