from django.shortcuts import render
from django.http import HttpResponse
from hotornot.models import Company
from django.template.loader import render_to_string
from django.http import JsonResponse


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


def company_page(request, stock_code):
    company = Company.objects.get(stock_code=stock_code)
    return render(request, 'company.html', context={'company': company})


