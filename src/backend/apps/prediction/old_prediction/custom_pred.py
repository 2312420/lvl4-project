from modules import prediction as pre
from modules import models as md
from datetime import datetime
import pandas as pd


def custom_prediction(start_date, end_date, stock_code):
    points = pre.get_points(stock_code, "3 month")

    data = pre.squish_sentiment(pre.filter_points(points))
    df = pre.format_df(data, stock_code)

    range_df = df[df['time'] > start_date]
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    days_into_future = (end_dt - range_df['time'].iloc[-1]).days + 2
    prediction_df = md.linear_regression(range_df, "close", days_into_future)

    new_preds = []
    for index, item in prediction_df.iterrows():
        date = datetime.strptime(str(index), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        pred = item['predictions']
        new_preds.append([date, pred])

    return new_preds

