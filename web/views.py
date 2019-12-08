from django.contrib.auth import authenticate, login, logout

from django.shortcuts import redirect
from .forms import LoginForm, SignupForm, CardForm, ProjectForm, CertificationForm
from django.forms import modelformset_factory

from django.shortcuts import render
from django.utils import timezone

import json
from django.http import HttpResponse

from .models import MyUser

from django.http import Http404
from .models import MyUser
from .models import Card
from .models import Project, Certification
from .models import Like

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    logined = False
    if request.user.is_authenticated:
        logined = True
    return render(request, 'web/index.html', {'logined': logined} )


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
                # return redirect('index')
                return redirect('main')
            else:
                return redirect('signin')
    else:
        form = LoginForm()

    return render(request, 'web/signin.html', {'form': form})


# Logout
def user_logout(request):
    logout(request)
    # return redirect('index')
    return redirect('main')


# 회원가입 페이지 구현
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            user = MyUser.objects.create_user(
                form.cleaned_data['name'],
                form.cleaned_data['email'],
                form.cleaned_data['date_of_birth'],
                form.cleaned_data['password'],
            )
            user.save()
            login(request, user)
            # return redirect('index')
            return redirect('main')
        else:
            return redirect('signup')
    else:
        form = SignupForm()

    return render(request, 'web/signup.html', {'form': form})



def main(request):
    logined = False
    has_a_card = False

    # Login Check
    if request.user.is_authenticated:
        logined = True

        # Card Check
        user = request.user
        card = Card.objects.filter(owner=user)
        if card.count() >= 1:
            has_a_card = True

    profile = []
    try:
        card_list = Card.objects.order_by('-created_at')
        # Search
        search_summary = request.GET.get('search_summary', None)
        if search_summary is not None:
            card_list = card_list.filter(summary__contains=search_summary)

        # 이건 해당 언어가 있는글만 출력해야댐
        # if selected_lang is not None:
        #     card_list = card_list.filter(summary__contains=)

        for card in card_list:
            users = MyUser.objects.get(email=card)
            name = users.name
            email = users.email
            likeNum = len(Like.objects.filter(liked=card))
            homepage = card.homepage
            certifications = Certification.objects.filter(card=card)[0:2]
            profile.append({'name': name, 'email': email, 'likeNum': likeNum, 'homepage': homepage})
            ''''certification1': ('None' if certifications[0] is None else certifications[0]), 'certification2': ('None' if certifications[1] is None else certifications[1])'''

        page = request.GET.get('page', 1)
        paginator = Paginator(profile, 6)

        profiles = paginator.page(page)

        arguments = {'profiles': profiles, 'logined': logined, 'has_a_card': has_a_card}

        # FAB : Stack PUSH & POP (# Stack Edit Modal)
        ProjectFormSet = modelformset_factory(
            Project, form=ProjectForm, extra=0, can_delete=True, min_num=0
        )
        CertificationFormSet = modelformset_factory(
            Certification, form=CertificationForm, extra=0, can_delete=True, min_num=0
        )
        if request.method == 'POST':
            # Stack Form PUSH
            if 'push' in request.POST:
                card_form = CardForm(request.POST)
                project_formset = ProjectFormSet(request.POST, prefix='proj')
                certification_formset = CertificationFormSet(request.POST, prefix='crtf')

                if card_form.is_valid() and project_formset.is_valid() and certification_formset.is_valid():
                    card = Card(
                        owner=request.user,
                        homepage=card_form.cleaned_data['homepage'],
                        summary=card_form.cleaned_data['summary'],
                        skill=card_form.cleaned_data['skill'],
                    )
                    card.save()

                    projects = project_formset.save(commit=False)
                    for project in projects:
                        project.card = card
                        project.save()

                    for del_obj in project_formset.deleted_objects:
                        del_obj.delete()

                    certifications = certification_formset.save(commit=False)
                    for ctfc in certifications:
                        ctfc.card = card
                        ctfc.save()

                    for del_obj in certification_formset.deleted_objects:
                        del_obj.delete()

                return redirect('main')

            # Stack Form POP
            elif 'pop' in request.POST:
                card = Card.objects.get(owner=request.user)
                card.delete()
                return redirect('main')
        # GET Stack Edit Modal
        else:
            user = request.user

            if has_a_card:
                card = Card.objects.get(owner=user)
                card_form = CardForm(initial={'homepage': card.homepage, 'skill': card.skill, 'summary': card.summary})
                project_formset = ProjectFormSet(queryset=Project.objects.filter(card=card), prefix='proj')
                certification_formset = CertificationFormSet(queryset=Certification.objects.filter(card=card), prefix='crtf')
            else:
                card_form = CardForm()
                project_formset = ProjectFormSet(prefix='proj')
                certification_formset = CertificationFormSet(prefix='crtf')

            stack_form = {'card_form': card_form, 'project_formset': project_formset,
                          'certification_formset': certification_formset}

            arguments = {'profiles': profiles, 'logined': logined, 'has_a_card': has_a_card, 'form': stack_form}

    except Card.DoesNotExist:
        raise Http404("Card does not exist.")
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)
        
    return render(request, 'web/main.html', arguments)


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
