from django import forms

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
        fields = ['title', 'product', 'date_signed', 'valid_until', 'cost', 'document']
