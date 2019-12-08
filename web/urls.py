from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # 로그인
    path('signin/', views.signin, name='signin'),
    path('user_logout/', views.user_logout, name='user_logout'),
    # 회원가입
    path('signup/', views.signup, name='signup'),
    # 메인 페이지 by 진호
    path('main/', views.main, name='main'),
    path('like/', views.like, name='like'),
    # path('search/<str:saerch>', views.search_post, name='search_post')
]