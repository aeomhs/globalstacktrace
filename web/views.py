from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import LoginForm, SignupForm, CardForm, ProjectForm, CertificationForm
from django.forms import modelformset_factory

from django.shortcuts import render
from django.utils import timezone

from .models import MyUser

from django.http import Http404
from .models import MyUser
from .models import Card
from .models import Project, Certification
from .models import Like

from django.core.paginator import Paginator


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
        cards = Card.objects.order_by('-created_at')[:6]
        i = 0
        while i < len(cards):
            users = MyUser.objects.get(email=cards[i])
            name = users.name
            likeNum = len(Like.objects.filter(liked=cards[i]))
            homepage = cards[i].homepage
            certifications = Certification.objects.filter(card=cards[i])[0:2]
            profile.append({'name': name, 'likeNum': likeNum, 'homepage': homepage})
            i+=1

        arguments = {'profiles': profile, 'logined': logined, 'has_a_card': has_a_card}

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
                project_formset = ProjectFormSet(request.POST)
                certification_formset = CertificationFormSet(request.POST)
                print("1:", project_formset)
                print("1:", certification_formset)
                print("2:", project_formset.errors)
                print("2:", certification_formset.errors)

                if card_form.is_valid() and project_formset.is_valid() and certification_formset.is_valid():
                    card = Card(owner=request.user, homepage=card_form.cleaned_data['homepage'])
                    card.save()

                    projects = project_formset.save(commit=False)
                    print("3:", project_formset.deleted_objects)
                    for project in projects:
                        project.card = card
                        project.save()

                    for del_obj in project_formset.deleted_objects:
                        del_obj.delete()

                    certifications = certification_formset.save(commit=False)
                    print("3:", certification_formset.deleted_objects)
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
                card_form = CardForm(initial={'homepage': card.homepage})
                project_formset = ProjectFormSet(queryset=Project.objects.filter(card=card), prefix='proj')
                certification_formset = CertificationFormSet(queryset=Certification.objects.filter(card=card), prefix='crtf')
                print(certification_formset)
            else:
                card_form = CardForm()
                project_formset = ProjectFormSet()
                certification_formset = CertificationFormSet()

            print(certification_formset)
            stack_form = {'card_form': card_form, 'project_formset': project_formset,
                          'certification_formset': certification_formset}

            arguments = {'profiles': profile, 'logined': logined, 'has_a_card': has_a_card, 'form': stack_form}

    except Card.DoesNotExist:
        raise Http404("Card does not exist.")

    return render(request, 'web/main.html', arguments)
