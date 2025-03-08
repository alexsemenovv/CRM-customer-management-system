from django.db import models

from productapp.models import Product


class Ad(models.Model):
    """Сущность: рекламная компания"""
    name = models.CharField(max_length=100, verbose_name="Название рекламной компании")
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Услуга")
    promotion_channel = models.CharField(max_length=100, verbose_name="Канал продвижения")
    advertising_budget = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name="Бюджет на рекламу")

    def __str__(self):
        return f"{self.name}"
