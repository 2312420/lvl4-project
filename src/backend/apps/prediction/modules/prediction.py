from datetime import date
from datetime import datetime
from modules import company_points
from models import prediction_model

# Date of first article in DB
first_article = "2020-11-11"


# dates in form YYYY-MM-DD
def custom_predictions(stock_code, start_date, end_date, target_feature):
    df = company_points.get_data(stock_code, start_date, end_date)

    range_df = df[df['time'] > start_date]
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    days_into_future = (end_dt - range_df['time'].iloc[-1]).days + 2
    prediction_df = prediction_model.linear_regression(range_df, "close", days_into_future)

    return prediction_df


# For updating stored company predictions
def new_predictions(company):
    days_into_future = 30
    end_date = date.today().strftime("%Y-%m-%d")

    stock_code = company['stock_code']
    data = company_points.get_data(stock_code, first_article, end_date)
    if data.empty == False:
        prediction_df = prediction_model.linear_regression(data, "close", days_into_future)
        new_preds = []
        for index, item in prediction_df.iterrows():
            item_date = datetime.strptime(str(index), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            pred = item['predictions']
            new_preds.append([item_date, pred])



        change = prediction_df['predictions'][-1] - data.__array__()[-1][5]
        if change > 1:
            return stock_code, "HOT", new_preds, change
        elif change < -1:
            return stock_code, "NOT", new_preds, change
        else:
            return stock_code, "HOLD", new_preds, change
    else:
        return stock_code, "NO-DATA", [], 0

