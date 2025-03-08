from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView, UpdateView, DeleteView,
)

from .models import Product


class ProductsListView(PermissionRequiredMixin, ListView):
    """Список всех услуг"""
    permission_required = "productapp.view_product"
    template_name = "productapp/products_list.html"
    context_object_name = 'products'
    queryset = Product.objects.all()


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """Создание новой услуги"""
    permission_required = "productapp.add_product"
    template_name = "productapp/products_create.html"
    model = Product
    fields = "name", "description", "price"
    success_url = reverse_lazy("productapp:products_list")


class ProductDetailsView(PermissionRequiredMixin, DetailView):
    """Просмотр деталей услуги"""
    permission_required = "productapp.view_product"
    template_name = "productapp/products_detail.html"
    model = Product


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    """Редактирование услуги"""
    permission_required = "productapp.change_product"
    template_name = "productapp/products_update.html"
    model = Product
    fields = ['name', 'description', 'price']

    def get_success_url(self):
        """После успешного обновления 'услуги' перенаправляемся на этот URL"""
        return reverse(
            "productapp:products_detail",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    """Удаление услуги"""
    permission_required = "productapp.delete_product"
    template_name = "productapp/products_delete.html"
    model = Product
    success_url = reverse_lazy("productapp:products_list")
