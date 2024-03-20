from django.shortcuts import render
from register.models import Member


def admin(request):
    all_members = Member.objects.all
    return render(request, 'admins/admin.html', {'all': all_members})

