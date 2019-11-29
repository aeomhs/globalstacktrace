from django.shortcuts import render
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request, 'web/index.html')

# TODO 로그인 페이지 구현
def signin(request):
    return render(request, 'web/signin.html')

# TODO 회원가입 페이지 구현
def signup(request):
    return render(request, 'web/signup.html')