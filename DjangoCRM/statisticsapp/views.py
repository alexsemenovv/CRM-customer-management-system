from http.client import HTTPResponse

from django.db.models import Count, Sum
from django.http import HttpRequest
from django.shortcuts import render

from adsapp.models import Ad
from contractsapp.models import Contract
from customersapp.models import Customer
from leadsapp.models import Lead
from productapp.models import Product


def get_statistics(request: HttpRequest) -> HTTPResponse:
    """
    Функция считает общую статистику:
    - Кол-во услуг
    - Кол-во рекламных компаний, а также кол-во лидов для каждой
    - Успешность каждой компании в %
    - Общее кол-во лидов
    - Общее кол-во активных клиентов
    """
    products = Product.objects.all()  # услуги
    leads = Lead.objects.annotate(count=Count("id"))  # потенциальные клиенты
    customers = Customer.objects.annotate(count=Count("id"))  # активные клиенты

    ads = Lead.objects.raw(
        """
        SELECT 
            aa.id,
            aa.name,
            COUNT(ll.id) as count_leads,
            (SUM(cc.cost) - aa.advertising_budget) / 100 as company_success
        FROM contractsapp_contract cc 
        JOIN productapp_product pp on pp.id = cc.product_id
        JOIN adsapp_ad aa on aa.product_id  = pp.id
        JOIN leadsapp_lead ll on ll.ad_id = aa.id
        GROUP BY aa.id
        """
    )

    context = {
        "products": products,
        "ads": ads,
        "leads": leads,
        "customers": customers,
    }
    return render(request, "statisticsapp/index.html", context=context)
