from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from register.models import Account, Transaction
from .forms import TransferMoneyForm
from django.db import transaction as db_transaction
from django.core.exceptions import ObjectDoesNotExist


@login_required
def transfer_money(request):
    if request.method == 'POST':
        form = TransferMoneyForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['username']
            amount = form.cleaned_data['amount']
            try:
                with db_transaction.atomic():
                    # Attempt to fetch sender's account safely
                    try:
                        sender_account = Account.objects.get(user=request.user)
                    except Account.DoesNotExist:
                        messages.error(request, 'Sender account not found.')
                        return redirect('transfer-money')

                    # Attempt to fetch recipient's account safely
                    try:
                        recipient_account = Account.objects.get(user__username=recipient_username)
                    except Account.DoesNotExist:
                        messages.error(request, 'Recipient account not found.')
                        return redirect('transfer-money')

                    if sender_account.balance < amount:
                        messages.error(request, 'Insufficient funds.')
                        return redirect('transfer-money')

                    sender_account.balance -= amount
                    sender_account.save()

                    recipient_account.balance += amount
                    recipient_account.save()

                    # Log the transaction for both sender and recipient
                    Transaction.objects.create(account=sender_account, amount=-amount, transaction_type='payment', description=f"Sent to {recipient_username}")
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='payment', description=f"Received from {request.user.username}")

                    messages.success(request, 'Transfer successful.')
                    return redirect('transfer-money')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        form = TransferMoneyForm()

    return render(request, 'members/transfer-money.html', {'form': form})