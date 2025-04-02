from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

from payment.models import Pay, Profile
from timestampclient import get_remote_timestamp
from .forms import CheckTransaction, PaymentForm

@login_required
def pay_to_user(request):
    sent_transactions = []
    received_transactions = []
    admin_flag=False
    if request.method == "POST" :
        form = PaymentForm(request.POST)
        if form.is_valid():
            payee_username = form.cleaned_data.get('payee')
            amount = form.cleaned_data.get('amount')

            try:
                payee = User.objects.get(username=payee_username)
                payer = request.user

                if payee == payer:
                    messages.error(request, "You cannot pay yourself.")
                    return redirect('pay_to_user')

                payer_profile = Profile.objects.get(user=payer)
                payee_profile = Profile.objects.get(user=payee)

                # Create a payment object but don't save yet
                payment = form.save(commit=False)
                payment.payer = payer
                payment.payee = payee
                payment.success = False

                if payer_profile.balance >= amount:
                    with transaction.atomic():
                        payer_profile.balance -= amount
                        payee_profile.balance += amount
                        payer_profile.save()
                        payee_profile.save()
                        payment.timestamp = get_remote_timestamp()
                        payment.success = True
                        payment.save()
                    messages.success(request, f"Successfully paid {amount} to {payee_username}.")
                    return redirect('pay_to_user')
                else:
                    messages.error(request, "Insufficient balance.")

            except User.DoesNotExist:
                messages.error(request, "Payee does not exist.")

    else:
        form = PaymentForm()

    # Fetch transaction history only when user is authenticated
    if request.user.is_authenticated:
        sent_transactions = Pay.objects.filter(payer=request.user)
        received_transactions = Pay.objects.filter(payee=request.user)

    return render(request, 'payment/payuser.html', {
        "form": form,
        "balance": request.user.profile.balance,
        "sent": sent_transactions,
        "receive": received_transactions,
        "flag": admin_flag
    })

@login_required
def check_transactions(request):
    transactions = []
    form = CheckTransaction()

    currency = None
    if request.method == "POST":
        form = CheckTransaction(request.POST)
        if form.is_valid():
            payee_username = form.cleaned_data.get('payee')
            currency = form.cleaned_data.get('currency')
            try:
                payee = User.objects.get(username=payee_username)
                sent = Pay.objects.filter(payer=payee)
                received = Pay.objects.filter(payee=payee)
                for t in sent.union(received).order_by('-timestamp'):
                    t.amount = t.amount * (1 if currency==None else currency.value)  # Convert amount
                    transactions.append(t)
            except User.DoesNotExist:
                transactions = []
    
    return render(request, 'payment/checktransactions.html', {
        "transactions": transactions,
        "form": form
    })
