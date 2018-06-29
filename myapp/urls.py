from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('ajaxobj', views.ajaxObj, name='ajaxObj'),
    path('home', views.home, name='home'),
    path('makepost', views.makePost, name='makePost'),
    path('makecomment/<int:post_id>', views.makeComment, name='makeComment'),
    path('likepost/<int:post_id>', views.likePost, name='likePost'),
    path('likedby/<int:post_id>', views.likedBy, name='likedBy'),
    path('searchprofile', views.searchProfile, name='searchProfile'),
    path('profile/<str:u_id>', views.profilePage, name='profilePage'),
    path('displayimage/<str:post_id>', views.displayImage, name='displayImage'),
    path('login', views.logIn, name='logIn'),
    path('signup', views.signUp, name='signUp'),
    path('logout', views.logOut, name='logOut'),
    path('follow', views.follow, name='follow'),
    path('followers', views.followers, name='followers'),
    path('following', views.following, name='following')
]
