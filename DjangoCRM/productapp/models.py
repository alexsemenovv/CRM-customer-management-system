from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Услуга: {self.name}\nОписание: {self.description}\nСтоимость: {self.price}"
