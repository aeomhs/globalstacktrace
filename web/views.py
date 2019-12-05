from django.shortcuts import render

from django.http import Http404
from .models import MyUser
from .models import Card
from .models import Certification
from .models import Like

from django.core.paginator import Paginator


# Create your views here.
def index(request):
    return render(request, 'web/index.html')


def signin(request):
    return render(request, 'web/signin.html')



def main(request):
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


        profiles = {'profiles': profile}

    except Card.DoesNotExist:
        raise Http404("Card does not exist.")

    return render(request, 'web/main.html', profiles)