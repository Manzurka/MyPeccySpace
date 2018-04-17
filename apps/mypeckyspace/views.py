from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
   return render(request,'mypeckyspace/index.html')

def validate(request):
   errors = User.objects.validation(request.POST)
   if errors:
       for tag, error in errors.iteritems():
           messages.error(request, error, extra_tags=tag)
       return redirect('/user')
   else:
       user=User.objects.create(name=request.POST['name'],username=request.POST['username'], email=request.POST['email'],skill= request.POST['skill'], location= request.POST['location'] ,password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
       request.session['name'] = request.POST['name']
       request.session ['id'] = user.id
       return redirect('/')

def login(request):
   errors = User.objects.login_validation(request.POST)
   if errors:
       if errors['login']  =="Successfully logged in!":
           user=User.objects.filter(email=request.POST['email'])
           request.session ['name'] = user[0].name
           request.session ['id'] = user[0].id
           return redirect('/user')
       for tag, error in errors.iteritems():
           messages.error(request, error, extra_tags=tag)
       return redirect('/')


def showUser(request):
    context = {
        "user": User.objects.get(id=request.session['id'])
    }
    return render(request, 'mypeckyspace/edituser.html', context)
