from django.urls import path

from .views import (
    LeadCreateView,
    LeadDeleteView,
    LeadDetailsView,
    LeadsListView,
    LeadUpdateView,
)

app_name = "leadsapp"

urlpatterns = [
    path("", LeadsListView.as_view(), name="leads_list"),
    path("new/", LeadCreateView.as_view(), name="leads_create"),
    path("<int:pk>/", LeadDetailsView.as_view(), name="leads_detail"),
    path("<int:pk>/edit/", LeadUpdateView.as_view(), name="leads_update"),
    path("<int:pk>/delete/", LeadDeleteView.as_view(), name="leads_delete"),
]
