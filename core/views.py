from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Profile, Year, Branch, Skill

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
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
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
    fields = [
        'name',
        'year',
        'branch',
        'skills',
        'contact_number',
        'facebook_url',
        'linkedin_url',
        'github_url',
    ]
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
    branch = user.profile.branch
    skills = user.profile.skills
    contact_number = user.profile.contact_number
    facebook_url = user.profile.facebook_url
    linkedin_url = user.profile.linkedin_url
    github_url = user.profile.github_url
    # check if urls are correct
    if facebook_url is None:
        facebook_url = '#'
    if linkedin_url is None:
        linkedin_url = '#'
    if github_url is None:
        github_url = '#'

    ret_dict = {
        'name': name,
        'year': year,
        'branch': branch,
        'skills': skills,
        'contact_number': contact_number,
        'facebook_url': facebook_url,
        'linkedin_url': linkedin_url,
        'github_url': github_url,
    }
    return render(request, "myaccount.html", ret_dict)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user:
        return redirect('myaccount')
    profile = user.profile
    return render(request, "user.html", {'profile':profile})


def list_user(request):
    # used for form filtering
    years = Year.objects.all()
    branches = Branch.objects.all()
    skills = Skill.objects.all()

    year = int(request.GET.get('year', -1))
    branch = int(request.GET.get('branch', -1))
    skill = request.GET.getlist('skill')

    profiles = Profile.objects.all()
    if len(skill) > 0:
        profiles = profiles.filter(skills__in = skill)

    if year != -1:
        profiles = profiles.filter(year=year)
    if branch != -1:
        profiles = profiles.filter(branch_id=branch)

    skill_int = list(map(int, skill))
    profiles = profiles.annotate(skill_count = Count('skills')).order_by('-skill_count')
    return render(
        request,
        "list_user.html",
        {
            'profiles': profiles,
            'years': years,
            'branches': branches,
            'skills': skills,
            'prev_year': year,
            'prev_branch': branch,
            'prev_skill': skill_int,

        }
    )