# Sentiment prediction model to fill in missing sentiemnt data
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from datetime import timedelta


# Used to fill in missing sentiment data
def past_sentiment_regression(df):
    train = df.copy()
    x_train = train.drop(["sentiment", "time"], axis=1)
    y_train = train['sentiment']
    model = LinearRegression()
    model.fit(x_train, y_train)
    return model