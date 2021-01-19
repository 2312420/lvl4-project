# Prediction to run to test if metric has improved
# Evaluates prediction with data gathered between 2020-11-11 to 2020-12-15

# 15 day
# 30 day
# 60 day

from modules import company_points
from models import prediction_model
import pandas as pd
from testing import metrics

def make_predictions(stock_code, days):
    data = company_points.get_data(stock_code, "2020-11-11", "2020-12-15")
    prediction_df = prediction_model.linear_regression(data, "close", days, "2020-12-15")
    return prediction_df


def run_metrics(stock_code, days):
    df = make_predictions(stock_code, days,)
    pd.set_option('display.max_rows', None)

    future_predictions = df["2020-12-16 00:00:00":]

    metrics.metric1(future_predictions, stock_code)
    metrics.metric2(future_predictions, stock_code)
    metrics.metric3(future_predictions,stock_code)
    pass



run_metrics("FB", 15)
