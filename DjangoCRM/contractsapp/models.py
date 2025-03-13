from django.db import models
from productapp.models import Product


class Contract(models.Model):
    """Сущность: контракт для клиента"""

    title = models.CharField(max_length=200, verbose_name="Название контракта")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Предоставляемая услуга"
    )
    document = models.FileField(
        null=True, upload_to="documents/", verbose_name="Файл с документом"
    )
    date_signed = models.DateField(
        null=True, blank=True, verbose_name="Дата заключения"
    )
    valid_until = models.DateField(
        null=True, blank=True, verbose_name="Период действия"
    )
    cost = models.DecimalField(
        default=0, max_digits=8, decimal_places=2, verbose_name="Сумма"
    )

    def __str__(self):
        return self.title
