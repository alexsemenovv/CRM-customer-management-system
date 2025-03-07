from http.client import HTTPResponse

from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render

from adsapp.models import Ad
from contractsapp.models import Contract
from customersapp.models import Customer
from leadsapp.models import Lead
from productapp.models import Product


def get_statistics(request: HttpRequest) -> HTTPResponse:
    """Функция считает общую статистику"""
    products = Product.objects.all()  # услуги
    leads = Lead.objects.annotate(count=Count("id"))  # потенциальные клиенты
    customers = Customer.objects.annotate(count=Count("id"))  # активные клиенты
    ads = Lead.objects.raw(
        """
        select aa.id, aa.name, COUNT(ll.id) as count
        from leadsapp_lead ll 
        JOIN adsapp_ad aa on aa.id = ll.ad_id
        GROUP BY aa.id
        """
    )
    print(customers)

    context = {
        "products": products,
        "ads": ads,
        "leads": leads,
        "customers": customers,
    }
    return render(request, "statisticsapp/index.html", context=context)

# TODO
#  число клиентов, перешедших из потенциальных в активных;
#  соотношение дохода от контрактов и расходов на рекламу.
