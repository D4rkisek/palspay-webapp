from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from register.models import Customer, Transaction, MoneyRequest
from django.contrib import messages


@login_required
def member_view(request):
    # Retrieve the current user's data
    user_account = Customer.objects.get(user=request.user)
    user_history_transactions = Transaction.objects.filter(account=user_account).order_by('-date')

    # Pass the account details to the template context
    context = {
        'user': request.user,
        'account_balance': user_account.balance,
        'account_currency': user_account.currency,
        'transactions': user_history_transactions,
    }
    return render(request, 'customers/customer-home.html', context)


@login_required
def manage_requests(request):
    try:
        user_account = Customer.objects.get(user=request.user)
        pending_requests = MoneyRequest.objects.filter(recipient=user_account, is_accepted=False)
    except Customer.DoesNotExist:
        messages.error(request, "User account not found.")
        pending_requests = []
    return render(request, 'customers/customer-requests.html', {'pending_requests': pending_requests})