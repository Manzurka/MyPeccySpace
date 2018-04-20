# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.storage import FileSystemStorage
import operator
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from .forms import *

# Create your views here.
def index(request):
   return render(request,'mypeckyspace/index.html')

def validate(request):
   errors = User.objects.validation(request.POST)
   if errors:
       for tag, error in errors.iteritems():
           messages.error(request, error, extra_tags=tag)
       return redirect('/')
   else:
       user=User.objects.create(name=request.POST['name'],username=request.POST['username'], email=request.POST['email'],skill= request.POST['skill'], location= request.POST['location'] ,password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
       request.session['name'] = request.POST['name']
       request.session ['id'] = user.id
       return redirect('/dashboard')

def login(request):
   errors = User.objects.login_validation(request.POST)
   if errors:
       if errors['login'] == "Successfully logged in!":
           user=User.objects.filter(email=request.POST['email'])
           request.session ['name'] = user[0].name
           request.session ['id'] = user[0].id
           return redirect('/dashboard')
       for tag, error in errors.iteritems(): 
           messages.error(request, error, extra_tags=tag)
       return redirect('/')

def dashboard(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, 'mypeckyspace/dashboard.html', { "posts": posts[:2], "comments" : Comment.objects.all()})
    
def results(request):
        if request.method == 'GET': # If the form is submitted
            if len(request.GET.get('search_box')) ==0:
                messages.info(request, 'Please enter search keyword!')
                return redirect('/dashboard')
            keyword = request.GET.get('search_box', None)
            if keyword:
                posts=Post.objects.all()
                results=posts.filter(content__icontains=keyword)
                context={
                        "results": results,
                        "comments" : Comment.objects.all()

                }
                print results
                
                if len(results) == 0:
                    return HttpResponse("No search results")

                return render(request, 'mypeckyspace/results.html', context)

def showUser(request, id):
    
    context = {
        "user": User.objects.get(id=id),
        "awards": Award.objects.all(),
        "user_awards" : User.objects.get(id=id).awards.all(),
       
    }
    return render(request, 'mypeckyspace/user.html', context)

def editUser(request, id):
    return render(request, "mypeckyspace/edituser.html", {"user": User.objects.get(id=id)})

def update(request, id):
    user=User.objects.get(id=id)
    errors = User.objects.update_validation(request.POST)
    if errors:
       for tag, error in errors.iteritems():
           messages.error(request, error, extra_tags=tag)
       return redirect(reverse ('main:edit_user_id', kwargs={'id': user.id}))
    else: 
        user=User.objects.get(id=id)
        user.name=request.POST['name']
        user.username=request.POST['username']
        user.password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user.location=request.POST['location']
        user.skill=request.POST['skill']
        user.save()
        return redirect(reverse ('main:user_id', kwargs={'id': user.id}))

def upload(request, id): 
    user=User.objects.get(id=id)
    if request.method == 'POST':
        form=ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
           user.image= form.cleaned_data['image']
           user.save()
           return redirect(reverse ('main:user_id', kwargs={'id': user.id}))
        else:
            messages.info(request, "No image is attached")
            return redirect(reverse ('main:edit_user_id', kwargs={'id': user.id}))

def showPost(request, id):
    return render(request, 'mypeckyspace/post.html', { "post": Post.objects.get(id=id), "comments": Comment.objects.all()})

def addPost(request):
    userid = request.session ['id'] 
    user=User.objects.get(id=userid)
    newpost=Post.objects.create(title=request.POST['title'], content=request.POST['content'], upload=request.FILES['myfile'], creator=user)
    return redirect('/dashboard')
    # if request.method == 'POST':
    #     form=FileUploadForm(request.POST, request.FILES)
    #     if form.is_valid():
    #        newpost.uploaded_file= form.cleaned_data['myfile']
    #        newpost.save()
    #        return redirect('/dashboard')
    #     else:
    #         messages.info(request, "Wrong format.Upload again", extra_tags='info')
    #         return redirect('/dashboard')
  

def uploadfile(request, id):
    post=Post.objects.get(id=id)
    post.upload= request.FILES['myfile']
    post.save()
    return redirect(reverse ('main:post_id', kwargs={'id': post.id}))
  

def comment(request, id):
    user=User.objects.get(id=request.session ['id'])
    post=Post.objects.get(id=id)
    Comment.objects.create(text=request.POST['text'], commenter=user, post=post)
    return redirect('/dashboard')

def deletepost(request, id):
    Post.objects.get(id=id).delete()
    return redirect('/dashboard')

def deletecomment(request, id):
    Comment.objects.get(id=id).delete()
    return redirect('/dashboard')

def page1(request):
    posts = Post.objects.all().order_by("-created_at")[:2]
    return render(request, 'mypeckyspace/dashboard.html', { "posts": posts, "comments" : Comment.objects.all()})

def page2(request):
    posts=Post.objects.all().order_by("-created_at")[2:4]
    return render(request, 'mypeckyspace/dashboard.html', { "posts": posts, "comments" : Comment.objects.all()})

def page3(request):
    posts=Post.objects.all().order_by("-created_at")[4:6]
    return render(request, 'mypeckyspace/dashboard.html', { "posts": posts, "comments" : Comment.objects.all()})

def page4(request):
    posts=Post.objects.all().order_by("-created_at")[6:8]
    return render(request, 'mypeckyspace/dashboard.html', { "posts": posts, "comments" : Comment.objects.all()})

def page5(request):
    posts=Post.objects.all().order_by("-created_at")[8:10]
    return render(request, 'mypeckyspace/dashboard.html', { "posts": posts, "comments" : Comment.objects.all()})

def awards(request, id):
    user=User.objects.get(id=id)
    award=Award.objects.create(award=request.POST['award'])
    award_user=User.objects.get(id=request.POST["user_id"])
    award.users.add(award_user)
    return redirect(reverse ('main:user_id', kwargs={'id': user.id}))

def showfile(request,id):
    
    return render(request, 'mypeckyspace/file.html', {"post": Post.objects.get(id=id)})

