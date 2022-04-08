from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
# Create your views here.


def home(request):
    return render(request, "home/home.html")


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             redirect('home.home')
#         # else:
#     return render(request, "home/login.html")

# Return an 'invalid login' error message.


class BasicLoginView(LoginView):
    template_name = 'home/login.html'
