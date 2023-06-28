from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, AccountForm
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            phone_number = form.cleaned_data['phone_number']
            if password_confirm == password:
                user = CustomUser()
                user.email = email
                user.password = password
                user.first_name = first_name
                user.last_name = last_name
                user.address = address
                user.city = city
                user.state = state
                user.phone = phone_number
                user.save()

                # Save additional fields to a user profile model if you have one
                # For example, if you have a UserProfile model with the above fields:
                # profile = UserProfile.objects.create(user=user, address=address, city=city, state=state, phone_number=phone_number)

                return redirect('login')  # Replace 'login' with the URL name of your login view
            else:
                form.add_error("password_confirm", "Passwords do not match")

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return redirect('employer_dashboard')
                else:
                    login(request, user)
                    return redirect('dashboard')
            else:
                form.add_error('email', "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@ login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')

@ login_required(login_url='/login/')
def account_view(request):
    user = request.user
    if request.method == 'POST':
        # Handle the form submission for updating user data
        # Retrieve the updated data from the form and update the user object
        # Save the user object
        form = AccountForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            phone_number = form.cleaned_data['phone_number']

            if password!="":
                user.password = password
            user.first_name = first_name
            user.last_name = last_name
            user.address = address
            user.city = city
            user.state = state
            user.phone = phone_number
            user.save()
        # Redirect to the "My Account" page or any other desired page
        return redirect('account')

        # Render the template with the user data
    return render(request, 'account.html', {'user': user})