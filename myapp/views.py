from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from myapp.models import Podcast, Genre, User
from myapp.forms import MP3UploadForm,MyForm
import bcrypt


def index(request):
    return render(request, 'index.html')


def signup(request):
    return render(request, 'signup.html')
    
def createsignup(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/signup')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=request.POST['first_name'],
                            last_name=request.POST['last_name'],
                            email=request.POST['email'],
                            user_name=request.POST['user_name'],
                            dob=request.POST['dob'],
                            password=pw_hash)
        request.session['user_name']=request.POST['first_name'] 
        return render(request, 'login.html')
        
def gologin(request):
    return render(request, 'login.html')

def login(request):
    user = User.objects.filter(email=request.POST['email']).first()
    if user:
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_name'] = user.first_name

            return redirect('/')
        else:
            messages.error(request, "Wrong Password")
            return redirect('/login')

        
    else:
        messages.error(request, "Email not found in the database")
        return redirect('/login')
    
""" def home(request):
    podcasts = Podcast.objects.all()
    return render(request, 'home.html', {'podcasts': podcasts})
"""

def podcast_detail(request, podcast_id):
    if 'user_name' in request.session:
        podcast = Podcast.objects.get(id=podcast_id)
        print(Podcast.objects.get(id=podcast_id).file.url)
        return render(request, 'playertest.html', {'podcast': podcast})
    else:
        return redirect('/login')
    
def my_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            mp3_file = form.cleaned_data['mp3_file']
            image_file = form.cleaned_data['image_file']
    else:
        form = MyForm()
    return render(request, 'create_podcast.html', {'form': form})


def create_podcast(request):
    if request.method == 'POST':
        form = MP3UploadForm(request.POST, request.FILES)
        if form.is_valid():
            podcast = form.save(commit=False)
            # podcast.user = request.user
            podcast.save()
            form.save_m2m()
            messages.success(
                request, 'Your podcast has been uploaded successfully!')
            return redirect('home')
    else:
        print("test")
        form = MP3UploadForm()
    return render(request, 'create_podcast.html', {'form': form})


def about(request):
    return render(request,'about.html')