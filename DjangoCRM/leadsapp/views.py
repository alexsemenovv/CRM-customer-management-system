from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Lead


class LeadsListView(PermissionRequiredMixin, ListView):
    """Список всех потенциальных пользователей"""

    permission_required = "leadsapp.view_lead"
    template_name = "leadsapp/leads_list.html"
    context_object_name = "leads"
    queryset = Lead.objects.prefetch_related("ad").all()


class LeadCreateView(PermissionRequiredMixin, CreateView):
    """Создание нового потенциального пользователя"""

    permission_required = "leadsapp.add_lead"
    template_name = "leadsapp/leads_create.html"
    model = Lead
    fields = "full_name", "phone_number", "email", "ad"
    success_url = reverse_lazy("leadsapp:leads_list")


class LeadDetailsView(PermissionRequiredMixin, DetailView):
    """Просмотр деталей потенциального пользователя"""

    permission_required = "leadsapp.view_lead"
    template_name = "leadsapp/leads_detail.html"
    model = Lead


class LeadUpdateView(PermissionRequiredMixin, UpdateView):
    """Редактирование потенциального пользователя"""

    permission_required = "leadsapp.change_lead"
    template_name = "leadsapp/leads_update.html"
    model = Lead
    fields = "full_name", "phone_number", "email", "ad"

    def get_success_url(self):
        """
        После успешного обновления 'потенциального пользователя',
        перенаправляемся на этот URL
        """
        return reverse(
            "leadsapp:leads_detail",
            kwargs={"pk": self.object.pk},
        )


class LeadDeleteView(PermissionRequiredMixin, DeleteView):
    """Удаление потенциального пользователя"""

    permission_required = "leadsapp.delete_lead"
    template_name = "leadsapp/leads_delete.html"
    model = Lead
    success_url = reverse_lazy("leadsapp:leads_list")
