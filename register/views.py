from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
from .models import Customer
import requests


@csrf_protect
def register_customer(request):
    if request.method == "POST":
        # Extracting form data
        username = request.POST.get('username')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        selected_currency = request.POST.get('currency')

        # Checking if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register-customer')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register-customer')

        # Creating the user
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password)  # Hash the pwd
        )

        # Fetching the "Customers" group and adding the user
        customers_group = Group.objects.get(name='Customers')
        customers_group.user_set.add(user)

        # Default balance in GBP
        balance = 1000.00
        # Attempt currency conversion if selected currency is not GBP
        if selected_currency != 'GBP':
            # Construct the URL for the GET request
            api_url = f"http://127.0.0.1:8000/conversion/GBP/{selected_currency}/1000/"
            response = requests.get(api_url)
            if response.status_code == 200:
                balance_data = response.json()
                balance = balance_data.get('converted_amount', 1000.00)  # Default to 1000 if conversion fails
            else:
                messages.error(request, 'Failed to convert currency.')
                return redirect('register-customer')

        # Creating an account for the user with the selected currency and balance
        Customer.objects.create(user=user, currency=selected_currency, balance=balance)

        messages.success(request, 'You have successfully registered!')
        return redirect('login-user')

    return render(request, 'register/register.html')


@csrf_protect
def login_user(request):
    # If user submits the form on the website
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["pwd"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user is in the Staff group
            if user.groups.filter(name='Staff').exists():
                return redirect('staff-homepage')  # Redirect to staff home page
            # Check if the user is in the Customers group
            elif user.groups.filter(name='Customers').exists():
                return redirect('customer-homepage')  # Redirect to members (customers) home page
        else:
            messages.error(request, "There was an error. Please try again.")
            return redirect('login-user')

    return render(request, 'register/login.html', {})
