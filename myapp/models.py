
from django.db import models
import re


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,6})+$')
        if not postData.get('first_name'):
            errors['first_name'] = 'First Name is required'
        if not postData.get('last_name'):
            errors['last_name'] = 'Last Name is required'
        if len(postData['first_name']) < 2:
            errors['first_name1'] = 'First Name should be at least 2 characters!'
        if len(postData['last_name']) < 2:
            errors['last_name1'] = 'First Name should be at least 2 characters!'

        if len(postData['user_name']) < 5:
            errors['last_name1'] = 'Username should be at least 5 characters!'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email2'] = "Invalid Email Address!"
        if not postData.get('email'):
            errors['email'] = 'Email is required'
        if len(postData['password']) < 8:
            errors['pass1'] = "Password should be at least 8 characters!"
        if postData['password'] != postData['confirmpw']:
            errors['pass2'] = "Passwords don't match!"
        if not postData.get('password'):
            errors['password'] = 'Password is required'
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
    following = models.ManyToManyField(
        'self', related_name='followed_by', symmetrical=False)
    picture = models.ImageField(upload_to='profiles_picture/', null=True)
    bio=models.TextField(null=True)
    objects = UserManager()





class Podcast(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=100,default='culture')
    shares = models.ManyToManyField(User, related_name='shared_podcasts')
    likes = models.ManyToManyField(User, related_name='liked_podcasts')
    file = models.FileField(upload_to='uploads/')
    cover = models.ImageField(upload_to='covers/', null=True)
    duration = models.CharField(max_length=10, null=True)
    added_by = models.ForeignKey(
        User, related_name="podcasts", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
