from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from register.models import Staff, Transaction


def staff_view(request):
    # View all members
    all_members = get_user_model().objects.select_related('customer').all()

    # View all transactions
    all_transactions = Transaction.objects.all()

    return render(request, 'staff/staff.html', {'all_members': all_members, 'all_transactions': all_transactions})


def register_staff(request):
    if request.method == "POST":
        # Extracting form data
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pwd']

        # Checking if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register-customer')

        # Creating the user
        user_admin = User.objects.create_user(    # Use 'create.user()' to hash the password
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user_admin.save()

        # Fetching the "Staff" group
        staff_group = Group.objects.get(name='Staff')
        # Adding the user to the "Staff" group
        staff_group.user_set.add(user_admin)

        # Creating an account for the user
        Staff.objects.create(user=user_admin)

        messages.success(request, 'You have successfully registered a Staff Member!')
        return redirect('login-user')


    return render(request, 'staff/registerstaff.html', {})
