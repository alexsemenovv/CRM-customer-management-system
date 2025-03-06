from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
)

from .models import Ad


class AdsListView(ListView):
    """Список всех рекламных компаний"""
    template_name = "adsapp/ads_list.html"
    context_object_name = 'ads'
    queryset = Ad.objects.prefetch_related('product').all()


class AdsCreateView(CreateView):
    """Создание рекламной компании"""
    template_name = "adsapp/ads_create.html"
    model = Ad
    fields = "name", "product", "promotion_channel", "advertising_budget"

    success_url = reverse_lazy("adsapp:ads_list")
