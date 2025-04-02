from django.shortcuts import render, redirect
from django.contrib import messages
from register.forms import RegisterForm
from django.contrib.auth import authenticate, login as auth_login, logout

def register(request):
    if request.method == "POST":  # Corrected
        form = RegisterForm(request.POST)
        if form.is_valid():  # Corrected
            form.save()
            messages.success(request, "Your account has been created. You can log in now!")
            return redirect("login_view")
        else:
            messages.error(request, "Saving user failed")
    else:
        form = RegisterForm()  # Ensure form is always defined

    return render(request, "register/register.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
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
    logout(request)
    return redirect('login_view')