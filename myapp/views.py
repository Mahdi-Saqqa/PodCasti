from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from myapp.models import Podcast, Genre
from myapp.forms import MP3UploadForm

def home(request):
    podcasts = Podcast.objects.all()
    return render(request, 'home.html', {'podcasts': podcasts})

def podcast_detail(request, podcast_id):
    podcast = Podcast.objects.get(id=podcast_id)
    print(Podcast.objects.get(id=podcast_id).file.url)
    return render(request, 'podcast_detail.html', {'podcast': podcast})

#@login_required
def create_podcast(request):
    if request.method == 'POST':
        form = MP3UploadForm(request.POST, request.FILES)
        if form.is_valid():
            podcast = form.save(commit=False)
            podcast.user = request.user
            podcast.save()
            form.save_m2m()
            messages.success(request, 'Your podcast has been uploaded successfully!')
            return redirect('home')
    else:
        form = MP3UploadForm()
    return render(request, 'create_podcast.html', {'form': form})
