from django.shortcuts import render, redirect
from .forms import MemberForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def register_user(request):
    # If user submits the form on the website
    if request.method == "POST":
        form = MemberForm(request.POST or None)
        if form.is_valid():
            # Save the submitted data into our db
            form.save()
            messages.success(request, 'You have successfully registered!')
            return redirect('login')

    return render(request, 'register/register.html', {})


def login_user(request):
    return render(request, 'register/login.html', {})
