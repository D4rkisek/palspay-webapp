from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from register.models import Account


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
def member_transactions(request, username):
    # Ensure the logged-in user is accessing only their transactions
    if request.user.username != username:
        return render(request, 'errors/forbidden.html', status=403)

    # Retrieve the current user's account
    user_account = Account.objects.get(user=request.user)

    # Pass the account details to the template context
    context = {
        'user': request.user,
        'account_balance': user_account.balance,
        'account_currency': user_account.currency,
    }
    return render(request, 'members/member-transactions.html', context)


def get_user_transactions(username):
    return []