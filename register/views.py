from django.shortcuts import render
from django.http import Http404

def register(request):
    return render(request, "register/register.html")

