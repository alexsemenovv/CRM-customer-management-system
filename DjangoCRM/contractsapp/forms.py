from django import forms

from .models import Contract

class ContractForm(forms.ModelForm):
    """Форма для создания контракта"""
    start_date = forms.DateField(
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
        label="Дата заключения",
    )
    end_date = forms.DateField(
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
        label="Период действия",
    )

    class Meta:
        model = Contract
        fields = ['title', 'product', 'start_date', 'end_date', 'cost', 'document']
