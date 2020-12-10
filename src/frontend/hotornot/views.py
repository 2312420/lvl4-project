from django.shortcuts import render
from django.http import HttpResponse
from hotornot.models import Company


def index(request):
    companies = Company.objects.all()
    print(companies)
    return render(request, 'home.html', context={'companies': companies})


def company_page(request, stock_code):
    company = Company.objects.get(stock_code=stock_code)
    return render(request, 'company.html', context={'company': company})