from django.contrib.auth import authenticate, login, logout
from django.shortcuts import reverse, redirect
from .forms import LoginForm, SignupForm

from django.shortcuts import render
from django.utils import timezone

import json
from django.http import HttpResponse

from .models import MyUser

from django.http import Http404
from .models import MyUser
from .models import Card
from .models import Certification
from .models import Like, LikeManager

from django.core.paginator import Paginator


# Create your views here.
def index(request):
    logined = False
    if request.user.is_authenticated:
        logined = True
    return render(request, 'web/index.html', {'logined':logined} )

# 로그인 페이지 구현
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

# 회원가입 페이지 구현
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            print("valied")
            user = MyUser.objects.create_user(
                form.cleaned_data['name'],
                form.cleaned_data['email'],
                form.cleaned_data['date_of_birth'],
                form.cleaned_data['password'],
            )
            user.save()
            login(request, user)
            return redirect('index')
        else:
            return redirect('signup')
    else :
        form = SignupForm()

    return render(request, 'web/signup.html', {'form':form})

# # main display
# def main(request):
#     profile = []
#     try:
#         cards = Card.objects.order_by('-created_at')[:6]
#         i = 0
#         while i < len(cards):
#             users = MyUser.objects.get(email=cards[i])
#             name = users.name
#             likeNum = len(Like.objects.filter(liked=cards[i]))
#             homepage = cards[i].homepage
#             certifications = Certification.objects.filter(card=cards[i])[0:2]
#             profile.append({'name': name, 'likeNum': likeNum, 'homepage': homepage})
#             i+=1
#
#         # print(profile[2])
#
#         profiles = {'profiles': profile}
#
#     except Card.DoesNotExist:
#         raise Http404("Card does not exist.")
#
#     return render(request, 'web/main.html', profiles)


def main(request):
    profile = []
    try:
        cards = Card.objects.order_by('-created_at')[:6]

        for card in cards:
            users = MyUser.objects.get(email=card)
            name = users.name
            email = users.email
            likeNum = len(Like.objects.filter(liked=card))
            homepage = card.homepage
            certifications = Certification.objects.filter(card=card)[0:2]
            profile.append({'name': name, 'email': email, 'likeNum': likeNum, 'homepage': homepage})
            ''''certification1': ('None' if certifications[0] is None else certifications[0]), 'certification2': ('None' if certifications[1] is None else certifications[1])'''


        profiles = {'profiles': profile}

    except Card.DoesNotExist:
        raise Http404("Card does not exist.")

    return render(request, 'web/main.html', profiles)


def like(request):

    if not request.user.is_authenticated:
        return redirect('signin')

    req_user = request.user
    req_email = request.POST.get('card', None)

    card_user = MyUser.objects.get(email=req_email)
    card = Card.objects.get(owner=card_user)
    likes = Like.objects.filter(user=req_user, liked=card)#.filter(likes=req_card)

    if likes.count() > 0:
        Like.objects.get(user=req_user, liked=card).delete()
        likes_count = Like.objects.filter(liked=card).count()
        print('like decrease, current like:', likes_count)
        context = {'email': req_email, 'likes_count': likes_count, 'message': 'like_decrease'}
        return HttpResponse(json.dumps(context), content_type='application/json')
    else:
        create_like = Like.objects.create(user=req_user, liked=card)
        create_like.save()
        likes_count = Like.objects.filter(liked=card).count()
        print('like increase, current like:', likes_count)
        context = {'email': req_email, 'likes_count': likes_count, 'message': 'like_increase'}
        return HttpResponse(json.dumps(context), content_type='application/json')

