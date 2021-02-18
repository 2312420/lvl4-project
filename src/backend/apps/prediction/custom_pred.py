from datetime import datetime
from modules import prediction


# Custom prediction between start data and end date for a given company
def custom_predictions(start_date, end_date, stock_code):
    prediction_df = prediction.custom_predictions(stock_code, start_date, end_date, 'close')
    new_preds = []
    for index, item in prediction_df.iterrows():
        item_date = datetime.strptime(str(index), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        pred = item['predictions']
        new_preds.append([item_date, pred])

    return new_preds



