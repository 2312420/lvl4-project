# Contains predictions models
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
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
    y_train = data['close']



    x_future = future_sentiment_regression(data, 5)

    #pipe = make_pipeline(StandardScaler(), LinearRegression())
    #pipe.fit(x_train, y_train)
    #preds = pipe.predict(x_future)
    #x_future['predictions'] = preds

    print(data[['sentiment']])
    print(x_future[['sentiment']])

    #plt.plot(data['close'])
    #plt.plot(x_future['predictions'])
    #plt.xticks(fontsize=5)
    #plt.show()

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
    # Create future sentiment model

    x_train = df[['day_year', 'day', 'day_month', 'day_week', 'day_hour', 'day_minute', 'day_dayofweek']]
    y_train = df['sentiment']

    scaler = StandardScaler()
    x_scale = scaler.fit_transform(x_train, y_train)

    model = LinearRegression()
    model.fit(x_scale, y_train)

    # Create future dataframe
    now = datetime.now()
    future_df = pd.DataFrame({'time': [now]})

    for i in range(future_days - 1):
        future_df = future_df.append({'time': now + timedelta(i)}, ignore_index=True)

    future_df = expand_time(future_df)
    future_df.index = future_df['time']
    future_df = future_df.drop(['time'], axis=1)

    # Predict future sentiment
    preds = model.predict(scaler.fit_transform(future_df))
    future_df['sentiment'] = preds
    return future_df