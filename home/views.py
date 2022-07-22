from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

# Create your views here.


def home_view(request):
    return render(request, "home/home.html")


def logout_view(request):
    logout(request)
    return redirect(reverse("home:login"))


class BasicLoginView(LoginView):
    template_name = "home/login.html"
