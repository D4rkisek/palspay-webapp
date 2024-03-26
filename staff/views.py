from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from register.models import Staff, Transaction
from django.contrib.auth.decorators import login_required


@login_required
def staff_view(request):
    # If the individual is not a staff member
    if not request.user.groups.filter(name='Staff').exists():
        return HttpResponse("You are not authorized to view this page.")

    # Get the staff group
    staff_group = Group.objects.get(name='Staff')

    # View all members that are not in the 'Staff' group and not superusers
    # This excludes both staff members and superusers
    all_members = get_user_model().objects.exclude(groups=staff_group).exclude(is_superuser=True).select_related('account').all()

    # View all transactions
    all_transactions = Transaction.objects.all()

    return render(request, 'staff/staff.html', {'all_members': all_members, 'all_transactions': all_transactions})


@login_required
def register_staff(request):
    # If the individual is not a staff member
    if not request.user.groups.filter(name='Staff').exists():
        return HttpResponse("You are not authorized to view this page.")

    if request.method == "POST":
        # Extracting form data
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pwd']

        # Checking if the username already exists
        if User.objects.filter(username=username).exists() or Staff.objects.filter(username=username).exists():
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
        Staff.objects.create(user_admin=user_admin)

        messages.success(request, 'You have successfully registered a Staff Member!')
        return redirect('login-user')


    return render(request, 'staff/registerstaff.html', {})
