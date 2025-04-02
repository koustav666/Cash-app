from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from payment.models import Profile


class RegisterForm(UserCreationForm):

    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(user=user, balance=self.cleaned_data.get("balance", 750))  # Ensure Profile is created
        return user