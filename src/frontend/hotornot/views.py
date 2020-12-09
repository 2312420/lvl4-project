from django.shortcuts import render
from django.http import HttpResponse
from hotornot.models import Company


def index(request):
    companies = Company.objects.all()
    print(companies)
    return render(request, 'home.html', context={'companies': companies})
