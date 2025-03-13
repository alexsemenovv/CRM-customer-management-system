from django import forms
from django.core.exceptions import ValidationError

from .models import Contract


class ContractForm(forms.ModelForm):
    """Форма для создания контракта"""

    date_signed = forms.DateField(
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
        label="Дата заключения",
    )
    valid_until = forms.DateField(
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
        label="Период действия",
    )

    class Meta:
        model = Contract
        fields = ["title", "product", "date_signed", "valid_until", "cost", "document"]

    def clean(self):
        """Метод для проверки дат"""
        cleaned_data = super().clean()
        date_signed = cleaned_data.get("date_signed")  # дата подписания
        valid_until = cleaned_data.get("valid_until")  # дата окончания

        if date_signed and valid_until:
            if (
                valid_until < date_signed
            ):  # Если дата подписания больше, чем дата окончания, то выкидываем ошибку
                raise ValidationError(
                    "Период действия не может быть меньше даты заключения контракта."
                )

        return cleaned_data
