import yfinance as yf
from datetime import datetime


# Data format is Year-Month-day
def get_stock_data(stock_code, start_date, end_date, peroid):
    stock_data = yf.Ticker(stock_code)
    stock_df = stock_data.history(period=peroid, start=start_date, end=end_date)
    return stock_df


# Takes date and time stirng and turns it into date time object
def to_datetime(date_string):
    date_time = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return date_time

