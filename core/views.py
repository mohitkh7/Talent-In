from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    # return HttpResponse("Om Gang Ganpataye Namah")
    return render(request,'base.html')

def user_login(request):
    """
    Handle the login logic for application
    """
    if request.method == "POST":
        # Login
        if "submit-login-form" in request.POST:
            print(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:

                login(request, user)
                return redirect('home')
            else:
                print("Error")
        # Register
        if "submit-register-form" in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')