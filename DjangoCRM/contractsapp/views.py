from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
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
    # fields = "title", "product", "document", "end_date", "cost"
    success_url = reverse_lazy("contractsapp:contracts_list")
