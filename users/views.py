from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            phone_number = form.cleaned_data['phone_number']

            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Save additional fields to a user profile model if you have one
            # For example, if you have a UserProfile model with the above fields:
            # profile = UserProfile.objects.create(user=user, address=address, city=city, state=state, phone_number=phone_number)

            return redirect('login')  # Replace 'login' with the URL name of your login view
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})