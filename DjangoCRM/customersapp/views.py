from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from leadsapp.models import Lead
from .models import Customer


class CustomerListView(PermissionRequiredMixin, ListView):
    """Просмотр всех активных клиентов"""
    permission_required = "customersapp.view_customer"
    template_name = "customersapp/customers_list.html"
    context_object_name = 'customers'
    queryset = Customer.objects.select_related('lead', 'contract').all()


class CustomerCreateView(PermissionRequiredMixin, CreateView):
    """Создание активного пользователя"""
    permission_required = "customersapp.add_customer"
    template_name = "customersapp/customers_create.html"
    model = Customer
    fields = "lead", "contract"
    success_url = reverse_lazy("customersapp:customers_list")

    def get_initial(self):
        """Предзаполняет поле 'lead' при создании нового клиента"""
        initial = super().get_initial()
        lead_id = self.request.GET.get("lead_id")  # Получаем lead_id из URL
        if lead_id:
            lead = get_object_or_404(Lead, pk=lead_id)
            initial["lead"] = lead
        return initial


class CustomerDetailsView(PermissionRequiredMixin, DetailView):
    """Просмотр деталей активного пользователя"""
    permission_required = "customersapp.view_customer"
    template_name = "customersapp/customers_detail.html"
    model = Customer


class CustomerUpdateView(PermissionRequiredMixin, UpdateView):
    """Редактирование активного пользователя"""
    permission_required = "customersapp.change_customer"
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


class CustomerDeleteView(PermissionRequiredMixin, DeleteView):
    """Удаление активного пользователя"""
    permission_required = "customersapp.delete_customer"
    template_name = "customersapp/customers_delete.html"
    model = Customer
    success_url = reverse_lazy("customersapp:customers_list")
