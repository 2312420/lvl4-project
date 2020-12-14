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
    company = Company.objects.get(stock_code=stock_code)

    current_price = round(si.get_live_price(stock_code), 2)
    print(current_price)

    if request.is_ajax():
        print("!")
        html = render_to_string(
            template_name="company-price-ticker.html",
            context={'current_data': {'price': current_price}}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    ## Stock Information
    stock_data = yf.Ticker(stock_code)
    stock_df = stock_data.history(start=(datetime.now() - timedelta(days=20)), end=datetime.now())

    close_labels = []
    for item in stock_df.index.to_list():
        close_labels.append(datetime.strptime(str(item), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))
    close_prices = stock_df['Close'].to_list()


    return render(request, 'company.html', context={'company': company,
                                                    'close_data':   {'labels': close_labels,
                                                                     'prices': close_prices},
                                                    'current_data': {'price': current_price }
                                                    })


def redirect(request):
    return redirect('/hotornot/')
