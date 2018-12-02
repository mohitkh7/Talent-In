from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView

from .models import Profile

# Create your views here.
def index(request):
    # return HttpResponse("Om Gang Ganpataye Namah")
    return render(request,'base.html')

def user_login(request):
    """
    Handle the login logic for application
    """
    logged_in  = False
    # check if user is already logged in 
    if request.user.is_authenticated:
        return redirect('myaccount')

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
                logged_in = True
                # return redirect('home')
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
                profile = Profile.objects.create(user=user)
                logged_in = True
                return redirect('profile-update')
            # return redirect('home')

        if logged_in == True:
            next_url =  request.GET.get('next',None)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')


@method_decorator(login_required, name="dispatch")
class ProfileUpdate(UpdateView):
    model=Profile
    fields = ['name','year', 'branch', 'skill', 'contact_number',]
    template_name="profile_update.html"

    def get_object(self):
        user =  self.request.user
        profile = user.profile
        return profile

    def get_success_url(self):
        return '/myaccount/'


@login_required
def myaccount(request):
    user = request.user
    name = user.profile.name
    year = user.profile.year
    print(year)
    ret_dict = {
        'name': name,
        'year': year,
    }
    return render(request, "myaccount.html", ret_dict)