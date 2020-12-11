from django.shortcuts import render
from django.http import HttpResponse
from hotornot.models import Company
from django.template.loader import render_to_string



def index(request):
    ctx = {}
    url_parameter = request.GET.get("f")

    if url_parameter:
        companies = Company.objects.filter(short_hand__icontains=url_parameter)
    else:
        companies = Company.objects.all()

    if request.is_ajax():
        html = render_to_string(

        )

    return render(request, 'home.html', context={'companies': companies})


def company_page(request, stock_code):
    company = Company.objects.get(stock_code=stock_code)
    return render(request, 'company.html', context={'company': company})


