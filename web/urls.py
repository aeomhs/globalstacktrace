from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # 로그인
    path('signin/', views.signin, name='signin'),
    # 회원가입
    path('signup/', views.signup, name='signup'),
]