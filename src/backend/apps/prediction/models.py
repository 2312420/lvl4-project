# Contains predictions models
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
import pandas as pd


# Linear regression model
def linear_regression(df):
    train = df[:32].copy()
    valid = df[32:].copy()

    x_train = train.drop('close', axis=1)
    y_train = train['close']
    x_valid = valid.drop('close', axis=1)
    y_valid = valid['close']

    model = LinearRegression()
    model.fit(x_train, y_train)

    preds = model.predict(x_valid)
    return preds, train, valid


# Random Forest Regressor
def random_for(df):

    train = df[:32].copy()
    valid = df[32:].copy()

    x_train = train.drop('close', axis=1)
    y_train = train['close']
    x_valid = valid.drop('close', axis=1)
    y_valid = valid['close']


    x_train['sentiment_cat'] = x_train['sentiment'].astype('category')
    x_train['sentiment_cat'] = x_train['sentiment_cat'].cat.codes

    x_train['open_cat'] = x_train['open'].astype('category')
    x_train['open_cat'] = x_train['open_cat'].cat.codes

    x_train['high_cat'] = x_train['high'].astype('category')
    x_train['high_cat'] = x_train['high_cat'].cat.codes

    x_train['low_cat'] = x_train['low'].astype('category')
    x_train['low_cat'] = x_train['low_cat'].cat.codes

    x_train['volume_cat'] = x_train['volume'].astype('category')
    x_train['volume_cat'] = x_train['volume_cat'].cat.codes


    x_valid['sentiment_cat'] = x_valid['sentiment'].astype('category')
    x_valid['sentiment_cat'] = x_valid['sentiment_cat'].cat.codes

    x_valid['open_cat'] = x_valid['open'].astype('category')
    x_valid['open_cat'] = x_valid['open_cat'].cat.codes

    x_valid['high_cat'] = x_valid['high'].astype('category')
    x_valid['high_cat'] = x_valid['high_cat'].cat.codes

    x_valid['low_cat'] = x_valid['low'].astype('category')
    x_valid['low_cat'] = x_valid['low_cat'].cat.codes

    x_valid['volume_cat'] = x_valid['volume'].astype('category')
    x_valid['volume_cat'] = x_valid['volume_cat'].cat.codes


    features = ['sentiment_cat', 'open_cat', 'high_cat', 'low_cat', 'volume_cat']

    model = RandomForestRegressor(n_estimators=1000, max_depth=1000, random_state=42)
    model.fit(x_train, y_train)

    preds = model.predict(x_valid)
    return preds, train, valid

