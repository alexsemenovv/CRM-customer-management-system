from django.db import models

from contractsapp.models import Contract
from leadsapp.models import Lead


class Customer(models.Model):
    """Сущность: активный клиент"""
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE)
