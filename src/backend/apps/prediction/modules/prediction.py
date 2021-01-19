from datetime import date
from datetime import datetime
from modules import company_points
from models import prediction_model

# Date of first article in DB
first_article = "2020-11-11"


# dates in form YYYY-MM-DD
def custom_predictions(stock_code, start_date, end_date, future_days, target_feature):
    data = company_points.get_data(stock_code, start_date, end_date)
    model = prediction_model.linear_regression(data, target_feature, future_days)


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

        if prediction_df['predictions'][-(days_into_future - 1)] < prediction_df['predictions'][-1]:
            return stock_code, "HOT", new_preds
        else:
            return stock_code, "NOT", new_preds
    else:
        return stock_code, "NO-DATA", []


print(new_predictions({"stock_code": "FB" }))
