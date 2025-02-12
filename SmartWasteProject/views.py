from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from Users.models import CustomUser
from django.contrib import messages

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        mobile_number = request.POST.get('mobile_number', '')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        user = CustomUser.objects.create_user(username=username, password=password, mobile_number=mobile_number)
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')
