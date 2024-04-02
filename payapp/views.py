from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from register.models import Customer, Transaction, MoneyRequest
from .forms import TransferMoneyForm
from django.db import transaction as db_transaction
from django.utils import timezone
import requests


@login_required
def transfer_money(request):
    if request.method == 'POST':
        form = TransferMoneyForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['username']
            amount = form.cleaned_data['amount']
            try:
                with db_transaction.atomic():
                    # Fetch sender and recipient accounts
                    sender_account = Customer.objects.get(user=request.user)
                    recipient_account = Customer.objects.get(user__username=recipient_username)

                    if sender_account.balance < amount:
                        messages.error(request, 'Insufficient funds.')
                        return redirect('transfer-money')

                    # Convert the amount if currencies differ
                    converted_amount = Decimal(amount)  # Ensure amount is a Decimal for consistency
                    if sender_account.currency != recipient_account.currency:
                        conversion_url = f"http://127.0.0.1:8000/conversion/{sender_account.currency}/{recipient_account.currency}/{amount}"
                        response = requests.get(conversion_url)
                        if response.status_code == 200:
                            # Convert the API response to Decimal before arithmetic operations
                            converted_amount = Decimal(response.json().get('converted_amount'))
                        else:
                            messages.error(request, 'Currency conversion failed.')
                            return redirect('transfer-money')

                    # Perform the transfer
                    sender_account.balance -= Decimal(amount)  # Convert amount to Decimal
                    sender_account.save()

                    recipient_account.balance += converted_amount  # converted_amount is already a Decimal
                    recipient_account.save()

                    # Log the transactions
                    Transaction.objects.create(
                        account=sender_account, amount=-Decimal(amount), transaction_type='payment',
                        description=f"Sent to {recipient_username}"
                    )
                    Transaction.objects.create(
                        account=recipient_account, amount=converted_amount, transaction_type='payment',
                        description=f"Received from {request.user.username}"
                    )

                    messages.success(request, 'Transfer successful.')
                    return redirect('transfer-money')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        form = TransferMoneyForm()

    return render(request, 'customers/transfer-money.html', {'form': form})


@login_required
def request_money(request):
    if request.method == 'POST':
        form = TransferMoneyForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['username']
            amount = form.cleaned_data['amount']
            try:
                sender_account = Customer.objects.get(user=request.user)
                recipient_account = Customer.objects.get(user__username=recipient_username)
                MoneyRequest.objects.create(sender=sender_account, recipient=recipient_account, amount=amount)
                messages.success(request, 'Request sent successfully.')
                return redirect('request-money')
            except Customer.DoesNotExist:
                messages.error(request, 'Account not found.')
    else:
        form = TransferMoneyForm()
    return render(request, 'customers/request-money.html', {'form': form})


@login_required
def respond_to_request(request):
    if request.method == 'POST':
        money_request_id = request.POST.get('money_request_id')
        response_action = request.POST.get('response')

        money_request = get_object_or_404(MoneyRequest, id=money_request_id, recipient__user=request.user)

        if response_action == 'Accept':
            try:
                with db_transaction.atomic():
                    # Fetch accounts
                    sender_account = money_request.sender
                    recipient_account = money_request.recipient

                    # Check if sender has sufficient balance
                    if sender_account.balance < money_request.amount:
                        messages.error(request, 'Your account has insufficient funds.')
                        return redirect('manage-requests')

                    # Perform transaction
                    sender_account.balance -= money_request.amount
                    sender_account.save()

                    recipient_account.balance += money_request.amount
                    recipient_account.save()

                    # Log transaction for sender and recipient
                    Transaction.objects.create(
                        account=sender_account,
                        amount=-money_request.amount,
                        transaction_type='payment',
                        description=f"Sent to {recipient_account.user.username}"
                    )
                    Transaction.objects.create(
                        account=recipient_account,
                        amount=money_request.amount,
                        transaction_type='payment',
                        description=f"Received from {sender_account.user.username}"
                    )

                    # Update money request status
                    money_request.is_accepted = True
                    money_request.date_responded = timezone.now()
                    money_request.save()

                    messages.success(request, 'Request accepted and money transferred.')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect('manage-requests')

        elif response_action == 'Reject':
            money_request.delete()
            messages.info(request, 'Request rejected.')
            return redirect('manage-requests')

    # Handle GET request
    pending_requests = MoneyRequest.objects.filter(recipient__user=request.user, is_accepted=False)
    return render(request, 'customers/customer-requests.html', {'pending_requests': pending_requests})
