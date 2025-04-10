from datetime import datetime
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
import requests

from payment.models import Pay, Profile, RequestPayment
from timestampclient import get_remote_timestamp
from .forms import CheckTransaction, PaymentForm, RequestPaymentForm

@login_required
def promote_to_admin(request):
    if request.user.profile.admin:
        try:
            username = request.POST.get("username")
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            profile.admin = True
            profile.save()
            messages.success(request, f"{user.username} has been promoted to admin.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
    else:
        messages.error(request, "You are not authorized to perform this action.")

    return redirect('check_transaction')


@login_required
def pay_to_user(request):
    sent_transactions = []
    received_transactions = []
    admin_flag=request.user.profile.admin
    if request.method == "POST" :
        form = PaymentForm(request.POST)
        if request.POST.get("accept_request") == "true":
            request_id = request.POST.get("id")
            RequestPayment.objects.filter(id=request_id).delete()

        if form.is_valid():
            payee_username = form.cleaned_data.get('payee')
            amount = form.cleaned_data.get('amount')
            try:
                payee = User.objects.get(username=payee_username)
                payer = request.user

                if payee == payer:
                    messages.error(request, "You cannot request yourself.")
                    return redirect('pay_to_user')

                payer_profile = Profile.objects.get(user=payer)
                payee_profile = Profile.objects.get(user=payee)
                response = requests.get(f"http://localhost:8000/api/conversion/{payer_profile.currency.code}/{payee_profile.currency.code}/{amount}/")
                if response.status_code == 200:
                    data = response.json()
                    converted_amount = Decimal(data.get("converted_amount"))
                # Create a payment object but don't save yet
                payment = form.save(commit=False)
                payment.payer = payer
                payment.payee = payee
                payment.success = False

                if payer_profile.balance >= amount:
                    with transaction.atomic():
                        payer_profile.balance -= amount
                        payee_profile.balance += converted_amount
                        payer_profile.save()
                        payee_profile.save()
                        payment.timestamp = get_remote_timestamp()
                        payment.success = True
                        payment.save()
                    messages.success(request, f"Successfully paid {amount} to {payee_username}.")
                    return redirect('pay_to_user')
                elif amount <= 0:
                    messages.error(request, "Amount must be greater than zero.")
                else:
                    messages.error(request, "Insufficient balance.")

            except User.DoesNotExist:
                messages.error(request, "Payee does not exist.")

    else:
        form = PaymentForm()
        if request.POST.get("accept_request") == "false":
            request_id = request.GET.get("id")
            RequestPayment.objects.filter(id=request_id).delete()
        

    if request.user.is_authenticated:
        payment_requests=RequestPayment.objects.filter(payer=request.user)
        sent_transactions = Pay.objects.filter(payer=request.user)
        received_transactions = Pay.objects.filter(payee=request.user)
        for t in received_transactions:
            payer = User.objects.get(username=t.payer)
            if payer.profile.currency.code != request.user.profile.currency.code:
                response = requests.get(f"http://localhost:8000/api/conversion/{payer.profile.currency.code}/{request.user.profile.currency.code}/{t.amount}/")
                if response.status_code == 200:
                    data = response.json()
                    t.amount = data.get("converted_amount")
            

    return render(request, 'payment/payuser.html', {
        "form": form,
        "balance": request.user.profile.balance,
        "currency_code": request.user.profile.currency.code,
        "sent": sent_transactions,
        "receive": received_transactions,
        "flag": admin_flag,
        "payment_requests": payment_requests,
    })

@login_required
def check_transactions(request):
    if request.user.profile.admin == False:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('pay_to_user')
    
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
                payee_profile = Profile.objects.get(user=payee)
                sent = Pay.objects.filter(payer=payee.username)
                received = Pay.objects.filter(payee=payee.username)
                transactions = sent.union(received).order_by('-timestamp')
                for t in transactions:
                    payer = User.objects.get(username=t.payer)
                    if payer.profile.currency.code != payee_profile.currency.code:
                        response = requests.get(f"http://localhost:8000/api/conversion/{payer.profile.currency.code}/{payee_profile.currency.code}/{t.amount}/")
                        if response.status_code == 200:
                            data = response.json()
                            t.amount = Decimal(data.get("converted_amount"))
                response = requests.get(f"http://localhost:8000/api/conversion/{payee_profile.currency.code}/{currency.code}/1/")
                if response.status_code == 200:
                    data = response.json()
                    conversion_rate = data.get("conversion_rate")
                balance = (payee_profile.balance * Decimal(conversion_rate)).quantize(Decimal('0.01'))
                for t in transactions:
                    t.amount = (t.amount * Decimal(conversion_rate)).quantize(Decimal('0.01'))
            except User.DoesNotExist:
                messages.error(request, "Payee does not exist.")
                transactions = []
    
    return render(request, 'payment/checktransactions.html', {
        "transactions": transactions,
        "form": form,
        "currency_code": currency.code if currency else None,
        "balance": balance if 'balance' in locals() else None,
    })

@login_required
def request_payment(request):
    
    
    form = RequestPaymentForm()
    if request.method == "POST":
        form = RequestPaymentForm(request.POST)
        if form.is_valid():
            payer_username = form.cleaned_data.get('payer')
            amount = form.cleaned_data.get('amount')

            try:
                payer = User.objects.get(username=payer_username)
                if request.user == payer:
                    messages.error(request, "You cannot request yourself.")
                    return redirect('request_payment')
                elif amount <= 0:
                    messages.error(request, "Amount must be greater than zero.")
                    return redirect('request_payment')
                else:
                    payer_profile = Profile.objects.get(user=payer)
                    requester_profile = Profile.objects.get(user=request.user)
                    response = requests.get(f"http://localhost:8000/api/conversion/{requester_profile.currency.code}/{payer_profile.currency.code}/1/")
                    if response.status_code == 200:
                        data = response.json()
                        conversion_rate = data.get("conversion_rate")
                    request_payment = form.save(commit=False)
                    request_payment.requester = request.user
                    request_payment.payer = payer
                    request_payment.amount = amount * Decimal(conversion_rate)
                    request_payment.success = False
                    request_payment.timestamp = get_remote_timestamp()
                    request_payment.save()
                    messages.success(request, f"Payment request of {amount} sent to {payer_username}.")
                    return redirect('request_payment')
            except User.DoesNotExist:
                messages.error(request, "Payer does not exist.")

    return render(request, 'payment/request_payment.html', {
        "form": form,
        "currency_code": request.user.profile.currency.code
    })
