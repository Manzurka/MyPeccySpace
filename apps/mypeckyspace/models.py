# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import bcrypt
import re
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@amazon.com$')

class UserManager(models.Manager):
    def validation(self, postData):
        errors={}
        if len(postData['name'])>0:
            if len(postData['name']) < 2:
                errors['name']="Name cannot be less than 2 characters!"
            if not NAME_REGEX.match(postData['name']):
                errors['name']="Invalid Name!"
        else:
            errors['name']="Name is required!"
        
        if len(postData['username'])>0:
            if len(postData['username']) < 2:
                errors['user']="Username cannot be less than 2 characters!"
            if not NAME_REGEX.match(postData['username']):
                errors['user']="Invalid username!"
        else: 
             errors['user']="Username is required!"

        if len(postData['email'])>0:
            if not EMAIL_REGEX.match(postData['email']):
                errors['email']="Must be an Amazon email address!"
            if self.filter(email=postData['email']):
                errors['email']="This email is in use.Please login!"
        else:
             errors['email']="Email Address is required!"

        if len(postData['password'])>0:
            if len(postData['password']) < 8:
                errors['password']="Password is less than 8 characters!"
        else:
             errors['password']="Password is required!"

        if postData['pw_confirmation']!= postData['password']:
            errors['pw_confirmation']="Password should match!"

        if postData['location'] == 'none':
            errors['location']= "Select the location"

        if postData['skill'] == 'none':
            errors['skill']= "Select the skill set"

        return errors

    def login_validation(self, postData):
        errors={}
        if User.objects.filter(email=postData['email']):
            user=User.objects.filter(email=postData['email'])
            if (bcrypt.checkpw(postData['password'].encode(), user[0].password.encode())):
                errors['login'] = "Successfully logged in!"
            if not (bcrypt.checkpw(postData['password'].encode(), user[0].password.encode())):
               errors['login'] = "Invalid password!"
        if not User.objects.filter(email=postData['email']):
            if len(postData['email'])== 0:
                errors['login'] = "Please enter the email address!"
            else:
                errors['login'] = "We could not match this email address to any user in our database!"
        
        return errors
    def update_validation(self, postData):
        errors={}
        if len(postData['name'])>0:
            if len(postData['name']) < 2:
                errors['name']="Name cannot be less than 2 characters!"
            if not NAME_REGEX.match(postData['name']):
                errors['name']="Invalid Name!"
        else:
            errors['name']="Name is required!"
        
        if len(postData['username'])>0:
            if len(postData['username']) < 2:
                errors['user']="Username cannot be less than 2 characters!"
            if not NAME_REGEX.match(postData['username']):
                errors['user']="Invalid username!"
        else: 
             errors['user']="Username is required!"

        
        if len(postData['password'])>0:
            if len(postData['password']) < 8:
                errors['password']="Password is less than 8 characters!"
        else:
             errors['password']="Password is required!"

        if postData['pw_confirmation']!= postData['password']:
            errors['pw_confirmation']="Password should match!"


        return errors


class User(models.Model):
    name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    location=models.CharField(max_length=255)
    skill=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    image=models.ImageField(upload_to='images/', default=None)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()


class Post(models.Model):
    title=models.CharField(max_length=255)
    content=models.TextField()
    uploaded_file=models.FileField(upload_to='documents/', default=None)
    creator=models.ForeignKey(User, related_name="posts")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class Comment(models.Model):
    text=models.TextField()
    post=models.ForeignKey(Post, related_name="post_comments")
    commenter=models.ForeignKey(User, related_name="user_comments")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Award(models.Model):
    award=models.CharField(max_length=255)
    users=models.ManyToManyField(User, related_name="awards")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)