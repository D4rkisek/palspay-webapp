from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from .models import Customer


def register_customer(request):
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
            return redirect('register-customer')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register-customer')

        # Creating the user
        user = User.objects.create_user(    # Use 'create.user()' to hash the password
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()

        # Fetching the "Customers" group
        customers_group = Group.objects.get(name='Customers')
        # Adding the user to the "Customers" group
        customers_group.user_set.add(user)

        # Creating an account for the user
        Customer.objects.create(user=user)

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
            # Check if the user is in the Staff group
            if user.groups.filter(name='Staff').exists():
                return redirect('staff-homepage')  # Redirect to staff home page
            # Check if the user is in the Customers group
            elif user.groups.filter(name='Customers').exists():
                return redirect('members-homepage')  # Redirect to members (customers) home page
            else:
                # Handle users who are neither Staff nor Customers
                return redirect('default-home-page')  # Redirect to a default home page
        else:
            messages.error(request, "There was an error, please try again.")
            return redirect('login-user')

    return render(request, 'register/login.html', {})