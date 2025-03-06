from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView, UpdateView, DeleteView,
)

from .models import Product


class ProductsListView(ListView):
    """Список всех услуг"""
    template_name = "productapp/products_list.html"
    context_object_name = 'products'
    queryset = Product.objects.all()


class ProductCreateView(CreateView):
    """Создание новой услуги"""
    template_name = "productapp/products_create.html"
    model = Product
    fields = "name", "description", "price"
    success_url = reverse_lazy("productapp:products_list")


class ProductDetailsView(DetailView):
    """Просмотр деталей услуги"""
    template_name = "productapp/products_detail.html"
    model = Product


class ProductUpdateView(UpdateView):
    """Редактирование услуги"""
    template_name = "productapp/products_update.html"
    model = Product
    fields = ['name', 'description', 'price']

    def get_success_url(self):
        """После успешного обновления 'услуги' перенаправляемся на этот URL"""
        return reverse(
            "productapp:products_detail",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(DeleteView):
    """Удаление услуги"""
    template_name = "productapp/products_delete.html"
    model = Product
    success_url = reverse_lazy("productapp:products_list")
