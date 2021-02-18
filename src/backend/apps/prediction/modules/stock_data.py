# Used for getting stock data from Yahoo Finances
import yfinance as yf
from datetime import datetime
from datetime import timedelta


# Data format is Year-Month-day
def get_stock_data(stock_code, start_date, end_date, peroid):
    stock_data = yf.Ticker(stock_code)
    stock_df = stock_data.history(interval = peroid, start=start_date, end=end_date)
    return stock_df
    # Stock DF: Open, High, Low, Close, Volume, Dividends, Split


# Takes date and time stirng and turns it into date time object
def to_datetime(date_string):
    try:
        date_time = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    except:
        date_time = datetime.strptime(date_string, "%m/%d/%Y %H:%M:%S")

    return date_time


# Get the data of stock at current date, accounts for weekends
def data_at_date(stock_code, date_time):
    base_date = to_datetime(date_time)
    stock_data = yf.Ticker(stock_code)
    stock_df = stock_data.history( interval="1d", start=base_date, end=base_date)
    if stock_df.empty:
        # Date is on weekend
        stock_df = stock_data.history(interval="1d", start=(base_date - timedelta(days=3)), end=base_date)
        if stock_df.empty:
            # Something wrong with stock code
            return stock_df
        else:
            return stock_df.iloc[-1]
    else:
        return stock_df.iloc[-1]
