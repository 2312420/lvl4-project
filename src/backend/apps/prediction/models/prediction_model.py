# Contains predictions models
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from datetime import timedelta

from models import common, sentiment_model


# Used to make actual predictions
def linear_regression(df, target_feature, future_days):
    data = common.expand_time(df.copy())

    x_train = data[['sentiment', 'day', 'day_year', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_train = data[target_feature]

    x_future = sentiment_model.future_sentiment_regression(x_train, future_days)
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