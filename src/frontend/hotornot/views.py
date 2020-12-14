# Django Imports
from django.shortcuts import render
from hotornot.models import Company
from django.template.loader import render_to_string
from django.http import JsonResponse

# Other Imports
from datetime import datetime
from datetime import timedelta
import yfinance as yf
import json

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



import pickle

# Company page view
def company_page(request, stock_code):
    company = Company.objects.get(stock_code=stock_code)

    stock_data = yf.Ticker(stock_code)
    stock_df = stock_data.history(start=(datetime.now() - timedelta(days=20)), end=datetime.now())

    labels = []
    for item in stock_df.index.to_list():
        labels.append(datetime.strptime(str(item), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'))

    close = stock_df['Close'].to_list()

    test = ['1','2']
    return render(request, 'company.html', context={'company': company, 'labels': labels, 'close': close, 'data': [1, 2, 3, 4, 5]})


def redirect(request):
    return redirect('/hotornot/')
