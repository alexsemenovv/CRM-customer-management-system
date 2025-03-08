from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    ListView, DetailView, UpdateView, DeleteView,
)

from .models import Contract
from .forms import ContractForm


class ContractListView(PermissionRequiredMixin, ListView):
    """Просмотр всех контрактов"""
    permission_required = "contractsapp.view_contract"
    template_name = "contractsapp/contracts_list.html"
    context_object_name = 'contracts'
    queryset = Contract.objects.prefetch_related('product').all()


class ContractCreateView(PermissionRequiredMixin, CreateView):
    """Создание контракта"""
    permission_required = "contractsapp.add_contract"
    template_name = "contractsapp/contracts_create.html"
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy("contractsapp:contracts_list")


class ContractDetailsView(PermissionRequiredMixin, DetailView):
    """Просмотр деталей контракта"""
    permission_required = "contractsapp.view_contract"
    template_name = "contractsapp/contracts_detail.html"
    model = Contract


class ContractUpdateView(PermissionRequiredMixin, UpdateView):
    """Редактирование контракта"""
    permission_required = "contractsapp.change_contract"
    template_name = "contractsapp/contracts_update.html"
    model = Contract
    form_class = ContractForm

    def get_success_url(self):
        """
        После успешного обновления 'контракта',
        перенаправляемся на этот URL
        """
        return reverse(
            "contractsapp:contracts_detail",
            kwargs={"pk": self.object.pk},
        )


class ContractDeleteView(PermissionRequiredMixin, DeleteView):
    """Удаление контракта"""
    permission_required = "contractsapp.delete_contract"
    template_name = "contractsapp/contracts_delete.html"
    model = Contract
    success_url = reverse_lazy("contractsapp:contracts_list")
