from django import forms
from django.contrib.auth.models import User
from payment.models import Currency, Pay, RequestPayment


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
        required=True,
        label="Select currency",
        widget=forms.Select(attrs={"class": "form-control"}),
        to_field_name="code"
    )

class RequestPaymentForm(forms.ModelForm):

    class Meta:
        model = RequestPayment
        fields = ['payer','amount']