from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'