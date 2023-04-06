from django.urls import path
from . import views
from .views import signout

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('loginaction', views.loginaction),
    path('signup', views.signup),
    path('signupaction', views.signupaction),
    path('addpodcast/', views.addpodcast, name='addpodcast'),
    path('podcast/<int:podcast_id>/', views.player, name='player'),
    path('about', views.about),
    path('profile', views.profile),
    path('profile/<int:id>/', views.otherprofile),
    path('library', views.library),
    path('update', views.update),
    path('signout', views.signout),
    path('updateaction', views.updateaction),
    path('likepodcast/<int:id>', views.likepodcast),
    path('unlikepodcast/<int:id>', views.unlikepodcast),
    path('deletepodcast/<int:id>', views.deletepodcast),
    path('genre/<str:genre>', views.genre),
    path('follow/<int:id>', views.follow),
    path('unfollow/<int:id>', views.unfollow),
]
