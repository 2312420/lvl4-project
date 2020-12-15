from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<str:stock_code>', views.company_page, name='company_page')
]