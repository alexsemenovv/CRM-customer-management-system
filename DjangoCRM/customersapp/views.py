from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Customer


class CustomerListView(ListView):
    """Просмотр всех активных клиентов"""
    template_name = "customersapp/customers_list.html"
    context_object_name = 'customers'
    queryset = Customer.objects.select_related('lead', 'contract').all()


class CustomerCreateView(CreateView):
    """Создание активного пользователя"""
    template_name = "customersapp/customers_create.html"
    model = Customer
    fields = "lead", "contract"
    success_url = reverse_lazy("customersapp:customers_list")


class CustomerDetailsView(DetailView):
    """Просмотр деталей активного пользователя"""
    template_name = "customersapp/customers_detail.html"
    model = Customer


class CustomerUpdateView(UpdateView):
    """Редактирование активного пользователя"""
    template_name = "customersapp/customers_update.html"
    model = Customer
    fields = "lead", "contract"

    def get_success_url(self):
        """
        После успешного обновления 'активного пользователя',
        перенаправляемся на этот URL
        """
        return reverse(
            "customersapp:customers_detail",
            kwargs={"pk": self.object.pk},
        )


class CustomerDeleteView(DeleteView):
    """Удаление активного пользователя"""
    template_name = "customersapp/customers_delete.html"
    model = Customer
    success_url = reverse_lazy("customersapp:customers_list")
