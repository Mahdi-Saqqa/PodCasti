from django.urls import path
from . import views
from .views import MP3UploadForm
""" from django.conf import settings
from django.conf.urls.static import static
"""
""" urlpatterns = [
    path('', views.index),
    path('upload/', MP3UploadView.as_view(), name='mp3_upload'),
]
"""
urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('home', views.home, name='home'),
    path('podcast/<int:podcast_id>/', views.podcast_detail, name='podcast_detail'),
    path('create_podcast/', views.create_podcast, name='create_podcast'),
    path('about',views.about)
]
