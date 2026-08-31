from django.urls import path
from django.shortcuts import render

urlpatterns = [
    path('login/', lambda request: render(request, 'auth/login.html'), name='login-page'),

    path('register/', lambda request: render(request, 'auth/register.html'), name='register-page'),

    path('profile/', lambda request: render(request, 'auth/profile.html'), name='profile-page')
]