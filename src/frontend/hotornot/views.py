# Django Imports
from django.shortcuts import render
from hotornot.models import Company
from django.template.loader import render_to_string
from django.http import JsonResponse

# Other Imports
from datetime import datetime
from datetime import timedelta
import yfinance as yf
from yahoo_fin import stock_info as si


# Home page view
def index(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        print("-")
        companies = Company.objects.filter(short_hand__icontains=url_parameter)
    else:
        companies = Company.objects.all()

    if request.is_ajax():
        print("!")
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

    if request.is_ajax():
        # Company Current Price data
        current_price = round(si.get_live_price(stock_code), 2)

        info = si.get_quote_table(stock_code)
        cur_diff = round(current_price - info['Previous Close'], 2)
        cur_per = round(cur_diff / info['Previous Close'] * 100, 2)

        pos = False
        if cur_diff > 0:
            cur_diff = "+" + str(cur_diff)
            cur_per = "(+" + str(cur_per) + ")"
            pos = True

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
    stock_data = yf.Ticker(stock_code)
    stock_df = stock_data.history(start=(datetime.now() - timedelta(days=50)), end=datetime.now())

    close_labels = []
    pred_labels = []
    for item in stock_df.index.to_list():
        time = datetime.strptime(str(item), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        close_labels.append(time)
        pred_labels.append(time)

    close_prices = stock_df['Close'].to_list()
    pred_prices = stock_df['Close'].to_list()
    for item in company.predictions:
        close_labels.append(item[0])
        pred_prices.append(item[1])

    return render(request, 'company.html', context={'company': company,
                                                    'close_data':   {'labels':  close_labels,
                                                                     'prices':  close_prices},
                                                    'pred_data':    {'prices':  pred_prices},
                                                    'current_data': {'pos': "NONE"}
                                                    })


def redirect(request):
    return redirect('/hotornot/')
