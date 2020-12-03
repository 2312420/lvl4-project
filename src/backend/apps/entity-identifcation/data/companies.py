import pandas as pd
import requests


# Data set from kaggle:
# https://www.kaggle.com/dgawlik/nyse?select=securities.csv
companies_df = pd.read_csv('companies.csv')


def add_company(stock_code, short_hand):
    url = "http://127.0.0.1:5000/company"
    payload = {"stock_code": stock_code, "short_hand": short_hand}
    r = requests.post(url, json=payload)


for company in companies_df.iterrows():
    stock_code = company[1]['Ticker symbol']
    short_hand = company[1]['Security']
    add_company(stock_code, short_hand)
    print("Company added")
