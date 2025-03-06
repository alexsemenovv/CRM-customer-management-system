from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    DetailView, UpdateView,
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


class AdsDetailView(DetailView):
    """Просмотр деталей компании"""
    template_name = "adsapp/ads_detail.html"
    model = Ad


class AdsUpdateView(UpdateView):
    """Редактирование компании"""
    template_name = "adsapp/ads_update.html"
    model = Ad
    fields = "name", "product", "promotion_channel", "advertising_budget"

    def get_success_url(self):
        """
        В случае успешного обновления,
        происходит перенаправление на страницу с деталями компании
        """
        return reverse(
            "adsapp:ads_detail",
            kwargs={"pk": self.object.pk},
        )
