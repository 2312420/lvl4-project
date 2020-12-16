# Used for testing predictions

# Imports
import requests

# Urls
prediction_url = "http://127.0.0.1:5004/"
base_url = "http://127.0.0.1:5000"


# Get all companies from db
def get_companies():
    url = base_url + "/company"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None


def run_predictions():
    for company in get_companies():
        r = requests.get()


def squared_loss(company):
    predictions = company['predictions']
    for point in predictions:
        print(point)

if __name__ == '__main__':
    for company in get_companies():
        print(company['short_hand'])
        squared_loss(company)
        break