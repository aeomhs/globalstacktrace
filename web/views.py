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

    checkbox_list = {'C': '', 'JAVA': '', 'PYTHON': '', 'search_summary': ''}
    get_request_list = {'C': '', 'JAVA': '', 'PYTHON': '', 'search_summary': ''}

    try:

        page = request.GET.get('page', 1)

        card_list = Card.objects.order_by('-created_at')
        # Search
        search_summary = request.GET.get('search_summary', None)
        if search_summary is not None and search_summary != '':
            card_list = card_list.filter(summary__contains=search_summary)
            checkbox_list['search_summary'] = search_summary
            get_request_list['search_summary'] = search_summary



        temp_list = []
        C_lang = request.GET.get('C', None)
        Java_lang = request.GET.get('JAVA', None)
        Python_lang = request.GET.get('PYTHON', None)
        if C_lang is not None and C_lang != '':
            temp_list.append('C')
            checkbox_list['C'] = 'checked'  #검색후에 값이 그대로 남아있게 하기위해
            get_request_list['C'] = 'C'

        if Java_lang is not None and Java_lang != '':
            temp_list.append('JAVA')
            checkbox_list['JAVA'] = 'checked'  #검색후에 값이 그대로 남아있게 하기위해
            get_request_list['JAVA'] = 'JAVA'

        if Python_lang is not None and Python_lang != '':
            temp_list.append('PYTHON')
            checkbox_list['PYTHON'] = 'checked'  #검색후에 값이 그대로 남아있게 하기위해
            get_request_list['PYTHON'] = 'PYTHON'



        delete_list = []
        for card in card_list:
            i = 0
            if len(temp_list) > len(card.skill):
                delete_list.append(card)
                continue

            for skill in card.skill:
                for temp in temp_list:
                    if skill == temp:
                        i += 1

            if i < len(temp_list):
                delete_list.append(card)

        for d_card in delete_list:
            card_list = card_list.exclude(owner=d_card)



        profile = []
        for card in card_list:
            users = MyUser.objects.get(email=card)
            name = users.name
            email = users.email
            likeNum = len(Like.objects.filter(liked=card))
            homepage = card.homepage
            summary = card.summary
            skill = card.skill
            liked = False
            if logined:
                result = Like.objects.filter(liked=card)
                result = result.filter(user=request.user)
                if result.count() == 1:
                    liked = True

            profile.append({
                'name': name,
                'email': email,
                'likeNum': likeNum,
                'homepage': homepage,
                'summary': summary,
                'skill': skill,
                'liked': liked})

        paginator = Paginator(profile, 6)

        print(page,'----------------------')
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
                project_formset = ProjectFormSet(queryset=Project.objects.none(), prefix='proj')
                certification_formset = CertificationFormSet(queryset=Certification.objects.none(), prefix='crtf')

            stack_form = {'card_form': card_form, 'project_formset': project_formset,
                          'certification_formset': certification_formset}

            arguments = {'profiles': profiles, 'logined': logined, 'has_a_card': has_a_card, 'form': stack_form, 'checkbox_list': checkbox_list, 'get_request_list': get_request_list}

    except Card.DoesNotExist:
        raise Http404("Card does not exist.")
    except PageNotAnInteger:
        profiles = paginator.page(1)
        arguments = {'profiles': profiles, 'logined': logined, 'has_a_card': has_a_card,
                     'checkbox_list': checkbox_list}
        return render(request, 'web/main.html', arguments)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)
        print('dddddddddddddd',paginator.num_pages)
        arguments = {'profiles': profiles, 'logined': logined, 'has_a_card': has_a_card,
                     'checkbox_list': checkbox_list}
        return render(request, 'web/main.html', arguments)

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
