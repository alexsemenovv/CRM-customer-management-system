from django.db import models

from contractsapp.models import Contract
from leadsapp.models import Lead


class Customer(models.Model):
    """Сущность: активный клиент"""
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, verbose_name="Потенциальный клиент")
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, verbose_name="Контракт")

    def __str__(self):
        return self.lead
