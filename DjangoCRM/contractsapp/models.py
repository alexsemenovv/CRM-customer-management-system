from django.db import models

from productapp.models import Product


class Contract(models.Model):
    """Сущность: контракт для клиента"""
    title = models.CharField(max_length=200, verbose_name="Название контракта")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Предоставляемая услуга')
    document = models.FileField(null=True, upload_to='documents/contract/', verbose_name="Файл с документом")
    start_date = models.DateField(auto_now_add=True, verbose_name="Дата заключения")
    end_date = models.DateField(verbose_name="Период действия")
    cost = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='Сумма')
