from django.shortcuts import render, redirect
from django.http import Http404
from .forms import MemberForm
from django.contrib import messages

def register(request):
    # If user submits the form on the website
    if request.method == "POST":
        form = MemberForm(request.POST or None)
        if form.is_valid():
            # Save the submitted data into our db
            form.save()
            messages.success(request, 'You have successfully registered!')
            return redirect('login')
    else:
        return render(request, 'register/register.html', {})

def login(request):
    return render(request, 'register/login.html', {})
