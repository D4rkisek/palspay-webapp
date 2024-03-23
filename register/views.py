from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Account


def register_user(request):
    if request.method == "POST":
        # Extracting form data
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pwd']

        # Checking if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register-user')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register-user')

        # Creating the user
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password)  # Hashes the password
        )
        user.save()

        # Creating an account for the user
        Account.objects.create(user=user)

        messages.success(request, 'You have successfully registered!')
        return redirect('login-user')

    return render(request, 'register/register.html')


def login_user(request):
    # If user submits the form on the website
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["pwd"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('members-home-page')
        else:
            messages.success(request, "There was an error, please try again.")
            return redirect('login-user')

    return render(request, 'register/login.html', {})
