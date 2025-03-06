from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,

)

from .models import Lead


class LeadsListView(ListView):
    """Список всех потенциальных пользователей"""
    template_name = "leadsapp/leads_list.html"
    context_object_name = 'leads'
    queryset = Lead.objects.prefetch_related('ad').all()


class LeadCreateView(CreateView):
    """Создание нового потенциального пользователя"""
    template_name = "leadsapp/leads_create.html"
    model = Lead
    fields = "full_name", "phone_number", "email", "ad"
    success_url = reverse_lazy("leadsapp:leads_list")


class LeadDetailsView(DetailView):
    """Просмотр деталей потенциального пользователя"""
    template_name = "leadsapp/leads_detail.html"
    model = Lead


class LeadUpdateView(UpdateView):
    """Редактирование потенциального пользователя"""
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


class LeadDeleteView(DeleteView):
    """Удаление потенциального пользователя"""
    template_name = "leadsapp/leads_delete.html"
    model = Lead
    success_url = reverse_lazy("leadsapp:leads_list")
