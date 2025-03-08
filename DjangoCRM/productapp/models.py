from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(null=False, blank=True, verbose_name="Описание")
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name="Стоимость")

    def __str__(self):
        return f"{self.name}"
