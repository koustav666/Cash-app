from django import forms
from django.contrib.auth.models import User
from payment.models import Currency, Pay


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Pay
        fields = ['payee','amount']

class CheckTransaction(forms.Form):
    payee = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label="Select a user",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        required=False,
        label="Switch currency",
        widget=forms.Select(attrs={"class": "form-control"}),
        to_field_name="code"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default currency to GBP if it's available
        if not self.initial.get('currency'):
            self.initial['currency'] = Currency.objects.get(code="GBP")

