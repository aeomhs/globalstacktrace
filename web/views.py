from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'web/index.html')

def signin(request):
    
    return render(request, 'web/signin.html')