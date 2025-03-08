from http.client import HTTPResponse

from django.db.models import Count, Sum, ExpressionWrapper, F, DecimalField
from django.http import HttpRequest
from django.shortcuts import render

from adsapp.models import Ad
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

    ads = Ad.objects.annotate(
        count_leads=Count('lead'),
        company_success=ExpressionWrapper(
            (Sum('product__contract__cost') - F('advertising_budget')),
            output_field=DecimalField()
        )
    )

    context = {
        "products": products,
        "ads": ads,
        "leads": leads,
        "customers": customers,
    }
    return render(request, "statisticsapp/index.html", context=context)
