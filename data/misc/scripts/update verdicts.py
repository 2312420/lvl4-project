# Updates verdict for comapnies
import requests

base_url = "http://127.0.0.1:5000"
pred_url = "http://127.0.0.1:5004/" + "/predictions"


# Get all companies from db
def get_companies():
    url = base_url + "/company"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None


for company in get_companies():
    r = requests.get(url=pred_url, json=company)
    print(company['stock_code'], r.status_code)
    url = base_url + "/company/predictions"
    r = requests.post(url= url, json=r.json())
    print(company['stock_code'], r.status_code)