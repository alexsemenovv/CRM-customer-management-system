from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    ListView, DetailView, UpdateView,
)

from .models import Contract
from .forms import ContractForm


class ContractListView(ListView):
    """Просмотр всех контрактов"""
    template_name = "contractsapp/contracts_list.html"
    context_object_name = 'contracts'
    queryset = Contract.objects.prefetch_related('product').all()


class ContractCreateView(CreateView):
    """Создание контракта"""
    template_name = "contractsapp/contracts_create.html"
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy("contractsapp:contracts_list")


class ContractDetailsView(DetailView):
    """Просмотр деталей контракта"""
    template_name = "contractsapp/contracts_detail.html"
    model = Contract


class ContractUpdateView(UpdateView):
    """Редактирование контракта"""
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
