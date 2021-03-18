import yfinance as yf
from sklearn.metrics import mean_squared_error, median_absolute_error


def get_pred_true(df, stock_code):
    stock_data = yf.Ticker(stock_code)
    times = []
    prices = []

    times = df.index
    predictions = df['predictions']
    history = stock_data.history(start=times[0], end=times[-1])

    pred = []
    true = []
    for index, point in history.iterrows():
        if index in times:
            pred.append(predictions[index])
            true.append(point['Close'])

    return pred, true


# Mean squared error
def metric1(df, stock_code):
    pred, true = get_pred_true(df, stock_code)
    result = mean_squared_error(y_true=true, y_pred=pred)
    return result


# Median absolute error
def metric2(df, stock_code):
    pred, true = get_pred_true(df, stock_code)
    result = median_absolute_error(y_true=true, y_pred=pred)
    return result




