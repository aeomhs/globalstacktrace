from django.contrib.auth import authenticate, login, logout
from django.shortcuts import reverse, redirect
from .forms import LoginForm

from django.shortcuts import render
from django.utils import timezone

# Create your views here.
def index(request):
    logined = False
    if request.user.is_authenticated:
        logined = True
    return render(request, 'web/index.html', {'logined':logined} )

# TODO 로그인 페이지 구현
def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else :
                return redirect('signin')
    else:
        form = LoginForm()

    return render(request, 'web/signin.html', {'form':form})

# Logout
def user_logout(request):
    logout(request)

    return redirect('index')

# TODO 회원가입 페이지 구현
def signup(request):
    return render(request, 'web/signup.html')