# Contains predictions models
import pandas as pd
from models import common, sentiment_model
from sklearn.ensemble import RandomForestRegressor


# Used to make actual predictions
def random_forest(df, target_feature, future_days, end_date=-1):
    data = common.expand_time(df.copy())

    x_train = data[['sentiment', 'day', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_train = data[target_feature]

    # Dataframe to store future sentiment and stock price predictions
    x_future = sentiment_model.future_sentiment_regression(x_train, future_days, end_date)
    x_future = x_future[['sentiment', 'day', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    x_future = pd.concat([x_train, x_future])

    # MODEL
    reg = RandomForestRegressor()

    # Prediction
    model = reg.fit(x_train, y_train)

    preds = model.predict(x_future)
    x_future['predictions'] = preds

    # Plot graph (for testing)
    # plt.plot(data['close'])
    # plt.plot(x_future['predictions'], color='green', alpha=0.4)
    # plt.xticks(fontsize=5)
    # plt.show()

    return x_future