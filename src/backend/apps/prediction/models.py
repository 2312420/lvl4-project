# Contains predictions models
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
import pandas as pd


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


def sentiment_regression(df):
    train = df.copy()

    x_train = train.drop(["sentiment", "time"], axis=1)

    print(x_train.columns)
    y_train = train['sentiment']

    model = LinearRegression()
    model.fit(x_train, y_train)

    return model
