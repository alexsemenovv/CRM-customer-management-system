from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ContractForm
from .models import Contract


class ContractListView(PermissionRequiredMixin, ListView):
    """Просмотр всех контрактов"""

    permission_required = "contractsapp.view_contract"
    template_name = "contractsapp/contracts_list.html"
    context_object_name = "contracts"
    queryset = Contract.objects.prefetch_related("product").all()


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
