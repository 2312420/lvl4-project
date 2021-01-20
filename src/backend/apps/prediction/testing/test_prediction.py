# Prediction to run to test if metric has improved
# Evaluates prediction with data gathered between 2020-11-11 to 2020-12-15

# 15 day
# 30 day
# 60 day

# Python scripts
from modules import company_points
from models import prediction_model
import pandas as pd
from testing import metrics

# Libs
from datetime import datetime
import csv
import requests

base_url = "http://127.0.0.1:5000"


# Get all companies from db
def get_companies():
    url = base_url + "/company"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None

# Used for getting specific company
def get_company(stock_code):
    url = base_url + "/company/" + stock_code
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None

# Get amount of sentences related to a company
def get_sentence_amount(stock_code):
    url = base_url + '/company/' + stock_code + '/sentences'
    r = requests.get(url)
    if r.status_code == 200:
        content = r.json()
        return len(content)


# Runs prediction on given company into given amount of days
def make_predictions(stock_code, days):
    data = company_points.get_data(stock_code, "2020-11-11", "2020-12-15")
    if data.empty:
        return data
    else:
        prediction_df = prediction_model.linear_regression(data, "close", days, "2020-12-15")
        return prediction_df


# Run all metrics on given company using current prediction system
def run_metrics(stock_code, days):
    df = make_predictions(stock_code, days,)
    if df.empty:
        return None, None
    else:
        pd.set_option('display.max_rows', None)
        future_predictions = df["2020-12-16 00:00:00":]
        scoreOne = metrics.metric1(future_predictions, stock_code)
        scoreTwo = metrics.metric2(future_predictions, stock_code)
        return scoreOne, scoreTwo


# Run metrics on predictions for number of days and store in CSV file
def test_all(days):
    companies = get_companies()
    now = datetime.now().strftime("%d-%m-%Y, %H-%M")
    file_name = "results/all/" + str(days) + "/" + now + ".csv"
    with open(file_name, "x") as f:
        fieldnames = ["stock_code", "short_hand", "sentences", "Mean Squared Error", "Median Absolute Error"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for company in companies:
            stock_code = company["stock_code"]
            short_hand = company["short_hand"]
            num_sent = get_sentence_amount(stock_code)

            # Sentences have been found for company
            if num_sent:
                scoreOne, scoreTwo = run_metrics(stock_code, days)
                if scoreOne:
                    writer.writerow({'stock_code': stock_code, 'short_hand': short_hand, 'sentences': num_sent,
                                 "Mean Squared Error": scoreOne, "Median Absolute Error": scoreTwo})
                    print(short_hand + " Analysed")
                else:
                    print(short_hand + "Company not listed")
            else:
                print(short_hand + " No Data")


# test metric for specific company and print to console
def test_company(stock_code, days):
    company = get_company(stock_code)
    if stock_code:
        num_sent = get_sentence_amount(stock_code)
        if num_sent:
            scoreOne, scoreTwo = run_metrics(stock_code, days)
            print("---" + stock_code + "---")
            print("Number of sentences:   " + str(num_sent))
            print("Mean Squared Error:    " + str(scoreOne))
            print("Median Absolute Error: " + str(scoreTwo))
        else:
            print("No data on company " + stock_code)
    else:
        print("Comapny with stock code" + stock_code + "does not exist in system")


if __name__ == '__main__':
    test_all(30)

