from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from register.models import Account, MoneyRequest
from django.contrib import messages


@login_required
def member_view(request):
    # Retrieve the current user's account
    user_account = Account.objects.get(user=request.user)

    # Pass the account details to the template context
    context = {
        'user': request.user,
        'account_balance': user_account.balance,
        'account_currency': user_account.currency,
    }
    return render(request, 'members/member-home.html', context)


@login_required
def manage_requests(request):
    try:
        user_account = Account.objects.get(user=request.user)
        pending_requests = MoneyRequest.objects.filter(recipient=user_account, is_accepted=False)
    except Account.DoesNotExist:
        messages.error(request, "User account not found.")
        pending_requests = []
    return render(request, 'members/manage-requests.html', {'pending_requests': pending_requests})