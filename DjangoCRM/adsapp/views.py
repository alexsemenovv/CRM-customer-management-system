from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    DetailView, UpdateView, DeleteView,
)

from .models import Ad


class AdsListView(PermissionRequiredMixin, ListView):
    """Список всех рекламных компаний"""
    permission_required = "adsapp.view_ad"
    template_name = "adsapp/ads_list.html"
    context_object_name = 'ads'
    queryset = Ad.objects.prefetch_related('product').all()


class AdsCreateView(PermissionRequiredMixin, CreateView):
    """Создание рекламной компании"""
    permission_required = "adsapp.add_ad"
    template_name = "adsapp/ads_create.html"
    model = Ad
    fields = "name", "product", "promotion_channel", "advertising_budget"

    success_url = reverse_lazy("adsapp:ads_list")


class AdsDetailView(PermissionRequiredMixin, DetailView):
    """Просмотр деталей компании"""
    permission_required = "adsapp.view_ad"
    template_name = "adsapp/ads_detail.html"
    model = Ad


class AdsUpdateView(PermissionRequiredMixin, UpdateView):
    """Редактирование компании"""
    permission_required = "adsapp.change_ad"
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

class AdsDeleteView(PermissionRequiredMixin, DeleteView):
    """Удаление рекламной компании"""
    permission_required = "adsapp.delete_ad"
    template_name = "adsapp/ads_delete.html"
    model = Ad
    success_url = reverse_lazy("adsapp:ads_list")