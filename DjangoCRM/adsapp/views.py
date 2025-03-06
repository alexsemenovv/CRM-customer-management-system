from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
)

from .models import Ad


class AdsListView(ListView):
    """Список всех рекламных компаний"""
    template_name = "adsapp/ads_list.html"
    context_object_name = 'ads'
    queryset = Ad.objects.prefetch_related('Product').all()

