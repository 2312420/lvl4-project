# Django Imports
from django.shortcuts import render
from hotornot.models import Company
from django.template.loader import render_to_string
from django.http import JsonResponse

# Other Imports
from datetime import datetime
from datetime import timedelta
import requests
import yfinance as yf
from yahoo_fin import stock_info as si


# Home page view
def index(request):
    ctx = {}
    url_parameter = request.GET.get("q")
    sort_parameter = request.GET.get("s")

    if url_parameter:
        companies = Company.objects.filter(short_hand__icontains=url_parameter)
    else:
        companies = Company.objects.all()

    if sort_parameter != "Sort by":
        if sort_parameter == "HOT":
            companies = companies.order_by('verdict')
        else:
            companies = companies.order_by('-verdict')

    if request.is_ajax():

        html = render_to_string(
            template_name="homepage-results.html",
            context={'companies': companies}
        )

        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'home.html', context={'companies': companies})


# Company page view
def company_page(request, stock_code):
    # Company DB data
    company = Company.objects.get(stock_code=stock_code)
    stock_data = yf.Ticker(stock_code)

    #Code for Custom predictions
    cus_labels = cus_prices = cus_pred_labels = cus_pred_price = None
    if request.method == "POST":
        dict = request.POST
        start = "2020-12-10" #dict['startdate']
        end = "2020-12-24" #dict['enddate']

        if start and end:
            url = "http://127.0.0.1:5004/predictions/custom"
            payload = {
                "start_date": start,
                "end_date": end,
                "stock_code": stock_code
            }
            r = requests.post(url, json=payload)
            if r.status_code == 200:

                # Formatting predicted data
                content = r.json()
                cus_labels = []
                cus_prices = []
                cus_pred_labels = []
                cus_pred_price = []

                for item in r.json():
                    cus_pred_labels.append(item[0])
                    cus_pred_price.append(item[1])

                # Getting historical Info
                stock_df = stock_data.history(start=datetime.strptime(start, "%Y-%m-%d"), end=datetime.strptime(end, "%Y-%m-%d"))
                for item in stock_df.index.to_list():
                    time = datetime.strptime(str(item), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                    cus_labels.append(time)
                cus_prices = stock_df['Close'].to_list()

        else:
            print("NOT VALID")


    # Updates live stock price
    if request.is_ajax():
        # Company Current Price data
        current_price = round(si.get_live_price(stock_code), 2)

        info = si.get_quote_table(stock_code)
        cur_diff = round(current_price - info['Previous Close'], 2)
        cur_per = round(cur_diff / info['Previous Close'] * 100, 2)

        pos = False
        if cur_diff > 0:
            cur_diff = "+" + str(cur_diff)
            cur_per = "(+" + str(cur_per) + "%)"
            pos = True
        else:
            cur_diff = str(cur_diff)
            cur_per = "(" + str(cur_per) + "%)"

        html = render_to_string(
            template_name="company-price-ticker.html",
            context={'current_data': {'price': current_price,
                                      'diff': cur_diff,
                                      'per': cur_per,
                                      'pos': pos}}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    # Historical stock Information
    stock_df = stock_data.history(start=(datetime.now() - timedelta(days=50)), end=datetime.now())

    close_labels = []
    pred_labels = []
    for item in stock_df.index.to_list():
        time = datetime.strptime(str(item), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        close_labels.append(time)

    close_prices = stock_df['Close'].to_list()
    pred_prices = stock_df['Close'].to_list()


    # Getting premade company predictions
    predictions = company.predictions
    import pandas
    df = pandas.DataFrame(predictions)

    for i, item in df.iterrows():
        if item[0] in close_labels:
            preds = df.iloc[i:]
            break

    pred_prices = []
    pred_labels = []
    for index, item in preds.iterrows():
        pred_labels.append(item[0])
        pred_prices.append(item[1])

    return render(request, 'company.html', context={'company': company,
                                                    'close_data':   {'labels':  close_labels,
                                                                     'prices':  close_prices},
                                                    'pred_data':    {'prices':  pred_prices,
                                                                     'labels': pred_labels},
                                                    'current_data': {'pos': "NONE"},
                                                    'custom_close': {'prices': cus_prices,
                                                                     'labels': cus_labels,},
                                                    'custom_pred': {'prices': cus_pred_price,
                                                                    'labels': cus_pred_labels}
                                                    })


def redirect(request):
    return redirect('/hotornot/')




