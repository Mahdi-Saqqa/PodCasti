
from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
        USERNAME_REGEX = r'^[a-zA-Z]+$'

        if not postData.get('first_name'):
            errors['first_name'] = 'First name is required.'
        if not postData.get('last_name'):
            errors['last_name'] = 'Last name is required.'
        if len(postData['first_name']) < 2:
            errors['first_name1'] = 'First name should be at least 2 char.'
        if len(postData['last_name']) < 2:
            errors['last_name1'] = 'First name should be at least 2 char.'
        if not USERNAME_REGEX.match(postData['first_name']):
            errors['first_name2'] = "First name should be letters only"
        if not USERNAME_REGEX.match(postData['last_name']):
            errors['last_name2'] = "Last name should be letters only"
        if len(postData['user_name']) < 5:
            errors['last_name1'] = 'User Name should be at least 5 char.'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email2'] = "Invalid Email address!"
        if not postData.get('email'):
            errors['email'] = 'Email is required.'
        if len(postData['password']) < 8:
            errors['pass1'] = "passwords doesn't match"
        if postData['password'] != postData['confirmpw']:
            errors['pass2'] = "passwords doesn't match"
        if not postData.get('password'):
            errors['password'] = 'Password is required.'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    following = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    objects = UserManager()


class Genre(models.Model):
    genre = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Podcast(models.Model):
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='audio/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    genre = models.ManyToManyField(Genre, related_name='podcasts')
    shares = models.ManyToManyField(User, related_name='shared_podcasts')
    likes = models.ManyToManyField(User, related_name='liked_podcasts')


class Comment(models.Model):
    comment = models.TextField()
    podcast = models.ForeignKey(Podcast, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Playlist(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='playlists', on_delete=models.CASCADE)
    podcasts = models.ManyToManyField(Podcast, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
