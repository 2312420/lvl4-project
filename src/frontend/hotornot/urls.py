from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('company/<str:stock_code>', views.company_page, name='company_page'),
    path('HowItWorks', views.how_it_works, name='how_it_works'),
    path('About', views.about, name='about')
]