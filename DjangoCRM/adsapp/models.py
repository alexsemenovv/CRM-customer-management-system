from django.db import models

from productapp.models import Product


class Ad(models.Model):
    """Сущность: рекламная компания"""
    name = models.CharField(max_length=100)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)  # услуга
    promotion_channel = models.CharField(max_length=100)  # канал продвижения
    advertising_budget = models.DecimalField(default=0, max_digits=8, decimal_places=2)
