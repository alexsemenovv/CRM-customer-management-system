from django.urls import path

from .views import (
    ContractListView,
    ContractCreateView,
    ContractDetailsView,
    ContractUpdateView,
)

app_name = 'contractsapp'

urlpatterns = [
    path('', ContractListView.as_view(), name='contracts_list'),
    path('new/', ContractCreateView.as_view(), name='contracts_create'),
    path('<int:pk>/', ContractDetailsView.as_view(), name='contracts_detail'),
    path('<int:pk>/edit/', ContractUpdateView.as_view(), name='contracts_update'),
]
