from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from myapp.models import *
from myapp.forms import *
import bcrypt



def index(request):    
    if 'user_id' in request.session:
        loged_user = User.objects.get(id=request.session['user_id'])
        profiles=User.objects.all()
        context ={
            'profiles':profiles,
            'loged_user':loged_user,
            'islogged':True,

        }
        return render(request, 'index.html', context)
    else:
        profiles=User.objects.all()
        context ={
            'profiles':profiles,
            'islogged':False,

        }
        return render(request, 'index.html',context)


def signup(request):
    return render(request, 'signup.html')


def signupaction(request):
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
        request.session['user_id'] = User.objects.last().id

        return redirect("/update")


def login(request):
    return render(request, 'login.html')


def loginaction(request):
    print('function run')
    user = User.objects.filter(email=request.POST['email']).first()
    if user:
        print('user found')
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/')
        else:
            print('wrong password')
            messages.error(request, "Wrong Password")
            return redirect('/login')
    else:
        print('email not found')
        messages.error(request, "Email not found in the database")
        return redirect('/login')


def addpodcast(request):
    print(request.POST['genre'])
    if 'user_id' in request.session:
        if request.method == 'POST':
            loged_user = User.objects.get(id=request.session['user_id'])
            print(loged_user.first_name)
            mp3_form = MP3UploadForm(request.POST, request.FILES)
            if mp3_form.is_valid():
                podcast = mp3_form.save(commit=False)
                podcast.description = request.POST['description']
                podcast.added_by = loged_user

                podcast.save()
                cat=Genre.objects.filter(genre=request.POST['genre']).first()
                
                podcast.genre.add(cat)
                return redirect('/')
        else:
            mp3_form = MP3UploadForm()
        context = {
                'mp3_form': mp3_form
                }
        return render(request, 'add_podcast.html', context)
    else:
        return redirect('/login')


def player(request, podcast_id):
    if 'user_id' in request.session:
        loged_user = User.objects.get(id=request.session['user_id'])
        podcast = Podcast.objects.get(id=podcast_id)
        user=podcast.added_by
        favorites = loged_user.liked_podcasts.all()
        print(user)
        print(loged_user)
        context={
            'podcast': podcast,
            'logged_user':loged_user,
            'user':user,
            'favorites':favorites

        }
        return render(request, 'player.html', context)
    else:
        
        return render(request, 'player.html', context)


def about(request):
    return render(request, 'about.html')


def profile(request):
    if 'user_id' in request.session:
        loged_user = User.objects.get(id=request.session['user_id'])
        followers_number=len(list(loged_user.followed_by.all()))
        followers=loged_user.following.all()
        following_number=len(list(loged_user.following.all()))
        following=loged_user.following.all()
        podcasts = loged_user.podcasts.all()
        context ={
            'podcasts':podcasts,
            'loged_user':loged_user,
            'user':loged_user,
            'islogged':True,
            'followers_number':followers_number,
            'following_number':following_number,
            'followers':followers,
            'following':following,
        }
        return render(request, 'profile.html', context)
    else:
        context={
            'message':'',
            'islogged':False

        }
        
        return render(request, 'profile.html', context)
        
def otherprofile(request, id):
    if 'user_id' in request.session:
        loged_user = User.objects.get(id=request.session['user_id'])
        user = User.objects.get(id=id)
        followers_number=len(list(user.followed_by.all()))
        followers=user.following.all()
        following_number=len(list(user.following.all()))
        following=user.following.all()
        podcasts = user.podcasts.all()
        context ={
            'podcasts':podcasts,
            'loged_user':loged_user,
            'user':user,
            'islogged':True,
            'followers_number':followers_number,
            'following_number':following_number,
            'followers':followers,
            'following':following,
        }
        return render(request, 'profile.html', context)
    else:
        context={
            'islogged':False

        }
        
        return render(request, 'profile.html', context)
    

def library(request):
    if 'user_id' in request.session:
        loged_user = User.objects.get(id=request.session['user_id'])
        podcasts = loged_user.liked_podcasts.all()
        favorites = loged_user.liked_podcasts.all()
        context ={
            'podcasts':podcasts,
            'islogged':True,
            'favorites':favorites,
            'loged_user':loged_user

        }
        for i in Genre.objects.all():
            print(i.genre)
        return render(request, 'library.html', context)
    else:
        return redirect('/')


def update(request):
    if 'user_id' in request.session:
        loged_user = User.objects.get(id=request.session['user_id'])
        context={
            'loged_user':loged_user
        }    
        return render(request, 'update.html', context)
    else:
        return redirect('/profile')
def updateaction(request):
    loged_user = User.objects.get(id=request.session['user_id'])

    loged_user.first_name=request.POST['first_name']
    
    loged_user.last_name=request.POST['last_name']
    loged_user.email=request.POST['email']
    loged_user.dob=request.POST['dob']
    loged_user.bio=request.POST['bio']
    try:
        loged_user.picture=request.FILES['profile_photo']
    except:
    # Handle the case where the file is not included in the request
        pass
    loged_user.save()

    return redirect('/profile')

def signout(request):
    logout(request)
    return redirect('/login')
def likepodcast(request,id):
    loged_user = User.objects.get(id=request.session['user_id'])
    podcast = Podcast.objects.get(id=id)
    loged_user.liked_podcasts.add(podcast)
    return redirect(request.META.get('HTTP_REFERER'))
def unlikepodcast(request,id):
    loged_user = User.objects.get(id=request.session['user_id'])
    podcast = Podcast.objects.get(id=id)
    loged_user.liked_podcasts.remove(podcast)
    return redirect(request.META.get('HTTP_REFERER'))

def deletepodcast(request,id):
    podcast = Podcast.objects.get(id=id)
    podcast.delete()
    return redirect('/')    
def genre(request,genre):
    if 'user_id' in request.session:
        loged_user = User.objects.get(id=request.session['user_id'])
        cat=Genre.objects.get(genre=genre)
        podcasts=cat.podcasts.all()
        context ={
            'podcasts':podcasts,
            'islogged':True,
            'loged_user':loged_user

        }
        return render(request, 'library.html', context)
    else:
        return redirect('/')