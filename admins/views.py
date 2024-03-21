from django.shortcuts import render
from django.contrib.auth import get_user_model


def admin_view(request):
    all_members = get_user_model().objects.all()
    return render(request, 'admins/admin.html', {'all_members': all_members})