#from modules import prediction as pre
#from modules import models as md
from datetime import datetime
from datetime import date
#import pandas as pd

from modules import prediction


def custom_predictions(start_date, end_date, stock_code):
    prediction_df = prediction.custom_predictions(stock_code, start_date, end_date, 'close')
    new_preds = []
    for index, item in prediction_df.iterrows():
        item_date = datetime.strptime(str(index), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        pred = item['predictions']
        new_preds.append([item_date, pred])

    return new_preds



