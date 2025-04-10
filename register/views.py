from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from payment.models import Currency, Profile
from register.forms import RegisterForm
from django.contrib.auth import authenticate, login as auth_login, logout

def register(request):
    if request.user.is_authenticated:
        return redirect("pay_to_user")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        currency_code = request.POST.get("Currency")
        currency = Currency.objects.get(code=currency_code)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            try:
                response = requests.get(f"http://localhost:8000/api/conversion/GBP/{currency}/750/")
                if response.status_code == 200:
                    data = response.json()
                    balance = data.get("converted_amount")
                else:
                    balance = 750
            except Exception as e:
                print("Currency conversion failed:", e)
                balance = 750
            Profile.objects.create(
                user=user,
                currency=currency,
                balance=balance,
                admin=False
            )
            messages.success(request, "Your account has been created. You can log in now!")
            return redirect("login_view")
        else:
            messages.error(request, "Saving user failed")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form, "currencys": ["USD", "EUR", "GBP"]})  # Added currencies for the template

def login_view(request):
    if request.user.is_authenticated:
        return redirect("pay_to_user") 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If the user is authenticated, log them in
            auth_login(request, user)
            return redirect('pay_to_user')  # Redirect to home page after login (adjust if needed)
        else:
            # If the user doesn't exist, redirect to registration page
            messages.error(request, "User not found. Please register first.")
            return redirect('register')  # Replace with your registration page URL

    else:
        return render(request, 'login/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login_view')