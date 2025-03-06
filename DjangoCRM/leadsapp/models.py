from django.db import models

from adsapp.models import Ad


class Lead(models.Model):
    """Сущность: потенциальный клиент"""
    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О.")
    phone_number = models.CharField(max_length=12, verbose_name="Телефон")
    email = models.EmailField(unique=True, verbose_name="Email")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

