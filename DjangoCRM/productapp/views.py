from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import Product


class ProductsListView(ListView):
    """Список всех услуг"""
    template_name = "productapp/products_list.html"
    context_object_name = 'products'
    queryset = Product.objects.all()


class ProductCreate(CreateView):
    """Создание новой услуги"""
    template_name = "productapp/products_form.html"
    model = Product
    fields = "name", "description", "price"
    success_url = reverse_lazy("productapp:products_list")
