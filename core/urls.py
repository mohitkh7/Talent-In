"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls import reverse

from . import views

urlpatterns = [
    path('', views.list_user, name="home"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('myaccount/', views.myaccount, name="myaccount"),
    path('myaccount/edit/', views.ProfileUpdate.as_view(), name="profile-update"),
    path('user/<str:username>/', views.user_profile, name="user-profile"),
    path('list/', views.list_user, name="list-user"),
]
