from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView


class ProductCreate(CreateView):
    """Создание новой услуги"""
    fields = "name", "description", "price"
    success_url = reverse_lazy("productapp:products_list")
