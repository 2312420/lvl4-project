import yfinance as yf


# Data format is Year-Month-day
def get_stock_data(stock_code, start_date, end_date, peroid):
    stock_data = yf.Ticker(stock_code)
    stock_df = stock_data.history(period=peroid, start=start_date, end=end_date)
    return stock_df




