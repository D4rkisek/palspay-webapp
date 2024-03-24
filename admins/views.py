from django.shortcuts import render
from django.contrib.auth import get_user_model

from register.models import Transaction


def admin_view(request):
    # View all members
    all_members = get_user_model().objects.select_related('account').all()

    # View all transactions
    all_transactions = Transaction.objects.all()

    return render(request, 'admins/admin.html', {'all_members': all_members, 'all_transactions': all_transactions})